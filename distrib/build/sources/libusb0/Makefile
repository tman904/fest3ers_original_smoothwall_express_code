# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = libusb
VER_MM = 0.1
VERSION = $(VER_MM).12
TARBALL = $(PACKAGE)-$(VERSION)
EXTENSION = .tar.gz

BASE_URL = http://heanet.dl.sourceforge.net/project/$(PACKAGE)/$(PACKAGE)-$(VER_MM)\ \(LEGACY\)/$(VERSION)

BUILDTARBALL = yes
$(TARGET_DIR)/smoothwall-$(PACKAGE)0.tar.gz: install
        tar -zcvf $(TARGET_DIR)/smoothwall-$(PACKAGE)0.tar.gz -C $(PKG_ROOT) .
        tar -zxvf $(TARGET_DIR)/smoothwall-$(PACKAGE)0.tar.gz -C /

include ../Makefile.rules

