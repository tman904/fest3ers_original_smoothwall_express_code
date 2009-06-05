# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = binutils
VERSION = 2.17

BASE_URL = http://ftp.gnu.org/gnu/binutils

COMPILE_DIR = $(DIR)-compile

PATCH_FILE1 = binutils_2.15-6.diff.gz

SPEC=/tools/lib/gcc-lib/*/*/specs

ifeq ($(BUILDENV), 1)
PRE_CONFIGURE = CC="gcc -B/usr/bin"

CONFIG_OPTS = --disable-nls --disable-werror

COMPILE = yes
INSTALL = yes

compile: configure
	@make -C $(COMPILE_DIR) configure-host
	@make -C $(COMPILE_DIR) LDFLAGS="-all-static"

install: compile
	@mkdir -p /tools/lib
ifdef BITS_64
	@(cd /tools; ln -s lib lib64)
endif
	@make -C $(COMPILE_DIR) install
	@make -C $(COMPILE_DIR)/ld clean
	@make -C $(COMPILE_DIR)/ld LDFLAGS="-all-static" LIB_PATH=/tools/lib

adjust:
	@make -C $(COMPILE_DIR)/ld DISTDIR=$(PKG_ROOT) install
ifeq ($(ARCH), x86_64)
	@sed -e 's@ /lib64/ld-linux-x86-64.so.2@ /tools/lib64/ld-linux-x86-64.so.2@g' \
		$(SPEC) > tempspec
	@mv -f tempspec $(SPEC)
endif
	@sed -e 's@ /lib/ld-linux.so.2@ /tools/lib/ld-linux.so.2@g' \
		$(SPEC) > tempspec
	@mv -f tempspec $(SPEC)
	@rm -f tempspec
	@rm -f /tools/lib/gcc-lib/*/*/include/{pthread.h,bits/sigthread.h}
endif

ifeq ($(BUILDENV), 2)
PRE_CONFIGURE = INSTALL=/tools/bin/install

CONFIG_OPTS = --disable-nls --enable-shared --with-lib-path=/$(TOOLS_DIR)/lib

INSTALL = yes

install: compile
	@make -C $(COMPILE_DIR) install

adjust:
	@make -C $(COMPILE_DIR)/ld clean
	@make -C $(COMPILE_DIR)/ld LIB_PATH=/usr/lib:/lib
endif

ifndef BUILDENV
CONFIG_OPTS = --enable-shared

COMPILE = yes
INSTALL = yes

compile: configure
	@make -C $(COMPILE_DIR) tooldir=$(PKG_ROOT)/$(PKG_DIR)
	
install: compile
	@mkdir -p $(PKG_ROOT)/$(PKG_DIR)/include
	@make -C $(COMPILE_DIR) DESTDIR=$(PKG_ROOT) install
	@cp $(DIR)/include/libiberty.h $(PKG_ROOT)/$(PKG_DIR)/include

adjust:
ifeq ($(ARCH), x86_64)
	@sed -e 's@ /tools/lib64/ld-linux-x86-64.so.2@ /lib64/ld-linux-x86-64.so.2@g' \
		$(SPEC) > tempspec
	@mv -f tempspec $(SPEC)
endif
	@sed -e 's@ /tools/lib/ld-linux.so.2@ /lib/ld-linux.so.2@g' \
		$(SPEC) > tempspec
	@mv -f tempspec $(SPEC)
	@rm -f tempspec
	@make -C $(COMPILE_DIR)/ld INSTALL=/$(TOOLS_DIR)/bin/install install
endif

include ../Makefile.rules
