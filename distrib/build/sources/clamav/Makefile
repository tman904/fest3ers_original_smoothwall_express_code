include ../Makefile.conf

PACKAGE = clamav
VERSION = 0.88.7

BASE_URL = http://heanet.dl.sourceforge.net/sourceforge/clamav/

CONFIG_OPTS = -sysconfdir=/etc --with-dbdir=/var/clamav --disable-clamav

PATCH_FILE1 = openlog.patch
PATCH_FILE2 = clamav-pidperms.patch

INSTALL = yes

install: compile
	-mkdir $(PKG_ROOT)
	@make -C $(COMPILE_DIR) DESTDIR=$(PKG_ROOT) install
	@chown -R nobody:nobody $(PKG_ROOT)/var/clamav

include ../Makefile.rules
