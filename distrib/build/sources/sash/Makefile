include ../Makefile.conf

PACKAGE = sash
VERSION = 3.4

BASE_URL = http://www.canb.auug.org.au/~dbell/programs/

PATCH_FILE1 = sash-3.4-scriptarg.patch

CONFIGURE = yes
INSTALL = yes

configure: patch
	@true

install: compile
	@install -D $(COMPILE_DIR)/sash $(PKG_ROOT)/bin/sash

include ../Makefile.rules
