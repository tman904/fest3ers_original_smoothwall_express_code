include ../../Makefile.versions

INITRD = initrd-$(KERNEL_VER)

default: clean
	@mkdir tmp

	@(cd tmp; \
	mkdir bin dev etc lib loopfs; \
	install -s -D /bin/sash bin/sash; \
	install -s -D /sbin/insmod.static bin/insmod; \
	install -m 755 -D ../linuxrc linuxrc; \
	cp -aR --parents \
		/dev/console /dev/null /dev/ram /dev/tty[0-4] \
	.);
	
	@dd if=/dev/zero of=$(INITRD) bs=1k count=8k
	@/sbin/mke2fs -m 0 -F $(INITRD)
	@mkdir initrd
	@/sbin/losetup /dev/loop0 $(INITRD)
	@mount /dev/loop0 initrd

	@cp -aR tmp/* initrd
	@rm -rf tmp/

	@sync
	@sleep 1

	@umount initrd
	@/sbin/losetup -d /dev/loop0

	@rm -f $(INITRD).gz
	@gzip $(INITRD)

	@rm -rf initrd
	@echo "$(INITRD) complete"
	
clean:
	@rm -rf initrd/ tmp/
	rm -f $(INITRD).gz
