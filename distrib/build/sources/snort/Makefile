# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = snort

# Deal with snort: get the latest version number dynamically. :)
#
VERSION := $(shell ../../toolcrib/get-snort-ver.sh -v $(PACKAGE))
URL := $(shell ../../toolcrib/get-snort-ver.sh -u $(PACKAGE))

BASE_URL = http://www.snort.org

PATCH_FILE1 = snort-pidfix.patch

CONFIG_OPTS = --enable-gre --enable-targetbased --enable-ppm \
	      --enable-perfprofiling --enable-zlib

# You're looking in here because the build system failed to find
# the snort source package or it failed to build.
#
# This makefile should always get the latest version of snort, whatever it is.
# However, the build might fail if the pidfile fix patch is no longer correct.

DOWNLOAD = yes
INSTALL = yes

download:
	@if [ ! -e ../../downloads/$(TARBALL)$(EXTENSION).done ]; then \
	  wget --no-check-certificate \
	       -O ../../downloads/$(TARBALL)$(EXTENSION) $(BASE_URL)$(URL); \
	  if [ $$? -eq 0 ]; then \
	    touch ../../downloads/$(TARBALL)$(EXTENSION).done; \
	  fi; \
	fi

PREPARE = yes
$(DIR)/: download
	@tar -xvf $(DOWNLOADS_DIR)/$(TARBALL)$(EXTENSION)

INSTALL = yes
install: compile
	@mkdir -p $(PKG_ROOT)
	@make -C $(COMPILE_DIR) DESTDIR=$(PKG_ROOT) install
	@mkdir -p $(PKG_ROOT)/var/smoothwall/snort/rules/
	@mkdir -p $(PKG_ROOT)/var/smoothwall/snort/preproc_rules/
	@mkdir -p $(PKG_ROOT)/var/smoothwall/snort/reputation_lists/
	@touch $(PKG_ROOT)/var/smoothwall/snort/rules/local.rules
	@touch $(PKG_ROOT)/var/smoothwall/snort/rules/deleted.rules
	@touch $(PKG_ROOT)/var/smoothwall/snort/reputation_lists/black.list
	@touch $(PKG_ROOT)/var/smoothwall/snort/reputation_lists/white.list
	@install -D $(COMPILE_DIR)/etc/unicode.map \
	    $(PKG_ROOT)/var/smoothwall/snort/unicode.map
	@install -D $(COMPILE_DIR)/etc/classification.config \
	    $(PKG_ROOT)/var/smoothwall/snort/classification.config
	@install -D $(COMPILE_DIR)/etc/reference.config \
	    $(PKG_ROOT)/var/smoothwall/snort/reference.config
	@install -D $(COMPILE_DIR)/preproc_rules/preprocessor.rules \
	    $(PKG_ROOT)/var/smoothwall/snort/preproc_rules/preprocessor.rules
	@install -D $(COMPILE_DIR)/preproc_rules/decoder.rules \
	    $(PKG_ROOT)/var/smoothwall/snort/preproc_rules/decoder.rules
	@chown nobody:nobody -R $(PKG_ROOT)/var/smoothwall/
	@mkdir -p $(PKG_ROOT)/$(MODULE_DIR)/usr/lib/smoothwall
	@echo $(VERSION) > $(PKG_ROOT)/$(MODULE_DIR)/usr/lib/smoothwall/snortversion
	SNORT_OPTS=`echo -n "$(CONFIG_OPTS)" | sed -e 's/ +/ /'`; \
	  sed -e "/OPTIONS :/s/:.*$$/: $$SNORT_OPTS/" \
	      -e '/OPTIONS :/a #     SWE built : $(PACKAGE)-$(VERSION)' \
	      < snort.conf > $(COMPILE_DIR)/snort.conf.sed
	install -D $(COMPILE_DIR)/snort.conf.sed $(PKG_ROOT)/etc/snort.conf
	chown root:root -R $(PKG_ROOT)/etc
	chmod 755 -R $(PKG_ROOT)/etc
	chmod 644 -R $(PKG_ROOT)/etc/snort.conf


include ../Makefile.rules
