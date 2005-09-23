include ../../../Makefile.conf
include ../Makefile.versions

PACKAGE = eagle-usb
VERSION = 2.3.2

BASE_URL = http://baud123.free.fr/eagle-usb/eagle-usb-2.3/

EXTENSION = .tar.bz2

CONFIG_OPTS = --with-kernel-src=$(SOURCES_DIR)/kernel-up/linux

MODULE_DIR = modules/$(MODULE_NAME)/

PKG_DIR = /$(MODULE_DIR)/usr/

COMPILE = yes
INSTALL = yes

compile: configure
	@make -C $(DIR)/driver EU_DIR=/$(MODULE_DIR)/etc/eagle-usb eagleuser dsp
	@make -C $(DIR)/pppoa

install: compile
	-mkdir $(PKG_ROOT)
	@make -C $(DIR)/driver DESTDIR=$(PKG_ROOT) EU_DIR=$(PKG_ROOT)/$(MODULE_DIR)/etc/eagle-usb installuser installdsp
	@make -C $(DIR)/pppoa DESTDIR=$(PKG_ROOT) install

include ../../../Makefile.rules
