include ../Makefile.conf

PACKAGE = pciutils
VERSION = 2.1.11

BASE_URL = ftp://ftp.kernel.org/pub/software/utils/pciutils/

CONFIGURE = yes
COMPILE = yes
INSTALL = yes

configure: $(DIR)/
	@true

compile: configure
	@make -C $(COMPILE_DIR) PREFIX=/$(PKG_DIR)

install: compile
	@make -C $(COMPILE_DIR) PREFIX=$(PKG_ROOT)/$(PKG_DIR) install

include ../Makefile.rules
