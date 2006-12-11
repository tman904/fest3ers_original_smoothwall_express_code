// proc filesystem side of iptableproc
// (c) Martin Houston, SmoothWall Ltd 2006.
// Released under the GPL.


#include "iptableproc.h"

// seqfile stuff, need a distinct position holder for this seq so kmalloc it
/*
 * Discussion of seq_read
 * if a struct file* is associated with a sequence (by seq_open) then attempts
 * by the user to read that file will come through the seq_read kernel
 * function.
 * 
 * The seq_file info is kept in the private_data area of the file struct
 * The intermediate kernel buffer is allocated to hold data being read
 * - the size of which is 1 page (i.e. 4k) so no single read op can be larger than this!
 * Note that seq_read has a lock on the seq_file struct in use.
 * This means more than one user cannot be calling seq_read on the same file
 * at the same time.
 */
static void *ct_seq_start(struct seq_file *s, loff_t *pos)
{
  // loff_t is a long long, we allocate one here and init it with
  // while in the 'file' we wish to start
  // normally this would be 0 but the user is free to seek on this interface
  // has to be dynamic as could have more than one reader!
	loff_t *spos = kmalloc(sizeof(loff_t), GFP_KERNEL);
	
	if (! spos) {
	  DBG0("kmalloc fail");
	  return NULL; // kmalloc fails!
	}
	*spos = *pos; // set initial value
	// DBG2("%s seq_start %ld\n", cnt->fullpath, (long int)*spos);
	return spos;
}

// v is the loff_t ptr we kmalloced in start
static void *ct_seq_next(struct seq_file *s, void *v, loff_t *pos)
{
	loff_t *spos = (loff_t *) v;
	
	// return and increment next position
	*pos = ++(*spos);
	
	return spos;
}
// v is the loff_t ptr we kmalloed in start
static void ct_seq_stop(struct seq_file *s, void *v)
{
  // if(s->private != NULL) {
	//iptableproc_counter *cnt = (iptableproc_counter *)s->private;
	// printk(KERN_INFO "%s seq_stop\n",cnt->fullpath);
  //}
  
  kfree (v);
}

static int ct_seq_show(struct seq_file *s, void *v)
{

	int timeout, ret, welocked;
	int i;
	unsigned char *rule = NULL;
	unsigned char *chain = NULL;
	unsigned char *table = NULL;
	char buf[25];
  	int bufcnt;
  	struct xt_counters *xt_cnt = NULL; // will be kmalloced
  	int numcnt = 0;
  	iptableproc_counter *cnt = NULL;
  	welocked = 0;
  	if(s->private != NULL) {
  		// lock as need to fetch counter and relate that back to parent
  		ret = iptables_global_lock(0,&welocked);
  		cnt = (iptableproc_counter *)s->private;
  		// work out where we are
  		if(cnt->rule) {
  			rule = cnt->rule->name;
  			chain = cnt->rule->parent_chain->name;
  			table = cnt->rule->parent_chain->parent_table->name;
  		}
  		else {
  			if(cnt->chain) {
  				chain = cnt->chain->name;
  				table = cnt->chain->parent_table->name;
  			}
  		}
		if(!table || !chain) {
			DBG0("seq_show bad params\n");
			ret = -1;
			goto err_return;
		
		}

  		timeout = iptableproc_find_sleep(cnt);
  		// DBG1("sleeping %d\n", timeout);
  		
  		msleep(timeout);
  		// now get the counters

  		if(iptableproc_get_counters(table, chain, rule, &xt_cnt, &numcnt) == 0) {
  		
  		if(!xt_cnt) {
  			DBG0("no counters!\n");
  			return -1;
  		}
		if(cnt->counter_type == bcnt) {
			for(i = 0; i < numcnt; i++) {
#ifdef IPTABLEPROC_HEX_OUTPUT
				// want zero filled hex - advantage: each report is a known size
				bufcnt = snprintf(buf, sizeof(buf)-1,"%016lX ", (long unsigned int)xt_cnt[i].bcnt);
#else
				// want decimal - advantage: each report is no larger than it needs to be
				// but in either case has to be null filled up to the buffer size the user requests 
				// or we will be hanging around in the seq code.
				bufcnt = snprintf(buf, sizeof(buf)-1,"%ld ", (long unsigned int)xt_cnt[i].bcnt);
#endif
				// DBG3("cnt = %d buf = %s (%d)\n", s->count, buf, bufcnt);
				memcpy(s->buf + s->count,buf,bufcnt);
				s->count += bufcnt;
			}
			// turn the last space into newline
				if(s->buf[s->count-1] == ' ') {
					s->buf[s->count-1] = '\n';
				}
				else {
					// DBG2("Cant see \t at %d in %s\n", s->count, s->buf);
				}
			}
			else if(cnt->counter_type == pcnt) {
				for(i = 0; i < numcnt; i++) {
#ifdef IPTABLEPROC_HEX_OUTPUT
					bufcnt = snprintf(buf, sizeof(buf)-1,"%016lX ", (long unsigned int)xt_cnt[i].pcnt);
#else
					bufcnt = snprintf(buf, sizeof(buf)-1,"%ld ", (long unsigned int)xt_cnt[i].pcnt);
#endif

					// DBG3("cnt = %d buf = %s (%d)\n", s->count, buf, bufcnt);
					memcpy(s->buf + s->count,buf,bufcnt);
					s->count += bufcnt;
				}
				// turn the last space into newline
				if(s->buf[s->count-1] == ' ') {
					s->buf[s->count-1] = '\n';
				}
			}
			else if(cnt->counter_type == raw_bcnt) {
				// no delimeters - raw 64 bit values
				for(i = 0; i < numcnt; i++) {
					memcpy(s->buf + s->count, &(xt_cnt[i].bcnt), sizeof(xt_cnt[i].bcnt));
					s->count += sizeof(xt_cnt[i].bcnt);
				}
			}
			else if(cnt->counter_type == raw_pcnt) {
				for(i = 0; i < numcnt; i++) {
					memcpy(s->buf + s->count, &(xt_cnt[i].pcnt), sizeof(xt_cnt[i].pcnt));
					s->count += sizeof(xt_cnt[i].pcnt);
				}
			}
			kfree(xt_cnt);
  		}
  		else {
  			DBG3("Failed to get counters for %s/%s/%s\n", table,chain,rule);
  			ret =-1;
  			goto err_return;
  		}

  	}
  	else {
		printk(KERN_ALERT "ct_seq_show - no associated data!\n");
		msleep(100);
  	}
  	// say we have it all - null padded
  
  	// DBG2("cnt = %d buf = %s \n", s->count, s->buf);
  	while(s->count < (s->size-1)) {
  		s->buf[s->count++] = 0;
  	}  
  	ret = 0;
err_return:
	iptables_global_unlock(0,&welocked);
  	return ret;
}

//
// Tie them all together into a set of seq_operations.
//

static struct seq_operations ct_seq_ops = {
	.start = ct_seq_start,
	.next  = ct_seq_next,
	.stop  = ct_seq_stop,
	.show  = ct_seq_show
};

// go via inode number of file to find associated data file.
// have to scan all ruledirs (most likley) followed by chaindirs and tabledirs to
// find an inode match
// This could probably benefit from some sort of btree sorted by inode
// linear search for now.
// before we do anything check that iptables is the same state and
// adjust our view accordingly.
// if the table/chain we are attempting to open is no longer there then fail.


static int ct_open(struct inode *inode, struct file *file)
{
	struct seq_file *seq;
	int ret; 
	// unsigned char *self = file->f_dentry->d_iname;
	unsigned char *parent = NULL;
	unsigned char *grandparent = NULL;
	unsigned char *greatgrandparent = NULL;
	iptableproc_counter *cnt;
	DBG1("ct_open of %s\n", file->f_dentry->d_iname);
	// iptableproc_build_filetree();
	// open a sequence using the above handlers
	ret = seq_open(file, &ct_seq_ops);

	if(ret)
	  return ret; // no good
	// DBG1("ct_open in %s\n", parent);
	// now associate the sequence with the right object
	// seq_open uses the private_data field of file to store sequence info 
	seq = file->private_data;
	if(seq) {
		if(file->f_dentry->d_parent) {
			cnt = NULL;
			parent = file->f_dentry->d_parent->d_iname;
			if(file->f_dentry->d_parent->d_parent) {
				grandparent = file->f_dentry->d_parent->d_parent->d_iname;
				if(file->f_dentry->d_parent->d_parent->d_parent)
					greatgrandparent = file->f_dentry->d_parent->d_parent->d_parent->d_iname;
			}
			// DBG4("ct_open %s/%s/%s/%s\n", greatgrandparent, grandparent, parent, self);
			
			// case of iptableproc/filter/INPUT/bcnt
			if(!strcmp(greatgrandparent,"iptableproc")) {
				// DBG0("Chain level\n");
				// we are a chain level counter, parent is chain, grandparent is table
				cnt =  iptableproc_lookup_counter(inode, grandparent, parent, NULL);
			}
			else {
				DBG3("Rule level %s/%s/%s\n",greatgrandparent, grandparent, parent);
				// we are a rule level counter, so greatgrandparent is table
				cnt =  iptableproc_lookup_counter(inode, greatgrandparent, grandparent, parent);
			}
	  		if(cnt) {
	  			seq->private = cnt;
	  		}
	  		else {
	  			printk(KERN_ALERT "breakdown in ct_open - no cnt\n");
				ret = -EIO;
	  		}	
	  }
	}
	else {
		printk(KERN_ALERT "breakdown in ct_open - no private_data\n");
		ret = -EIO;
	} 
	return ret;
};

//
// The file operations structure contains our open function along with  set of the canned seq_ ops.
//
static struct file_operations ct_file_ops = {
	.owner  = THIS_MODULE,
	.open	= ct_open,
	.read	= seq_read,
	.llseek  = seq_lseek,
	.release = seq_release
};

// utility function - set up the sequence file f of type t using name name in parent r or c
int iptableproc_init_seq_file(iptableproc_counter *f, info_type t, 
							  const unsigned char *name, 
							  iptableproc_rule_info *r, iptableproc_chain_info *c) {

  
  f->rule = r;
  f->chain = c;
 
  f->file =  create_proc_entry(name,0,(r ? r->thisdir : c->thisdir));
  if (f->file) {
	f->file->proc_fops = &ct_file_ops; // so opening does the righ thing for seq
	f->file->mode = S_IFREG | S_IRUGO; // regualr file read only
	f->counter_type = t;
  }
  else {
	f->counter_type = invalid;
	printk(KERN_ALERT "Error: Could not create_proc_entry for %s\n", name);
	return -ENOMEM;
  }	
 
  return 0;
}

