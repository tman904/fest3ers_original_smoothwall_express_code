# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = tcl
VERSION = 8.4.6

BASE_URL = http://aleron.dl.sourceforge.net/sourceforge/tcl/

PATCH_FILE1 = configure-tcl-fixes-bash3.patch
PATCH_FILE2 = dash-fix.patch

TARBALL = $(PACKAGE)$(VERSION)-src

DIR = $(PACKAGE)$(VERSION)

ifdef BITS_64
CONFIG_OPTS = --enable-64bit
endif

CONFIGURE = yes
COMPILE = yes
INSTALL = yes

configure: patch
	@(cd $(DIR)/unix; ./configure --prefix=/$(PKG_DIR) $(CONFIG_OPTS))

compile: configure
	@make -C $(DIR)/unix

install: compile
	@make -C $(DIR)/unix INSTALL_ROOT=$(PKG_ROOT) install
	@ln -s tclsh8.4 $(PKG_ROOT)/$(PKG_DIR)/bin/tclsh

include ../Makefile.rules
