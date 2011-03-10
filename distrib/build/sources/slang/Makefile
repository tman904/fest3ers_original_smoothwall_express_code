include ../Makefile.conf

PACKAGE = slang
VERSION = 2.2.3

LICENCE_FILE = $(DIR)/COPYING

BASE_URL = ftp://space.mit.edu/pub/davis/slang/v2.2/

NO_PARA = yes

PATCH_FILE1 = WCONTINUED-fixup.patch

INSTALL = yes

install: compile
	@mkdir $(PKG_ROOT)
	@make -C $(COMPILE_DIR) DESTDIR=$(PKG_ROOT) install
	@rm -f $(PKG_ROOT)/$(PKG_DIR)/lib/libsnewt*.so*

include ../Makefile.rules
