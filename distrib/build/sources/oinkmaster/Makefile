# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = oinkmaster
VERSION = 1.2

BASE_URL = http://www.snort.org/dl/current

INSTALL = yes

install: patch
	-mkdir -p $(PKG_ROOT)/var/smoothwall/snort
	@install -D $(COMPILE_DIR)/oinkmaster.pl $(PKG_ROOT)/usr/bin/oinkmaster.pl
	@install -D $(COMPILE_DIR)/oinkmaster.conf $(PKG_ROOT)/var/smoothwall/snort/oinkmaster.conf
	@chown nobody:nobody -R $(PKG_ROOT)/var/smoothwall/

include ../Makefile.rules
