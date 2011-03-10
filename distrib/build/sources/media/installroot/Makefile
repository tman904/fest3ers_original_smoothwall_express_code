# Copyright 2004-2010 SmoothWall Ltd

include ../../Makefile.versions
include ../../Makefile.conf

INSTALL_ROOT = installroot
BB = /opt/busybox

WORKING_DIR = /build/sources/media/installroot/$(INSTALL_ROOT)

BASICROOTFS_DIR = /build/buildroot/basicrootfs

all: clean
	mkdir $(INSTALL_ROOT)

	touch $(INSTALL_ROOT)/cdrominstall

	(cd $(INSTALL_ROOT); cat $(BASICROOTFS_DIR)/usr/lib/installer/basicrootfs.gz | gzip -d | cpio -H newc -iv)
	
	cp -dvR /build/target/install $(INSTALL_ROOT)/bin/installer
	cp -dvR etc/* $(INSTALL_ROOT)/etc
	cp -dvR init $(INSTALL_ROOT)/

	(cd /build/buildroot/kernel/; \
	cp --parents -dvR /lib/modules/$(KERNEL_VER)-$(KERNEL_PL)-runtime/kernel/ $(WORKING_DIR); \
	cp --parents -dvR /lib/modules/$(KERNEL_VER)-$(KERNEL_PL)-runtime/modules.* $(WORKING_DIR); \
	cp --parents -dvR /lib/firmware $(WORKING_DIR); \
	rm -rf $(WORKING_DIR)/lib/modules/$(KERNEL_VER)-$(KERNEL_PL)-runtime/kernel/drivers/net)
	
	(cd $(INSTALL_ROOT); find . -print | cpio -H newc -ov > ../../$(INSTALL_ROOT)image)
	gzip -9 ../$(INSTALL_ROOT)image

	echo "installroot build complete"
	
clean:
	rm -rf $(INSTALL_ROOT)
	rm -f ../$(INSTALL_ROOT)image.gz
