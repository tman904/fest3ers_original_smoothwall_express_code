include ../Makefile.conf

PACKAGE = mktemp
VERSION = 1.5

BASE_URL = ftp://ftp.mktemp.org/pub/mktemp

INSTALL = yes

install: compile
	@make -C $(COMPILE_DIR) prefix=$(PKG_ROOT)/$(PKG_DIR) install

include ../Makefile.rules
