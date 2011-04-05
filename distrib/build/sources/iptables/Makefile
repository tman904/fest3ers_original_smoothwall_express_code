# Copyright 2004-2010 SmoothWall Ltd

include ../Makefile.conf
include ../Makefile.versions

PACKAGE = iptables
VERSION = $(IPTABLES_VER)

LICENCE_FILE = $(DIR)/COPYING

EXTENSION = .tar.bz2

BASE_URL = http://www.netfilter.org/projects/iptables/files/

#PATCH_FILE1 = iptables-mod.diff
PATCH_FILE2 = iptables-1.4.3.2-imq_xt.diff
#PATCH_FILE3 = ipt_ACCOUNT.patch

CONFIG_OPTS = --enable-libipq

INSTALL = yes

install: compile
	@make -C $(DIR) DESTDIR=$(PKG_ROOT)/ install
	@mkdir $(PKG_ROOT)/sbin
	@(cd $(PKG_ROOT)/sbin; ln -s /usr/sbin/iptables)

include ../Makefile.rules
