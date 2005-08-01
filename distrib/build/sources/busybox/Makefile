include ../Makefile.conf

PACKAGE = busybox
VERSION = 1.00

BASE_URL = http://busybox.net/downloads/

PKG_DIR = opt/busybox

CONFIGURE = yes
INSTALL = yes

configure: $(DIR)/
	@cp -avR config $(COMPILE_DIR)/.config

install: compile
	@make -C $(COMPILE_DIR) PREFIX=$(PKG_ROOT)/$(PKG_DIR) install

include ../Makefile.rules
