/* SmoothWall install program.
 *
 * This program is distributed under the terms of the GNU General Public
 * Licence.  See the file COPYING for details.
 *
 * (c) Lawrence Manning, 2001
 *
 * filename: install.h
 * Main include file. */

#include <libsmooth.h>

#define IDE_EMPTY 0
#define IDE_CDROM 1
#define IDE_HD 2
#define IDE_UNKNOWN 3

/* CDROMS and harddisks. */
struct devparams
{
	char devnode[STRING_SIZE];
	int module;
	char modulename[STRING_SIZE];
	char options[STRING_SIZE];
};

/* ide.c */
int checkide(char letter);
char findidetype(int type);

/* cdrom.c */
int ejectcdrom(char *dev);

/* nic.c */
int networkmenu(struct keyvalue *ethernetkv);

/* net.c */
int downloadtarball(void);

/* config.c */
int writeconfigs(struct devparams *dp, struct keyvalue *ethernetkv, char *lang);
