include ../Makefile.conf

PACKAGE = nasm
VERSION = 0.98.37

BASE_URL = http://heanet.dl.sourceforge.net/sourceforge/nasm

INSTALL = yes

install: compile
	@mkdir -p $(PKG_ROOT)/$(PKG_DIR)/bin $(PKG_ROOT)/$(PKG_DIR)/man/man1
	@make -C $(COMPILE_DIR) INSTALLROOT=$(PKG_ROOT) install

include ../Makefile.rules
