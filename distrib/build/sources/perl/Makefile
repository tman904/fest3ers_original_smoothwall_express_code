include ../Makefile.conf

PACKAGE = perl
VERSION = 5.8.4

BASE_URL = http://ftp.funet.fi/pub/CPAN/src/

CONFIGURE = yes

configure: patch
	@(cd $(COMPILE_DIR); \
	./configure.gnu --prefix=/$(PKG_DIR) -Dpager="/bin/less -isR");

include ../Makefile.rules
