include ../Makefile.conf

PACKAGE = expat
VERSION = 1.95.8
SFMIRROR = heanet
BASE_URL = http://$(SFMIRROR).dl.sourceforge.net/sourceforge/$(PACKAGE)/

INSTALL = yes

install: compile
	@make -C $(COMPILE_DIR) install prefix=$(PKG_ROOT)/$(PKG_DIR)

include ../Makefile.rules