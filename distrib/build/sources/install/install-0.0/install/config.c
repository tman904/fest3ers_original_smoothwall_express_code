/* SmoothWall install program.
 *
 * This program is distributed under the terms of the GNU General Public
 * Licence.  See the file COPYING for details.
 *
 * (c) Lawrence Manning, 2001
 * 
 * filename: config.c
 * Write the config and get password stuff. */

#include "install.h"

extern FILE *flog;
extern char *logname;

extern char **ctr;

/* called to write out all config files using the keyvalue interface. */
int writeconfigs(struct blockdevice *hd, struct keyvalue *ethernetkv, char *lang)
{
	char devnode[STRING_SIZE];
	struct keyvalue *kv = initkeyvalues();
	
	/* Write out the network settings we got from a few mins ago. */
	writekeyvalues(ethernetkv, "/harddisk" CONFIG_ROOT "ethernet/settings");
	
	/* default stuff for main/settings. */
	replacekeyvalue(kv, "LANGUAGE", lang);
	replacekeyvalue(kv, "HOSTNAME", "smoothwall");
	writekeyvalues(kv, "/harddisk" CONFIG_ROOT "main/settings");
	freekeyvalues(kv);
	
	/* dev node links. */
	snprintf(devnode, STRING_SIZE, "%s", hd->devnode);
	if (symlink(devnode, "/harddisk/dev/harddisk"))
	{
		errorbox(ctr[TR_UNABLE_TO_MAKE_SYMLINK_DEV_HARDDISK]);
		return 0;
	}
	snprintf(devnode, STRING_SIZE, "%s1", hd->devnode);
	if (symlink(devnode, "/harddisk/dev/harddisk1"))
	{
		errorbox(ctr[TR_UNABLE_TO_MAKE_SYMLINK_DEV_HARDDISK1]);
		return 0;
	}
	snprintf(devnode, STRING_SIZE, "%s2", hd->devnode);
	if (symlink(devnode, "/harddisk/dev/harddisk2"))
	{
		errorbox(ctr[TR_UNABLE_TO_MAKE_SYMLINK_DEV_HARDDISK2]);
		return 0;
	}
	snprintf(devnode, STRING_SIZE, "%s3", hd->devnode);
	if (symlink(devnode, "/harddisk/dev/harddisk3"))
	{
		errorbox(ctr[TR_UNABLE_TO_MAKE_SYMLINK_DEV_HARDDISK3]);
		return 0;
	}
	snprintf(devnode, STRING_SIZE, "%s4", hd->devnode);
	if (symlink(devnode, "/harddisk/dev/harddisk4"))
	{
		errorbox(ctr[TR_UNABLE_TO_MAKE_SYMLINK_DEV_HARDDISK4]);
		return 0;
	}
		
	return 1;
}

/* Taken from the cdrom one. */
int getpassword(char *password, char *text)
{
	char *values[] = {	NULL, NULL, NULL };	/* pointers for the values. */
	struct newtWinEntry entries[] =
	{ 
		{ ctr[TR_PASSWORD_PROMPT], &values[0], 2 },
		{ ctr[TR_AGAIN_PROMPT], &values[1], 2 },
		{ NULL, NULL, 0 }
	};
	int rc;
	int done;
	
	do
	{
		done = 1;
		rc = newtWinEntries(TITLE, text,
			50, 5, 5, 20, entries, ctr[TR_OK], ctr[TR_CANCEL], NULL);
		
		if (rc != 2)
		{
			if (strlen(values[0]) == 0 || strlen(values[1]) == 0)
			{
				errorbox(ctr[TR_PASSWORD_CANNOT_BE_BLANK]);
				done = 0;
				strcpy(values[0], "");
				strcpy(values[1], "");				
			}
			else if (strcmp(values[0], values[1]) != 0)
			{
				errorbox(ctr[TR_PASSWORDS_DO_NOT_MATCH]);
				done = 0;
				strcpy(values[0], "");
				strcpy(values[1], "");					
			}
		}
	}
	while (!done);

	strncpy(password, values[0], STRING_SIZE);

	if (values[0]) free(values[0]);
	if (values[1]) free(values[1]);

	return rc;
}
	
