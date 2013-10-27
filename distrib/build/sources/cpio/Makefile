# Copyright 2004-2010 SmoothWall Ltd

include ../Makefile.conf

PACKAGE = cpio
VERSION = 2.11

LICENCE_FILE = $(DIR)/COPYING

#PATCH_FILE1 = cpio-2.9-gcc4_3.patch

PRE_CONFIGURE = CFLAGS="$(CFLAGS)"

CONFIG_OPTS = --prefix=/usr \
	      --bindir=/bin \
	      --libexecdir=/tmp \
	      --disable-silent-rules \
	      --with-rmt=/usr/sbin/rmt

include ../Makefile.rules
