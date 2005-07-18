include ../Makefile.conf

PACKAGE = cdrtools
VERSION = 2.00.3

BASE_URL = ftp://ftp.berlios.de/pub/cdrecord/

CONFIGURE = yes
COMPILE = yes
INSTALL = yes

configure: $(DIR)/
	@true

compile: configure
	@make -C $(COMPILE_DIR)

install: compile
	@install -D $(COMPILE_DIR)/mkisofs/OBJ/*/mkisofs $(PKG_ROOT)/sbin/mkisofs

include ../Makefile.rules
