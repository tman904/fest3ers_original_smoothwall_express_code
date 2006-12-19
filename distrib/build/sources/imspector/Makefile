# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = imspector
VERSION = 0.3

BASE_URL = http://www.imspector.org/downloads/

CONFIGURE = yes
INSTALL = yes

configure: patch
	@true

install: compile
	@make -C $(DIR) install PREFIX=$(PKG_ROOT)/$(PKG_DIR)

include ../Makefile.rules
