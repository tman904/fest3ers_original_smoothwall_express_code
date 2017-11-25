# When a new kernel is installed, xtables-addons must also be installed so thats
#   /lib/modules/X/extra/ is installed and available.

UPDATE_PACKAGES = \
		  apcupsd \
		  bc \
		  device-ids \
		  cacert-bundle \
		  c_icap \
		  c_icap_modules \
		  dhcpcd \
		  dnsmasq \
		  e2fsprogs \
		  eudev \
		  file \
		  findutils \
		  fping \
		  gawk \
		  grep \
		  httpd \
		  iproute2 \
		  ipbatch \
		  ipset \
		  iptables \
		  isdn4k-utils \
		  kmod \
		  libevent \
		  libosip2 \
		  libmnl \
		  libnetfilter_acct \
		  libnetfilter_conntrack \
		  libnetfilter_cthelper \
		  libnetfilter_cttimeout \
		  libnetfilter_log \
		  libnetfilter_queue \
		  libnfnetlink \
		  libnftnl \
		  libnl \
		  libsmooth+setup \
		  listtables \
		  linux \
		  linux-firmware \
		  lm_sensors \
		  nspr \
		  nss \
		  openssh \
		  openssl \
		  openswan \
		  pcmciautils \
		  qemu \
		  siproxd \
		  smoothd \
		  snort \
		  squid \
		  suricata \
		  squidclamav \
		  strace \
		  sysklogd \
		  trafficstats \
		  unbound \
		  util-linux \
		  wget \
		  xtables-addons \
		  wireless_tools \
		  wpa_supplicant \
		  xz \
		  coretree


UPDATE_ID = 009
UPDATE_NAME = Update9

CLAMAV = yes
KERNEL = yes
EXTRA_UPDATE_FILES = tzdata2017c.tar.gz
$(shell cp ../../../downloads/$(EXTRA_UPDATE_FILES) . 2>/dev/null)

include ../Makefile.update
