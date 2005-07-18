include ../Makefile.conf

PACKAGE = hdparm
VERSION = 5.6

BASE_URL = http://www.ibiblio.org/pub/Linux/system/hardware/

CONFIGURE = yes
INSTALL = yes

configure: patch
	@true

install: compile
	@mkdir -p $(PKG_ROOT)/sbin
	@make -C $(COMPILE_DIR) DESTDIR=$(PKG_ROOT) install

include ../Makefile.rules
