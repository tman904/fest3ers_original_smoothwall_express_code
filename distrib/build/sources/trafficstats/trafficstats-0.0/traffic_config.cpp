#include "traffic_config.hpp"
#include <sys/stat.h>
#include <sstream> // for ostringstream

// take a string quanity plus units and converts to double bits  value
// coded for speed, sees NUM then optional k or m or g then bit or bps
// bit is bits bps is bytes so mult by 8


double to_bits(const char *in) {

    char numbit[20] = {0};
    double multiplier = 1.0;
    char c;
    int i;
    for(i = 0; i < 20 && in[i]; i++) {
        c = tolower(in[i]);
                   
        if(isdigit(c))
            numbit[i] = c;
        if(c == 'k')
            multiplier = 1024; 
        
        if(c == 'm')
            multiplier = 1024*1024; 
        
        if(c == 'g')
            multiplier = 1024*1024*1024; 
        
        if(c == 'p') {
            multiplier *= 8; // seen bps bytes per sec -> bits
            break;
        }
       
    }
    return safeatoi(numbit) * multiplier;
}
// and from a string
double to_bits(const std::string &in) {
    return to_bits(in.c_str());
}

double traffic_config::interface_speed(std::string dev, std::string direction) {
    struct stat st;
    std::string idx, file;
    file = MODSWROOT "/chosen_speeds";
    if(stat(file.c_str(), &st)) {
        // chosen_speeds not there so default to stadard ADSL for upload/download
        // and 100mbit ethernet if not
        if(direction == "upload")
            return to_bits("256kbit");
        else if(direction == "download")
            return to_bits("512kbit");
        else
            return to_bits("100mbit");
    }
    if(st.st_mtime >  chosen_speeds_last_mod) {
        chosen_speeds.readvar(file);
        chosen_speeds_last_mod = st.st_mtime;
    }
    if(direction != "")
        idx = dev + "_" + direction;
    else
        idx = dev;
    if(chosen_speeds[idx] != "") {
        return to_bits(chosen_speeds[idx]);
    }
    else {
        return 0.0;
    }
}
    
// need to look up the map of numbers to names last left when traffic
// implemented


int traffic_config::pos_to_rulenum(const int rule) {
   
    std::ostringstream out;
    out << rule;
    std::string rstr = out.str();
    return pos_to_rulenum(rstr);
}

int traffic_config::pos_to_rulenum(const std::string &rstr) {
    struct stat st;
    std::string file = MODSWROOT "/rulenumbers";
    if(stat(file.c_str(), &st)) {
        // if non zero there is no rulenumbers file so return 0
        return 0;
    }
    if(st.st_mtime >  rule_numbers_last_mod) {
        rule_numbers.readvar(file);
        rule_numbers_last_mod = st.st_mtime;
    }
    
    return safeatoi(rule_numbers[rstr]);
    
}

// change a rule (connection tracking) number into associated class

std::string traffic_config::rule_to_classid(const int rule) {
   
    std::ostringstream out;
    out << rule;
    std::string str = out.str();
    return rule_to_classid(str);
}

std::string traffic_config::rule_to_classid(const std::string &res) { 
    struct stat st;     
    
    std::string file = MODSWROOT "/rule2class";
    if(stat(file.c_str(), &st)) {
        // cant look up rules to classids without this file
        return res;
    }
    if(st.st_mtime >  rule_to_class_last_mod) {
        rule_to_class.readvar(file);
        rule_to_class_last_mod = st.st_mtime;
    }
   
    return rule_to_class[res];
    
}

std::string traffic_config::class_name(const std::string &res) {
    struct stat st;
    std::string file = MODSWROOT "/classnames";
    if(stat(file.c_str(), &st)) {
        // if non zero there is no classnames file so return raw classid
        return res;
    }
    if(st.st_mtime >  class_names_last_mod) {
        class_names.readvar(file);
        class_names_last_mod = st.st_mtime;
    }
    
    return class_names[res];
   
}

// we turn rule numbers into current names
std::string traffic_config::rule_name(const int rulenum) {
   
    std::ostringstream out;
    out << rulenum;
    std::string res = out.str();
    return rule_name(res);
}

std::string traffic_config::rule_name(const std::string & rulenum) {
    struct stat st;
    std::string file = MODSWROOT  "/rulenames";
    if(stat(file.c_str(), &st)) {
        // if non zero there is no rulenames file so return raw rule number
        return rulenum;
    }
    if(st.st_mtime >  rule_names_last_mod) {
        rule_names.readvar(file);
        rule_names_last_mod = st.st_mtime;
    }
    
    return rule_names[rulenum];
}

