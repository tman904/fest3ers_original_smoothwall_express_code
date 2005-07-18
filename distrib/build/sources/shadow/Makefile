include ../Makefile.conf

PACKAGE = shadow
VERSION = 4.0.7

BASE_URL = ftp://ftp.pld.org.pl/software/shadow

INSTALL = yes

install: compile
	@make -C $(COMPILE_DIR) DESTDIR=$(PKG_ROOT) install
	@rm -f $(PKG_ROOT)/bin/sg $(PKG_ROOT)/bin/vigr

include ../Makefile.rules
