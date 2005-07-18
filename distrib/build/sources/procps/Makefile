include ../Makefile.conf

PACKAGE = procps
VERSION = 3.2.1

BASE_URL = http://procps.sourceforge.net/

CONFIGURE = yes
INSTALL = yes

configure: $(DIR)/
	@true

install: compile
	@make -C $(COMPILE_DIR) DESTDIR=$(PKG_ROOT) install
	@rm -f $(PKG_ROOT)/lib/libproc.so
		
include ../Makefile.rules
