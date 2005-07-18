include ../Makefile.conf

PACKAGE = binutils
VERSION = 2.15

BASE_URL = ftp://ftp.gnu.org/gnu/binutils/

COMPILE_DIR = $(DIR)-compile

SPEC=/tools/lib/gcc-lib/*/*/specs

ifeq ($(BUILDENV), 1)
CONFIG_OPTS = --disable-nls

COMPILE = yes

compile: configure
	@make -C $(COMPILE_DIR) configure-host
	@make -C $(COMPILE_DIR) LDFLAGS="-all-static"

adjust:
	@make -C $(COMPILE_DIR)/ld DISTDIR=$(PKG_ROOT) install
	@sed -e 's@ /lib/ld-linux.so.2@ /tools/lib/ld-linux.so.2@g' \
		$(SPEC) > tempspec
	@mv -f tempspec $(SPEC)
	@rm -f tempspec
	@rm -f /tools/lib/gcc-lib/*/*/include/{pthread.h,bits/sigthread.h}
endif

ifeq ($(BUILDENV), 2)
CONFIG_OPTS = --enable-shared --with-lib-path=/$(TOOLS_DIR)/lib

adjust:
	@make -C $(COMPILE_DIR)/ld clean
	@make -C $(COMPILE_DIR)/ld LIB_PATH=/usr/lib:/lib
endif

ifndef BUILDENV
COINFIG_OPTS = --enable-shared

COMPILE = yes
INSTALL = yes

compile: configure
	@make -C $(COMPILE_DIR) tooldir=$(PKG_ROOT)/$(PKG_DIR)
	
install: compile
	@mkdir -p $(PKG_ROOT)/$(PKG_DIR)/include
	@make -C $(COMPILE_DIR) tooldir=$(PKG_ROOT)/$(PKG_DIR) install
	@cp $(DIR)/include/libiberty.h $(PKG_ROOT)/$(PKG_DIR)/include

adjust:
	@make -C $(COMPILE_DIR)/ld INSTALL=/$(TOOLS_DIR)/bin/install install
	@sed -e 's@ /tools/lib/ld-linux.so.2@ /lib/ld-linux.so.2@g' \
		$(SPEC) > tempspec
	@mv -f tempspec $(SPEC)
	@rm -f tempspec
endif

include ../Makefile.rules
