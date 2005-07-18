include ../Makefile.conf

PACKAGE = iana-etc
VERSION = 1.00

EXTENSION = .tar.bz2

BASE_URL = http://www.sethwklein.net/projects/iana-etc/downloads/

CONFIGURE = yes
INSTALL = yes

configure: $(DIR)/
	@true
	
install: compile
	@mkdir -p $(PKG_ROOT)/etc
	@make -C $(COMPILE_DIR) PREFIX=$(PKG_ROOT) install

include ../Makefile.rules
