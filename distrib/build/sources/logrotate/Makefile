include ../Makefile.conf

PACKAGE = logrotate
VERSION = 3.7

BASE_URL = http://ftp.debian.org/debian/pool/main/l/logrotate

DIR = $(PACKAGE)-$(VERSION)
TARBALL = $(PACKAGE)_$(VERSION).orig

PATCH_FILE1 = logrotate_3.7-2.diff.gz

CONFIGURE = yes
INSTALL = yes

configure: patch
	@true;

install: compile
	@make -C $(DIR) PREFIX=$(PKG_ROOT) install

include ../Makefile.rules
