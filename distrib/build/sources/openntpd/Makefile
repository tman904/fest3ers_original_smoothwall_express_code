include ../Makefile.conf

PACKAGE = openntpd
VERSION = 20040824p

BASE_URL = http://www.openntpd.org/dist/portable

CONFIG_OPTS = --with-ssl-dir=/usr/ssl

PATCH_FILE1 = openntpd-username.patch
PATCH_FILE2 = openntpd-pidfile.patch

INSTALL = yes

install: compile
	@install -D $(COMPILE_DIR)/ntpd $(PKG_ROOT)/$(PKG_DIR)/sbin/ntpd

include ../Makefile.rules
