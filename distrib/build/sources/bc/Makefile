# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = bc
VERSION = 1.06.95

BASE_URL = http://alpha.gnu.org/gnu/$(PACKAGE)

EXTENSION = .tar.bz2

PATCH_FILE1 = bc-1.06.95-memory_leak-1.patch

CONFIG_OPTS = --prefix=/usr \
	      --with-readline \
	      --mandir=/usr/share/man \
	      --infodir=/usr/share/info

include ../Makefile.rules
