include ../Makefile.conf

PACKAGE = lilo
VERSION = 22.6.1

BASE_URL = http://home.san.rr.com/johninsd/pub/linux/lilo/

TARBALL = $(PACKAGE)-$(VERSION).src

DIR = $(PACKAGE)-$(VERSION)

CONFIGURE = yes
INSTALL = yes

configure: $(DIR)/
	 true

install: compile
	@mkdir -p $(PKG_ROOT)/$(PKG_DIR)/sbin
	@make -C $(COMPILE_DIR) ROOT=$(PKG_ROOT) install
	@cp $(COMPILE_DIR)/{bitmap.b,bootsect.b} $(PKG_ROOT)/boot

include ../Makefile.rules
