# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf
include ../Makefile.versions

PACKAGE = iptables
VERSION =  $(IPTABLES_VER)

EXTENSION = .tar.bz2

BASE_URL = ftp://ftp.netfilter.org/pub/iptables

CONFIGURE = yes
COMPILE = yes
INSTALL = yes

configure: $(DIR)/
	@true

compile: configure
	@make -C $(COMPILE_DIR) KERNEL_DIR=$(SOURCES_DIR)/kernel-up/linux PREFIX=/$(PKG_DIR)

install: compile
	@make -C $(DIR) KERNEL_DIR=$(SOURCES_DIR)/kernel-up/linux PREFIX=$(PKG_ROOT)/$(PKG_DIR) install
	@mkdir $(PKG_ROOT)/sbin
	@(cd $(PKG_ROOT)/sbin; ln -s /usr/sbin/iptables)

include ../Makefile.rules
