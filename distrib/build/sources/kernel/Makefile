# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf
include ../Makefile.versions

KERNEL_DIR = $(SOURCES_DIR)/kernel/linux
IPTABLES_DIR = $(SOURCES_DIR)/iptables/iptables-$(IPTABLES_VER)

PACKAGE = linux
VERSION = $(KERNEL_VERSION)

PATCH_O_MATIC_VER = 20050814
UNICORN_VER = 0.9.0
USR_VER = 1.08

COMPILER = /opt/gcc-3.2.3/bin/gcc

download:
	@$(DL_CMD) http://www.kernel.org/pub/linux/kernel/v2.6/linux-$(KERNEL_VER).tar.bz2
	@$(DL_CMD) http://www.openswan.org/download/$(FREESWAN_TYPE)-$(FREESWAN_VER).tar.gz
	@$(DL_CMD) ftp://ftp.netfilter.org/pub/patch-o-matic-ng/snapshot/patch-o-matic-ng-$(PATCH_O_MATIC_VER).tar.bz2
	@$(DL_CMD) http://www.bewan.com/bewan/drivers/bast-$(UNICORN_VER).tgz

prepare: download
	@tar -jxvf $(DOWNLOADS_DIR)/linux-$(KERNEL_VER).tar.bz2
	@tar -zxvf $(DOWNLOADS_DIR)/$(FREESWAN_TYPE)-$(FREESWAN_VER).tar.gz
	@tar -jxvf $(DOWNLOADS_DIR)/patch-o-matic-ng-$(PATCH_O_MATIC_VER).tar.bz2
	@tar -zxvf $(DOWNLOADS_DIR)/bast-$(UNICORN_VER).tgz

	@rm -f linux
	@ln -s linux-$(KERNEL_VER) linux

	@make -C linux mrproper

	@cp ../kernel.config linux/.config

	@make -C linux CC=$(COMPILER) clean prepare

	@make -C $(FREESWAN_TYPE)-$(FREESWAN_VER) CC=$(COMPILER) KERNELSRC=$(KERNEL_DIR) precheck verset kpatch

apply-pom: prepare
	@(export KERNEL_DIR=$(KERNEL_DIR); \
	export IPTABLES_DIR=$(IPTABLES_DIR); \
	cd patch-o-matic-ng-$(PATCH_O_MATIC_VER); \
	./runme --batch CONNMARK; \
	./runme --batch quake3-conntrack-nat; \
	./runme --batch pptp-conntrack-nat; \
	./runme --batch mms-conntrack-nat; \
	./runme --batch sip-conntrack-nat; \
	./runme --batch h323-conntrack-nat;)

compile-kernel: apply-pom
	@cp ../kernel.config linux/.config

	@make -C linux CC=$(COMPILER) clean oldconfig dep bzImage modules

compile-unicorn: compile-kernel
	@make -C unicorn/libm CC=$(COMPILER) KERNEL_SOURCES=$(KERNEL_DIR)
	@(cd unicorn/unicorn_pci; make CC=$(COMPILER) KERNEL_SOURCES=$(KERNEL_DIR))

package-kernel: compile-kernel
	@mkdir $(PKG_ROOT)
	@(cd $(PKG_ROOT); \
	make -C $(KERNEL_DIR) CC=$(COMPILER) INSTALL_MOD_PATH=$(PKG_ROOT) modules_install; \
	mkdir -p boot; \
	cp $(KERNEL_DIR)/arch/i386/boot/bzImage boot/vmlinuz-$(KERNEL_VER); \
	cp $(KERNEL_DIR)/System.map boot/System.map-$(KERNEL_VER); \
	rm -f lib/modules/$(KERNEL_VER)/build; \
	cp $(KERNEL_DIR)/.config $(SOURCES_DIR)/kernel.config.new)

package-unicorn: compile-unicorn
	@mkdir $(PKG_ROOT)/lib/modules/$(KERNEL_VER)/kernel/drivers/misc
	@cp $(SOURCES_DIR)/kernel/unicorn/unicorn_pci/unicorn_pci_atm.ko \
		$(PKG_ROOT)/lib/modules/$(KERNEL_VER)/kernel/drivers/misc
	@cp $(SOURCES_DIR)/kernel/unicorn/unicorn_pci/unicorn_pci_eth.ko \
		$(PKG_ROOT)/lib/modules/$(KERNEL_VER)/kernel/drivers/misc

build-tarball: package-kernel package-unicorn
	@(cd $(PKG_ROOT); \
	tar -zcvf $(TARGET_DIR)/smoothwall-kernel-$(KERNEL_VER).tar.gz .; \
	tar -zxvf $(TARGET_DIR)/smoothwall-kernel-$(KERNEL_VER).tar.gz -C /);

clean:
	@rm -f linux
	@rm -rf linux-$(KERNEL_VER)
	@rm -rf $(FREESWAN_TYPE)-$(FREESWAN_VER)
	@rm -rf patch-o-matic-ng-$(PATCH_O_MATIC_VER)
	@rm -rf unicorn
	@rm -rf usr-sureconnect
	@rm -rf $(PKG_ROOT)

all: clean build-tarball

packageinfo.html:
	@echo "<li><span style='font-size:large;'>$(PACKAGE) $(VERSION)</span><br>" >>/tmp/packageinfo.html
	@cp -avR $(DOWNLOADS_DIR)/linux-$(KERNEL_VER).tar.bz2 /tmp/downloads
	@cp -avR $(DOWNLOADS_DIR)/$(FREESWAN_TYPE)-$(FREESWAN_VER).tar.gz /tmp/downloads
	@cp -avR $(DOWNLOADS_DIR)/patch-o-matic-ng-$(PATCH_O_MATIC_VER).tar.bz2 /tmp/downloads
	@cp -avR $(DOWNLOADS_DIR)/unicorn-$(UNICORN_VER).tar.gz /tmp/downloads
	@cp -avR $(DOWNLOADS_DIR)/usr-sureconnect.tar.gz /tmp/downloads
	@echo "Kernel Download: <a href='http://www.uk.kernel.org/pub/linux/kernel/v2.4/linux-$(KERNEL_VER).tar.bz2'>http://www.uk.kernel.org/pub/linux/kernel/v2.4/linux-$(KERNEL_VER).tar.bz2</a>" >>/tmp/packageinfo.html
	@echo "(<a href='downloads/linux-$(KERNEL_VER)'>Local mirror</a>)<br>" >>/tmp/packageinfo.html
	@echo "Openswan: <a href='http://www.openswan.org/download/$(FREESWAN_TYPE)-$(FREESWAN_VER).tar.gz'>http://www.openswan.org/download/$(FREESWAN_TYPE)-$(FREESWAN_VER).tar.gz</a>" >>/tmp/packageinfo.html
	@echo "(<a href='downloads/$(FREESWAN_TYPE)-$(FREESWAN_VER).tar.gz'>Local mirror</a>)<br>" >>/tmp/packageinfo.html
	@echo "Netfilter Download: <a href='http://www.netfilter.org/files/patch-o-matic-ng-$(PATCH_O_MATIC_VER).tar.bz2'>http://www.netfilter.org/files/patch-o-matic-ng-$(PATCH_O_MATIC_VER).tar.bz2</a>" >>/tmp/packageinfo.html
	@echo "(<a href='downloads/patch-o-matic-ng-$(PATCH_O_MATIC_VER).tar.bz2'>Local mirror</a>)<br>" >>/tmp/packageinfo.html
	@echo "Unicoron Local mirror: <a href='downloads/unicorn-$(UNICORN_VER).tar.gz'>unicorn-$(UNICORN_VER).tar.gz</a>" >>/tmp/packageinfo.html
	@echo "(<a href='downloads/usr-sureconnect.tar.gz'>Local mirror</a>)<br>" >>/tmp/packageinfo.html
	@echo "Patches:<br>" >>/tmp/packageinfo.html
	@echo "<ul>" >>/tmp/packageinfo.html
	@(for PATCH in patch-o-matic-pptp-fix.patch; do \
		echo "<li><a href='downloads/$$PATCH'>$$PATCH</a>" >>/tmp/packageinfo.html; \
		cp -avR ../kernel-patches/$$PATCH /tmp/downloads; \
	done) 
	@echo "</ul>" >>/tmp/packageinfo.html
