include ../Makefile.conf

PACKAGE = mtools
VERSION = 3.9.9

BASE_URL = http://mtools.linux.lu/

INSTALL = yes

install: compile
	@make -C $(COMPILE_DIR) prefix=$(PKG_ROOT)/$(PKG_DIR) install

include ../Makefile.rules
