# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = MAKEDEV
VERSION = 3.3.8

BASE_URL = http://www.aslak.net/smoothmirror/

TARBALL = $(PACKAGE)-$(VERSION)-2

DIR = $(PACKAGE)-$(VERSION)

CONFIGURE = yes

configure: patch
	@true

devnodes:
	@(cd /dev; mkdir pts; \
	./MAKEDEV random urandom mem kmem null port zero core full \
		ram raid tty console tty pty fd hd sd loop scd sg apm usb initctl ppp net isdn rtc);
	@chmod 664 /dev/isdninfo
	@tar -zcvf /$(TARGET_DIR)/smoothwall-devnodes.tar.gz -C / --exclude ./dev/MAKEDEV ./dev;

include ../Makefile.rules
