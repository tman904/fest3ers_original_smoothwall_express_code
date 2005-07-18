include ../Makefile.conf

PACKAGE = sysklogd
VERSION = 1.4.1

BASE_URL = http://www.infodrom.org/projects/sysklogd/download/

PATCH_FILE1 = sysklogd-1.4.1-security.patch

CONFIGURE = yes
COMPILE = yes
INSTALL = yes

configure: patch
	@true

compile: configure
	@make -C $(DIR) CFLAGS="$(CFLAGS) -DSYSV"

install: compile
	@mkdir -p $(PKG_ROOT)/$(PKG_DIR)/man/man{5,8} $(PKG_ROOT)/$(PKG_DIR)/sbin
	@make -C $(COMPILE_DIR) MANDIR=$(PKG_ROOT)/$(PKG_DIR)/man \
		BINDIR=$(PKG_ROOT)/$(PKG_DIR)/sbin install

include ../Makefile.rules
