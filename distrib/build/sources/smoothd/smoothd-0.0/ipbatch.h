/* SmoothWall helper program - header file
 *
 * Written by Martin Houston <martin.houston@smoothwall.net>
 * This program is distributed under the terms of the GNU General Public
 * Licence.  See the file COPYING for details.
 *
 * filename: ipbatch.h
 * Direct interface into iptables. 
 * If you need to do iptables commands in youtr plugin include this
 * header file and you have a choice of two APIs.
 * The preferred method is with a vector but there is also
 * a function callable from C code that takes just a char *
 * What is provided is a valid iptables command line
 * e.g. "iptables -nvL"
 * All iptables commands must be valid and must succeed - i.e. you must not 
 * attempt to remove a table that is not there. As commands are 
 * being submitted as a batch any failure will leave iptables
 * in an undefined state.
 */
#ifndef __IPBATCH_H
#define __IPBATCH_H
#include <stdio.h>
#include <stdarg.h>
#include <stdlib.h>
// C++ side
#include <string>
#include <iostream>
#define BATCHSTORE_SIZE 10240
// this only actualy does something if one of the args is "commit"
// in which case a non zero return code indicates some failure.
int ipbatch(std::vector<std::string> &arg);

int ipbatch(const std::string & arg);

extern "C" {
	int ipbatch(const char *arg);
}

// has to be in C for iptables linkage
// could be used directly from other places
// if they have a buffer ready in place.
extern "C" {
	int dobatch(char *store);
}

// this is here because its handy to use with ipbatch.
// Beware!
// this may call each argument twice, if the amount of data resulting each
// time differes then have a potential buffer overflow problem!
// must not used with functions that can return a different value each time they// are called - such a value should be saved into a variable first.

inline std::string Sprintf(const char *fmt, ...) 
{
	va_list argp;
	char fixed_fmtbuf[256]; // should be enough for most cases - if not malloc
	char *fmtbuf = fixed_fmtbuf;
	unsigned int n;
	std::string retstr = "";
	va_start(argp, fmt);
	if((n = vsnprintf(fmtbuf,sizeof(fixed_fmtbuf)-1, fmt, argp)) >= (sizeof(fixed_fmtbuf)-1)) 
	{
		if((fmtbuf = (char *)malloc(n+1))) 
			vsnprintf(fmtbuf, n+1, fmt, argp); // bound to work this time	  
	}
	if(fmtbuf) 
	{
		retstr = fmtbuf; // malloc did not fail etc.
		if(fmtbuf != fixed_fmtbuf)
			free(fmtbuf); // as it was malloced
	}
	return retstr;
}
#endif
