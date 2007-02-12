# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = glibc
VERSION = 2.3.2

EXTENSION = .tar.bz2

BASE_URL = ftp://ftp.gnu.org/gnu/glibc

PATCH_FILE1 = generic-sscanf.diff
PATCH_FILE2 = glibc_2.3.2.ds1-22sarge4.diff.gz

COMPILE_DIR = $(DIR)-compile

ifeq ($(BUILDENV), 1)
CONFIG_OPTS = --disable-profile --enable-add-ons=linuxthreads \
    --with-binutils=/tools/bin --with-headers=/tools/include \
    --without-gd --without-cvs
else
CONFIG_OPTS = --disable-profile --enable-add-ons=linuxthreads \
    --libexecdir=/usr/lib --with-headers=/usr/include \
    --without-cvs
endif

DOWNLOAD = yes
PREPARE = yes
INSTALL = yes
BUILDTARBALL = yes

download:
	$(DL_CMD) $(BASE_URL)/glibc-$(VERSION)$(EXTENSION)
	$(DL_CMD) $(BASE_URL)/glibc-linuxthreads-$(VERSION)$(EXTENSION)

$(DIR)/: download
	tar -jxvf $(DOWNLOADS_DIR)/$(DIR)$(EXTENSION)
	tar -jxvf $(DOWNLOADS_DIR)/glibc-linuxthreads-$(VERSION)$(EXTENSION) -C $(DIR)

install: compile
ifndef BUILDENV
	@mkdir -p $(PKG_ROOT)/lib
	@mkdir -p $(PKG_ROOT)/usr/lib

ifdef BITS_64
	@(cd $(PKG_ROOT); ln -s lib lib64)
	@(cd $(PKG_ROOT)/usr; ln -s lib lib64)
endif
endif
	make -C $(COMPILE_DIR) install_root=$(PKG_ROOT) install

$(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz: install
	@tar -zcvf $(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz -C $(PKG_ROOT) .
	@tar -zxvf $(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz -C / --exclude ./etc/localtime

include ../Makefile.rules
