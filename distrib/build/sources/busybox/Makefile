# Copyright 2004-2010 SmoothWall Ltd

include ../Makefile.conf

PACKAGE = busybox
VERSION = 1.18.0

EXTENSION = .tar.bz2

LICENCE_FILE = $(DIR)/LICENSE

BASE_URL = http://busybox.net/downloads/

PKG_DIR = /opt/busybox

CONFIGURE = yes
INSTALL = yes

configure: $(DIR)/
	@cp -avR config $(COMPILE_DIR)/.config
#	@make -C $(DIR) oldconfig

install: compile
	@make -C $(COMPILE_DIR) CONFIG_PREFIX=$(PKG_ROOT)/$(PKG_DIR) install
	@for I in $$($(PKG_ROOT)/$(PKG_DIR)/bin/busybox --list); do ln -s busybox $(PKG_ROOT)/$(PKG_DIR)/bin/$$I; done

include ../Makefile.rules
