# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = wget
VERSION = 1.13.3

BASE_URL = ftp://ftp.gnu.org/gnu/wget

ifndef BUILDENV
export CFLAGS += -I/usr/ssl/include
export LDFLAGS += -L/usr/ssl/lib

CONFIG_OPTS = --with-ssl -with-ssl=openssl
else
CONFIG_OPTS = --without-ssl
endif

include ../Makefile.rules
