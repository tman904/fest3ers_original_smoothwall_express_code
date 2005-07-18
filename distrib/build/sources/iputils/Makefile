include ../Makefile.conf

PACKAGE = iputils
VERSION = 20020927

BASE_URL = http://ftp.debian.org/debian/pool/main/i/iputils/

DIR = $(PACKAGE)
TARBALL = $(PACKAGE)_$(VERSION).orig

PATCH_FILE1 = iputils_20020927-2.diff.gz

CONFIGURE = yes
INSTALL = yes

configure: patch
	@true;

install: compile
	-mkdir $(PKG_ROOT)
	@install -m 4755 -D $(DIR)/ping $(PKG_ROOT)/$(PKG_DIR)/bin/ping

include ../Makefile.rules
