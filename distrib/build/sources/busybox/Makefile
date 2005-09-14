# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = busybox
VERSION = 1.00

BASE_URL = http://busybox.net/downloads/

PKG_DIR = opt/busybox

CONFIGURE = yes
INSTALL = yes

configure: $(DIR)/
	@cp -avR config $(COMPILE_DIR)/.config

install: compile
	@make -C $(COMPILE_DIR) PREFIX=$(PKG_ROOT)/$(PKG_DIR) install

include ../Makefile.rules
