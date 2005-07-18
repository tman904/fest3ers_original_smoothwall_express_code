include ../Makefile.conf

PACKAGE = libcap
VERSION = 1.10

BASE_URL = http://http.us.debian.org/debian/pool/main/libc/libcap/

DIR = $(PACKAGE)-$(VERSION).orig
TARBALL = $(PACKAGE)_$(VERSION).orig

PATCH_FILE1 = libcap_1.10-14.diff.gz

CONFIGURE = yes

configure: patch
	@true;

include ../Makefile.rules
