# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = gmp
VERSION = 4.1.4

BASE_URL = ftp://ftp.gnu.org/gnu/gmp

ifeq ($(ARCH), i386)
CONFIG_OPTS = --disable-nls --host=i386-pc-linux-gnu
endif

include ../Makefile.rules
