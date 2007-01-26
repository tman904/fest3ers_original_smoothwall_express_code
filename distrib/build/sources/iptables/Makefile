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

PATCH_FILE1 = ipt_ACCOUNT.patch

CONFIGURE = yes
COMPILE = yes
INSTALL = yes

configure: $(DIR)/ patch
	@true

compile: configure
	@make -C $(COMPILE_DIR) COPT_FLAGS='$(CFLAGS)' KERNEL_DIR=$(SOURCES_DIR)/kernel-runtime/linux PREFIX=/$(PKG_DIR)

install: compile
	@make -C $(DIR) KERNEL_DIR=$(SOURCES_DIR)/kernel-runtime/linux PREFIX=$(PKG_ROOT)/$(PKG_DIR) install
	@mkdir $(PKG_ROOT)/sbin
	@(cd $(PKG_ROOT)/sbin; ln -s /usr/sbin/iptables)

include ../Makefile.rules
