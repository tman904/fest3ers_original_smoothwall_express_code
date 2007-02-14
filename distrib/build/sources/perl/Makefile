# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = perl
VERSION = 5.8.8

BASE_URL = http://ftp.funet.fi/pub/CPAN/src/

CONFIGURE = yes

configure: patch
	@(cd $(COMPILE_DIR); \
	./configure.gnu --prefix=/$(PKG_DIR) -Dpager="/bin/less -isR");

include ../Makefile.rules
