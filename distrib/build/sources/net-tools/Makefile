# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = net-tools
VERSION = 1.60

EXTENSION = .tar.bz2

BASE_URL = http://www.tazenda.demon.co.uk/phil/net-tools/

PATCH_FILE1 = net-tools-1.60-miitool-gcc33-1.patch
PATCH_FILE2 = net-tools-2.4.28-fddi-fix.patch
PATCH_FILE3 = net-tools-1.60-kernel-26-fix.patch

PKG_DIR = 

CONFIGURE = yes
INSTALL = yes

configure: patch
	@cp -f config.h $(DIR)
	@cp -f config.make $(DIR)

install: compile
	@make -C $(DIR) BASEDIR=$(PKG_ROOT)/$(PKG_DIR) install

include ../Makefile.rules
