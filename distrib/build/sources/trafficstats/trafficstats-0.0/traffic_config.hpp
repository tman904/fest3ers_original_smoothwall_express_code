#ifndef TRAFFIC_CONFIG_INC
#define TRAFFIC_CONFIG_INC

#include "configvar.hpp"
#include <time.h>


class traffic_config {
private:
 
    // our various config files
    configvar rule_names;
    configvar rule_numbers;
    configvar class_names; 
    configvar rule_to_class;
    configvar chosen_speeds;
    time_t rule_names_last_mod;
    time_t rule_numbers_last_mod;
    time_t class_names_last_mod;
    time_t rule_to_class_last_mod;
    time_t chosen_speeds_last_mod;
    
public:

    traffic_config() {
        rule_names_last_mod = 0; 
        rule_numbers_last_mod = 0;
        class_names_last_mod = 0;
        rule_to_class_last_mod = 0;
        chosen_speeds_last_mod = 0;
    };
    double interface_speed(std::string dev, std::string direction = "");
    int pos_to_rulenum(const int rule);
    int pos_to_rulenum(const std::string &rstr);
    std::string rule_to_classid(const int rule);
    std::string rule_to_classid(const std::string &rstr);
    std::string class_name(const std::string &res);
    std::string rule_name(const int rulenum);
    std::string rule_name(const std::string & rulenum);
};


// defined in the main prog
extern traffic_config traf_config;

#endif
