/* SysShutdown Module for the SmoothWall SUIDaemon                        */
/* Contains functions relating to shutting down and rebooting             */
/* (c) 2004 SmoothWall Ltd                                                */
/* ---------------------------------------------------------------------- */
/* Original Author : D.K.Taylor                                           */

/* Based on "SmoothWall helper program - smoothiedeath/smoothierebirth    */
/* (c) Lawrence Manning, 2001                                             */

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

#include <glob.h>

extern "C" {
	int load(std::vector<CommandFunctionPair> & );

	int set_inbound(std::vector<std::string> & parameters, std::string & response);
	int set_outbound(std::vector<std::string> & parameters, std::string & response);
	int set_internal(std::vector<std::string> & parameters, std::string & response);
}

std::map<std::string, std::vector<std::string>, eqstr> portlist;

int load_portlist()
{
	/* open the portlist file for reading */

	glob_t globbuf;

	memset(&globbuf, 0, sizeof(glob_t));

	glob("/var/smoothwall/knownports/*", GLOB_DOOFFS, NULL, &globbuf);

	for (size_t i = 0; i < globbuf.gl_pathc; i++)
	{
		std::ifstream input(globbuf.gl_pathv[i]);
		char buffer[2048];

		/* determine the filename */
		char *section = globbuf.gl_pathv[i] + strlen("/var/smoothwall/knownports/");
		
		if (!input) continue;

		while (input)
		{
			if (!input.getline(buffer, sizeof(buffer)))
				break;
	
			if (strlen(buffer) > 0)
			{
				char *name = buffer;
				char *value = strstr(name, ",");	

				if (value && *value)
				{
					*value = '\0';
					value++; 
				} 
				else
					value = name;

				std::vector<std::string> & vect = portlist[section];
				vect.push_back(value);
			}
		}
		input.close();
	}

	return 0;
}

int load(std::vector<CommandFunctionPair> & pairs)
{
	/* CommandFunctionPair name("command", "function"); */
	CommandFunctionPair  set_inbound_function("setinbound", "set_inbound", 0, 0);
	CommandFunctionPair  set_outbound_function("setoutbound", "set_outbound", 0, 0);
	CommandFunctionPair  set_internal_function("setinternal", "set_internal", 0, 0);

	pairs.push_back( set_inbound_function);
	pairs.push_back( set_outbound_function);
	pairs.push_back( set_internal_function);

	return 0;
}

int set_inbound(std::vector<std::string> & parameters, std::string & response)
{
	int error = 0;

	std::string::size_type n;
	std::vector<std::string>ipb;
	response = "portforw rules loaded";
	ConfigSTR localip("/var/smoothwall/red/local-ipaddress");
	ConfigSTR iface("/var/smoothwall/red/iface");
	ConfigCSV fwdfile("/var/smoothwall/portfw/config");

	if ((error = (localip.str() == "")))
	{
		response = "Couldn't open local ip file";
		goto EXIT;
	}
	// carry on
	if ((n = localip.str().find_first_not_of(IP_NUMBERS)) != std::string::npos) 
	{
		// illegal characters
		response = "Bad local IP: " + localip.str();
		error = 1;
		goto EXIT;
	}
	if ((error = (iface.str() == "")))
	{
		response = "Couldn't open iface file";
		goto EXIT;
	}
	// carry on
	if ((n = iface.str().find_first_not_of(LETTERS_NUMBERS)) != std::string::npos) 
	{
		// illegal characters
		response = "Bad iface: " + iface.str();
		error = 1;
		goto EXIT;
	}
	if (fwdfile.first())
	{
		response = "Couldn't open portfw settings file";
		error = 1;
		goto EXIT;
	}
	ipb.push_back("iptables -F portfwf");
	ipb.push_back("iptables -t nat -F portfw");

	// iterate the CSV
	for (int line = fwdfile.first(); line == 0; line = fwdfile.next())
	{
		std::string remdouble;
		const std::string & protocol = fwdfile[0];
		const std::string & extip = fwdfile[1];
		const std::string & locport = fwdfile[2];
		const std::string & remip = fwdfile[3];

		// this last one want to change maybe
		std::string remport = fwdfile[4];
		const std::string & enabled = fwdfile[5];
		if ((n = protocol.find_first_not_of(LETTERS)) != std::string::npos)
		{
			response = "Bad protocol: " + protocol;
			error = 1;
			goto EXIT;
		}
		if ((n = extip.find_first_not_of(IP_NUMBERS)) != std::string::npos)
		{
			response = "Bad external IP: " + extip;
			error = 1;
			goto EXIT;
		}
		if ((n = locport.find_first_not_of(NUMBERS_COLON)) != std::string::npos)
		{
			response = "Bad local port: " + locport;
			error = 1;
			goto EXIT;
		}
		if ((n = remip.find_first_not_of(IP_NUMBERS)) != std::string::npos)
		{
			response = "Bad remote IP: " + remip;
			error = 1;
			goto EXIT;
		}
		if ((n = remport.find_first_not_of(NUMBERS)) != std::string::npos)
		{
			response = "Bad remote port: " + remport;
			error = 1;
			goto EXIT;
		}

		if (enabled == "on")
		{
			if (remport == "0")
				remport = locport;
			// if locport does not have : or originally remport not zero 
			if(locport.find_first_of(":") == std::string::npos || fwdfile[4] != "0")
				remdouble = remip + ":" + remport;
			else 
				remdouble = remip;

			ipb.push_back("iptables -A portfwf -m state --state NEW -i " + 
				iface.str() + " -p " + protocol +  			
				" -s " + extip +  			
				" -d " + remip +  			
				" --dport " + remport + " -j ACCEPT");
			ipb.push_back("iptables -t nat -A portfw -p " + protocol +
				" -s " + extip +  
				" -d " + localip.str() +  			
				" --dport " + locport + " -j DNAT --to " + remdouble);
		}
	}

	error = ipbatch(ipb);
	if (error)
		response = "ipbatch failure";
	else
		response = "Portfw rules set";

EXIT:
	return (error);
}

int set_outbound(std::vector<std::string> & parameters, std::string & response)
{
	int error = 0;
	ConfigCSV config("/var/smoothwall/outbound/settings");
	std::vector<std::string>ipb;
	std::string::size_type n;
	
	load_portlist();

	if (config.first())
	{
		response = "Couldn't open outbound config file";
		error = 1;
		goto EXIT;
	}

	ipb.push_back("iptables -F outgreen\n");
	ipb.push_back("iptables -F outorange");
	ipb.push_back("iptables -F outpurple");

	for (int line = config.first(); line == 0; line = config.next())
	{
		std::string colour = config[0];
		const std::string & enabled = config[1];
		const std::string & port = config[2];

		for (int j = 0; j < (int)colour.length(); ++j)
			colour[j] = tolower(colour[j]);

		// are we complete?
		if (colour == "" || port == "" || enabled == "")
			continue;

		if ((n = colour.find_first_not_of(LETTERS)) != std::string::npos)
		{
			response = "Bad colour: " + colour;
			error = 1;
			goto EXIT;
		}
		
		if (enabled == "on")
		{
			if ((n = port.find_first_not_of(NUMBERS)) != std::string::npos)
			{
				if (portlist[port.c_str()].size() > 0)
				{
					/* it's a mapped port! */
					std::vector<std::string> & vect = portlist[port.c_str()];
					for (std::vector<std::string>::iterator i = vect.begin();
						i != vect.end(); i++)
					{
						std::string nport = *i;
						ipb.push_back("iptables -A out" + colour + " -p tcp --dport " + nport + " -j ACCEPT");
						ipb.push_back("iptables -A out" + colour + " -p udp --dport " + nport + " -j ACCEPT");
					}
				}
				else
				{
					response = "Bad port: " + port;
					error = 1;
					goto EXIT;
				}
			} 
			else
			{
				ipb.push_back("iptables -A out" + colour + " -p tcp --dport " + port + " -j ACCEPT");
				ipb.push_back("iptables -A out" + colour + " -p udp --dport " + port + " -j ACCEPT");
			}
		}
	}

	error = ipbatch(ipb);
	if (error)
		response = "ipbatch failure";
	else
		response = "Outbound ports set";

EXIT:
	return error;
}


int set_internal(std::vector<std::string> & parameters, std::string & response)
{
	int error = 0;

	ConfigCSV config("/var/smoothwall/dmzholes/config");
	std::vector<std::string>ipb;
	std::string::size_type n;

	if (config.first())
	{
		response = "Couldn't open dmzholes config file";
		error = 1;
		goto EXIT;
	}
	
	ipb.push_back("iptables  -F dmzholes");

	for (int line = config.first(); line == 0; line = config.next())
	{
		const std::string & protocol = config[0];
		const std::string & locip = config[1];
		const std::string & remip = config[2];
		const std::string & remport = config[3];
		const std::string & enabled = config[4];

		// are we complete?
		if (protocol == "" || locip == "" || remip == "" || remport == "" || enabled == "")
			continue;

		if ((n = protocol.find_first_not_of(LETTERS)) != std::string::npos)
		{
			response = "Bad protocol: " + protocol;
			error = 1;
			goto EXIT;
		}
		if ((n = locip.find_first_not_of(IP_NUMBERS)) != std::string::npos)
		{
			response = "Bad local IP: " + locip;
			error = 1;
			goto EXIT;
		}
		if ((n = remip.find_first_not_of(IP_NUMBERS)) != std::string::npos)
		{
			response = "Bad remote IP: " + remip;
			error = 1;
			goto EXIT;
		}
		
		if (enabled == "on")
		{
			if ((n = remport.find_first_not_of(NUMBERS)) != std::string::npos)
			{
				if (portlist[remport.c_str()].size() > 0)
				{
					/* it's a mapped port! */
					std::vector<std::string> & vect = portlist[remport.c_str()];
					for (std::vector<std::string>::iterator i = vect.begin();
						i != vect.end(); i++)
					{
						std::string nport = *i;
						ipb.push_back("iptables -A dmzholes -m state --state NEW -p " + protocol + " -s " + locip + " -d " + remip + " --dport  " + nport + " -j ACCEPT");
					}
				}
				else
				{
					response = "Bad remote port: " + remport;
					error = 1;
					goto EXIT;
				}
			}
			else
				ipb.push_back("iptables -A dmzholes -m state --state NEW -p " + protocol + " -s " + locip + " -d " + remip + " --dport  " + remport + " -j ACCEPT");
		}
	}

	error = ipbatch(ipb);

	if (error)
		response = "ipbatch failure";
	else
		response = "DMZ Holes set";

EXIT:
	return (error);
}

