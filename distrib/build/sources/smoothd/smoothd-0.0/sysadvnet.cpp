/* SysAdvNet Module for the SmoothWall SUIDaemon                           */
/* Contains functions relating to setting advanced networking                  */
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
	int set_advnet(std::vector<std::string> & parameters, std::string & response);
}

int load(std::vector<CommandFunctionPair> & pairs)
{
	/* CommandFunctionPair name("command", "function"); */
	CommandFunctionPair set_advnet_function("setadvnet", "set_advnet", 0, 0);

	pairs.push_back(set_advnet_function);

	return 0;
}

int set_advnet(std::vector<std::string> & parameters, std::string & response)
{
	struct stat sb;
	int error = 0;
	int fd = -1;
	char noping[] = "0\n";
	char cookies[] = "0\n";
	std::vector<std::string>ipb;

	if (stat("/var/smoothwall/advnet/noping", &sb) == 0)
		noping[0] = '1';
	if (stat("/var/smoothwall/advnet/cookies", &sb) == 0)
		cookies[0] = '1';

	if ((fd = open("/proc/sys/net/ipv4/icmp_echo_ignore_all", O_WRONLY)) != -1)
	{
		write(fd, noping, 2);
		close(fd);
	}

	if ((fd = open("/proc/sys/net/ipv4/tcp_syncookies", O_WRONLY)) != -1)
	{
		write(fd, cookies, 2);
		close(fd);
	}
	
	ipb.push_back("iptables -F advnet"); // at least flush out any existing rules
	if (stat("/var/smoothwall/advnet/noigmp", &sb) == 0)
		ipb.push_back("iptables -A advnet -p igmp -j DROP");
	
	if (stat("/var/smoothwall/advnet/nomulticast", &sb) == 0)
		ipb.push_back("iptables -A advnet -d 224.0.0.0/4 -j DROP");

	error = ipbatch(ipb);

	if (error)
		response = "ipbatch failure";
	else
		response = "advnetset OK";

	return error;
}
