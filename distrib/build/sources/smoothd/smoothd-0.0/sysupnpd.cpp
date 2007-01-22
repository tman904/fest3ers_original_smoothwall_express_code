/* SysUpnpd Module for the SmoothWall SUIDaemon                           */
/* Contains functions relating to starting/restarting upnpd                  */
/* (c) 2007 SmoothWall Ltd                                                */
/* ----------------------------------------------------------------------  */
/* Original Author  : Lawrence Manning                                     */
/* Translated to C++: M. W. Houston                                        */

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
#include "ipbatch.h"
#include "setuid.h"

extern "C" {
	int load(std::vector<CommandFunctionPair> &  );
	int restart_upnpd(std::vector<std::string> & parameters, std::string & response );
	int start_upnpd(std::vector<std::string> & parameters, std::string & response );
	int stop_upnpd(std::vector<std::string> & parameters, std::string & response );
}

int load(std::vector<CommandFunctionPair> & pairs )
{
	/* CommandFunctionPair name("command", "function" ); */
	CommandFunctionPair restart_upnpd_function("upnpdrestart", "restart_upnpd", 0, 0);
	CommandFunctionPair start_upnpd_function("upnpdstart", "start_upnpd", 0, 0);
	CommandFunctionPair stop_upnpd_function("upnpdstop", "stop_upnpd", 0, 0);

	pairs.push_back(restart_upnpd_function);
	pairs.push_back(start_upnpd_function);
	pairs.push_back(stop_upnpd_function);

	return 0;
}

int restart_upnpd(std::vector<std::string> & parameters, std::string & response)
{
	int error = 0;
	
	error += stop_upnpd(parameters, response);
	
	if (!error)
		error += start_upnpd(parameters, response);
	
	if (!error)
		response = "Upnpd Restart Successful";
	
	return error;
}

int stop_upnpd(std::vector<std::string> & parameters, std::string & response)
{
	int error = 0;
	
	killunknownprocess("upnpd");
	simplesecuresysteml("/sbin/route", "del", "-net", "239.0.0.0", "netmask", "255.0.0.0", NULL);

	response = "Upnpd Process Terminated";

	return error;
}

int start_upnpd(std::vector<std::string> & parameters, std::string & response)
{
	int error = 0;
	ConfigSTR iface("/var/smoothwall/red/iface");
	struct stat sb;
	std::string::size_type n;
	int enabled = (stat("/var/smoothwall/advnet/upnp", &sb) == 0);

	if (iface.str() == "")
	{
		response = "Couldn't open iface file";
		goto EXIT;
	}
	if ((n = iface.str().find_first_not_of(LETTERS_NUMBERS)) != std::string::npos) 
	{
		response = "Bad iface: " + iface.str();
		error = 1;
		goto EXIT;
	}
	
	if (enabled)
	{
		error = simplesecuresysteml("/sbin/route", "add", "-net", "239.0.0.0",  "netmask", "255.0.0.0", "eth0", NULL);
		if (!error)
		{
			error = simplesecuresysteml("/usr/sbin/upnpd " , iface.str().c_str() , "eth0", NULL);
			if (error)
				response = "Can't start Upnpd";
			else
				response = "Upnpd Start Successful";
		}
		else
			response = "Can't add route";
	}
	
EXIT:
	return error;
}
