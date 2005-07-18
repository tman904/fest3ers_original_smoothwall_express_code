// C++ interface to tc and netfilter traffic stats collection
#include <sys/time.h>
#include <asm/types.h>
#include <linux/pkt_sched.h>
#include <string>
#include <iostream>
#include <sstream>
#include <vector>
#include <map>
#include <set>
#include <sstream>
#include <syslog.h>
#include "configvar.hpp"
#include "traffic_config.hpp"
#include "timestamp.hpp"


// An item that specifies class or rule stats
// designed to work for either tc or iptables info


class traf_stat {


    // has to all be public as need to populate from a callback from C code
public:
    timestamp tstamp;
    std::string error;
    std::string classid; // classid of this class
    std::string parentid; // classid of the parent
    std::string dev; // associated device
    // floating point bytes, bits and packets values
    // derrived by comparing to previous sample
    double bytes_per_sec, bits_per_sec, pkts_per_sec;
    __u32 info;
    double rate,ceiling; // if this is a class these are guaranteed rate and ceiling
    // for that class - so we can express a true bits per sec rate as 
    // (over)percentage of rate and percentage of ceiling as well as
    // percentage of whole interface speed.

    int rule_num; // if this is not 0 then this is for a rule
                  // and parentid not relivant
   
    struct tc_stats stats;
    // this is the same algorithm tc uses to show speeds


    std::string tc_classid(__u32) const;
    
    
   
    traf_stat() {
        gettimeofday(&tstamp.t, NULL);
        classid = "";
        parentid = "";
        info = (__u32)0;
        error = "";
        dev = "";
        rule_num = -1;
        bytes_per_sec = bits_per_sec = pkts_per_sec = 0.0;
        stats.bytes = 0;
        stats.packets = 0;
        stats.drops = 0;
        stats.overlimits = 0;
        stats.bps = 0;
        stats.pps = 0;
        stats.qlen = 0;
        stats.backlog = 0;
        rate = ceiling = 0;
    };
    bool is_rule() const { return rule_num >= 0; };
    bool is_class() const { return rule_num < 0 && classid != ""; };
    bool has_parent() const { return parentid != ""; };    
    bool has_class() const { return classid != ""; };
    bool has_dev() const { return dev != ""; };
    
    __u64 bytes() const { return stats.bytes;};
    __u32 packets() const { return stats.packets;};
    __u32 drops() const { return stats.drops;}; 
    __u32 overlimits() const { return stats.overlimits; };
    __u32 bps() const { return stats.bps; }; // bytes per sec
    __u32 pps() const { return stats.pps; }; // packets per sec
    __u32 qlen() const { return stats.qlen; };
    __u32 backlog() const { return stats.backlog; };

   
   
};

// so can sort these in classid/parent order
bool operator < (const traf_stat &a, const traf_stat &b);
// so can print out everything
std::ostream& operator << (std::ostream& out,  const traf_stat& i);

typedef std::vector<std::string> Vstring;
typedef Vstring ::iterator Vstring_iterator;
typedef Vstring ::const_iterator Vstring_const_iterator;

typedef std::vector<traf_stat> Vtraf_stat;
typedef Vtraf_stat  ::iterator Vtraf_iterator;
typedef Vtraf_stat  ::const_iterator Vtraf_const_iterator;

std::ostream& operator << (std::ostream& out, const Vtraf_stat & i);


// take a device name and return vector of stats for that class
Vtraf_stat list_class(std::string dev);
Vtraf_stat list_class(const char * dev);

// get a list of rules in a specific chain and counters for them
Vtraf_stat list_rules(std::string chain);
// get a list of rules in a specific chain and counters for them
Vtraf_stat list_rules_for_dev(std::string dev);
Vtraf_stat list_rules_for_dev(const char *dev);


typedef std::set<std::string> StrSet;
typedef StrSet ::iterator StrSet_iterator;
typedef StrSet ::const_iterator StrSet_const_iterator;

typedef std::map<std::string, traf_stat> traf_stat_hash;
typedef traf_stat_hash ::iterator traf_stat_hash_iterator;
typedef traf_stat_hash ::const_iterator traf_stat_hash_const_iterator;

// now we collect all the stats we can togther as a single timestamped sample
void calculate_rates(traf_stat & older, traf_stat & newer,
                     double &bytes_per_sec, 
                     double &bits_per_sec, 
                     double &pkts_per_sec);
void calculate_rates(traf_stat & older, traf_stat & newer);
static traf_stat_hash latest_stats;


class traf_stat_collection_item {

public:
    timestamp collection_start, collection_end;
    // internal, external devices, classes, rules available in this sample
    // as this MAY WELL CHANGE over time!
    StrSet int_devs, ext_devs, classes, rules;
    // lump all stats together in same hash, info from int_devs and ext_devs
    // classes and rules lets us form keys
    
    traf_stat_hash stats;

    traf_stat_collection_item();

    // return the class element indexes in their proper sort order
    // i.e. not alphabetic
    Vstring class_indexes_in_order();

            
    // cull  any stats that have not changed since last time
    void compress ();

};



typedef std::vector<traf_stat_collection_item> Vtraf_stat_samples;
typedef Vtraf_stat_samples ::iterator Vtraf_stat_samples_iterator;
typedef Vtraf_stat_samples ::const_iterator Vtraf_stat_samples_const_iterator;

std::ostream& operator << (std::ostream& out, const traf_stat_collection_item & i);
 // speed this interface runs at, in bits per sec
double interface_speed(std::string dev, std::string direction = "");
    double time_interval( const timestamp &oldtime, const timestamp &newtime);
bool collect_a_sample(Vtraf_stat_samples &samples);
int collect_samples(int number, int interval, Vtraf_stat_samples &samples);

// make an average of the last (default 10) samples
// going for the record matching idx each time
// double average_bit_rate(Vtraf_stat_samples &samples, const std::string &idx, unsigned int num = 10);
// take an average over a time period
double average_bit_rate(Vtraf_stat_samples &samples, const std::string &idx, const timestamp &start, const timestamp &end);
// remove samples older than certain time
void truncate_sample_set(Vtraf_stat_samples &samples, const timestamp &oldest);
std::string format_rate(double tmp);
// do two at once
std::string format_rate(double t1, double t2);

// indicate if the rules we need are minimally in place
bool traffic_iptables_missing();

