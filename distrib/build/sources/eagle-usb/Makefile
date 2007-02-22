# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = eagle-usb
VERSION = 2.3.3

BASE_URL = http://baud123.free.fr/eagle-usb/eagle-usb-2.3/

EXTENSION = .tar.bz2

CONFIG_OPTS = --disable-module --disable-eagleconnect --disable-hotplug

INSTALL = yes

install: compile
	@make -C $(DIR)/driver/firmware DESTDIR=$(PKG_ROOT) install
	@make -C $(DIR)/driver/user DESTDIR=$(PKG_ROOT) install
	@make -C $(DIR)/pppoa DESTDIR=$(PKG_ROOT) install
	
include ../Makefile.rules
