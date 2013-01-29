# Copyright 2004-2013 SmoothWall Ltd

include ../Makefile.conf

PACKAGE = busybox
VERSION = 1.20.2

BASE_URL = http://busybox.net/downloads/
EXTENSION = .tar.bz2

LICENCE_FILE = $(DIR)/LICENSE

PKG_DIR = /opt/busybox

PATCH_FILE1 = libbb.h.patch

CONFIGURE = yes
INSTALL = yes

configure: $(DIR)/
	@cp -avR config $(COMPILE_DIR)/.config
#	@$(MAKE) $(JOBS) -C $(DIR) oldconfig

install: compile
	@mkdir -p $(PKG_ROOT)
	@$(MAKE) $(JOBS) -C $(COMPILE_DIR) CONFIG_PREFIX=$(PKG_ROOT)/$(PKG_DIR) install
	@for I in $$($(PKG_ROOT)$(PKG_DIR)/bin/busybox --list); do \
	    ln -s busybox $(PKG_ROOT)$(PKG_DIR)/bin/$$I; done

include ../Makefile.rules
