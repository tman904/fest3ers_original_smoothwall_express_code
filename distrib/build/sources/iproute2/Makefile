# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf
include ../Makefile.versions

PACKAGE = iproute2
VERSION = 2.6.39

BASE_URL = http://devresources.linuxfoundation.org/dev/iproute2/download
EXTENSION=.tar.gz

PATCH_FILE1 = m_xt.c.patch

CONFIGURE = yes
COMPILE = yes
INSTALL = yes
CLEAN = yes

PATHS = SBINDIR=/usr/sbin CONFDIR=/etc/iproute2 DOCDIR=/usr/share/doc/iproute2 MANDIR=/usr/share/man LIBDIR=/usr/lib/

configure: patch
	@sed -i '/^TARGETS/s@ arpd@@g' $(COMPILE_DIR)/misc/Makefile

compile: configure
	$(MAKE) $(JOBS) -C $(COMPILE_DIR) KERNEL_INCLUDE=/usr/include $(PATHS)
	ln -s $(DIR) $(PACKAGE)

install: compile
	@mkdir -p $(PKG_ROOT)$(PKG_DIR)
	@make -C $(COMPILE_DIR) DESTDIR=$(PKG_ROOT) MODDESTDIR=$(PKG_ROOT)/lib/tc $(PATHS) install

clean:
	@echo -n " $(PACKAGE)"
	@rm -rf $(DIR)
	@rm -rf $(COMPILE_DIR)
	@rm -f $(PACKAGE)
ifeq ($(BUILD_PHASE), Final)
	@rm -rf $(PKG_ROOT)
	@rm -f $(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz
endif
	
include ../Makefile.rules
