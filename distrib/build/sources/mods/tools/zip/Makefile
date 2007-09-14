include ../../../Makefile.conf

PACKAGE = zip
VERSION = 232

BASE_URL = http://www.mirrorservice.org/sites/ftp.info-zip.org/pub/infozip/src/

TARBALL = $(PACKAGE)$(VERSION)

DIR = $(PACKAGE)-2.32

EXTENSION = .tgz

CONFIGURE = yes
COMPILE = yes
INSTALL = yes

configure: patch
	@true

compile: configure
	@make -C $(DIR) -f unix/Makefile CC="gcc $(CFLAGS)" generic

install: compile
	@make -C $(DIR) -f unix/Makefile prefix=$(PKG_ROOT)/$(PKG_DIR) install

include ../../../Makefile.rules
