# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = gcc
VERSION = 3.3.5

BASE_URL = ftp://ftp.gnu.org/gnu/gcc/gcc-$(VERSION)

COMPILE_DIR = $(DIR)-compile

PATCH_FILE1 = gcc-HAVE_LD_RO_RW_SECTION_MIXING.diff
PATCH_FILE2 = gcc-3.3_3.3.6-13.diff.gz
PATCH_FILE3 = gcc-3.3.3-no_fixincludes-1.patch

ifeq ($(BUILDENV), 1)
CONFIG_OPTS = --disable-nls --with-local-prefix=/tools \
    --disable-nls --enable-shared --enable-languages=c --disable-multilib

COMPILE = yes
INSTALL = yes

compile: configure
	@make -C $(COMPILE_DIR) BOOT_LDFLAGS="-static" bootstrap

install: compile
	@make -C $(COMPILE_DIR) DESTDIR=$(PKG_ROOT) install
	@(cd $(PKG_ROOT)/$(PKG_DIR)/bin; ln -s gcc cc);
	@(cd $(PKG_ROOT)/$(PKG_DIR)/lib; ln -s /$(PKG_DIR)/bin/cpp);
endif

ifeq ($(BUILDENV), 2)
PATCH_FILE4 = gcc-3.3.3-specs-1.patch

CONFIG_OPTS = --enable-clocale=gnu --enable-shared \
    --enable-threads=posix --enable-__cxa_atexit \
    --enable-languages=c,c++ --disable-multilib

COMPILE = yes
INSTALL = yes

compile: configure
	@make -C $(COMPILE_DIR)
#	@make -C $(COMPILE_DIR) -k check

install:  compile
	@make -C $(COMPILE_DIR) DESTDIR=$(PKG_ROOT) install
endif

ifndef BUILDENV

CONFIG_OPTS = -enable-shared --enable-threads=posix \
	--enable-__cxa_atexit --enable-clocale=gnu \
	--enable-languages=c,c++ --disable-multilib

CONFIGURE = yes
COMPILE = yes
INSTALL = yes

configure: patch
	@sed -i 's/install_to_$(INSTALL_DEST) //' $(DIR)/libiberty/Makefile.in
	@(if [ ! -e $(COMPILE_DIR) ]; then mkdir $(COMPILE_DIR); fi)
ifneq ($(DIR), $(COMPILE_DIR))
	@(cd $(COMPILE_DIR); ../$(DIR)/configure --prefix=/$(PKG_DIR) $(CONFIG_OPTS))
else
	@(cd $(COMPILE_DIR); ./configure --prefix=/$(PKG_DIR) $(CONFIG_OPTS))
endif

compile: configure
	@make -C $(COMPILE_DIR)
#	@make -C $(COMPILE_DIR) -k check

install: compile
	@make -C $(COMPILE_DIR) DESTDIR=$(PKG_ROOT) install
	@(cd $(PKG_ROOT)/$(PKG_DIR)/bin; ln -s gcc cc);
	@(cd $(PKG_ROOT)/$(PKG_DIR)/lib; ln -s /$(PKG_DIR)/bin/cpp);
endif

libgcc:
	@tar -zcvf $(TARGET_DIR)/smoothwall-libgcc.tar.gz -C $(PKG_ROOT) /$(PKG_DIR)/lib*/libgcc*

include ../Makefile.rules
