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

#define TRIM_DISK_SIZE 60000

FILE *flog = NULL;
char *logname;

char **ctr;

extern char *english_tr[];

static int partitiondisk(char *diskdevnode, int *partitionsizes);

int main(int argc, char *argv[])
{
	char fmtpartdevnode[STRING_SIZE];
	struct blockdevice hd, cdrom;	/* Params for CDROM and HD */
	int cdmounted;			/* Loop flag for inserting a cd. */ 
	int rc;
	char commandstring[STRING_SIZE];
	int installtype = CDROM_INSTALL; 
	char *insertmessage, *insertdevnode;
	char tarballfilename[STRING_SIZE];
	char shortlangname[10];
	int allok = 0;
	struct keyvalue *ethernetkv = initkeyvalues();
	FILE *handle;
	int maximum_free, current_free;
	int log_partition, boot_partition, root_partition, swap_partition;
	struct keyvalue *hwprofilekv = initkeyvalues();
	FILE *hkernelcmdline;
	char kernelcmdline[STRING_SIZE];
	int ramsize;
	int trimbigdisk = 0;
	int partitionsizes[5];
	int c = 0;

	setenv("TERM", "linux", 0);

	sethostname("smoothwall", 10);

	memset(&hd, 0, sizeof(struct blockdevice));
	memset(&cdrom, 0, sizeof(struct blockdevice));
	memset(fmtpartdevnode, 0, STRING_SIZE);
	memset(kernelcmdline, 0, STRING_SIZE);
	memset(partitionsizes, 0, 5 * sizeof(int));

	/* Log file/terminal stuff. */
	if (argc >= 2)
	{		
		if (!(flog = fopen(argv[1], "w+")))
			return 0;
	}
	else
		return 0;
	
	logname = argv[1];
	
	fprintf(flog, "Install program started.\n");

	if (!(hkernelcmdline = fopen("/proc/cmdline", "r")))
		return 0;
	fgets(kernelcmdline, STRING_SIZE - 1, hkernelcmdline);
	fclose(hkernelcmdline);
	
	if (strstr(kernelcmdline, "trimbigdisk"))
		trimbigdisk = 1;

	/* Load USB keyboard modules so dialogs can respond to USB-keyboards */
	fprintf(flog, "Loading USB-keyboard modules.\n");

	mysystem("/sbin/modprobe usbhid");

	newtInit();
	newtCls();

	/* Preapre storage drivers and load them, only if we haven't
	 * got a IDE disk. */
	mysystem("/sbin/udevd --daemon");
	mysystem("/sbin/udevadm trigger");
	mysystem("/sbin/udevadm settle");		
	
	ctr = english_tr;
	strcpy(shortlangname, "en");
			
	newtDrawRootText(0, 0, "                SmoothWall Express 3.0 -- http://smoothwall.org/");
	newtPushHelpLine(ctr[TR_HELPLINE]);

	newtWinMessage(TITLE, ctr[TR_OK], ctr[TR_WELCOME]);
	
	/* Get device letter for the IDE HD.  This has to succeed. */
	if (!(findharddiskorcdrom(&hd, DISK_HD)))
	{
		errorbox(ctr[TR_NO_HARDDISK]);
		goto EXIT;
	}

	if (!(findharddiskorcdrom(&cdrom, DISK_CDROM)))
	{
		mysystem("/sbin/modprobe usb-storage");
		sleep(10);
		if (!(findharddiskorcdrom(&cdrom, DISK_CDROM)))
			installtype = URL_INSTALL;
		else
			installtype = CDROM_INSTALL;
	}
	else
		installtype = CDROM_INSTALL;
	
	if (installtype == CDROM_INSTALL)
	{
		insertmessage = ctr[TR_INSERT_CDROM];
		insertdevnode = cdrom.devnode;

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
		ctr[TR_PREPARE_HARDDISK], hd.devnode);
	if (rc != 1)
		goto EXIT;

	rc = newtWinChoice(ctr[TR_PREPARE_HARDDISK_WARNING], ctr[TR_OK], ctr[TR_CANCEL],
		ctr[TR_PREPARE_HARDDISK_WARNING_LONG]);
	if (rc != 1)
		goto EXIT;

	/* If this fails, ramsize will be set to 0.  We can still cope though as this
	 * figure is only used as a guide to setting the swap size. */
	ramsize = gettotalmemory();
	fprintf(flog, "%d MB RAM detected.\n", ramsize);

	/* Partition, mkswp, mkfs. */
	/* before partitioning, first determine the sizes of each
	 * partition.  In order to do that we need to know the size of
	 * the disk. */
	maximum_free = getdisksize(hd.devnode);
	
	if (trimbigdisk)
		maximum_free = maximum_free > TRIM_DISK_SIZE ? TRIM_DISK_SIZE : maximum_free;

	fprintf(flog, "%d MB disk space (Trimming: %d)\n", maximum_free, trimbigdisk);
	
	boot_partition = 80; /* in MB */
	current_free = maximum_free - boot_partition;

	/* Trim swap to tiny if disk is small, like a CF. */
	if (maximum_free < 3000)
		swap_partition = 4;
	else
		swap_partition = ramsize < 64 ? 64 : ramsize; /* in MB */
	current_free -= swap_partition;
	
	log_partition = (current_free / 3) > 20 ? current_free / 3 : 20;
	current_free -= log_partition;

	root_partition = current_free;
	fprintf(flog, "boot = %d, swap = %d, log = %d, root = %d\n",
		boot_partition, swap_partition, log_partition, root_partition);

	handle = fopen("/tmp/partitiontable", "w");
	if (trimbigdisk)
	{
		/* Disk usage is limited, so we must specify root's size in order
		 * to leave the rest of the disk unused. */
		fprintf(handle, ",%d,83,\n,%d,82,\n,%d,83,\n,%d,83,*\n",
			boot_partition, swap_partition, log_partition, root_partition);
	}
	else
	{
		fprintf(handle, ",%d,83,\n,%d,82,\n,%d,83,\n,,83,*\n",
			boot_partition, swap_partition, log_partition);
	}
	fclose(handle);		

	c = 0;
	partitionsizes[c++] = boot_partition;
	partitionsizes[c++] = swap_partition;
	partitionsizes[c++] = log_partition;
	partitionsizes[c++] = 0;
	
	if (partitiondisk(hd.devnode, partitionsizes))
	{
		errorbox(ctr[TR_UNABLE_TO_PARTITION]);
		goto EXIT;
	}

	snprintf(commandstring, STRING_SIZE, "/bin/mke2fs -L BOOT -t ext4 -j %s1", hd.devnode);	
	if (runcommandwithstatus(commandstring, ctr[TR_MAKING_BOOT_FILESYSTEM]))
	{
		errorbox(ctr[TR_UNABLE_TO_MAKE_BOOT_FILESYSTEM]);
		goto EXIT;
	}
	snprintf(commandstring, STRING_SIZE, "/bin/mkswap -L SWAP %s2", hd.devnode);
	if (runcommandwithstatus(commandstring, ctr[TR_MAKING_SWAPSPACE]))
	{
		errorbox(ctr[TR_UNABLE_TO_MAKE_SWAPSPACE]);
		goto EXIT;
	}
	snprintf(commandstring, STRING_SIZE, "/bin/mke2fs -L LOG -t ext4 -j %s3", hd.devnode);
	if (runcommandwithstatus(commandstring, ctr[TR_MAKING_LOG_FILESYSTEM]))
	{
		errorbox(ctr[TR_UNABLE_TO_MAKE_LOG_FILESYSTEM]);
		goto EXIT;
	}
	snprintf(commandstring, STRING_SIZE, "/bin/mke2fs -L ROOT -t ext4 -j %s4", hd.devnode);	
	if (runcommandwithstatus(commandstring, ctr[TR_MAKING_ROOT_FILESYSTEM]))
	{
		errorbox(ctr[TR_UNABLE_TO_MAKE_ROOT_FILESYSTEM]);
		goto EXIT;
	}
	/* Mount harddisk. */
	snprintf(commandstring, STRING_SIZE, "/sbin/mount %s4 /harddisk", hd.devnode);
	if (runcommandwithstatus(commandstring, ctr[TR_MOUNTING_ROOT_FILESYSTEM]))
	{
		errorbox(ctr[TR_UNABLE_TO_MOUNT_ROOT_FILESYSTEM]);
		goto EXIT;
	}
	mkdir("/harddisk/boot", S_IRWXU|S_IRWXG|S_IRWXO);
	mkdir("/harddisk/var", S_IRWXU|S_IRWXG|S_IRWXO);
	mkdir("/harddisk/var/log", S_IRWXU|S_IRWXG|S_IRWXO);
	
	snprintf(commandstring, STRING_SIZE, "/sbin/mount %s1 /harddisk/boot", hd.devnode);
	if (runcommandwithstatus(commandstring, ctr[TR_MOUNTING_BOOT_FILESYSTEM]))
	{
		errorbox(ctr[TR_UNABLE_TO_MOUNT_BOOT_FILESYSTEM]);
		goto EXIT;
	}
	snprintf(commandstring, STRING_SIZE, "/bin/swapon %s2", hd.devnode);
	if (runcommandwithstatus(commandstring, ctr[TR_MOUNTING_SWAP_PARTITION]))
	{
		errorbox(ctr[TR_UNABLE_TO_MOUNT_SWAP_PARTITION]);
		goto EXIT;
	}
	snprintf(commandstring, STRING_SIZE, "/sbin/mount %s3 /harddisk/var/log", hd.devnode);
	if (runcommandwithstatus(commandstring, ctr[TR_MOUNTING_LOG_FILESYSTEM]))
	{
		errorbox(ctr[TR_UNABLE_TO_MOUNT_LOG_FILESYSTEM]);
		goto EXIT;
	}

	if (installtype == URL_INSTALL)
	{
		/* Network driver and params. */
		if (!(networkmenu(ethernetkv)))
		{
			errorbox(ctr[TR_NETWORK_SETUP_FAILED]);
			goto EXIT;
		}
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
	if (runcommandwithprogress(45, 4, TITLE, commandstring, 27238,
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

	replacekeyvalue(hwprofilekv, "STORAGE_DEVNODE", hd.devnode);
	replacekeyvalue(hwprofilekv, "CDROM_DEVNODE", cdrom.devnode);
	replacekeyvalue(hwprofilekv, "FS", "ext4");
	writekeyvalues(hwprofilekv, "/harddisk/" CONFIG_ROOT "/main/hwprofile");

	if (runcommandwithstatus("/bin/chroot /harddisk /sbin/depmod -a",
		ctr[TR_CALCULATING_MODULE_DEPENDANCIES]))
	{
		errorbox(ctr[TR_UNABLE_TO_CALCULATE_MODULE_DEPENDANCIES]);
		goto EXIT;
	}

	if (!(writeconfigs(&hd, ethernetkv, shortlangname)))
	{
		errorbox(ctr[TR_ERROR_WRITING_CONFIG]);
		goto EXIT;
	}
	
	mysystem("/sbin/mount proc -t proc /harddisk/proc");

	if (runcommandwithstatus("/bin/chroot /harddisk /usr/bin/installer/makeinitrd", ctr[TR_SETTING_UP_BOOT_DRIVERS]))
	{
		errorbox(ctr[TR_UNABLE_TO_SETUP_BOOT_DRIVERS]);
		goto EXIT;
	}
	if (runcommandwithstatus("/bin/chroot /harddisk /usr/bin/smoothwall/updatestorageuuids.pl", ctr[TR_SETTING_UP_BOOT_DRIVERS]))
	{
		errorbox(ctr[TR_UNABLE_TO_SETUP_BOOT_DRIVERS]);
		goto EXIT;
	}
	if (runcommandwithstatus("/bin/chroot /harddisk /usr/bin/smoothwall/writefstab.pl", ctr[TR_SETTING_UP_BOOT_DRIVERS]))
	{
		errorbox(ctr[TR_UNABLE_TO_SETUP_BOOT_DRIVERS]);
		goto EXIT;
	}
	
	if (runcommandwithstatus("/bin/chroot /harddisk /usr/bin/smoothwall/writegrubconf.pl", ctr[TR_SETTING_UP_BOOT_DRIVERS]))
	{
		errorbox(ctr[TR_UNABLE_TO_SETUP_BOOT_DRIVERS]);
		goto EXIT;
	}
	if (runcommandwithstatus("/bin/chroot /harddisk /usr/bin/smoothwall/installgrub.pl",
		ctr[TR_INSTALLING_GRUB]))
	{
		errorbox(ctr[TR_UNABLE_TO_INSTALL_GRUB]);
		goto EXIT;
	}
	
	if (installtype == CDROM_INSTALL)
	{
		if (mysystem("/sbin/umount /cdrom"))
		{
			errorbox(ctr[TR_UNABLE_TO_UNMOUNT_CDROM]);
			goto EXIT;
		}

		if (!(ejectcdrom(cdrom.devnode)))
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
	/* We don't need udev anymore. */
	mysystem("/bin/killall udevd");

	fprintf(flog, "Install program ended.\n");	
	fflush(flog);
	fclose(flog);

	if (!(allok))
		newtWinMessage(TITLE, ctr[TR_OK], ctr[TR_PRESS_OK_TO_REBOOT]);	
	
	newtFinished();
	
	freekeyvalues(ethernetkv);

	if (allok)
	{
		if (system("/bin/chroot /harddisk /usr/sbin/setup /dev/tty2 INSTALL"))
			printf("Unable to run setup.\n");
	}
	
	mysystem("/sbin/umount /harddisk/proc");
	
	reboot();

	return 0;
}

static int partitiondisk(char *diskdevnode, int *partitionsizes)
{
	int c = 0;
	int start = 1; int end = 0;
	char commandstring[STRING_SIZE];
	
	memset(commandstring, 0, STRING_SIZE);
	
	snprintf(commandstring, STRING_SIZE - 1, "/bin/parted %s --script -- mklabel gpt", diskdevnode);
	if (runcommandwithstatus(commandstring, ctr[TR_PARTITIONING_DISK]))
	{
		return 1;
	}
	
	for (c = 0; partitionsizes[c]; c++)
	{
		end += partitionsizes[c];
		snprintf(commandstring, STRING_SIZE - 1, "/bin/parted %s --script -- mkpart primary %d %d",
			diskdevnode, start, end);
		if (runcommandwithstatus(commandstring, ctr[TR_PARTITIONING_DISK]))
		{
			return 1;
		}
		start += partitionsizes[c];
	}
	
	end = -1;
	snprintf(commandstring, STRING_SIZE - 1, "/bin/parted %s --script -- mkpart primary %d -1",
		diskdevnode, start);
	if (runcommandwithstatus(commandstring, ctr[TR_PARTITIONING_DISK]))
	{
		return 1;
	}
	
	sleep(2);
	
	return 0;
}
