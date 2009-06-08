include ../Makefile.conf

PACKAGE = binutils
VERSION = 2.17.20070103cvs

BASE_URL = http://archive.ubuntu.com/ubuntu/pool/main/b/binutils/

TARBALL = $(PACKAGE)_$(VERSION).orig

DIR = $(PACKAGE)-$(VERSION).orig

COMPILE_DIR = $(DIR)-compile

SPEC=/tools/lib/gcc-lib/*/*/specs

ifeq ($(BUILDENV), 1)
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
CONFIG_OPTS = --disable-nls --enable-shared --with-lib-path=/$(TOOLS_DIR)/lib

CONFIGURE = yes
INSTALL = yes

configure: patch
	@(if [ ! -e $(COMPILE_DIR) ]; then mkdir $(COMPILE_DIR); fi)
ifneq ($(DIR), $(COMPILE_DIR))
	@(cd $(COMPILE_DIR); INSTALL=/tools/bin/install ../$(DIR)/configure --prefix=/$(PKG_DIR) $(CONFIG_OPTS))
else
	@(cd $(COMPILE_DIR); INSTALL=/tools/bin/install ./configure --prefix=/$(PKG_DIR) $(CONFIG_OPTS))
endif

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
CONFIGURE = yes

configure: patch
	@(if [ ! -e $(COMPILE_DIR) ]; then mkdir $(COMPILE_DIR); fi)
ifneq ($(DIR), $(COMPILE_DIR))
	@(cd $(COMPILE_DIR); INSTALL=/tools/bin/install ../$(DIR)/configure --prefix=/$(PKG_DIR) $(CONFIG_OPTS))
else
	@(cd $(COMPILE_DIR); INSTALL=/tools/bin/install ./configure --prefix=/$(PKG_DIR) $(CONFIG_OPTS))
endif


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
