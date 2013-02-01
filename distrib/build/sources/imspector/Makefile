# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = imspector
#VERSION = 20101029
VERSION = 0.9

#BASE_URL = http://www.imspector.org/downloads/snapshots/
BASE_URL = http://www.imspector.org/downloads/

CONFIGURE = yes
COMPILE = yes
INSTALL = yes

OPTS = PREFIX=$(PKG_ROOT)$(PKG_DIR)
DIR = imspector-$(VERSION)

PATCH_FILE1 = ssl_method.patch

export ADD_PLUGINS = dbfilterplugin.so censordfilterplugin.so catsloggingplugin.so dbresponderplugin.so

configure: patch
	cd $(DIR); sed -i -e 's/LIBS = -ldl/& -lcrypto/' Makefile
	@true

compile: configure
	@$(MAKE) $(JOBS) -C $(DIR) $(OPTS)

install: compile
	@mkdir -p $(PKG_ROOT)
	@make -C $(DIR) $(OPTS) install
	@rm -f $(PKG_ROOT)$(PKG_DIR)/etc/imspector/imspector.conf

include ../Makefile.rules
