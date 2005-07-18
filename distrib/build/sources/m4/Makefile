include ../Makefile.conf

PACKAGE = m4
VERSION = 1.4

BASE_URL = ftp://ftp.gnu.org/gnu/m4

INSTALL = yes

install: compile
	@make -C $(COMPILE_DIR) prefix=$(PKG_ROOT)/$(PKG_DIR) install

include ../Makefile.rules
