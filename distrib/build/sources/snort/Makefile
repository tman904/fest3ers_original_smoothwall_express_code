include ../Makefile.conf

PACKAGE = snort
VERSION = 2.3.0

BASE_URL = http://www.snort.org/dl/old

PATCH_FILE1 = snort-pidfix.patch

INSTALL = yes

install: compile
	@mkdir -p $(PKG_ROOT)/var/smoothwall/snort/rules/
	@install -D $(COMPILE_DIR)/src/snort $(PKG_ROOT)/usr/bin/snort
	@install -D $(COMPILE_DIR)/rules/*.rules $(PKG_ROOT)/var/smoothwall/snort/rules/
	@install -D $(COMPILE_DIR)/etc/unicode.map $(PKG_ROOT)/var/smoothwall/snort/unicode.map
	@install -D $(COMPILE_DIR)/etc/classification.config $(PKG_ROOT)/var/smoothwall/snort/classification.config
	@install -D $(COMPILE_DIR)/etc/reference.config $(PKG_ROOT)/var/smoothwall/snort/reference.config
	
include ../Makefile.rules
