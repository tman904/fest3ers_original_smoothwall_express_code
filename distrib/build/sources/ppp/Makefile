# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = ppp
VERSION = 2.4.2

BASE_URL = ftp://ftp.samba.org/pub/ppp/

PATCH_FILE1 = ppp-2.4.2-pppoatm.patch
PATCH_FILE2 = ppp-2.4.2-pppoatm-persist.patch
PATCH_FILE3 = ppp-2.4.2-signal.patch

CONFIGURE = yes
COMPILE = yes
INSTALL = yes

COMPILE_FLAGS = -DHAVE_PATHS_H -DIPX_CHANGE -DHAVE_MMAP -D_PATH_VARRUN=\\\"/var/run\\\"

configure: patch
	@(cd $(DIR); ./configure)

compile: configure
	@make -C $(DIR) DESTDIR=$(MODULE_DIR) COMPILE_FLAGS="$(COMPILE_FLAGS)"

install: compile
	-mkdir $(PKG_ROOT)
	@make -C $(COMPILE_DIR) DESTDIR=$(PKG_ROOT)/$(MODULE_DIR) install
	@rm -f $(PKG_ROOT)/etc/ppp/chap-secrets
	@rm -f $(PKG_ROOT)/etc/ppp/pap-secrets
	
include ../Makefile.rules
