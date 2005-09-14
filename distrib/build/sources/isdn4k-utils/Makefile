# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = isdn4k-utils
VERSION = CVS-2003-09-23

BASE_URL = ftp://ftp.isdn4linux.de/pub/isdn4linux/CVS-Snapshots/

EXTENSION = .tar.bz2

CONFIGURE = yes

configure: patch
	@cp -avR config $(DIR)/.config
	@make -C $(DIR) subconfig

include ../Makefile.rules
