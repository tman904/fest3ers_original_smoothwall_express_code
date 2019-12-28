# When a new kernel is installed, xtables-addons must also be installed so that
#   /lib/modules/X/extra/ is installed and available.

# Put kernel-drivers and linux-firmware at the end before coretree to ensure
#   that they override those files in linux when linux is updated.

UPDATE_PACKAGES = \
		  bison \
		  c_icap_modules \
		  clamav \
		  curl \
		  device-ids \
		  dhcpcd \
		  iproute2 \
		  libreswan \
		  linux \
		  miniupnpd \
		  openssh \
		  openssl \
		  smoothd \
		  snort \
		  squid \
		  suricata \
		  unbound \
		  xtables-addons \
		  kernel-drivers \
		  linux-firmware \
		  coretree


UPDATE_ID = 011
UPDATE_NAME = Update11

CLAMAV = yes
KERNEL = yes
EXTRA_UPDATE_FILES = tzdata2019c.tar.gz
$(shell cp ../../../downloads/$(EXTRA_UPDATE_FILES) . 2>/dev/null)

include ../Makefile.update
