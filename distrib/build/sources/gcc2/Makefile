include ../Makefile.conf

PACKAGE = gcc
#VERSION = 2.95.3
VERSION = 3.2.3

BASE_URL = ftp://ftp.gnu.org/gnu/gcc

COMPILE_DIR = $(DIR)-compile

PKG_DIR = opt/$(PACKAGE)-$(VERSION)

PKG_ROOT = $(ROOT)/build/buildroot/$(PACKAGE)2

#PATCH_URLS = http://linuxfromscratch.mirror.ac.uk/sites/www.linuxfromscratch.org/patches/lfs/5.0/gcc-2.95.3-2.patch \
#	http://linuxfromscratch.mirror.ac.uk/sites/www.linuxfromscratch.org/patches/lfs/5.0/gcc-2.95.3-no-fixinc.patch \
#	http://linuxfromscratch.mirror.ac.uk/sites/www.linuxfromscratch.org/patches/lfs/5.0/gcc-2.95.3-returntype-fix.patch

CONFIG_OPTS = -enable-shared --enable-languages=c \
    --enable-threads=posix

CONFIGURE = ues
COMPILE = yes
INSTALL = yes

configure: patch
	@echo timestamp > $(DIR)/gcc/cstamp-h.in
	@(if [ ! -e $(COMPILE_DIR) ]; then mkdir $(COMPILE_DIR); fi)
ifneq ($(DIR), $(COMPILE_DIR))
	@(cd $(COMPILE_DIR); ../$(DIR)/configure --prefix=/$(PKG_DIR) $(CONFIG_OPTS))
else
	@(cd $(COMPILE_DIR); ./configure --prefix=/$(PKG_DIR) $(CONFIG_OPTS))
endif

compile: configure
	@make -C $(COMPILE_DIR) bootstrap

install: compile
	@make -C $(COMPILE_DIR) prefix=$(PKG_ROOT)/$(PKG_DIR) install

include ../Makefile.rules
