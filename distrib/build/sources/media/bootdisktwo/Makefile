include ../../Makefile.versions
include ../../Makefile

bootdisktwo.img: bin lib
	
	@mkdir tmp

	@tar -zcf tmp/drivers.tar.gz bin/ lib/

	@touch tmp/threepointzero

	@dd if=/dev/zero of=../cdrom/images/$(BASENAME)-bootdisktwo.img bs=1k count=1440
	@/sbin/mkfs.ext2 -F ../cdrom/images/$(BASENAME)-bootdisktwo.img

	@/sbin/losetup /dev/loop0 ../cdrom/images/$(BASENAME)-bootdisktwo.img

	@mkdir floppy
	@mount /dev/loop0 floppy

	@cp -aR tmp/* floppy

	@sleep 1
	@sync

	@umount floppy
	@/sbin/losetup -d /dev/loop0

	@rmdir floppy
	@rm -rf bin lib

	@echo "$(BASENAME)-bootdisktwo.img complete"
bin:
	@mkdir bin
	@cp -aR /sbin/mke2fs /sbin/sfdisk /sbin/insmod /sbin/modprobe /sbin/rmmod bin
	@cp -aR /build/target/install bin/install
	@strip bin/*

lib:
	@cp --parents -aR /lib/modules/$(KERNEL_VER)/kernel/drivers/net .
	@cp --parents -aR /lib/modules/$(KERNEL_VER)/kernel/lib .

	@cp --parents -aR /lib/modules/$(KERNEL_VER)/modules.dep .

clean:
	@rm -rf lib bin tmp floppy
