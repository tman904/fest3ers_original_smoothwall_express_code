#ifndef __IPTABLEPROC_H__
#define __IPTABLEPROC_H__
#include <linux/module.h>	// Needed by all modules 
#include <linux/kernel.h>	// Needed for KERN_INFO 
#include <linux/proc_fs.h>	// Necessary because we use the proc fs 
#include <linux/delay.h>
#include <linux/seq_file.h>
#ifdef OLD_KERNEL
#include <linux/netfilter/ip_tables.h>
#else
#include <linux/netfilter/x_tables.h>
#endif
#include <linux/netfilter_ipv4/ip_tables.h>
#include <linux/kmod.h>
#include <linux/syscalls.h>
#include <linux/fcntl.h>
#include <linux/vmalloc.h>
#include <asm/uaccess.h>	// for copy_from_user

#ifndef VERSION
#define VERSION "0.1"
#endif

#define DRIVER_AUTHOR "Martin Houston <martin.houston@smoothwall.net>"
#define DRIVER_DESC "/proc interface for iptables"

#define MYDEBUG 1
// or KERN_INFO
#define MY_INFO KERN_INFO
#if MYDEBUG == 2
// FMT has to be a string constant of some sort A1 etc can be anything
#define XDBG(li) printk(MY_INFO " iptableproc " __FILE__ " (" #li ") "
#define YDBG(li) XDBG(li)
#define DBG0(FMT) YDBG(__LINE__) FMT)
#define DBG1(FMT,A1) YDBG(__LINE__) FMT, A1)
#define DBG2(FMT,A1,A2) YDBG(__LINE__) FMT, A1,A2)
#define DBG3(FMT,A1,A2,A3) YDBG(__LINE__) FMT, A1,A2,A3)
#define DBG4(FMT,A1,A2,A3,A4) YDBG(__LINE__) FMT, A1,A2,A3,A4)
#endif

#if MYDEBUG == 1
#define DBG0(FMT) printk(MY_INFO " iptableproc " FMT)
#define DBG1(FMT,A1) printk(MY_INFO " iptableproc " FMT,A1)
#define DBG2(FMT,A1,A2) printk(MY_INFO " iptableproc " FMT,A1,A2)
#define DBG3(FMT,A1,A2,A3) printk(MY_INFO " iptableproc " FMT,A1,A2,A3)
#define DBG4(FMT,A1,A2,A3,A4) printk(MY_INFO " iptableproc " FMT,A1,A2,A3,A4)
#endif

#ifndef DBG0
#define DBG0(FMT)
#endif

#ifndef DBG1 
#define DBG1(FMT,A1)
#endif

#ifndef DBG2 
#define DBG2(FMT,A1,A2)
#endif

#ifndef DBG3 
#define DBG3(FMT,A1,A2,A3)
#endif

#ifndef DBG4
#define DBG4(FMT,A1,A2,A3,A4)
#endif 


// generic counter type for byte/packet cooked/raw

typedef enum { pcnt=0, bcnt=1, raw_pcnt=2, raw_bcnt=3, invalid=4 } info_type;

#define CHAIN_USERDEF -1
#define CHAIN_NONE 0

// predeclarations
struct iptableproc_rule_info;
struct iptableproc_chain_info;
struct iptableproc_table_info;

// each chain and rule directory can contain all the different choices of counter access
// bcnt - byte count formatted as ascii with a newline at end.
// for whole chains a tab separated sequence of counts for the rules in each chain.
// pcnt ditto for packets.
// raw_bcnt - just the raw counter values, for a single rule that would just be a single 64bit value in native byte order.
// for a chain a sequence of 64bit values in native byte order.
// for a table the above just concatenated together. The application is assumed to know the order of chains and
// how many rules are in each. The idea of raw versions is to minimise the kernel side work.
// rate at which samples are sent is controlled on a per directory basis - i.e. there is no provision for
// one user to use bcnt at 10 x a second while another users uses raw_pcnt at 50 x a second.

typedef struct iptableproc_counter {

	info_type counter_type; // what sort of file is this i.e. which behaviour
	struct proc_dir_entry *file; // its presence in /proc
	struct iptableproc_rule_info *rule; // is NULL if this is whole chain counter
	struct iptableproc_chain_info *chain; // is NULL if this is a single rule counter
} iptableproc_counter;



// we have a hirachy in proc:
// /proc/iptableproc/filter/INPUT/0 represents rule 0 of the INPUT chain of the filter table.
// we want to be able to extract all counters for a chain or even for a whole table so we have the bcnt/pcnt etc files at the 
// other directory levels too.

// binary info about a rule

typedef struct rule_basic_facts {
	unsigned char iniface[XT_FUNCTION_MAXNAMELEN]; // incomming interface
	unsigned char outiface[XT_FUNCTION_MAXNAMELEN]; // outgoing interface
	struct in_addr src,dst,smsk,dmsk; // source, destination addresses and masks
	u_int16_t proto; // protocol this rule is for 0 = any
} rule_basic_facts;

typedef struct iptableproc_rule_info {
	struct list_head list; // list this rule is on
	struct proc_dir_entry *thisdir;
	struct iptableproc_chain_info *parent_chain; // chain we are in
	unsigned char name[XT_FUNCTION_MAXNAMELEN]; // may want to allow symbolicly named rules at some point
	iptableproc_counter cnt[4]; // 4 files bytes packets and raw vers of each
	struct proc_dir_entry *interval_file;
	// of this interval in 1000ths of a sec
	// if 0 use parents and so on until reach global value
	unsigned int interval;
	// info about the rule both as space separated text
	struct proc_dir_entry *info;
	// and as a struct rule_basic_facts
	struct proc_dir_entry *raw_info;
} iptableproc_rule_info;

typedef struct iptableproc_chain_info {
	struct list_head list; // list this chain is on
	struct proc_dir_entry *thisdir;
	struct iptableproc_table_info *parent_table; // chain we are in
	struct list_head rules; // linked list of rules in this chain
	unsigned char name[XT_FUNCTION_MAXNAMELEN]; // name of this chain
	struct iptableproc_counter cnt[4]; // 4 files bytes packets and raw vers of each for whole chain stats
	struct proc_dir_entry *interval_file;
	unsigned int interval;
} iptableproc_chain_info;


	
typedef struct iptableproc_table_info {
	struct list_head list; // list of tables we are on
	struct proc_dir_entry *thisdir;
	struct list_head chains; // linked list of chains in this table
	unsigned char name[XT_FUNCTION_MAXNAMELEN]; // name of this table
	// no per table counters or interval
} iptableproc_table_info;

// defined in seqstuff.c
int iptableproc_init_seq_file(iptableproc_counter *f, info_type t, const unsigned char *name, 
iptableproc_rule_info *r, iptableproc_chain_info *c);
iptableproc_counter * iptableproc_lookup_counter(struct inode *inode, 
												 const unsigned char *table, 
												 const unsigned char *chain, 
												 const unsigned char *rule);
int iptableproc_find_sleep(const iptableproc_counter *c);
extern int iptableproc_dummy_rate_pattern[];

// get the names of tables present at the moment
int iptableproc_get_tablenames(unsigned char ***tablenames);
// get the names of chains present in the named table
int iptableproc_get_chainnames(const unsigned char *tablename, unsigned char ***chainnames);
// get the rule names (numbers actually) in the named table/chain
int iptableproc_get_rulenames(const unsigned char *tablename, const unsigned char *chain, unsigned char ***rulenames);
// works for tables and chains and rules so called anynames
void iptableproc_free_anynames(unsigned char ***names);

// copy the current bcnt and pcnt counter values for this paricular rule into the supplied pointer

int iptableproc_get_counters(const unsigned char *table, const unsigned char *chain, const unsigned char *rule, struct xt_counters **cnt, int *num_cnt);

int iptableproc_build_filetree(void);

// get the 'other' info about this rule, things that form a core part of the rule
// rather than being extension specific.
int iptableproc_get_facts_for_rule(iptableproc_rule_info *r, rule_basic_facts *facts);

// these lock but only unless we already know we hold a 
// lock. Allow locking to be done at a higher level in some funcs
int iptables_global_lock(int locked, int *welocked);
int iptables_global_unlock(int locked, int *welocked);


#endif
