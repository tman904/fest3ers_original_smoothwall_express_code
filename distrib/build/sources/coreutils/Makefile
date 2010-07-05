# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = coreutils
VERSION = 6.7

BASE_URL = ftp://ftp.gnu.org/gnu/coreutils/

CONFIGURE = yes

configure: $(DIR)/
	@(cd $(COMPILE_DIR); \
	DEFAULT_POSIX2_VERSION=199209 ./configure --prefix=/$(PKG_DIR));

ifndef BUILDENV
INSTALL = yes

install: compile
	@make -C $(COMPILE_DIR) DESTDIR=$(PKG_ROOT) install
	@(mkdir -p $(PKG_ROOT)/bin; \
	for FILE in basename cat chgrp chmod chown cp cut date dd df echo env false link ln \
		 ls mkdir mknod mv nice pwd rm rmdir sleep sort stty sync touch true uname unlink; \
	do \
		mv $(PKG_ROOT)/$(PKG_DIR)/bin/$$FILE $(PKG_ROOT)/bin; \
	done);
	@(cd $(PKG_ROOT)/usr/bin; ln -s /bin/env)
endif
	         
include ../Makefile.rules
