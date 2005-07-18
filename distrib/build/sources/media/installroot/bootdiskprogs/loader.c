/* SmoothWall loader program.
 *
 * This program is distributed under the terms of the GNU General Public
 * Licence.  See the file COPYING for details.
 *
 * (c) Lawrence Manning, 2001
 *
 * filename: loader.c */

#include "setuid.h"

#define WAIT_FOR_KEY	fgets(dummy, STRING_SIZE, stdin);
#define WHITE_FG	printf("\033[37m");
#define BLACK_FG	printf("\033[30m");
#define BLUE_BG		printf("\033[44m");
#define BOLD		printf("\033[1m");
#define NORMAL		printf("\033[0m");
#define HOME_CLEAR	printf("\033[2J\033[0;0H");

int main(int argc, char *argv[])
{
	struct stat statbuf;
	int floppymounted = 0;
	int cdrominstall = 0;
	char dummy[STRING_SIZE];
	FILE *hfile = NULL;

	memset(dummy, 0, STRING_SIZE);

	if (stat("/cdrominstall", &statbuf) == 0)
		cdrominstall = 1;
	else
		cdrominstall = 0;

	BLUE_BG WHITE_FG HOME_CLEAR BOLD	

	printf("                             SmoothWall " PRODUCT_NAME PRODUCT_VERSION "\n\n");

	NORMAL BLUE_BG WHITE_FG

	if (!cdrominstall)
	{
		printf("INSTRUCTIONS\n\n");
	
		printf("You are installing from floppy disk. This method of installation requires\n");
		printf("access to the second boot floppy disk to continue.\n\n");
	
		while (!floppymounted)
		{
			printf("Insert disk two and press ");
			BOLD
			printf("RETURN.\n");
			NORMAL BLUE_BG WHITE_FG
			WAIT_FOR_KEY

			if (!system("/bin/mount dev/fd0 /bootdisktwo"))
			{
				if ((hfile = fopen("/bootdisktwo/gpltwo", "r")))
				{
					fclose(hfile);
					floppymounted = 1;
				}
				else
				{
					system("/bin/umount /dev/fd0");
				}			
			}
		}
	}
	
	printf("Extracting drivers...\n");
	if (system("/bin/tar -zxvf /bootdisktwo/drivers.tar.gz -C /"))
		goto FAILURE;
	
	if (floppymounted)
		system("/bin/umount /dev/fd0");

	system("/bin/install /dev/tty2");

	NORMAL

	printf("\n");			

	return 0;

FAILURE:

	if (floppymounted)
		system("/bin/umount /dev/fd0");

	printf("\n\n");
	printf("COMMAND FAILED.\n\n");
	printf("Sleeping 30 seconds and then trying again.  Sorry it didn't work out.\n");
	sleep(30);

	return 1;	
}
