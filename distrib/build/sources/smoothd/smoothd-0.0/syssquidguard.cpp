/* Syssquidguard Module for the SmoothWall SUIDaemon                           */
/* (c) 2007 SmoothWall Ltd                                                */
/* ----------------------------------------------------------------------  */
/* Original Author  : Lawrence Manning                                     */
/* Portions (c) Stanford Prescott                                        */

/* include the usual headers.  iostream gives access to stderr (cerr)     */
/* module.h includes vectors and strings which are important              */
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>

#include <iostream>
#include <fstream>
#include <fcntl.h>
#include <syslog.h>
#include <signal.h>

#include "module.h"
#include "setuid.h"

extern "C" {
	int load( std::vector<CommandFunctionPair> &  );
	int sg_prebuild(std::vector<std::string> & parameters, std::string & response);
       int errrpt(const std::string & parameter);
	int sg_autoupdate(std::vector<std::string> & parameters, std::string & response);
}

int load( std::vector<CommandFunctionPair> & pairs )
{
	/* CommandFunctionPair name( "command", "function" ); */
	CommandFunctionPair sg_prebuild_function("sgprebuild", "sg_prebuild", 0, 0);
	CommandFunctionPair sg_autoupdate_function("sgautoupdate", "sg_autoupdate", 0, 0);

	pairs.push_back(sg_prebuild_function);
	pairs.push_back(sg_autoupdate_function);

	return 0;
}

int sg_prebuild(std::vector<std::string> & parameters, std::string & response)
{
   int error = 0;
   response = "squidGuard: updating blacklists.";
   error = simplesecuresysteml("/var/smoothwall/urlfilter/bin/prebuild.pl", NULL);

   if (!error)
     response = "squidGuard: blacklists updated.";
   else
     response = "squidGuard: unable to update blacklists!";
	
  return errrpt (response);
}

int sg_autoupdate(std::vector<std::string> & parameters, std::string & response)
{
   int error = 0;

   ConfigVAR settings("/var/smoothwall/urlfilter/autoupdate/autoupdate.conf");

   std::string updsrc  = settings["UPDATE_SOURCE"];
   std::string custsrc = settings["CUSTOM_UPDATE_URL"];
   std::string updpath = "/var/smoothwall/urlfilter/bin/sgbl-autoupdate";
   std::string filestr = "#!/bin/sh\n\n/var/smoothwall/urlfilter/bin/autoupdate.pl ";
   std::string updfilestr  = filestr + updsrc;
   std::string custfilestr = filestr + custsrc;
   std::string url = "";

   FILE *exists;
   FILE *updfile;

   if ( exists = fopen("/etc/cron.daily/sgbl-autoupdate", "r") )
   {
     error = simplesecuresysteml("/bin/rm", "-f", "/etc/cron.daily/sgbl-autoupdate", NULL);
     fclose(exists);
   }

   if ( exists = fopen("/etc/cron.weekly/sgbl-autoupdate", "r") )
   {
     error = simplesecuresysteml("/bin/rm", "-f", "/etc/cron.weekly/sgbl-autoupdate", NULL);
     fclose(exists);
   }

   if ( exists = fopen("/etc/cron.monthly/sgbl-autoupdate", "r") )
   {
     error = simplesecuresysteml("/bin/rm", "-f", "/etc/cron.monthly/sgbl-autoupdate", NULL);
     fclose(exists);
   }

   if ( settings["ENABLE_AUTOUPDATE"] == "on" )
   {
     if (updsrc == "custom") 
       url = custfilestr;
     else
       url = updfilestr;

     if (updfile = fopen( "/var/smoothwall/urlfilter/bin/sgbl-autoupdate", "w" ))
     {
        fputs( (char*) url.c_str(), updfile );
        fclose(updfile);
     }

     if ((settings["UPDATE_SCHEDULE"] == "daily") ||
        (settings["UPDATE_SCHEDULE"] == "weekly") ||
        (settings["UPDATE_SCHEDULE"] == "monthly"))
     {
       error = simplesecuresysteml("/bin/cp", "-f", updpath.c_str(), "/etc/cron."+settings["UPDATE_SCHEDULE"], NULL);
     }
   }

   if (!error)
     response = "squidGuard: Success setting up autoupdate.";
   else
     response = "squidGuard: Unable to setup autoupdate.";
	
  return errrpt (response);
}

int errrpt(const std::string & logdata)
{
 int err = 0;

 syslog(LOG_INFO, "squidGuard:  %s", logdata.c_str());

 return err;
}
