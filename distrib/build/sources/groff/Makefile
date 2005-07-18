include ../Makefile.conf

PACKAGE = groff
VERSION = 1.19

BASE_URL = ftp://ftp.gnu.org/gnu/groff

INSTALL = yes

install: compile
	@mkdir -p $(PKG_ROOT)/$(PKG_DIR)
	@make -C $(COMPILE_DIR) prefix=$(PKG_ROOT)/$(PKG_DIR) install

include ../Makefile.rules
