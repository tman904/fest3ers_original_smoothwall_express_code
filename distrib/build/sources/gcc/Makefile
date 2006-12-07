# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = gcc
VERSION = 3.3.2

BASE_URL = ftp://ftp.gnu.org/gnu/gcc

COMPILE_DIR = $(DIR)-compile

ifeq ($(BUILDENV), 1)
PATCH_FILE1 = configure_trap.patch
CONFIG_OPTS = --disable-nls --with-local-prefix=/tools \
    --disable-nls --enable-shared --enable-languages=c

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
PATCH_FILE1 = gcc-3.3.3-no_fixincludes-1.patch
PATCH_FILE2 = gcc-3.3.3-specs-1.patch

CONFIG_OPTS = --enable-clocale=gnu --enable-shared \
    --enable-threads=posix --enable-__cxa_atexit \
    --enable-languages=c,c++

COMPILE = yes
INSTALL = yes

compile: configure
	@make -C $(COMPILE_DIR)
#	@make -C $(COMPILE_DIR) -k check

install:  compile
	@make -C $(COMPILE_DIR) DESTDIR=$(PKG_ROOT) install
endif

ifndef BUILDENV
PATCH_FILE1 = gcc-3.3.3-no_fixincludes-1.patch

CONFIG_OPTS = -enable-shared --enable-threads=posix \
	--enable-__cxa_atexit --enable-clocale=gnu \
	--enable-languages=c,c++

CONFIGURE = ues
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
	@tar -zcvf $(TARGET_DIR)/smoothwall-libgcc.tar.gz -C $(PKG_ROOT) /$(PKG_DIR)/lib/libgcc*

include ../Makefile.rules
