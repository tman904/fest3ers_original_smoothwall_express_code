# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf
include ../Makefile.versions

PACKAGE = $(FREESWAN_TYPE)
VERSION = $(FREESWAN_VER)

BASE_URL = http://www.openswan.org/code/

#PATCH_FILE1 = openswan-paths.patch
#PATCH_FILE2 = openswan-script-paths.patch
#PATCH_FILE4 = openswan-logipsecevents.patch

TARBALL = $(FREESWAN_TYPE)-$(FREESWAN_VER)

CONFIGURE = yes
COMPILE = yes
INSTALL = yes

configure: patch
	@true
	
compile: configure
	@make -C $(COMPILE_DIR) INC_USRLOCAL=$(PKG_DIR) FINALCONFDIR=$(PKG_DIR)/etc FINALRCDIR=$(PKG_DIR)/bin programs

install: compile
	@mkdir -p $(PKG_ROOT)/$(PKG_DIR)
	@make -C $(COMPILE_DIR) DESTDIR=$(PKG_ROOT)/ INC_USRLOCAL=$(PKG_DIR) FINALCONFDIR=$(PKG_DIR)/etc FINALRCDIR=$(PKG_DIR)/bin install
#	@rm -rf $(PKG_ROOT)/usr $(PKG_ROOT)/$(PKG_DIR)/etc

include ../Makefile.rules
