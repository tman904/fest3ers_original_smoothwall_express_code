# Copyright 2004-2010 SmoothWall Ltd

include ../Makefile.conf

PACKAGE = grub
VERSION = 0.97

ifeq ($(ARCH), i386)
LICENCE_FILE = $(DIR)/COPYING

BASE_URL = ftp://alpha.gnu.org/gnu/grub/

PATCH_FILE1 = cvs-sync.patch
PATCH_FILE2 = grub-special_device_names.diff
PATCH_FILE3 = raid_cciss.diff
PATCH_FILE4 = grub-ext4-patch.diff
PATCH_FILE5 = grub-0.97-gpt.diff

export LDFLAGS = -static

INSTALL = yes

install: compile
	@mkdir -p $(PKG_ROOT)
	@make -C $(DIR) DESTDIR=$(PKG_ROOT) install
	@mkdir -p $(PKG_ROOT)/boot/grub
	@cp -av $(PKG_ROOT)/usr/lib/grub/*/* $(PKG_ROOT)/boot/grub
	@touch $(PKG_ROOT)/boot/grub/default
else
BASE_URL = http://downloads.smoothwall.org/buildmirror/

TARBALL = smoothwall-$(PACKAGE)-$(VERSION)-i686

INSTALL = yes
CLEAN = yes

install: download
	$(MAKE) clean
	@mkdir $(PKG_ROOT)
	@tar -zxvf $(DOWNLOADS_DIR)/$(TARBALL)$(EXTENSION) -C $(PKG_ROOT)

clean:
	@rm -rf $(PKG_ROOT)
	
endif	

include ../Makefile.rules
