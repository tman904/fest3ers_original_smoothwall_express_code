include ../Makefile.conf
include ../Makefile.versions

PACKAGE =  ipp2p
VERSION =  $(IPP2P_VER)

LICENCE_FILE = $(DIR)/COPYING

BASE_URL = http://www.ipp2p.org/downloads/

CONFIGURE = yes
COMPILE = yes
INSTALL = yes

configure: $(DIR)/
	@true

compile: configure
	@make -C $(COMPILE_DIR) KERNEL_SRC=$(SOURCES_DIR)/kernel-runtime/linux KERNEL_SERIES=2.6 IPTABLES_VERSION=$(IPTABLES_VER) IPTABLES_SRC=$(SOURCES_DIR)/iptables/iptables-$(IPTABLES_VER) PREFIX=/$(PKG_DIR) libipt_ipp2p.so

install: compile
	@install -D $(COMPILE_DIR)/libipt_ipp2p.so $(PKG_ROOT)/$(PKG_DIR)/lib/iptables/libipt_ipp2p.so

include ../Makefile.rules
