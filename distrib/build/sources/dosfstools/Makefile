include ../Makefile.conf

PACKAGE = dosfstools
VERSION = 2.11

BASE_URL = ftp://ftp.uni-erlangen.de/pub/Linux/LOCAL/dosfstools/

TARBALL = $(PACKAGE)-$(VERSION).src

DIR = $(PACKAGE)-$(VERSION)

CONFIGURE = yes
INSTALL = yes

configure: patch
	@true

install: compile
	@make -C $(COMPILE_DIR) PREFIX=$(PKG_ROOT) install

include ../Makefile.rules
