include ../Makefile.conf
include ../Makefile.versions

PACKAGE = coretree
VERSION = 0.0

distrib:
	@mkdir distrib;
	@cp -avR tree/* distrib

	@chown -R root:root distrib/
	@chmod -v 700 distrib/root
	@chmod -v 1777 distrib/tmp

	@chown -R nobody:nobody distrib/var/smoothwall
	@chown -R nobody:nobody distrib/var/patches
	@chown -R 100:100 distrib/var/spool/squid
	@chown -R 100:100 distrib/var/log/squid
	@chown -R 101:101 distrib/var/log/snort
	
	@chown root:nobody distrib/usr/bin/setuids/*
	@chmod 4750 distrib/usr/bin/setuids/*
	
	@(cd distrib/etc/httpd/conf; ln -s /var/smoothwall/main/hostname.conf)
	@(cd distrib/usr/etc ln -s /var/smoothwall/dhcp/dhcpd.conf)
	@(cd distrib/etc; ln -s /var/smoothwall/time/localtime)
	@(cd distrib/etc; ln -s /var/smoothwall/vpn/ipsec.conf)
	@(cd distrib/etc; ln -s /var/smoothwall/vpn/ipsec.secrets)
	@(cd distrib/usr/etc; ln -s /var/smoothwall/dhcp/dhcpd.conf)
	@(cd distrib/etc/ppp; ln -s /var/smoothwall/ppp/secrets chap-secrets)
	@(cd distrib/etc/ppp; ln -s /var/smoothwall/ppp/secrets pap-secrets)
	@(cd distrib/etc/ppp; ln -s /var/smoothwall/ppp/ibod.cf)
	@(cd distrib/usr/etc; ln -s /var/smoothwall/time/ntpd.conf)
	
	@(cd distrib/var/smoothwall/time; ln -s /usr/share/zoneinfo/posix/Europe/London localtime)

	@(cd distrib; rm -rf `find -name CVS`)

all: distrib
	@tar -zcvf $(TARGET_DIR)/smoothwall-$(PACKAGE)-$(VERSION).tar.gz -C distrib .

clean:
	@rm -rf distrib
	@rm -f $(TARGET_DIR)/smoothwall-$(PACKAGE)-$(VERSION).tar.gz

download:
	@true
