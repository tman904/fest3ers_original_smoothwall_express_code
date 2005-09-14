# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

GCC = gcc

PACKAGE = libstdc++
VERSION = 3.3.2

BASE_URL = ftp://ftp.gnu.org/gnu/gcc

TARBALL = $(GCC)-$(VERSION)

DIR = $(TARBALL)/libstdc++-v3

CLEAN = yes

clean:
	@rm -rf $(GCC)-$(VERSION)
	@rm -rf $(PKG_ROOT)
	
include ../Makefile.rules
