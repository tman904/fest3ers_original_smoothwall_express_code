# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = zlib
VERSION = 1.2.2

BASE_URL = http://www.zlib.net/

INSTALL = yes

CONFIG_OPTS =

install: compile
	@make -C $(DIR) install prefix=$(PKG_ROOT)/$(PKG_DIR)

include ../Makefile.rules
