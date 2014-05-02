# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = linux-firmware
VERSION = 20140316

EXTENSION = .tar.gz

export pkgName = $(PACKAGE)
export gitURL = https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git
export gitCommitID = dec41bce4
export gitBranch = $(VERSION)

PREPARE = yes
$(DIR)/:
	true

COMPILE = yes
compile:
	true

INSTALL = yes
install: download
	rm -rf $(PKG_ROOT)
	mkdir -p $(PKG_ROOT)/lib/firmware
	tar xvf $(DOWNLOADS_DIR)/$(TARBALL)$(EXTENSION) -C $(PKG_ROOT)/lib/firmware
	chown -R root:root $(PKG_ROOT)
	chmod -R 444 $(PKG_ROOT)

include ../Makefile.rules
