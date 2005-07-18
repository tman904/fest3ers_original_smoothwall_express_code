include ../Makefile.conf

PACKAGE = iproute2
VERSION = 2.4.7-now-ss020116-try

BASE_URL = http://ftp.iasi.roedu.net/mirrors/ftp.inr.ac.ru/ip-routing/

PATCH_FILE1 = iproute2-2.4.7-htb3-tc.patch
PATCH_FILE2 = iproute2-2.4.7-db.patch
PATCH_FILE3 = iproute2-2.4.7-nomisc.patch

DIR = iproute2

CONFIGURE = yes
COMPILE = yes
INSTALL = yes

configure: patch
	@true

compile: configure
	@make -C $(COMPILE_DIR) KERNEL_INCLUDE=/usr/include

install: compile
	@mkdir -p $(PKG_ROOT)/sbin
	@install -D $(COMPILE_DIR)/ip/ip $(PKG_ROOT)/sbin/ip
	@install -D $(COMPILE_DIR)/tc/tc $(PKG_ROOT)/sbin/tc

include ../Makefile.rules
