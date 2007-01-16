# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../../Makefile

PROGS = bootdiskprogs
INSTALL_ROOT = installroot
BB = /opt/busybox

default: clean
	@make -C $(PROGS)

	@mkdir tmp

	@(cd tmp; \
	mkdir bin bootdisktwo cdrom dev etc harddisk lib proc tmp usr; \
	ln -s bin sbin; \
	install -D /usr/share/terminfo/l/linux usr/share/terminfo/l/linux; \
	cp -aR $(BB)/bin/busybox bin; \
	cd bin; \
	for FILE in \
		ash cat chroot echo ifconfig init \
		kill killall linuxrc mkswap mount reboot \
		sh sleep swapoff swapon tar test umount wget; \
	do \
		ln -s busybox $$FILE; \
	done; \
	cd ..; \
	cp -aR ../$(PROGS)/loader  ../$(PROGS)/iowrap bin; \
	cp -aR /lib/ld-*.so /lib/ld-*.so.* /lib/libc-*.so /lib/libc.so.* lib; \
ifdef BITS_64
	ln -s lib lib64; \
endif
	cp -aR ../etc/fstab etc; \
	cp -aR ../etc/group etc; \
	cp -aR ../etc/inittab etc; \
	cp -aR ../etc/mtab etc; \
	cp -aR ../etc/passwd etc; \
	cp -aR ../etc/shells etc; \
	cp -aR ../etc/termcap etc; \
	cp -aR ../etc/rc etc; chmod 755 etc/rc; \
	cp -aR ../etc/halt etc; chmod 755 etc/halt; \
	cp -aR ../etc/modules.conf etc; \
	cp -aR ../etc/storagedevices etc; \
	touch etc/ld.so.conf; \
	/sbin/ldconfig -r .; \
	strip bin/busybox bin/loader bin/iowrap lib/*; \
	mkdir dev/ida dev/rd; \
	cp -aR --parents \
		/dev/console /dev/fd0 /dev/fd0H1440 /dev/tty[1-6] \
		/dev/hd[a-h] /dev/hd[a-h][1-4] /dev/sda /dev/sda[1-4] /dev/scd0 \
		/dev/{ida,rd,cciss}/c0d0 /dev/{ida,rd,cciss}/c0d0p[1-4] \
		/dev/kmem /dev/mem /dev/null \
	.);

ifeq ($(MEDIA), cdrom)
	@touch tmp/cdrominstall
	@cp -aR ../bootdisktwo/tmp/* tmp/bootdisktwo
endif

	@dd if=/dev/zero of=../$(INSTALL_ROOT)image bs=1k count=8k
	@/sbin/mke2fs -m 0 -F ../$(INSTALL_ROOT)image
	@mkdir $(INSTALL_ROOT)
	@/sbin/losetup /dev/loop1 ../$(INSTALL_ROOT)image
	@mount /dev/loop1 $(INSTALL_ROOT)

	@cp -aR tmp/* $(INSTALL_ROOT)
	@rm -rf tmp/

	@sync
	@sleep 1

	@umount $(INSTALL_ROOT)
	@/sbin/losetup -d /dev/loop1

	@rm -f ../$(INSTALL_ROOT)image.gz
	@gzip ../$(INSTALL_ROOT)image

	@rm -rf installroot/
	@echo "installroot build for $(MEDIA) complete"
	
clean:
	@make -C $(PROGS) clean
	@rm -rf $(INSTALL_ROOT) tmp/
	rm -f ../$(INSTALL_ROOT)image.gz
