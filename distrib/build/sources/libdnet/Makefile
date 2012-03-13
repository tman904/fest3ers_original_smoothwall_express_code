include ../Makefile.conf

PACKAGE = libdnet
VERSION = 1.11

LICENCE_FILE = $(DIR)/LICENSE

BASE_URL = http://kent.dl.sourceforge.net/libdnet/

PREPARE = yes

$(DIR)/: download
	@tar -zxvf $(DOWNLOADS_DIR)/$(PACKAGE)-$(VERSION)$(EXTENSION)
	@(cd $(DIR); autoconf)

include ../Makefile.rules

