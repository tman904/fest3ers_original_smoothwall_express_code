/* SmoothWall install program.
 *
 * This program is distributed under the terms of the GNU General Public
 * Licence.  See the file COPYING for details.
 *
 * (c) Lawrence Manning, 2001
 *
 * filename: main.c
 * Contains main entry point, and misc functions. */

#include "install.h"

#define CDROM_INSTALL 0
#define URL_INSTALL 1

FILE *flog = NULL;
char *log;

char **ctr;

extern char *english_tr[];

int main(int argc, char *argv[])
{
	char hdletter, cdromletter;		/* Drive letter holder. */
	struct devparams hdparams, cdromparams;	/* Params for CDROM and HD */
	int cdmounted;			/* Loop flag for inserting a cd. */ 
	int rc;
	char commandstring[STRING_SIZE];
	char *installtypes[] = { "CDROM", "HTTP", NULL };
	int installtype = CDROM_INSTALL; 
	char *insertmessage, *insertdevnode;
	char tarballfilename[STRING_SIZE];
	int choice;
	char shortlangname[10];
	int allok = 0;
	struct keyvalue *ethernetkv = initkeyvalues();
	FILE *handle;
	char disksize[STRING_SIZE];
	char filename[STRING_SIZE];
	int maximum_free, current_free;
	int log_partition, boot_partition, root_partition, swap_partition;

	setenv("TERM", "linux", 0);

	sethostname("smoothwall", 10);
	
	memset(&hdparams, 0, sizeof(struct devparams));
	memset(&cdromparams, 0, sizeof(struct devparams));

	/* Log file/terminal stuff. */
	if (argc >= 2)
	{		
		if (!(flog = fopen(argv[1], "w+")))
			return 0;
	}
	else
		return 0;
	
	log = argv[1];
	
	fprintf(flog, "Install program started.\n");

	newtInit();
	newtCls();
	
	ctr = english_tr;
	strcpy(shortlangname, "en");
			
	newtDrawRootText(0, 0, "ALPHA           SmoothWall Express 3.0 -- http://smoothwall.org/");
	newtPushHelpLine(ctr[TR_HELPLINE]);

	newtWinMessage(TITLE, ctr[TR_OK], ctr[TR_WELCOME]);
						
	/* Get device letter for the IDE HD.  This has to succeed. */
	if (!(hdletter = findidetype(IDE_HD)))
	{
		errorbox(ctr[TR_NO_IDE_HARDDISK]);
		goto EXIT;
	}
	
	/* Make the hdparms struct and print the contents. */
	snprintf(hdparams.devnode, STRING_SIZE, "/dev/hd%c", hdletter);
	hdparams.module = 0;

	rc = newtWinMenu(ctr[TR_SELECT_INSTALLATION_MEDIA], 
		ctr[TR_SELECT_INSTALLATION_MEDIA_LONG],
		50, 5, 5, 6, installtypes, &installtype, ctr[TR_OK],
		ctr[TR_CANCEL], NULL);
	
	if (rc == 2)
		goto EXIT;	
	
	if (installtype == CDROM_INSTALL)
	{	
		/* First look for an IDE CDROM. */
		if (!(cdromletter = findidetype(IDE_CDROM)))
		{
			/* If it fails, go the CDROM menu. */
//			fprintf(flog, "No IDE CDROM found.\n");
//			if (!(cdrommenu(&cdromparams)))
//			{
				/* Didn't work, oops. */
				errorbox(ctr[TR_NO_IDE_CDROM]);
				goto EXIT;
//			}
		}
		else
		{
			snprintf(cdromparams.devnode, STRING_SIZE, "/dev/hd%c", cdromletter);
			cdromparams.module = 0;
		}
		
		insertmessage = ctr[TR_INSERT_CDROM];
		insertdevnode = cdromparams.devnode;

		/* Try to mount /cdrom in a loop. */
		cdmounted = 0;
		snprintf(commandstring, STRING_SIZE, "/bin/mount %s /cdrom", insertdevnode);
		while (!cdmounted)
		{
			rc = newtWinChoice(TITLE, ctr[TR_OK], ctr[TR_CANCEL], insertmessage);
			if (rc != 1)
			{
				errorbox(ctr[TR_INSTALLATION_CANCELED]);
				goto EXIT;
			}
			if (!(mysystem(commandstring)))
				cdmounted = 1;
		}
	}

	rc = newtWinChoice(TITLE, ctr[TR_OK], ctr[TR_CANCEL],
		ctr[TR_PREPARE_HARDDISK], hdparams.devnode);
	if (rc != 1)
		goto EXIT;

	rc = newtWinChoice(ctr[TR_PREPARE_HARDDISK_WARNING], ctr[TR_OK], ctr[TR_CANCEL],
		ctr[TR_PREPARE_HARDDISK_WARNING_LONG]);
	if (rc != 1)
		goto EXIT;


	/* Partition, mkswp, mkfs. */
	/* before partitioning, first determine the sizes of each
	 * partition.  In order to do that we need to know the size of
	 * the disk.  we can get the disk size from
	 * /proc/ide/hda/capacity.  unfortunately, it appears that this
	 * number is the "raw" number and makes you think you have more
	 * disk space than you really do.  We'll cope... */
	snprintf(filename, STRING_SIZE, "/proc/ide/hd%c/capacity", hdletter);
	handle = fopen(filename, "r");
	fgets(disksize, STRING_SIZE, handle);
	fclose(handle);
	maximum_free = atoi(disksize) / 2048;
	
	boot_partition = 5; /* in MB */
	current_free = maximum_free - boot_partition;

	swap_partition = 16; /* in MB */
	current_free = maximum_free - swap_partition;
	
	log_partition = (current_free / 5) > 20 ? current_free / 5 : 20;
	current_free = maximum_free - log_partition;

	root_partition = current_free;
	fprintf(flog, "boot = %d, swap = %d, log = %d, root = %d\n",
		boot_partition, swap_partition, log_partition, root_partition);

	handle = fopen("/tmp/partitiontable", "w");
	fprintf(handle, ",%d,83,\n,%d,82,\n,%d,83,\n,,83,*\n",
		boot_partition, swap_partition, log_partition);
	fclose(handle);		

	snprintf(commandstring, STRING_SIZE, "/bin/sfdisk -uM %s < /tmp/partitiontable", hdparams.devnode);
	if (runcommandwithstatus(commandstring, ctr[TR_PARTITIONING_DISK]))
	{
		errorbox(ctr[TR_UNABLE_TO_PARTITION]);
		goto EXIT;
	}
	snprintf(commandstring, STRING_SIZE, "/bin/mke2fs -j %s1", hdparams.devnode);	
	if (runcommandwithstatus(commandstring, ctr[TR_MAKING_BOOT_FILESYSTEM]))
	{
		errorbox(ctr[TR_UNABLE_TO_MAKE_BOOT_FILESYSTEM]);
		goto EXIT;
	}
	snprintf(commandstring, STRING_SIZE, "/bin/mkswap %s2", hdparams.devnode);
	if (runcommandwithstatus(commandstring, ctr[TR_MAKING_SWAPSPACE]))
	{
		errorbox(ctr[TR_UNABLE_TO_MAKE_SWAPSPACE]);
		goto EXIT;
	}
	snprintf(commandstring, STRING_SIZE, "/bin/mke2fs -j %s3", hdparams.devnode);
	if (runcommandwithstatus(commandstring, ctr[TR_MAKING_LOG_FILESYSTEM]))
	{
		errorbox(ctr[TR_UNABLE_TO_MAKE_LOG_FILESYSTEM]);
		goto EXIT;
	}
	snprintf(commandstring, STRING_SIZE, "/bin/mke2fs -j %s4", hdparams.devnode);	
	if (runcommandwithstatus(commandstring, ctr[TR_MAKING_ROOT_FILESYSTEM]))
	{
		errorbox(ctr[TR_UNABLE_TO_MAKE_ROOT_FILESYSTEM]);
		goto EXIT;
	}
	/* Mount harddisk. */
	snprintf(commandstring, STRING_SIZE, "/sbin/mount %s4 /harddisk", hdparams.devnode);
	if (runcommandwithstatus(commandstring, ctr[TR_MOUNTING_ROOT_FILESYSTEM]))
	{
		errorbox(ctr[TR_UNABLE_TO_MOUNT_ROOT_FILESYSTEM]);
		goto EXIT;
	}
	mkdir("/harddisk/boot", S_IRWXU|S_IRWXG|S_IRWXO);
	mkdir("/harddisk/var", S_IRWXU|S_IRWXG|S_IRWXO);	
	mkdir("/harddisk/var/log", S_IRWXU|S_IRWXG|S_IRWXO);
	
	snprintf(commandstring, STRING_SIZE, "/sbin/mount %s1 /harddisk/boot", hdparams.devnode);
	if (runcommandwithstatus(commandstring, ctr[TR_MOUNTING_BOOT_FILESYSTEM]))
	{
		errorbox(ctr[TR_UNABLE_TO_MOUNT_BOOT_FILESYSTEM]);
		goto EXIT;
	}
	snprintf(commandstring, STRING_SIZE, "/bin/swapon %s2", hdparams.devnode);
	if (runcommandwithstatus(commandstring, ctr[TR_MOUNTING_SWAP_PARTITION]))
	{
		errorbox(ctr[TR_UNABLE_TO_MOUNT_SWAP_PARTITION]);
		goto EXIT;
	}
	snprintf(commandstring, STRING_SIZE, "/sbin/mount %s3 /harddisk/var/log", hdparams.devnode);
	if (runcommandwithstatus(commandstring, ctr[TR_MOUNTING_LOG_FILESYSTEM]))
	{
		errorbox(ctr[TR_UNABLE_TO_MOUNT_LOG_FILESYSTEM]);
		goto EXIT;
	}

	/* Network driver and params. */
	if (!(networkmenu(ethernetkv)))
	{
		errorbox(ctr[TR_NETWORK_SETUP_FAILED]);
		goto EXIT;
	}

	/* Either use traball from cdrom or download. */
	if (installtype == CDROM_INSTALL)
		strncpy(tarballfilename, "/cdrom/smoothwall.tgz", STRING_SIZE);
	else
	{
		if (!(downloadtarball()))
		{
			errorbox(ctr[TR_NO_TARBALL_DOWNLOADED]);
			goto EXIT;
		}
		strncpy(tarballfilename, "/harddisk/smoothwall.tgz", STRING_SIZE);
	}
	
	/* unpack... */
	snprintf(commandstring, STRING_SIZE, 
		"/bin/tar -C /harddisk -zxvf %s",
		tarballfilename);
	if (runcommandwithprogress(45, 4, TITLE, commandstring, 7771,
		ctr[TR_INSTALLING_FILES]))
	{
		errorbox(ctr[TR_UNABLE_TO_INSTALL_FILES]);
		goto EXIT;
	}
	
	/* Remove temp tarball if we downloaded. */
	if (installtype == URL_INSTALL)
	{
		if (unlink("/harddisk/smoothwall.tgz"))
		{
			errorbox(ctr[TR_UNABLE_TO_REMOVE_TEMP_FILES]);
			goto EXIT;
		}
	}

	if (runcommandwithstatus("/bin/chroot /harddisk /sbin/depmod -a",
		ctr[TR_CALCULATING_MODULE_DEPENDANCIES]))
	{
		errorbox(ctr[TR_UNABLE_TO_CALCULATE_MODULE_DEPENDANCIES]);
		goto EXIT;
	}

	if (!(writeconfigs(&hdparams, ethernetkv, shortlangname)))
	{
		errorbox(ctr[TR_ERROR_WRITING_CONFIG]);
		goto EXIT;
	}

	if (runcommandwithstatus("/harddisk/sbin/lilo -r /harddisk",
		ctr[TR_INSTALLING_LILO]))
	{
		errorbox(ctr[TR_UNABLE_TO_INSTALL_LILO]);
		goto EXIT;
	}
	
	if (installtype == CDROM_INSTALL)
	{
		if (mysystem("/sbin/umount /cdrom"))
		{
			errorbox(ctr[TR_UNABLE_TO_UNMOUNT_CDROM]);
			goto EXIT;
		}

		if (!(ejectcdrom(cdromparams.devnode)))
		{
			errorbox(ctr[TR_UNABLE_TO_EJECT_CDROM]);
			goto EXIT;
		}
	}

	if (touchfile("/harddisk/var/smoothwall/patches/available"))
	{
		errorbox("Unable to touch patch list file.");
		goto EXIT;
	}		

	newtWinMessage(ctr[TR_CONGRATULATIONS], ctr[TR_OK],
		ctr[TR_CONGRATULATIONS_LONG]);
		
	allok = 1;
				
EXIT:
	fprintf(flog, "Install program ended.\n");	
	fflush(flog);
	fclose(flog);

	if (!(allok))
		newtWinMessage(TITLE, ctr[TR_OK], ctr[TR_PRESS_OK_TO_REBOOT]);	
	
	newtFinished();
	
	freekeyvalues(ethernetkv);

	if (allok)
	{
		/* /proc is needed by the module checker.  We have to mount it
		 * so it can be seen by setup, which is run chrooted. */
		if (system("/sbin/mount proc -t proc /harddisk/proc"))
			printf("Unable to mount proc in /harddisk.");
		else
		{
			if (system("/bin/chroot /harddisk /usr/sbin/setup /dev/tty2 INSTALL"))
				printf("Unable to run setup.\n");
			if (system("/sbin/umount /harddisk/proc"))
				printf("Unable to umount /harddisk/proc.\n");
		}
	}
	
	reboot();

	return 0;
}
