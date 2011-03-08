# Copyright 2004-2010 SmoothWall Ltd

include ../Makefile.conf

PACKAGE = e2fsprogs
VERSION = 1.41.12

LICENCE_FILE = $(DIR)/COPYING

BASE_URL = http://kent.dl.sourceforge.net/sourceforge/e2fsprogs/

COMPILE_DIR = $(DIR)-compile

#CONFIG_OPTS = --with-root-prefix="" --disable-libuuid --disable-uuidd --disable-libblkid
CONFIG_OPTS = --with-root-prefix="" --enable-elf-shlibs --disable-tls

INSTALL = yes

install: compile
	@mkdir -p $(PKG_ROOT)
	@make -C $(COMPILE_DIR) DESTDIR=$(PKG_ROOT) install
	@make -C $(COMPILE_DIR) DESTDIR=$(PKG_ROOT) install-libs
#	@rm -rf $(PKG_ROOT)/sbin/
	
include ../Makefile.rules
