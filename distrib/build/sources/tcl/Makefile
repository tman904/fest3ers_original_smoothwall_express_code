include ../Makefile.conf

PACKAGE = tcl
VERSION = 8.4.6

BASE_URL = http://aleron.dl.sourceforge.net/sourceforge/tcl/

TARBALL = $(PACKAGE)$(VERSION)-src

DIR = $(PACKAGE)$(VERSION)

CONFIGURE = yes
COMPILE = yes
INSTALL = yes

configure: $(DIR)/
	@(cd $(DIR)/unix; ./configure --prefix=/$(PKG_DIR) $(CONFIG_OPTS))

compile: configure
	@make -C $(DIR)/unix

install: compile
	@make -C $(DIR)/unix INSTALL_ROOT=$(PKG_ROOT) install
	@ln -s tclsh8.4 $(PKG_ROOT)/$(PKG_DIR)/bin/tclsh

include ../Makefile.rules
