include ../Makefile.conf

PACKAGE = bash
VERSION = 2.05b

BASE_URL = ftp://ftp.gnu.org/gnu/bash/

PATCH_FILE1 = bash-2.05b-2.patch

CONFIG_OPTS = --build=i686-pc-linux-gnu

ifndef BUILDENV
CONFIG_OPTS = --bindir=/bin
endif

ifeq ($(BUILDENV), 1)
INSTALL = yes

install: compile
	@make -C $(DIR) DESTDIR=$(PKG_ROOT) install
	@(cd $(PKG_ROOT)/$(PKG_DIR)/bin; ln -s bash sh);
endif

ifndef BUILDENV
INSTALL = yes

install: compile
	@make -C $(DIR) DESTDIR=$(PKG_ROOT) install
	@(cd $(PKG_ROOT)/bin; ln -s bash sh);
endif

include ../Makefile.rules
