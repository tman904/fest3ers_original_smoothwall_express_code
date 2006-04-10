# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = eagle-usb
VERSION = 2.3.2

BASE_URL = http://baud123.free.fr/eagle-usb/eagle-usb-2.3/

EXTENSION = .tar.bz2

CONFIG_OPTS = --with-kernel-src=$(SOURCES_DIR)/kernel-runtime/linux

COMPILE = yes
INSTALL = yes

COMPILER = /opt/gcc-3.2.3/bin/gcc

PATCH_FILE1 = gcc-fix.patch

compile: configure
	@make CC=$(COMPILER) -C $(DIR)/driver
	@make -C $(DIR)/pppoa

install: compile
	-mkdir $(PKG_ROOT)
	@make -C $(DIR)/driver DESTDIR=$(PKG_ROOT) install
	@make -C $(DIR)/pppoa DESTDIR=$(PKG_ROOT) install

include ../Makefile.rules
