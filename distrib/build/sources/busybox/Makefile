include ../Makefile.conf

PACKAGE = busybox
VERSION = 0.60.5

BASE_URL = http://busybox.net/downloads/

PKG_DIR = opt/busybox

CONFIGURE = yes
INSTALL = yes

configure: $(DIR)/
	@cp -avR Config.h $(COMPILE_DIR)

install: compile
	@make -C $(COMPILE_DIR) PREFIX=$(PKG_ROOT)/$(PKG_DIR) install

include ../Makefile.rules
