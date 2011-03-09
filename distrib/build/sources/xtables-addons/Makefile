# Copyright 2004-2010 SmoothWall Ltd

include ../Makefile.conf
include ../Makefile.versions

PACKAGE = xtables-addons
VERSION =  $(XTADDONS_VER)

LICENCE_FILE = $(DIR)/COPYING

EXTENSION = .tar.bz2

BASE_URL = http://$(SOURCEFORGE_MIRROR).dl.sourceforge.net/sourceforge/xtables-addons/

PATCH_FILE1 = mod-xtables-addon.patch
PATCH_FILE2 = no-kernel-ver-check.patch

CONFIG_OPTS = --with-kbuild=/build/sources/kernel-up/linux

COMPILE = yes
INSTALL = yes

compile: configure
	@make -C $(DIR)/extensions -j $(PARA_JOBS) AM_CFLAGS=-I/build/sources/kernel-up/linux/include user-all-local

install: compile
	@make -C $(DIR)/extensions DESTDIR=$(PKG_ROOT)/ user-install-local

include ../Makefile.rules
