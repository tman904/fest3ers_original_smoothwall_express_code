/* SysProxy Module for the SmoothWall SUIDaemon                           */
/* Contains functions relating to the management of the SQUID Proxy       */
/* (c) 2005 SmoothWall Ltd                                                */
/* ---------------------------------------------------------------------- */
/* Original Author : D.K.Taylor                                           */

/* include the usual headers.  iostream gives access to stderr (cerr)     */
/* module.h includes vectors and strings which are important              */
#include <iostream>
#include <fstream>
#include <fcntl.h>
#include <syslog.h>
#include <signal.h>
#include "module.h"

extern "C" {
	int load( std::vector<CommandFunctionPair> &  );

	int restart_im( std::vector<std::string> & parameters, std::string & response );
	int   start_im( std::vector<std::string> & parameters, std::string & response );
	int    stop_im( std::vector<std::string> & parameters, std::string & response );
}

int load( std::vector<CommandFunctionPair> & pairs )
{
	/* CommandFunctionPair name( "command", "function" ); */
	CommandFunctionPair restart_im_function( "imrestart", "restart_im", 0, 0 );
	CommandFunctionPair   start_im_function( "imstart",     "start_im", 0, 0 );
	CommandFunctionPair    stop_im_function( "imstop",       "stop_im", 0, 0 );

	pairs.push_back( restart_im_function );
	pairs.push_back(   start_im_function );
	pairs.push_back(    stop_im_function );

	return ( 0 );
}

int restart_im( std::vector<std::string> & parameters, std::string & response )
{
	int error = 0;

	error += stop_im( parameters, response );

	if ( !error )
		error += start_im( parameters, response );

	if ( !error )
		response = "IMSpector Restart Successful";

	return error;
}


int stop_im( std::vector<std::string> & parameters, std::string & response )
{
	response = "IMSpector Process Terminated";

	signalprocess("/var/run/imspector.pid", 15);

	FILE *output = popen("/usr/sbin/ipbatch", "w");
	fprintf(output, "/sbin/iptables -t nat -F im\n");
	fflush(output);
	fprintf(output, "commit\n");
	fflush(output);
	fprintf(output, "end\n");
	fflush(output);
	pclose(output);

	return 0;
}

int start_im( std::vector<std::string> & parameters, std::string & response )
{
	response = "IMSpector Process started";

	ConfigVAR settings("/var/smoothwall/im/settings");

	FILE *output = popen("/usr/sbin/ipbatch", "w");

	fprintf(output, "/sbin/iptables -t nat -F im\n");
	fflush(output);

	syslog(LOG_ERR, "starting accordingly");
	if (settings["ENABLE"] == "on")
	{
		if (settings["MSN"] == "on")
		{
			fprintf(output, "/sbin/iptables -t nat -A im -p tcp --dport 1863 -j REDIRECT --to-ports 16667\n");
			fflush(output);
		}
		if (settings["ICQ"] == "on")
		{
			fprintf(output, "/sbin/iptables -t nat -A im -p tcp --dport 5190 -j REDIRECT --to-ports 16667\n");
			fflush(output);
		}
		if (settings["YAHOO"] == "on")
		{
			fprintf(output, "/sbin/iptables -t nat -A im -p tcp --dport 5050 -j REDIRECT --to-ports 16667\n");
			fflush(output);
		}
		if (settings["IRC"] == "on")
		{
			fprintf(output, "/sbin/iptables -t nat -A im -p tcp --dport 6667 -j REDIRECT --to-ports 16667\n");
			fflush(output);
		}
	}

	fprintf(output, "commit\n");
	fflush(output);
	fprintf(output, "end\n");
	fflush(output);
	pclose(output);

	syslog(LOG_ERR, "starting accordingly");
	if (settings["ENABLE"] == "on")
	{
		syslog(LOG_ERR, "im enabled, starting accordingly");
		simplesecuresysteml("/usr/sbin/imspector", "-c", "/var/smoothwall/im/imspector.conf", NULL);
	}

	return 0;
}
