# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = iproute2
VERSION = 2.6.37

BASE_URL = http://developer.osdl.org/dev/iproute2/download/

PATCH_FILE1 = iproute2-2.4.7-nomisc.patch

EXTENSION = .tar.bz2

CONFIGURE = yes
COMPILE = yes
INSTALL = yes

PATHS = SBINDIR=/usr/sbin CONFDIR=/etc/iproute2 DOCDIR=/usr/share/doc/iproute2 MANDIR=/usr/share/man LIBDIR=/usr/lib/

configure: patch
	@true

compile: configure
	@make -C $(COMPILE_DIR) -j $(PARA_JOBS) KERNEL_INCLUDE=/usr/include $(PATHS)
	@ln -s $(DIR) $(PACKAGE)

install: compile
	@make -C $(COMPILE_DIR) $(PATHS) DESTDIR=$(PKG_ROOT) MODDESTDIR=$(PKG_ROOT)/usr/lib/tc install
	
include ../Makefile.rules
