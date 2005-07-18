include ../Makefile.conf

PACKAGE = libpcap
VERSION = 2005.04.30

BASE_URL = http://www.tcpdump.org/daily/

INSTALL = yes

install: compile
	-mkdir $(PKG_ROOT)
	@make -C $(COMPILE_DIR) DESTDIR=$(PKG_ROOT) install
	@mkdir -p $(PKG_ROOT)/usr/include/net
	@(cd $(PKG_ROOT)/usr/include/net; ln -s ../pcap-bpf.h bpf.h)

include ../Makefile.rules
