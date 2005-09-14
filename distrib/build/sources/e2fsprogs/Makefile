# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = e2fsprogs
VERSION = 1.35

BASE_URL = http://heanet.dl.sourceforge.net/sourceforge/e2fsprogs/

COMPILE_DIR = $(DIR)-compile

CONFIG_OPTS = --with-root-prefix=""

INSTALL = yes

install: compile
	@mkdir $(PKG_ROOT)
	@make -C $(COMPILE_DIR) DESTDIR=$(PKG_ROOT) install
	@make -C $(COMPILE_DIR) DESTDIR=$(PKG_ROOT) install-libs
	
include ../Makefile.rules
