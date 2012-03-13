include ../Makefile.conf

PACKAGE = libdnet
VERSION = 1.11

LICENCE_FILE = $(DIR)/LICENSE

BASE_URL = http://ignum.dl.sourceforge.net/project/$(PACKAGE)/$(PACKAGE)/$(TARBALL)

PREPARE = yes

$(DIR)/: download
	@tar -zxvf $(DOWNLOADS_DIR)/$(PACKAGE)-$(VERSION)$(EXTENSION)
	@(cd $(DIR); autoconf)

include ../Makefile.rules

