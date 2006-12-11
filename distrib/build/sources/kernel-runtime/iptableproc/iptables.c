// iptables side of iptableproc
// (c) 2006 Martin Houston, <martin.houston@smoothwall.net> 
// SmoothWall Ltd.
// Released under the GPLv2.

// all the kernel includes we need are in here...
#include "iptableproc.h"

// eveything that does not needed to be seen by other files is static.

// odd these dont seem to be an available resource kernelside
static unsigned char *hooknames[] = {"PREROUTING", "INPUT", "FORWARD", "OUTPUT", "POSTROUTING"};
// returns true if we are a built in table
// args are this entry, info about the table we are in
// and a pointer where the stat of the entries table that this entry is in
// so that we can check that the data pointed at by hook_entry[i] is us.
// 0 return for not found
static inline unsigned int ent_is_hook_entry(struct ipt_entry *e,
						 struct ipt_table *t,
						 void *entrytable) {
	unsigned int i;
	struct xt_table_info *private = t->private;
	for (i = 0; i < NF_IP_NUMHOOKS; i++) {
		// if the bit for this hook is set and the entry defined as the hook entry
		// appropriate for this table has the same address as this entry
		// everything is done with offsets, not pointers as remember the
		// entrytable is all duplicated per cpu.
		if ((t->valid_hooks & (1 << i))
			&& (struct ipt_entry *)(entrytable + private->hook_entry[i]) == e) {
			return i+1; // so 0 is available as failure
		}
	}
	return 0;
}

// need to find out from iptables what is out there
// get the names of tables and put them in supplied **
// reads  /proc/net/ip_tables_names to get this info, which is otherwise only static data within iptables
// so have to go by this route.

int iptableproc_get_tablenames(unsigned char ***tablenames) {
	int fd,i,cnt;
	mm_segment_t old_fs;
	int num_tables = 0;
	
	unsigned char *bigbuf = kcalloc(1,512, GFP_KERNEL);
	unsigned char *s;
	if(tablenames == NULL || bigbuf == NULL){
		// come on - nowhere to stick this?
		printk(KERN_ALERT "Error: no memory provided for iptableproc_get_tablenames");
			return -ENOMEM;
	}
	if(*tablenames != NULL){
		// must assume that this is an existing kmalloc - free it
		iptableproc_free_anynames(tablenames);
	}
	// we have a pointer to a array of array of char 
	// need to find out how many tables there are by reading 
	// we count the newlines
	old_fs = get_fs();
	set_fs(KERNEL_DS); // so can use sys_open/sys_read
	fd = sys_open("/proc/net/ip_tables_names", O_RDONLY, 0);
	if(fd >= 0) {
			cnt = sys_read(fd, bigbuf, 511);
			sys_close(fd);
			set_fs(old_fs);
			if(cnt >= 511) {
				// no way this should be 1k of data! Its only table names
				printk(KERN_ALERT "Error: too much data returned from /proc/net/ip_tables_names");
				return -EIO;
			}
		
		for(i = 0; bigbuf[i] && i < cnt; i++) {
		if(bigbuf[i] == '\n') {
				bigbuf[i] = 0; // so nicley null terminated
				num_tables++;
			}
		}
		if(num_tables > 0) {
			// we have some		
			*tablenames = kcalloc(num_tables+1, sizeof(unsigned char **), GFP_KERNEL);
			if(*tablenames == NULL) {
				printk(KERN_ALERT "Error: Could not get memory for iptableproc_get_tablenames\n");
				return -ENOMEM;
			}
			s = bigbuf;
			for(i = 0; i < num_tables; i++) {
				(*tablenames)[i] = kmalloc(strlen(s)+1, GFP_KERNEL);
				if((*tablenames)[i] == NULL) {
					printk(KERN_ALERT "Error: Could not get memory for iptableproc_get_tablenames\n");
					return -ENOMEM;
				}
				strcpy((*tablenames)[i], s);
				// move past the NULL			
				s += strlen(s) + 1;
			}
			(*tablenames)[i] = NULL; // NULL terminate the whole thing
			
		}
	}
	else {
		*tablenames = NULL; // didnt get any
	}
	kfree(bigbuf);
	return 0;
	
}

// assume names is pointer to a NULL terminated array of kmalloced pointers
// kfree each pointer then kfree the array
// char *[] ---> char *
//          ---> char *
//          ---> NULL
// there is probably something generic this could be replaced with...
void iptableproc_free_anynames(unsigned char ***names) {
	int i;
	if(names == NULL || *names == NULL)
		return;  // been passed a null or the thing pointed at is already empty so no work to do
	// deref once to get the char **
	// the iterate through to get individual strings
	// depend on this being NULL terminated
	for(i = 0; (*names)[i] != NULL; i++) {
		kfree((*names)[i]);
	}
	// and the pointer storage
	kfree(*names);
	// and make sure the now freed memory does not get referenced
	// this is why we are passed a char ***
	*names = NULL;
}

// decide what sort of chain this is
// -1 for user defined, 0 for none, positive for one of the bultins
static inline int ischain(struct ipt_entry *e, struct ipt_table *t, void *etable) {
	unsigned int builtin;	
	struct ipt_entry_target *tgt = ipt_get_target(e);
	// if the target name == "ERROR"		
	if(tgt->u.kernel.target->name && !strcmp(tgt->u.kernel.target->name,XT_ERROR_TARGET)) {
		// user defined chain - the data contains the real name, ignoring it if that too is called ERROR
		if((unsigned char *)tgt->data && strcmp((unsigned char *)tgt->data,XT_ERROR_TARGET)) 
			return CHAIN_USERDEF;
	}
	else if((builtin = ent_is_hook_entry(e,t,etable)) != 0) 
		// This e is one of the known hook entry points
		return (int)builtin;
	
	return CHAIN_NONE;
}

// Callback for use with IPT_ENTRY_ITERATE
// increment i if we see a chain so i gets left with count of chains seen
static inline int
count_one(struct ipt_entry *e, struct ipt_table *t, void *etable, unsigned int *i) {
	if(ischain(e,t,etable) != CHAIN_NONE) // dont care which at this point
		(*i)++;
	// return of 0 means carry on iterating to next entry
	return 0;
}

// returns a count of the chains leaving it in the chaincount pointer
// we look at the entries table for the current cpu
// and apply count_one to each entry in turn.
// which counts the chains for us.
static void count_chains(struct ipt_table *t, unsigned int *chaincount)
{	
	struct xt_table_info *p;	
	unsigned int curcpu = raw_smp_processor_id();
	
	if(!t || !chaincount)
		return; // cant work if not given pointers
	p = t->private;
	IPT_ENTRY_ITERATE(p->entries[curcpu],p->size,
			  count_one,t,(void *)(p->entries[curcpu]),chaincount);
}	

// now allocate the chain name
static inline int
kmalloc_one(struct ipt_entry *e, struct ipt_table *t, void *etable, unsigned char **vec, unsigned int * i) {
	struct ipt_entry_target *tgt = ipt_get_target(e);
	
	int ct = ischain(e,t,etable);
	if(ct == CHAIN_USERDEF) {
		vec[*i] = kmalloc(strlen((unsigned char *)tgt->data)+1, GFP_KERNEL);
		if(vec[*i] == NULL) {
			printk(KERN_ALERT "Error: Could not get memory for iptableproc_get_chainnames\n");
			return -ENOMEM; // stops list iteration
		}
		strcpy(vec[*i], (unsigned char *)tgt->data);
		(*i)++; // so point at next
		
	}
	else if(ct > CHAIN_NONE) {
		vec[*i] = kmalloc(strlen(hooknames[ct-1])+1, GFP_KERNEL);
		if(vec[*i] == NULL) {
			printk(KERN_ALERT "Error: Could not get memory for iptableproc_get_chainnames\n");
			return -ENOMEM; // stops list iteration
		}
		strcpy(vec[*i], hooknames[ct-1]);
		(*i)++;
	}
	return 0;
}

// assigns the chain names
// assumes that the table is big enough to take all chains
static void assign_chains(struct ipt_table *t, unsigned char **table)
{
	unsigned int i = 0;
	
	unsigned int curcpu = raw_smp_processor_id();
	struct xt_table_info *p;
	if(!t || !table)
		return; // cant work 
	p = t->private;	
	IPT_ENTRY_ITERATE(p->entries[curcpu], p->size,
			  kmalloc_one, t, (void *)p->entries[curcpu], table, &i);
	// NULL terminate the table
	table[i] = NULL;
	
}
	
// This is a different strategy to get_tablenames, we need to iterate
// through the available chains for this table.
// need to have lock for seeing how many chains there are and then allocating space for the names.
int iptableproc_get_chainnames(const unsigned char *tablename, unsigned char ***chainnames) { 
	unsigned int num_names = 0;
  	unsigned char name[IPT_TABLE_MAXNAMELEN];
	struct ipt_table *t;
	int ret =0;
	if(!tablename || !chainnames)
		return -ENOMEM; // is this a good error?
	
	// so are sure this is not too long...
	strncpy(name, tablename, IPT_TABLE_MAXNAMELEN);
	name[IPT_TABLE_MAXNAMELEN-1] = '\0';
	if(chainnames == NULL){
		// come on - nowhere to stick this?
		printk(KERN_ALERT "Error: no memory provided for iptableproc_get_chainnames");
		return -ENOMEM;
	}
	if(*chainnames != NULL){
		// old junk - free it (sets *chainnames to NULL)
		iptableproc_free_anynames(chainnames);
	}	
	
	// looking for the table called name - may have to load a module to get it
	// if this code looks familiar its because its been stolen from iptables.c :)
	// our needs are much the same as sending this stuff userspacewards
	
	t = try_then_request_module(xt_find_table_lock(AF_INET, name), "iptable_%s", name);
	// locked from now on...
	if (t && !IS_ERR(t)) {
		count_chains(t, &num_names); 
		if(num_names > 0) {
			*chainnames = kcalloc(num_names+1, sizeof(unsigned char **), GFP_KERNEL);
			if(*chainnames == NULL) {
				printk(KERN_ALERT "Error: Could not get memory for iptableproc_get_chainnames\n");
				ret = -ENOMEM;
				goto error_state;
			}
			// while still locked fetch the names of the chains
			assign_chains(t, *chainnames);
		}
					
		ret = 0; // ok 
error_state:
		xt_table_unlock(t);
		module_put(t->me);
	}
	else {
		ret = t ? PTR_ERR(t) : -ENOENT;
	}
	return ret;
}  


// sets inchain if we are in the chain, if we are in the chain increment count of rules
static inline int
scan_for_rule(struct ipt_entry *e, struct ipt_table *t, void *etable,const unsigned char *chainname, int *i, int *inchain, int *rulecount) {
	
	struct ipt_entry_target *tgt = ipt_get_target(e);
	
	int ct = ischain(e,t,etable);
	// user defined chain, dont count this as one of the rules			
	if(ct == CHAIN_USERDEF) {	
		if(!strcmp(chainname,(unsigned char *)tgt->data)) {
			*inchain = 1;
			*rulecount = 0;
			// DBG4("In chain for user def %s (%s) at %d count=%d\n", chainname, (ussigned char *)tgt->data, *i, *rulecount);
		}
		else {
			// not in this chain anymore
			*inchain = 0;
		}
	}
	else if(ct > CHAIN_NONE) {
		if(!strcmp(chainname,hooknames[ct-1])) {
			*inchain = 1;
			*rulecount = 0;
			//DBG4("In chain for builtin %s (%s) at %d count=%d\ ", chainname, hooknames[ct-1], *i, *rulecount);
		}
		else {
			// not in builtin chain anymore
			*inchain = 0;
		}
		
		goto process_rule; // consider as a rule too
	}
	else { // not a chain head
process_rule:
		if(*inchain) {
			(*rulecount)++;
			// DBG4("Chain %s (%d) seen rule %d inchain %d\n", chainname, *i, *rulecount, *inchain);
		}
	}

	// always increment - our index through this 'array'
	(*i)++;
	// return early if no longer in a chain and have seen rules - got to next chain
	if(!*inchain && *rulecount) {
		// DBG0("early ret\n");
		return 1;
	}
	else {
		return 0;
	}
}

// applies scan_for_rule to each rule in the table, ending as soon as transition 
// from collecting rules to not collecting them
// note the last rule in the chain is its default policy if the chain is a builtin one.

static void get_num_rules_in_chain(struct ipt_table *t, const unsigned char *chainname, int *num_rules)
{
	unsigned int i = 0;
	int inchain = 0;
	
	unsigned int curcpu = raw_smp_processor_id();
	struct xt_table_info *p;
	
	if(!t || !chainname || !num_rules)
		return; // cant work
	p = t->private;
	*num_rules = 0; // start with no rules, all valid built in chains
	// have at least one rule (the policy) user defined chains do not.
	IPT_ENTRY_ITERATE(p->entries[curcpu], p->size,
			  scan_for_rule,t,(void *)(p->entries[curcpu]),chainname,&i,&inchain,num_rules);
		
}
	
// we need to iterate along the chain and find each rule in it, the actual rulenames themselves are just small ints as an
// array of strings (NULL terminated)
int iptableproc_get_rulenames(const unsigned char *tablename, const unsigned char *chain, unsigned char ***rulenames) {
  	unsigned char name[IPT_TABLE_MAXNAMELEN];
	struct ipt_table *t;
	int ret =0;
	int num;
	int num_rules = 0;
	// DBG1("get_chainnames %s\n", tablename);
	// so are sure this is not too long...
	strncpy(name, tablename, IPT_TABLE_MAXNAMELEN);
	name[IPT_TABLE_MAXNAMELEN-1] = '\0';
	if(rulenames == NULL){
		// come on - nowhere to stick this?
		printk(KERN_ALERT "Error: no memory provided for iptableproc_get_rulenames");
		return -ENOMEM;
	}
	if(*rulenames != NULL){
		// old junk - free it (sets *rulenames to NULL)
		iptableproc_free_anynames(rulenames);
	}	
	
	// looking for the table called name - may have to load a module to get it
	// if this code looks familiar its because its influenced by what goes on in iptables userspace
	// our needs are much the same as sending this stuff userspacewards
	
	t = try_then_request_module(xt_find_table_lock(AF_INET, name), "iptable_%s", name);
	// locked from now on...
	if (t && !IS_ERR(t)) {
		get_num_rules_in_chain(t,  chain, &num_rules);
		if(num_rules > 0) {
			// DBG2("%s generating %d rules\n", chain, num_rules);
			*rulenames = kcalloc(num_rules+1, sizeof(unsigned char **), GFP_KERNEL);
			if(*rulenames == NULL) {
				printk(KERN_ALERT "Error: Could not get memory for iptableproc_get_rulenames\n");
				return -ENOMEM;
			}
			// just numbers so fixed size kmalloc 10 bytes each - no way will encounter rules numbered into the hundreds of millions!
			for(num = 0; num < num_rules; num++) {
				(*rulenames)[num] = kmalloc(10, GFP_KERNEL);
				if((*rulenames)[num] == NULL) {
					printk(KERN_ALERT "Error: Could not get memory for iptableproc_get_rulenames\n");
					return -ENOMEM;
				}
				snprintf((*rulenames)[num],10, "%d", num);
			}
			(*rulenames)[num] = NULL;
		}
		ret = 0; // ok 
		xt_table_unlock(t);
		module_put(t->me);
	}
	else {
		ret = t ? PTR_ERR(t) : -ENOENT;
	}
	return ret;	
}


// go through much the same logic as scan_for_rule but instead of counting them, get the counters if this is the
// rulename rule of chainname chain
// each cpu keeps separate counters - but we need these summed to get totals
static inline int get_counters_callback(struct ipt_entry *e, // the entry itself
										struct ipt_table *t, // table we are in - needed to find chain
										void *etable, // base of table this entry is in 
										const unsigned char *chainname, // chain we are looking for
										const unsigned char *rulename, // rule we are looking for
										int *i, // index within the table as a whole
										int *inchain, // remember if we are in the chain,
										int *rulecount,// which rulenumber this is
										struct xt_counters counters[]) {
	int rulenum, rcnt;
	unsigned int cpu,curcpu;
	struct ipt_entry *other;
	unsigned int offset;
	struct xt_table_info *p;
	
	if(!chainname || !rulename)
		rcnt = 1; // bad params so stop scan here, assume everything else is ok
	else {
		p = t->private;
		sscanf(rulename,"%d", &rulenum);
		// reuse this code, we are scan_for_rule plus a bit
		rcnt = scan_for_rule(e,t,etable,chainname,i,inchain,rulecount);
		if(*inchain && (*rulecount == rulenum)) {
			// we are in the required chain and the rule number
			curcpu = raw_smp_processor_id();
			// we are already pointing at the right cpu
			SET_COUNTER(counters[0], e->counters.bcnt, e->counters.pcnt);
			// the layout of rules for each extra CPU is identical so just do offset maths
			// rather than chasing through the atble again
			offset = (void *)e - etable;
			for_each_cpu(cpu) {
				if (cpu == curcpu)
					continue;
				other = (struct ipt_entry *)((void *)(p->entries[cpu] + offset)); // and now pointing at other cpus data
				ADD_COUNTER(counters[0], other->counters.bcnt, other->counters.pcnt);
			}
			rcnt = 1; // return early
		}
		else
			rcnt = 0; // normal iteration return - not found it yet
	}	
	// increment our index through this 'array'
	(*i)++;
	return rcnt;
}

// same thing but for a whole chain at once, or rather the first num_cnt rules.
			
static inline int get_chain_counters_callback(struct ipt_entry *e, // the entry itself
										struct ipt_table *t, // table we are in - needed to find chain
										void *etable, // base of table this entry is in 
										const unsigned char *chainname, // chain we are looking for
										int *i, // index within the table as a whole
										int *inchain, // remember if we are in the chain,
										int *rulecount,// which rulenumber this is										
										struct xt_counters counters[],
										int *num_cnt) {
	int rcnt;
	unsigned int cpu,curcpu;
	struct ipt_entry *other;
	unsigned int offset;
	struct xt_table_info *p;
	
	if(!chainname) {
		DBG0("Bad chainname!");
		rcnt = 1; // bad params so stop scan here, assume everything else is ok
	}
	else {
		p = t->private;
		// reuse this code, we are scan_for_rule plus a bit
		rcnt = scan_for_rule(e,t,etable,chainname,i,inchain,rulecount);
		if(rcnt == 0) {
			// DBG1("get_chain_counters_callback  rcnt %d\n", *rulecount);
			if(*inchain && (*rulecount <= *num_cnt)) {
				
				// we are in the required chain and the rule number
				curcpu = raw_smp_processor_id();
				// we are already pointing at the right cpu
				SET_COUNTER(counters[*rulecount], e->counters.bcnt, e->counters.pcnt);
				
				// the layout of rules for each extra CPU is identical so just do offset maths
				// rather than chasing through the atble again
				offset = (void *)e - etable;
				
				for_each_cpu(cpu) {
					if (cpu == curcpu)
						continue;
					other = (struct ipt_entry *)((void *)(p->entries[cpu] + offset)); // and now pointing at other cpus data
					ADD_COUNTER(counters[*rulecount], other->counters.bcnt, other->counters.pcnt);
				}
				
				rcnt = (*rulecount > *num_cnt); // if too many return now
			} 
		}
		else
			rcnt = 0; // normal iteration return - not found it yet
	}
	// increment our index through this 'array'
	(*i)++;	
	return rcnt;
}


// get the counters for the named table/chain/rule
// or just the table/chain if no rule bit.
// the xt_counters ** is assumed to be an array of counters, num_cnt starts as the number of slots available
// and gets written with the number of slots used.
// Works for individual rules and whole chains.
// if passed a null cnt we kmalloc the counters  
int iptableproc_get_counters(const unsigned char *table, const unsigned char *chain,
							 const unsigned char *rule, struct xt_counters **cnt, int *num_cnt) {
	unsigned int curcpu;
	struct ipt_table *t;
	struct xt_table_info *p;
	int i = 0;
	int inchain = 0;
	int rulecount = 0;
	int ret = 0;
	if(!table|| !chain)
		return -ENOMEM; // is this a good error? 
	
	if(!cnt) {
		// come on - nowhere to stick this?
		printk(KERN_ALERT "Error: no memory provided for iptableproc_get_counters");
		return -ENOMEM;
	}
	t = try_then_request_module(xt_find_table_lock(AF_INET, table), "iptable_%s", table);
	// locked from now on...
	if (t && !IS_ERR(t)) {
		curcpu = raw_smp_processor_id();	
		p = t->private;	
		if(rule) {
			if(*cnt == NULL) {
				(*cnt) = (struct xt_counters *)kcalloc(1,sizeof(struct xt_counters),  GFP_KERNEL);
				if(*cnt == NULL) {
					printk(KERN_ALERT "Error: Could not get memory for iptableproc_get_counters\n");
					ret = -ENOMEM;
					goto error_return;
				}
				
			}
			// have been give single instance of storage and have specified a rule
			IPT_ENTRY_ITERATE(p->entries[curcpu], p->size,
					get_counters_callback, t, (void *)p->entries[curcpu], chain, rule,
										   &i, &inchain, &rulecount, *cnt);
			*num_cnt = 1; // we wrote one counter
		}
		else {
			
			// rule not specified - want whole chain stats, so while locked get count of rules in this chain - it may have changed
			get_num_rules_in_chain(t,  chain, &rulecount);
			
			if(*cnt == NULL && rulecount > 0) {
				// permission to allocate memory - the caller will need to kfree this later
				(*cnt) = (struct xt_counters *)kcalloc(rulecount,sizeof(struct xt_counters), GFP_KERNEL);
				if((*cnt) == NULL) {
					printk(KERN_ALERT "Error: Could not get memory for iptableproc_get_counters\n");
					ret = -ENOMEM;
					goto error_return;
				}
				
				*num_cnt = rulecount; // how many we are collecting
				
				
				// passed pointer to array of xt_counters, want num_cnt of them 
				IPT_ENTRY_ITERATE(p->entries[curcpu], p->size,
					get_chain_counters_callback, t, (void *)p->entries[curcpu], chain,
								     &i, &inchain, &rulecount, *cnt, num_cnt);
				// what we managed to get
				*num_cnt = rulecount;
				
			}
			else {
				// if *cnt not null have no way of knowing if its big enough - so dont use
				// DBG1("Chain %s has no rules\n", chain);
				*num_cnt = 0;
			}
		}
		ret = 0; // ok
error_return: 
		xt_table_unlock(t);
		module_put(t->me);
	}
	else {
		DBG0("did not get t!!\n");
		ret = t ? PTR_ERR(t) : -ENOENT;
	}
	return ret;
}

static inline int get_facts_callback(struct ipt_entry *e, // the entry itself
									 struct ipt_table *t, // table we are in - needed to find chain
									 void *etable, // base of table this entry is in 
									 const unsigned char *chainname, // chain we are looking for
									 const unsigned char *rulename, // rule we are looking for
									 int *i, // index within the table as a whole
									 int *inchain, // remember if we are in the chain,
									 int *rulecount,// which rulenumber this is
									 rule_basic_facts *facts) {
	int rulenum, rcnt;
	struct xt_table_info *p;
	p = t->private;
	sscanf(rulename,"%d", &rulenum);
	rcnt = scan_for_rule(e,t,etable,chainname,i,inchain,rulecount);	
	if(*inchain && (*rulecount == rulenum)) {
		// we are in the required chain and the rule number - so fill in the other facts	
		strncpy(facts->iniface, e->ip.iniface, sizeof(e->ip.iniface));
		strncpy(facts->outiface, e->ip.outiface, sizeof(e->ip.outiface));
		facts->src.s_addr = e->ip.src.s_addr;
		facts->dst.s_addr = e->ip.dst.s_addr;
		facts->smsk.s_addr = e->ip.smsk.s_addr;
		facts->dmsk.s_addr = e->ip.dmsk.s_addr;
		facts->proto = e->ip.proto;
		rcnt = 1; // we found it so stop iterating
	}	
	// increment our index through this 'array'
	(*i)++;
	return rcnt;
}

// get other information about this rule
// efficiency7 is not important here as it is rarley called , just when some process reads the 
// info or raw_info file associated with the rule.
int iptableproc_get_facts_for_rule(iptableproc_rule_info *r, rule_basic_facts *facts) {
	int ret;
	unsigned char *table, *chain, *rule;
	struct ipt_table *t;
	struct xt_table_info *p;
	unsigned int curcpu;
	int i = 0;
	int inchain = 0;
	int rulecount = 0;
	
	if(!r)
		return -1;
	
	table = r->parent_chain->parent_table->name;
	chain = r->parent_chain->name;
	rule = r->name;
	
	t = try_then_request_module(xt_find_table_lock(AF_INET, table), "iptable_%s", table);
	// locked from now on...
	if (t && !IS_ERR(t)) {
		curcpu = raw_smp_processor_id();	
		p = t->private;	
		
		IPT_ENTRY_ITERATE(p->entries[curcpu], p->size,
			  	get_facts_callback, t, (void *)p->entries[curcpu], chain, rule,
			  						&i, &inchain, &rulecount, facts);
			
		ret = 0; // ok
		xt_table_unlock(t);
		module_put(t->me);
	}
	else {
		DBG0("did not get t!!\n");
		ret = t ? PTR_ERR(t) : -ENOENT;
	}
	return ret;	
	
}
