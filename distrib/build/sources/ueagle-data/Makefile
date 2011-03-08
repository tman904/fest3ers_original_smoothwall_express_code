include ../Makefile.conf

PACKAGE = ueagle-data
VERSION = 1.1

BASE_URL = http://eagle-usb.org/ueagle-atm/non-free/

INSTALL = yes

install: patch
	mkdir -p $(PKG_ROOT)/lib/firmware/ueagle-atm
	cp $(DIR)/* $(PKG_ROOT)/lib/firmware/ueagle-atm

include ../Makefile.rules
