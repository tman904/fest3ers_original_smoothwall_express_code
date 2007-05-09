/* SysUpDown Module for the SmoothWall SUIDaemon                           */
/* For bringing external interface up or taking it down                    */
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
	int load(std::vector<CommandFunctionPair> & );
	int timed_access(std::vector<std::string> & parameters, std::string & response);
	int set_timed_access(std::vector<std::string> & parameters, std::string & response);
	
	bool indaterange(ConfigVAR &settings);
	int setallowed(std::string mode, bool allowed, bool override);
}

int load(std::vector<CommandFunctionPair> & pairs)
{
	/* CommandFunctionPair name("command", "function"); */
	CommandFunctionPair timed_access_function(1, "timed_access", 0, 0);
	CommandFunctionPair set_timed_access_function("settimedaccess", "set_timed_access", 0, 0);
	
	pairs.push_back(timed_access_function);
	pairs.push_back(set_timed_access_function);
	
	return (0);
}

int timed_access(std::vector<std::string> & parameters, std::string & response)
{
	int error = 0;
	static bool firsttime = true;
	
	ConfigVAR settings("/var/smoothwall/timedaccess/settings");
	
	std::string mode = settings["MODE"];

	if (settings["ENABLE"] != "on")
	{
		setallowed("ALLOW", true, false);
		return error;
	}

	/* Assume outside date range. */
	if (firsttime)
	{
		setallowed(mode, false, true);
		firsttime = false;
	}
	
	if (indaterange(settings))
		setallowed(mode, true, false);
	else
		setallowed(mode, false, false);
	
	return error;
}

int set_timed_access(std::vector<std::string> & parameters, std::string & response)
{
	int error = 0;
	ConfigCSV config("/var/smoothwall/timedaccess/machines");
	std::vector<std::string>ipb;
	std::string::size_type n;
	
	ipb.push_back("iptables -F timedaccess\n");

	for (int line = config.first(); line == 0; line = config.next())
	{
		const std::string &ip = config[0];
		
		if ((n = ip.find_first_not_of(IP_NUMBERS)) != std::string::npos) 
		{
			// illegal characters
			response = "Bad IP: " + ip;
			error = 1;
			goto EXIT;
		}
		
		ipb.push_back("iptables -A timedaccess -s " + ip + " -j timedaction");
	}
	
	error = ipbatch(ipb);
	if (error)
		response = "ipbatch failure";
	else
		response = "timed access set";

EXIT:		
	return error;
}

bool indaterange(ConfigVAR &settings)
{
	unsigned int starthour = atol(settings["START_HOUR"].c_str());
	unsigned int endhour = atol(settings["END_HOUR"].c_str());
	unsigned int startmin = atol(settings["START_MIN"].c_str());
	unsigned int endmin = atol(settings["END_MIN"].c_str());

	time_t tnow;  // to hold the result from time()
	struct tm *tmnow;  // to hold the result from localtime()
	unsigned int hour, min, wday;

	time(&tnow);  // get the time after the lock so all entries in order
	tmnow = localtime(&tnow);  // convert to local time (BST, etc)

	hour = tmnow->tm_hour;
	min = tmnow->tm_min;
	wday = tmnow->tm_wday;

	/* Wrap week to start on Monday. */
	if (wday == 0) wday = 7;
	wday--;
	
	bool matchday = false;

	std::string key = "DAY_" + stringprintf("%d", wday);

	if (settings[key.c_str()] == "on") matchday = true;

	if (!matchday) return false;
	if (hour < starthour) return false;
	if (hour > endhour) return false;
	if (hour == starthour)
	{
		if (min < startmin) return false;
	}
	if (hour == endhour)
	{
		if (min > endmin) return false;
	}

	return true;
}

int setallowed(std::string mode, bool allowed, bool override)
{
	static bool lastallowed = true;

	if (mode == "REJECT") allowed = !allowed;

	if (!override && lastallowed == allowed) return 0;
	
	std::vector<std::string> ipb;

	if (allowed)
	{
		syslog(LOG_INFO, "Timed access: Ok, allowing");
		ipb.push_back("iptables -R timedaction 1 -j RETURN");
	}
	else
	{
		syslog(LOG_INFO, "Timed access: Not allowing");
		ipb.push_back("iptables -R timedaction 1 -j REJECT");
	}
		
	lastallowed = allowed;
	
	return ipbatch(ipb);
}
