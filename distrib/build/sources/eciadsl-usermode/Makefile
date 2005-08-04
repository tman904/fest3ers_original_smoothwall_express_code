include ../Makefile.conf

PACKAGE = eciadsl-usermode
VERSION = 0.9

BASE_URL = http://eciadsl.flashtux.org/download/

CONFIG_OPTS = 

INSTALL = yes

install: compile
	@mkdir -p $(PKG_ROOT)/$(PKG_DIR)/bin;
	@mkdir -p $(PKG_ROOT)/etc/eciadsl
	@(cd $(DIR); \
	install -s -D pppoeci eci-load1 eci-load2 $(PKG_ROOT)/$(PKG_DIR)/bin; \
	install -D *.bin $(PKG_ROOT)/etc/eciadsl)
		
include ../Makefile.rules
