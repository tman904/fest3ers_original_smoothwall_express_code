# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = arp-scan
VERSION = 20151122

EXTENSION = .tar.gz

export pkgName = $(PACKAGE)
export gitURL = git://github.com/royhills/$(PACKAGE).git
export gitCommitID=69b2f7058856
export gitBranch=20151122

CONFIGURE = yes
configure: patch
	cd $(COMPILE_DIR); \
	  autoreconf -v --install
	cd $(COMPILE_DIR); ./configure --prefix=$(PKG_DIR) $(CONFIG_OPTS)


include ../Makefile.rules
