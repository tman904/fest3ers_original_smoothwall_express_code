include ../Makefile.conf

PACKAGE = bzip2
VERSION = 1.0.2

BASE_URL = ftp://sources.redhat.com/pub/bzip2/v102/

CONFIGURE = yes
INSTALL = yes

configure : $(DIR)/
	@true

install : compile
	@make -C $(DIR) PREFIX=$(PKG_ROOT)/$(PKG_DIR) install

include ../Makefile.rules

