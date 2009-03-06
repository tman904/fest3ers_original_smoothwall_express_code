# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf
include ../Makefile.versions

PACKAGE = install
VERSION = 0.0

compile:
	@make -C $(COMPILE_DIR)

install: compile
	@install -D $(COMPILE_DIR)/install/install $(TARGET_DIR)/$(PACKAGE)

all: install
	@true

clean:
	@make -C $(COMPILE_DIR) clean

download:
	@true

packageinfo.html: clean
	@echo "<li><span style='font-size:large;'>$(PACKAGE) $(VERSION)</span><br>" >>/tmp/packageinfo.html
	@tar --exclude .svn -zcvf /tmp/downloads/$(TARBALL).tar.gz $(DIR)
	@echo "Download: <a href='downloads/$(TARBALL).tar.gz'>$(TARBALL).tar.gz</a><br>" >>/tmp/packageinfo.html
	