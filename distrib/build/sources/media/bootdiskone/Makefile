# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

INSTALL_ROOT = installroot

include ../../Makefile.versions
include ../../Makefile

default:
ifeq ($(MEDIA), diskone)
	@dd if=/dev/zero of=../cdrom/images/$(BASENAME)-boot$(MEDIA).img bs=1k count=1440
else
	@dd if=/dev/zero of=../cdrom/images/$(BASENAME)-boot$(MEDIA).img bs=1k count=2880
endif
	@/sbin/mkfs.msdos -f 1 ../cdrom/images/$(BASENAME)-boot$(MEDIA).img

	@mkdir floppy

	@/sbin/losetup /dev/loop0 ../cdrom/images/$(BASENAME)-boot$(MEDIA).img
	@mount /dev/loop0 floppy/

	@cp -R syslinux.cfg floppy

	@cp -R dosfiles/message.txt dosfiles/message.lss floppy

	@cp -R /boot/vmlinuz-$(KERNEL_VER) floppy/vmlinuz
	@make -C ../installroot MEDIA=$(MEDIA)
	@cp -R ../$(INSTALL_ROOT)image.gz floppy/initrd.img

	@sleep 1
	@sync

	@umount floppy
	@/sbin/losetup -d /dev/loop0

	@rm -rf floppy

	@syslinux ../cdrom/images/$(BASENAME)-boot$(MEDIA).img
	@echo "$(BASENAME)-boot$(MEDIA).img build complete"

clean:
	@rm -rf ../cdrom/images/$(BASENAME)-boot$(MEDIA).img floppy
	@make -C ../installroot clean
