# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = libipt_ACCOUNT
VERSION =  1.2

BASE_URL = http://www.intra2net.com/de/produkte/opensource/ipt_account/

COMPILE = yes

compile: configure
	@make -C $(DIR) CFLAGS="$(CFLAGS) -I$(SOURCES_DIR)/kernel-runtime/linux/include"

include ../Makefile.rules
