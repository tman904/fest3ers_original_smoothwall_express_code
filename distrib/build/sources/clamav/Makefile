include ../Makefile.conf

PACKAGE = clamav
VERSION = 0.95.1

BASE_URL = http://mesh.dl.sourceforge.net/sourceforge/clamav/

CONFIG_OPTS = --sysconfdir=/usr/lib/smoothwall --with-dbdir=/var/clamav --disable-clamav

PATCH_FILE1 = clamav-pidperms.patch

INSTALL = yes

install: compile
	-mkdir $(PKG_ROOT)
	@make -C $(COMPILE_DIR) DESTDIR=$(PKG_ROOT) install
	@chown -R 105:105 $(PKG_ROOT)/var/clamav

include ../Makefile.rules
