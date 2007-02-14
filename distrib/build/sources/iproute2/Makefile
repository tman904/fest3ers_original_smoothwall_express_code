# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = iproute2
VERSION = 2.6.18-061002

BASE_URL = http://developer.osdl.org/dev/iproute2/download/

PATCH_FILE1 = iproute2-2.4.7-nomisc.patch


CONFIGURE = yes
COMPILE = yes
INSTALL = yes

configure: patch
	@true

compile: configure
	@make -C $(COMPILE_DIR) KERNEL_INCLUDE=/usr/include

install: compile
	@mkdir -p $(PKG_ROOT)/sbin
	@install -D $(COMPILE_DIR)/ip/ip $(PKG_ROOT)/sbin/ip
	@install -D $(COMPILE_DIR)/tc/tc $(PKG_ROOT)/sbin/tc

include ../Makefile.rules
