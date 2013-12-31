# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

OPENSSL_VER = 1.0.1e

PACKAGE = openssl
VERSION = $(OPENSSL_VER)

BASE_URL = http://www.openssl.org/source/

# If building for 486, generate only 386 code. Otherwise, building
#   'modern' code should be OK.
ifeq ($(mARCH),i486)
ONLY386 = 386
endif

CONFIGURE = yes
COMPILE = yes
INSTALL = yes
CLEAN = yes

configure: $(DIR)/
	sed -i -e '/^  \*86-\*-linux2/i \
  FUBAR\
\toptions="$$options $(CFLAGS)";;' $(DIR)/config
	sed -i -e '/^  \*86-\*-linux2/,+11d' $(DIR)/config
	sed -i -e 's/  FUBAR$$/  *86-*-linux2) OUT="linux-elf"/' $(DIR)/config
	@(cd $(DIR); \
	./config shared --prefix=$(PKG_DIR) --openssldir=/$(PKG_DIR)/lib/ssl $(ONLY386); \
	patch < ../Makefile-MANDIR.patch);

compile: configure
	@$(MAKE) -C $(PACKAGE)-$(VERSION)

install: compile
	@mkdir -p $(PKG_ROOT)
	@make -C $(PACKAGE)-$(OPENSSL_VER) INSTALL_PREFIX=$(PKG_ROOT) install
	@./mk-ca-bundle.pl $(PKG_ROOT)/$(OPENSSLDIR)/certs/ca-certificates.crt

clean:
	@echo -n " $(PACKAGE)"
	@rm -rf $(DIR)
	@rm -rf $(COMPILE_DIR)
	@rm -f certdata.txt
ifeq ($(BUILD_PHASE), Final)
	@rm -rf $(PKG_ROOT); mkdir $(PKG_ROOT)
	@rm -f $(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz
endif

include ../Makefile.rules
