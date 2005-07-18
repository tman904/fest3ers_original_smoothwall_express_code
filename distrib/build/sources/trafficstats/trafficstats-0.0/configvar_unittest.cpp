#include "configvar.hpp"

// use really simple facilities
#include <stdio.h>
#include <string.h>

void dotest(int iteration) {
    // write out a config
    char conffile_name[80];
    FILE *fd;
    sprintf(conffile_name,"/tmp/configvar_unittest_%d", getpid());
    if((fd = fopen(conffile_name, "w")) != NULL) {
        fprintf(fd,"ITEM1=1\nitem2=\"a string\"\nIteM3=string_no_spaces\n");
        fclose(fd);
        
        configvar thisvar(conffile_name);
        unlink(conffile_name);
        std::vector<std::string> keys = thisvar.keys();

        if(keys.size() != 3) {
            printf("%d Wrong number of keys %d\n", iteration, keys.size());
         
            exit(1);
        }
        if(safeatoi(thisvar["ITEM1"]) != 1) {
            printf("%d ITEM1 bad\n", iteration);
         
            exit(1);
        }
        if(thisvar["item2"] != "a string") {
            printf("%d ITEM2 bad\n", iteration);
         
            exit(1);
        }
        if(thisvar["IteM3"] != "string_no_spaces") {
            printf("%d ITEM3 bad\n", iteration);
         
            exit(1);
        }
    }
    else {
        printf("%d cant open %s\n", iteration, conffile_name);
         
            exit(1);
    }
}

int main() {
    int i;
    for(i = 0; i < 100000; i++)
        dotest(i);
}
