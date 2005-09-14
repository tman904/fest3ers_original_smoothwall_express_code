# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = expect
VERSION = 5.42

BASE_URL = http://expect.nist.gov/old/

PATCH_FILE1 = expect-5.41.0-spawn-1.patch

TARBALL = $(PACKAGE)-$(VERSION).1

DIR = $(PACKAGE)-$(VERSION)

CONFIG_OPTS = --with-tcl=/$(PKG_DIR)/lib \
	--with-tclinclude=$(SOURCES_DIR)/tcl/tcl8.4.6 --with-x=no

include ../Makefile.rules
