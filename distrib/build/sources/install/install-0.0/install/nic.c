/* SmoothWall install program.
 *
 * This program is distributed under the terms of the GNU General Public
 * Licence.  See the file COPYING for details.
 *
 * (c) Lawrence Manning, 2001
 * 
 * filename: nic.c
 * Contains stuff related to firing up the network card, including a crude
 * autodector. */

#include "install.h"

#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

extern FILE *flog;
extern char *log;

extern char **ctr;

extern struct nic nics[];

int networkmenu(struct keyvalue *ethernetkv)
{
	int rc;
	char driver[STRING_SIZE] = "";
	char driveroptions[STRING_SIZE] = "";
	struct keyvalue *kv = initkeyvalues();
	int result = 0;
	char commandstring[STRING_SIZE];
	char address[STRING_SIZE], netmask[STRING_SIZE];
	int done;
	char description[1000];
	char message[1000];

	done = 0;
	while (!done)
	{
		rc = newtWinTernary(ctr[TR_CONFIGURE_NETWORKING], ctr[TR_PROBE], 
			ctr[TR_SELECT], ctr[TR_CANCEL], ctr[TR_CONFIGURE_NETWORKING_LONG]);
		
		if (rc == 0 || rc == 1)
		{
			probecards(driver, driveroptions);
			if (!strlen(driver))
				errorbox(ctr[TR_PROBE_FAILED]);
			else
			{
                char cardInfo[STRING_SIZE], mac[STRING_SIZE];
				findnicdescription(driver, description);
                // GREEN is hard coded at "eth0"
                if ( (GetNicMAC(mac, sizeof(mac), "eth0")) )
                  // If MAC found put it at the end of nic description.
                  snprintf(cardInfo, sizeof(cardInfo), "%s [%s]",
                           description, mac);
                else
                  // MAC lookup failed so just display nic description.
                  snprintf(cardInfo, sizeof(cardInfo), "%s", description);
                // Ensure that the cardinfo array is null terminated
                cardInfo[sizeof(cardInfo)-1] = '\0';
				sprintf(message, ctr[TR_FOUND_NIC], cardInfo);
				newtWinMessage(TITLE, ctr[TR_OK], message);
			}		
		}			
		else if (rc == 2)
			choosecards(driver, driveroptions);
		else
			done = 1;	
			
		if (strlen(driver))
			done = 1;
	}
	
	if (!strlen(driver))
		goto EXIT;

	/* Default is a GREEN nic only. */
	/* Smoothie is not untarred yet, so we have to delay actually writing the
	 * settings till later. */
	replacekeyvalue(ethernetkv, "CONFIG_TYPE", "0");
	replacekeyvalue(ethernetkv, "GREEN_DRIVER", driver);
	replacekeyvalue(ethernetkv, "GREEN_DRIVER_OPTIONS", driveroptions);
	replacekeyvalue(ethernetkv, "GREEN_DEV", "eth0");
	replacekeyvalue(ethernetkv, "GREEN_DISPLAYDRIVER", driver);
	
	if (!(changeaddress(ethernetkv, "GREEN", 0, "")))
		goto EXIT;
	
	strcpy(address, ""); findkey(ethernetkv, "GREEN_ADDRESS", address);
	strcpy(netmask, ""); findkey(ethernetkv, "GREEN_NETMASK", netmask);

	snprintf(commandstring, STRING_SIZE, "/bin/ifconfig eth0 %s netmask %s up", 
		address, netmask);
	if (mysystem(commandstring))
	{
		errorbox(ctr[TR_INTERFACE_FAILED_TO_COME_UP]);
		goto EXIT;
	}

	result = 1;
	
EXIT:
	freekeyvalues(kv);
	
	return result;
}
			
