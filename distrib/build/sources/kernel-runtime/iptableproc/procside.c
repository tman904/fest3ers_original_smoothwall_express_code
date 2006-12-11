// proc filesystem side of iptableproc
// (c) Martin Houston, SmoothWall Ltd 2006.
// Released under the GPL.

#include "iptableproc.h"


// module data
static int sample_delay = 100;
static int (*orig_readdir) (struct file *, void *, filldir_t);
// the names of the counter files to create
static unsigned char *cnt_filenames[] = { "pcnt","bcnt","raw_pcnt","raw_bcnt"};

module_param(sample_delay, int, S_IRUSR | S_IWUSR | S_IRGRP | S_IWGRP);
MODULE_PARM_DESC(sample, "Global test resampling delay, in usec, min acceptable value is 100 (i.e 10 samples per sec)");


#define toplevel_name "iptableproc"

struct proc_dir_entry *toplevel;

// we dynamicaly allocate info for all the tables
static struct list_head known_tables;
// and any processes sleeping while reading our stuff
static struct list_head known_sleepers;
// anything to do with accessing the known tables tree is subject to a global lock
static struct semaphore known_tables_mutex;
// this is set to true only in module unload - before that there may be someone reading something.
static int known_tables_teardown_ok = 0;
// 
// these lock but only unless we already know we hold a 
// lock. Allow locking to be done at a higher level in some funcs
int iptables_global_lock(int locked, int *welocked) {
	int ret = 0;
	if(!locked) {
  		// try to lock it
  		ret = down_interruptible(&known_tables_mutex);
		if (ret != 0)
			return ret; // failed to lock it!
		*welocked = 1;
  	}
  	return ret;
}
// and the opposite
// only unlock if we were the one who locked
// otherwise this is a noop
int iptables_global_unlock(int locked, int *welocked) {
	int ret = 0;
	if(welocked) {
  		// we locked it so free it
  		up(&known_tables_mutex);
  	}
  	return ret;
}
// needed from seqstuff - turn file inode number into which
// of our records it applies to. Linear search for now but have chain and possibly
// also rule names as the file associated with the inode had directory info
// We assume that the underlying iptables data can change at any time so for the relativle small
// amounts involved here probably not worth building a hash.
iptableproc_counter * iptableproc_lookup_counter(struct inode *inode, 
												 const unsigned char *table, 
												 const unsigned char *chain, 
												 const unsigned char *rule) {
	iptableproc_table_info *t = NULL;
	iptableproc_chain_info *c = NULL;
	iptableproc_rule_info *r = NULL;
  	unsigned int this_ino = inode->i_ino;
  	iptableproc_counter *cnt;
  	int ret, welocked;
  	iptableproc_counter *rval = NULL;

  	DBG1("Looking for inode %X\n", this_ino);
  	
  	ret = iptables_global_lock(0, &welocked);
	if (ret != 0) {
		DBG0("Lock failed!");
		return NULL; // failed to lock it!
	}	
  	list_for_each_entry(t, &known_tables, list) {
  		if(!strcmp(t->name, table)) {
  			DBG1("In table %s\n", table);
  			// we are in the right table
  			list_for_each_entry(c, &(t->chains), list) {
  				if(!strcmp(c->name, chain)) {
  					DBG1("In chain %s\n", chain);
  					// and the right chain
  					if(!rule) {
  						// no rules - whole chain counters
  						for(cnt = &(c->cnt[0]); 
  							cnt < &(c->cnt[sizeof(c->cnt)/sizeof(*(c->cnt))]);
  							cnt++) {
  							DBG3("%d Comparing %X to %X\n", (int)cnt->counter_type,
  								this_ino, cnt->file->low_ino);
  							if(this_ino == cnt->file->low_ino) {
  								DBG1("Match at chain file %d\n", (int)cnt->counter_type);
  								rval = cnt; // found it
  								break;
  							}
  						}
  					}
  					else {
  						// scan rules too
  						list_for_each_entry(r, &(c->rules), list) {
  							if(!strcmp(r->name, rule)) {
  								DBG1("In rule %s\n", rule);
  								for(cnt = &(r->cnt[0]); cnt < 
  									&(r->cnt[sizeof(r->cnt)/sizeof(*(r->cnt))]); 
  									cnt++) {
  									if(this_ino == cnt->file->low_ino) {
  										DBG1("Match at rule file %d\n", (int)cnt->counter_type);
  										rval = cnt; // found it
  										break;
  									}
  								}
  							}	
  						}
  					}
  				}
  			}
  		}
  	}
  	iptables_global_unlock(0,&welocked);				
					
	return rval;
}

// function find_sleep - to find the approprate timeout to sleep for
// look in parent and parents parent if present, use global if nothing else
int iptableproc_find_sleep(const iptableproc_counter *cnt) {
	iptableproc_rule_info *r;
	iptableproc_chain_info *c;
  
	if(cnt != NULL) {
  		if(cnt->rule != NULL) {
  			// are a rule counter
			r = cnt->rule;
			if(r->interval)
				return r->interval;
			// look to parent chain
			c = r->parent_chain;
  		}
  		else {
  			// are a chain counter
  			c = cnt->chain;
  		}
  		if(c && c->interval)
  			return c->interval;
	}
	else {
		DBG0("iptableproc_find_sleep passed a NULL pointer!");
	}
  		
	// global default
  	return sample_delay;
}


// the interval file is a simple case as it just contains an integer read/write is as ascii.
static int procfile_interval_read(char *buffer,
		  						  char **buffer_location,
								  off_t offset, int buffer_length, int *eof, void *data) {
	unsigned int *ourdata = (unsigned int *)data;

	int ret = 0;

	if(ourdata == NULL) {
		printk(KERN_ALERT "Error: procfile_interval_read cannot find data\n");
		return ret;
	}

	*eof = 1;
	ret = snprintf(buffer, buffer_length,"%d\n", *ourdata);
	return ret;
}
	
// this is the handler to write the interval file for this rule - this 
// controlls how many thousandths of a second to wait between samples.	
static int procfile_interval_write(struct file *file, const char *buffer, unsigned long count,void *data) {
	unsigned int *ourdata = (unsigned int *)data;
	int ret = 0;
	unsigned int interval;
	char buf[20];

	if(ourdata == NULL) {
		printk(KERN_ALERT "Error: procfile_interval_read cannot find data\n");
		return ret;
	}
	// string the user sends us
	if(copy_from_user(buf, buffer, (count < sizeof(buf)-1 ? count: sizeof(buf)-1))) 
		return -EFAULT;
	sscanf(buf, "%d", &interval);
	if(interval >0 && interval < 100)
  		interval = 100; // 10 samples a sec max rate if specified - sanity level
	*ourdata = interval;
	return count;
}		

// handler for reading the info file
static int proc_info_read(char *buffer,
		  				  char **buffer_location,
						  off_t offset, int buffer_length, int *eof, void *data) {
	iptableproc_rule_info *r = (iptableproc_rule_info *)data;
	rule_basic_facts facts;
	int ret = 0;

	if(r == NULL) {
		printk(KERN_ALERT "Error: procfile_info_read cannot find data\n");
		return ret;
	}
	
	*eof = 1;
	ret = iptableproc_get_facts_for_rule(r, &facts);
	if(ret == 0) {

		ret = snprintf(buffer,buffer_length,
			"table=%s\nchain=%s\nrule=%s\nin=%s\nout=%s\nin_addr=%x\nout_addr=%x\nsrc_mask=%x\ndst_mask=%x\nproto=%x\n",
			r->parent_chain->parent_table->name, 
			r->parent_chain->name,
			r->name,
			facts.iniface, facts.outiface, facts.src.s_addr, facts.dst.s_addr, facts.smsk.s_addr, facts.dmsk.s_addr,
			(int) facts.proto);
		return ret;
	}
	else {
		return 0;
	}
}

// handler for reading the raw_info file
static int proc_raw_info_read(char *buffer,
		  				  char **buffer_location,
						  off_t offset, int buffer_length, int *eof, void *data) {
	iptableproc_rule_info *ourdata = (iptableproc_rule_info *)data;
	int ret = 0;
	rule_basic_facts facts;

	if(ourdata == NULL) {
		printk(KERN_ALERT "Error: procfile_raw_info_read cannot find data\n");
		return ret;
	}
	*eof = 1;
	ret = iptableproc_get_facts_for_rule(ourdata, &facts);
	if(ret == 0) {
		memcpy(buffer, &facts, sizeof(facts));
		ret = sizeof(facts);
		return ret;
	}
	else {
		return 0; // nothing to read
	}
}
						  


// we need to remove our rule,
// takes a parameter - are we locked already?
static int takedown_rule(iptableproc_rule_info *r, int locked) {
	int ret,i;
	int welocked = 0;
	if(!known_tables_teardown_ok)
		return 0;
	ret = iptables_global_lock(locked, &welocked);
	
	if (ret != 0)
		return ret; // failed to lock it!
  	for(i = 0; i < sizeof(r->cnt)/sizeof(iptableproc_counter); i++) {
  		DBG3("Removing %s/%s/%s\n", r->parent_chain->name, r->name, cnt_filenames[i]);
  		remove_proc_entry(cnt_filenames[i], r->thisdir);
  	}
  	// The interval file
  	if(r->interval_file) {
  		DBG2("Removing %s/%s/interval\n", r->parent_chain->name,r->name);
  		remove_proc_entry("interval", r->thisdir);
  	}
  	// The info and raw_info files
  	if(r->info) {
  		DBG2("Removing %s/%s/info\n", r->parent_chain->name,r->name);
  		remove_proc_entry("info", r->thisdir);
  	}
  	if(r->raw_info) {
  		DBG2("Removing %s/%s/raw_info\n", r->parent_chain->name,r->name);
  		remove_proc_entry("raw_info", r->thisdir);
  	}
  	// and this directory itself
  	DBG2("removing %s/%s\n", r->parent_chain->name, r->name);
  	remove_proc_entry(r->name, r->parent_chain->thisdir);
  	DBG2("freeing rule %s of chain %s\n", r->name, r->parent_chain->name);
  	list_del(&(r->list));
  	kfree(r);
  	return iptables_global_unlock(locked,&welocked);
}

// we need to remove our chain,
// takes a parameter - are we locked already?
static int takedown_chain(iptableproc_chain_info *c, int locked) {
	int i;
	int ret;
	int welocked = 0;
	iptableproc_rule_info *r,*tmp;
	if(!known_tables_teardown_ok)
		return 0;
	ret = iptables_global_lock(locked, &welocked);
	
	if (ret != 0)
		return ret; // failed to lock it!
	
	// first does a chain have any rules?
	
	// use list_for_each_safe as are removing the entries
	// we are locked by now so return value of takedown_rule not important
  	list_for_each_entry_safe(r, tmp, &(c->rules), list) {
  		DBG2("Chain %s Taking down rule %s\n", c->name, r->name); 
  		takedown_rule(r,1);
  	}				
  		
  	// now our own chain counters
 	for(i = 0; i < sizeof(c->cnt)/sizeof(iptableproc_counter); i++) {
 		DBG2("Removing %s/%s\n", c->name, cnt_filenames[i]);
 		remove_proc_entry(cnt_filenames[i], c->thisdir);
  	}
  	// The interval file
  	if(c->interval_file) {
  		DBG1("Removing %s/interval\n", c->name);
  		remove_proc_entry("interval", c->thisdir);
  	}
  	// and this directory itself
  	DBG2("removing chain %s/%s\n", c->parent_table->name, c->name);
  	remove_proc_entry(c->name, c->parent_table->thisdir);
  	DBG2("freeing chain %s of table %s\n", c->name, c->parent_table->name);
  	list_del(&(c->list));
  	kfree(c);
  	return iptables_global_unlock(locked,&welocked);
} 	
 
// we need to remove our table,
// takes a parameter - are we locked already?

static int takedown_table(iptableproc_table_info *t, int locked) {
  	iptableproc_chain_info *c,*tmp;
  	int ret;
  	int welocked = 0;
  	if(!known_tables_teardown_ok)
		return 0;
  	ret = iptables_global_lock(locked, &welocked);
	
	if (ret != 0)
		return ret; // failed to lock it!
  	
  	
  	list_for_each_entry_safe(c, tmp, &(t->chains), list) {
  		// we are locked by now so return value of takedown chain not important
  		(void)takedown_chain(c, 1);
  	}

  	// and this directory itself
  	DBG1("remove proc entry for %s\n", t->name);
  	remove_proc_entry(t->name, toplevel);
  	DBG1("freeing table %s\n", t->name);
  	list_del(&(t->list));
  	kfree(t); 
  	return iptables_global_unlock(locked,&welocked);	
}
// this scans the list of tables/chains etc and makes our view agree with what is in iptables just now
// The locked parameter is set if we are already locked, if not locked then we must lock
// before doing anything to the tree
static int rule_add_if_not_there(iptableproc_chain_info *c,const unsigned char *name, int locked) {
	iptableproc_rule_info *r = NULL;
	int ret,i;
  	int welocked = 0;
  	// suppress making rule 0 as it isnt a real rule
  	if(!strcmp(name, "0"))
  		return 0;
  	ret = iptables_global_lock(locked, &welocked);
	
	if (ret != 0)
		return ret; // failed to lock it!
  
	// see if we already have a chain of this name, if not create one
	
	list_for_each_entry(r, &(c->rules), list) {
		if(!strcmp(r->name, name))
			DBG1("Found %s already\n", name);
			break; // found a match
	}
	
	
	if(!r || strcmp(r->name, name)) {
		// nothing there yet or not a match
		DBG1("Need to make rule %s\n", name);
		r = (iptableproc_rule_info *)kcalloc(1, sizeof(iptableproc_rule_info), GFP_KERNEL);
		if(r == NULL) {
			printk(KERN_ALERT "Error: Could not get memory for table_add_if_not_there\n");
			ret = -ENOMEM;
			goto error_state;
		}
		else {
			// create our /proc resources
			DBG2("Creating  %s/%s\n", c->name, name);
			r->thisdir = proc_mkdir(name, c->thisdir);
			if(r->thisdir == NULL) {
				printk(KERN_ALERT "Error: Could not do proc_mkdir of %s in rule_add_if_not_there\n", name);
				ret = -ENOMEM;
				goto error_state;
			}
			r->thisdir->owner = THIS_MODULE;
			r->parent_chain = c;
			strncpy(r->name, name, sizeof(r->name));
			r->interval_file = create_proc_entry("interval",0,r->thisdir);
			if(r->interval_file == NULL) {
				printk(KERN_ALERT "Error: Could not do create_proc_entry of interval in rule_add_if_not_there\n");
				ret = -ENOMEM;
				goto error_state;
			}
			// set handlers for it
  			r->interval_file->read_proc = procfile_interval_read;
  			r->interval_file->write_proc = procfile_interval_write;
  			r->interval_file->owner = THIS_MODULE;
  			r->interval_file->mode = S_IFREG |  S_IRUGO | S_IWUGO; // read and writeable
  			r->interval_file->uid = 0;
  			r->interval_file->gid = 0;
  			r->interval_file->size = sizeof(unsigned int);
			
  			r->interval_file->data = (void *)&(r->interval); // so we can get back
  			r->interval = 0;  // undefined by default
  			
  			// and the info file
  			r->info = create_proc_entry("info",0,r->thisdir);
			if(r->info == NULL) {
				printk(KERN_ALERT "Error: Could not do create_proc_entry of info in rule_add_if_not_there\n");
				ret = -ENOMEM;
				goto error_state;
			}
			// set handlers for it
  			r->info->read_proc = proc_info_read;
  			r->info->owner = THIS_MODULE;
  			r->info->mode = S_IFREG | S_IRUGO;
  			r->info->uid = 0;
  			r->info->gid = 0;
  			r->info->size = 0; // work this out later
			
  			r->info->data = (void *)r; // so we can get back this rule
  			r->raw_info = create_proc_entry("raw_info",0,r->thisdir);
			if(r->raw_info == NULL) {
				printk(KERN_ALERT "Error: Could not do create_proc_entry of raw_info in rule_add_if_not_there\n");
				ret = -ENOMEM;
				goto error_state;
			}
			// set handlers for it
  			r->raw_info->read_proc = proc_raw_info_read;
  			r->raw_info->owner = THIS_MODULE;
  			r->raw_info->mode = S_IFREG | S_IRUGO;
  			r->raw_info->uid = 0;
  			r->raw_info->gid = 0;
  			r->raw_info->size = sizeof(rule_basic_facts);
			
  			r->raw_info->data = (void *)r; // so we can get back this rule
  			
  			for(i = 0; i < sizeof(cnt_filenames)/sizeof(*cnt_filenames); i++) {
  				iptableproc_init_seq_file(&(r->cnt[i]), (info_type)i, cnt_filenames[i], r, NULL);
  				r->cnt[i].rule = r; // we belong to a rule
  				r->cnt[i].chain = NULL; // not a chain
  			}
  			
  			// we already have one rule so just add this to the list
  			list_add(&(r->list), &(c->rules)); // add to the list
  			
		}
	}
	ret = 0;
error_state:
	
  	iptables_global_unlock(locked,&welocked);
  	return ret;
}
// we are given a list of rules and a list 
int rule_remove_if_not_there(iptableproc_chain_info *c, unsigned char **names, int locked) {
	iptableproc_rule_info *r, *tmp;
	int i,found;
	int ret;
  	int welocked = 0;
  	
  	ret = iptables_global_lock(locked, &welocked);
	
	if (ret != 0)
		return ret; // failed to lock it!
  	
	list_for_each_entry_safe(r, tmp, &(c->rules), list) {
		// now see if this is a currently known name
		DBG1("Looking at rule %s\n", r->name);
		found = 0;
		for(i = 0; names[i]; i++) {
				
			if(!strcmp(names[i], r->name)) {
				DBG1("Rule %s still there\n", names[i]);
				found = 1;
				break;
			}
		}
		if(!found) {
			// oh dear - this rule no longer here
			DBG3("Rule %s/%s/%s seems to have dissappeared\n", r->parent_chain->parent_table->name,
														  r->parent_chain->name, r->name);
			takedown_rule(r,1);
		}
	}
	
  	return iptables_global_unlock(locked,&welocked);
}
	
// check if rules are as specified in chain - remove any rules no longer mentioned
// assume c is a valid chain - called form chain_add_if_not_there
static int check_rules(iptableproc_chain_info *c, int locked) {
	unsigned char **rules = NULL;
	int ri;
	int ret;
  	int welocked = 0;
  	ret = iptables_global_lock(locked, &welocked);
	
	if (ret != 0)
		return ret; // failed to lock it!
  	
	if(!c || !c->parent_table)
		return -ENOMEM;
		
	DBG2("Getting rules for %s/%s\n", c->parent_table->name, c->name);
		
	if(iptableproc_get_rulenames(c->parent_table->name, c->name, &rules) == 0) {
		for(ri = 0; rules[ri]; ri++) {
			DBG3("check_rules Looking for %s/%s/%s\n", c->parent_table->name, c->name, rules[ri]);
			rule_add_if_not_there(c, rules[ri], 1);
		}
		rule_remove_if_not_there(c, rules, 1); // remove any tables that have gone
		iptableproc_free_anynames(&rules);
	}
	else {
		// hmm - we seem to no longer have any chains.
		DBG1("Chain %s seems to no longer have any rules - so removing it\n", c->name);
		takedown_chain(c,1);
	}
	
  	return iptables_global_unlock(locked,&welocked);
}

// If this function is called with a name then that name is a currentley valid
// chain name for table t.
// If table t does not already have such a chain it need to have one made
// In any case have to check that the chain has the same number of rules that it used to.
static int chain_add_if_not_there(iptableproc_table_info *t, const unsigned char *name, int locked) {
	iptableproc_chain_info *c = NULL;
	int i;
	int ret = 0;
	int welocked = 0;
	ret = iptables_global_lock(locked, &welocked);
	
	if (ret != 0)
		return ret; // failed to lock it!
  	
	// see if we already have a chain of this name, if not create one
		list_for_each_entry(c, &(t->chains), list) {
		if(!strcmp(c->name, name)) {
			DBG2("%s has a chain %s\n", t->name, c->name);
			break; // found a match
		}
	}
	
	
	if(!c || strcmp(c->name, name)) {
		// nothing there yet or not a match
		DBG2("%s does not yet have a chain %s\n", t->name, name);
		c = (iptableproc_chain_info *)kcalloc(1, sizeof(iptableproc_chain_info), GFP_KERNEL);
		if(c == NULL) {
			printk(KERN_ALERT "Error: Could not get memory for chain_add_if_not_there\n");
			ret = -ENOMEM;
			goto error_exit; // so unlock properley
		}
		else {
			// create our /proc resources
			DBG2("Creating chain %s/%s\n", t->name,name);
			// the chain dir is a subdir of the table dir
			c->thisdir = proc_mkdir(name, t->thisdir);
			if(c->thisdir == NULL) {
				printk(KERN_ALERT "Error: Could not do proc_mkdir of %s in chain_add_if_not_there\n", name);
				ret = -ENOMEM;
				goto error_exit;
			}
			c->thisdir->owner = THIS_MODULE;
			c->parent_table = t;
			strncpy(c->name, name, sizeof(c->name));
			INIT_LIST_HEAD(&(c->rules));
			// now the files that have to be in this dir
			c->interval_file = create_proc_entry("interval",0,c->thisdir);
			if(c->interval_file == NULL) {
				printk(KERN_ALERT "Error: Could not do create_proc_entry of interval in chain_add_if_not_there\n");
				ret = -ENOMEM;
				goto error_exit;
			}
			// set handlers for it
  			c->interval_file->read_proc = procfile_interval_read;
  			c->interval_file->write_proc = procfile_interval_write;
  			c->interval_file->owner = THIS_MODULE;
  			c->interval_file->mode = S_IFREG | S_IWUGO; // regular file writeable
  			c->interval_file->uid = 0;
  			c->interval_file->gid = 0;
  			c->interval_file->size = sizeof(unsigned int);
			
  			c->interval_file->data = (void *)&(c->interval); // so we can get back
  			c->interval = 0;
  			// and the counters, rule NULL - these are whole chain counters
  			for(i = 0; i < sizeof(cnt_filenames)/sizeof(*cnt_filenames); i++) {
  				iptableproc_init_seq_file(&(c->cnt[i]), (info_type)i, cnt_filenames[i], NULL, c);
  				c->cnt[i].rule = NULL;
  				c->cnt[i].chain = c;
  			} 			
  			list_add(&(c->list), &(t->chains)); // add to the list
		}
	}
	// regardless now investigate rules in this chain
	DBG2("Checking rules in %s/%s\n", t->name,c->name);
	check_rules(c,1);
	ret = 0;
	
error_exit:
	iptables_global_unlock(locked,&welocked);
  	return ret;
}

// we are given a list of chains and a list 
int chain_remove_if_not_there(iptableproc_table_info *t, unsigned char **names, int locked) {
	iptableproc_chain_info *c, *tmp;
	int i,found;
	int ret;
  	int welocked = 0;
  	ret = iptables_global_lock(locked, &welocked);
	
	if (ret != 0)
		return ret; // failed to lock it!
  	
	list_for_each_entry_safe(c, tmp, &(t->chains), list) {
		// now see if this is a currently known name
		found = 0;
		for(i = 0; names[i]; i++) {
			if(!strcmp(names[i], c->name)) {
				found = 1;
				break;
			}
		}
		if(!found) {
			// oh dear - this chain no longer here
			DBG2("Chain %s/%s seems to have dissappeared\n", t->name,c->name);
			takedown_chain(c,1);
		}
	}
  	return iptables_global_unlock(locked,&welocked);
}

	

// this scans the list of tables/chains etc and makes our view agree with what is in iptables just now

// check if chains are as specified in table - remove any chains no longer mentioned, visit the others to check rules
// assume t is a valid table - called form table_add_if_not_there
static int check_chains(iptableproc_table_info *t, int locked) {
	unsigned char **chains = NULL;
	int ci;
	int ret;
  	int welocked = 0;
  	ret = iptables_global_lock(locked, &welocked);
	
	if (ret != 0)
		return ret; // failed to lock it!
  	
  	DBG1("Checking chains in %s\n", t->name);	
	if(iptableproc_get_chainnames(t->name, &chains) == 0) {
		for(ci = 0; chains[ci]; ci++) {
			chain_add_if_not_there(t, chains[ci], 1);
		}
		chain_remove_if_not_there(t, chains, 1); // remove any tables that have gone
		iptableproc_free_anynames(&chains);
	}
	else {
		// hmm - we seem to no longer have any chains.
		DBG1("Table %s seems to no longer have any chains - so removing it\n", t->name);
		takedown_table(t,1);
	}
	
  	return iptables_global_unlock(locked,&welocked);	
}
// adds a table if there is not one already present and in any case go on to look at chains
// this is the only case where the param is a **, in inner cases the param is the outer pointer object
static int table_add_if_not_there(struct list_head *tp, const char *name, int locked) {
	iptableproc_table_info *t = NULL;
	int ret;
  	int welocked = 0;
  	ret = iptables_global_lock(locked, &welocked);
	
	if (ret != 0)
		return ret; // failed to lock it!
  	
	// see if we already have a table of this name, if not create one
	
	list_for_each_entry(t, tp, list) {
		if(!strcmp(t->name, name)) {
			DBG1("Found %s - no need to add\n", name);
			break; // found a match
		}
	}
	
	
	if(!t || strcmp(t->name, name)) {
		// nothing there yet or not a match
		DBG1("Adding table %s\n", name);
		t = (iptableproc_table_info *)kcalloc(1, sizeof(iptableproc_table_info), GFP_KERNEL);
		if(t == NULL) {
			printk(KERN_ALERT "Error: Could not get memory for table_add_if_not_there\n");
			ret = -ENOMEM;
			goto error_return;
		}
		else {
			// create our /proc resources
			DBG1("Creating table %s\n", name);
			t->thisdir = proc_mkdir(name, toplevel);
			if(t->thisdir == NULL) {
				printk(KERN_ALERT "Error: Could not do proc_mkdir of %s in table_add_if_not_there\n", name);
				ret = -ENOMEM;
				goto error_return;
			}
			t->thisdir->owner = THIS_MODULE;
			strncpy(t->name, name, sizeof(t->name));
			INIT_LIST_HEAD(&(t->chains));
			
  			list_add(&(t->list), tp); // add to the list
		}
	}
	// regardless now investigate chains on this table
	DBG1("Now checking chains in %s\n", t->name);
	check_chains(t,1);
	ret = 0;
error_return:
	iptables_global_unlock(locked,&welocked);
  	return ret;
}
  			
// we are given a pointer to list of tables and a list of names of currentley known tables
int table_remove_if_not_there(struct list_head *tp, unsigned char **names, int locked) {
	iptableproc_table_info *t, *tmp;
	int i,found;
  	int ret = 0;
  	int welocked = 0;
  	
  	ret = iptables_global_lock(locked, &welocked);
	
	if (ret != 0)
		return ret; // failed to lock it!
  		
	list_for_each_entry_safe(t, tmp, tp, list) {
		// now see if this is a currently known name
		found = 0;
		for(i = 0; names[i]; i++) {
			if(!strcmp(names[i], t->name)) {
				found = 1;
				DBG1("%s is a still known table\n", names[i]);
				break;
			}
		}
		if(!found) {
			// oh dear - this table no longer here
			DBG1("%s seems to have dissappeared\n", t->name);
			ret = takedown_table(t,1);
		}
	}
	iptables_global_unlock(locked,&welocked);
  	return ret;
}

			
	
int iptableproc_build_filetree(void) {
	int ret;
	int i;
	int welocked = 0;
	unsigned char **tables = NULL;
	

	// DBG0("build_filetree\n");
	ret = iptables_global_lock(0, &welocked);
	
	if (ret != 0)
		return ret; // failed to lock it!
	
	// DBG0("Got lock\n");
	if(iptableproc_get_tablenames(&tables) == 0) {
		for(i = 0; tables[i]; i++) {
			// DBG1("scanning table %s\n", tables[i]);
			table_add_if_not_there(&known_tables, tables[i],1); // 1 indicates we already have the lock
		}
		// DBG0("Seeing if any tables are gone\n");
		table_remove_if_not_there(&known_tables, tables,1); // remove any tables that have gone
		iptableproc_free_anynames(&tables);
	}

	// DBG0("Freeing lock\n");
	iptables_global_unlock(0,&welocked);
	return 0;	
}
//
// intercept the readdir
static int our_proc_readdir(struct file * filp,void * dirent, filldir_t filldir) {
	static struct timeval lastrun = {0};
	struct timeval now = {0};
	do_gettimeofday(&now);
	if(now.tv_sec >( lastrun.tv_sec+5)) {
		// do this once every 5 secs max rate
		// DBG1("our_proc_readdir %ld\n", now.tv_sec);
		// iptableproc_build_filetree();
		lastrun.tv_sec = now.tv_sec;
	}
	return orig_readdir(filp, dirent,filldir);
}

static int __init iptableproc_init(void) {
  
  unsigned char ** tables = NULL;
#ifdef VERBOSE
  int i,j,k;
  unsigned char ** chains = NULL; 
  unsigned char ** rules = NULL;
#endif
	// quick sanity check that have not exceeded parameters

	INIT_LIST_HEAD(&known_tables);
	INIT_LIST_HEAD(&known_sleepers);

	// initialise our mutex for known_tables tree  
	init_MUTEX(&known_tables_mutex);
	printk(KERN_INFO "iptableproc %s loaded\n", VERSION);
	printk(KERN_INFO "sample_delay = %d usec\n", sample_delay);

	// walk the trees just to log what we see initialy
	if(iptableproc_get_tablenames(&tables) == 0) {
#ifdef VERBOSE
		// announce it
		for(i = 0; tables[i] != NULL; i++) {
			printk(KERN_INFO "table %s\n", tables[i]);
			
			if(iptableproc_get_chainnames(tables[i], &chains) == 0) {
				// and the chains
				
				if(chains) {
					for(j = 0; chains[j] != NULL; j++) {
						printk(KERN_INFO "	chain %s\n", chains[j]);
						if(iptableproc_get_rulenames(tables[i], chains[j], &rules) == 0) {
							if(rules) {
								for(k = 0; rules[k]; k++) {
									printk(KERN_INFO "		rule %s\n", rules[k]);
								}
								iptableproc_free_anynames(&rules);
							}
							else {
								printk(KERN_INFO "table %s chain %s NO RULES\n", tables[i], chains[j]);
							}
						}
						else {
							printk(KERN_ALERT "iptableproc: iptableproc_get_rulenames failure");
							return -ENOMEM;
						}
					}
					iptableproc_free_anynames(&chains);
				}
				else {
					printk(KERN_INFO "table %s NO CHAINS\n", tables[i]);
				}
				
			}
			else {
				printk(KERN_ALERT "iptableproc: iptableproc_get_chainnames failure");
				return -ENOMEM;
			}
		}
#endif
		iptableproc_free_anynames(&tables);
	}
	else {
		printk(KERN_ALERT "iptableproc: does not look like iptables is loaded? - no tables even!");
		return -ENOMEM;
	}
		

	// now make initial view of the state of iptables
	toplevel = proc_mkdir(toplevel_name, NULL);

	if(toplevel == NULL) {
		remove_proc_entry(toplevel_name,NULL);
		printk(KERN_ALERT "Error: Could not initialize /proc/%s\n", toplevel_name);
		return -ENOMEM;	
	}
	// DBG1("Initied /proc/%s\n", toplevel_name);
	toplevel->owner = THIS_MODULE;			
	orig_readdir = toplevel->proc_fops->readdir;
	// toplevel->proc_fops->readdir = &our_proc_readdir;

	// initial build
	iptableproc_build_filetree();
		
	/* 
	 * A non 0 return means init_module failed; module can't be loaded. 
	 */
	return 0;
}


// note the __exit macro will cause this function to be omitted if 
// the code is built into the kernel
static void __exit iptableproc_exit(void)
{	
	int ret, welocked =0;
	iptableproc_table_info *t, *tmp;
  	// take down our /proc prescence 
	
	known_tables_teardown_ok = 1;
	// need it inform any known_sleepers to quit
	// TO BE DONE
	ret = iptables_global_lock(0, &welocked);
	if(ret != 0) {
		DBG1("Failed to get lock! Err %d\n", ret);
		return;
	}
	list_for_each_entry_safe(t, tmp, &(known_tables), list)
  		takedown_table(t,1);
  
  	
	// root last
	remove_proc_entry(toplevel_name, NULL);
	printk(KERN_INFO "iptableproc %s unloaded\n", VERSION);
	iptables_global_unlock(0,&welocked);
}

module_init(iptableproc_init);
module_exit(iptableproc_exit);

MODULE_LICENSE("GPL");

MODULE_AUTHOR(DRIVER_AUTHOR);	// Who wrote this module? 
MODULE_DESCRIPTION(DRIVER_DESC); // What does this module do ?

