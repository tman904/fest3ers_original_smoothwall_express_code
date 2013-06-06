# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = wget
VERSION = 1.14

BASE_URL = ftp://ftp.gnu.org/gnu/wget
EXTENSION = .tar.xz

# Some sites disallow HTTP
CONFIG_OPTS = --with-ssl=openssl

COMPILE = yes
compile: configure
	$(MAKE) $(JOBS) -C $(COMPILE_DIR)

include ../Makefile.rules
