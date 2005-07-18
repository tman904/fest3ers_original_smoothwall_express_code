include ../Makefile.conf

PACKAGE = MAKEDEV
VERSION = 3.3.8

BASE_URL = http://sotonfs/

TARBALL = $(PACKAGE)-$(VERSION)-2

DIR = $(PACKAGE)-$(VERSION)

CONFIGURE = yes
PACKAGEINFO = yes

configure: patch
	@true

devnodes:
	@(cd /dev; mkdir pts; \
	./MAKEDEV random urandom mem kmem null port zero core full \
		ram raid tty console tty pty fd hd sd loop scd sg apm usb initctl ppp net isdn);
	@tar -zcvf /$(TARGET_DIR)/smoothwall-devnodes-0.0.tar.gz -C / --exclude ./dev/MAKEDEV ./dev;

packageinfo.html: 
	@echo "<li><span style='font-size:large;'>$(PACKAGE) $(VERSION)</span><br>" >>/tmp/packageinfo.html
	@cp -avR $(DOWNLOADS_DIR)/$(TARBALL)$(EXTENSION) /tmp/downloads/
	@echo "Download: <a href='downloads/$(TARBALL)$(EXTENSION)'>$(TARBALL)$(EXTENSION)</a><br>" >>/tmp/packageinfo.html

include ../Makefile.rules
