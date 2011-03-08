# Copyright 2004-2010 SmoothWall Ltd

include ../Makefile.conf

PACKAGE = udev
VERSION = 136

LICENCE_FILE = $(DIR)/COPYING

BASE_URL = http://www.kernel.org/pub/linux/utils/kernel/hotplug/

PATCH_FILE1 = rmdir-ignore-EBUSY.patch

CONFIG_OPTS = --prefix=/usr --sysconfdir=/etc --sbindir=/sbin --exec-prefix=/

INSTALL = yes

install: compile
	make -C $(DIR) DESTDIR=$(PKG_ROOT) install
	install -D 65-mdadm.vol_id.rules $(PKG_ROOT)/lib/udev/rules.d/65-mdadm.vol_id.rules
	
include ../Makefile.rules
