# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../../Makefile.versions
include ../../Makefile

bootdisktwo.img: bin lib
	
	@mkdir tmp

	@tar -zcf tmp/drivers.tar.gz bin/ lib/

	@touch tmp/threepointzero

	@rm -rf bin lib

bin:
	@mkdir bin
	@cp -aR /sbin/mke2fs /sbin/sfdisk /sbin/insmod /sbin/modprobe /sbin/rmmod bin
	@cp -aR /build/target/install bin/install
	@strip bin/*

lib:
	@(tar -cvf - -C /build/buildroot/kernel-runtime \
	/lib/modules/$(KERNEL_VER)-$(KERNEL_PL)/kernel/drivers/scsi \
	/lib/modules/$(KERNEL_VER)-$(KERNEL_PL)/kernel/drivers/usb \
	/lib/modules/$(KERNEL_VER)-$(KERNEL_PL)/kernel/lib \
	/lib/modules/$(KERNEL_VER)-$(KERNEL_PL)/modules.dep \
	| \
	tar -xvf -)

clean:
	@rm -rf lib bin tmp floppy
