# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf
include ../Makefile.versions

PACKAGE = libipt_ACCOUNT
VERSION =  1.2

EXTENSION = .tar.gz

BASE_URL = http://www.intra2net.com/de/produkte/opensource/ipt_account/

CONFIGURE=yes

configure: patch
	@(if [ ! -e $(COMPILE_DIR) ]; then mkdir $(COMPILE_DIR); fi)
ifneq ($(DIR), $(COMPILE_DIR))
	@(cd $(COMPILE_DIR); CFLAGS="-I$(SOURCES_DIR)/kernel-runtime/linux/include" ../$(DIR)/configure --prefix=/$(PKG_DIR) $(CONFIG_OPTS))
else
	@(cd $(COMPILE_DIR); CFLAGS="-I$(SOURCES_DIR)/kernel-runtime/linux/include" ./configure --prefix=/$(PKG_DIR) $(CONFIG_OPTS))
endif

include ../Makefile.rules
