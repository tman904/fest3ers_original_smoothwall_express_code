include ../Makefile.conf

PACKAGE = smoothd
VERSION = 0.0

compile:
	@make -C $(COMPILE_DIR)

install: compile
	@install -D $(COMPILE_DIR)/libsmoothd.so $(PKG_ROOT)/usr/lib/libsmoothd.so
	@install -D $(COMPILE_DIR)/smoothd $(PKG_ROOT)/usr/sbin/smoothd 
	@install -D $(COMPILE_DIR)/default $(PKG_ROOT)/usr/lib/smoothd/sockets/default 

	@install -D $(COMPILE_DIR)/module.h $(PKG_ROOT)/usr/include/smoothwall/module.h
	@install -D $(COMPILE_DIR)/setuid.h $(PKG_ROOT)/usr/include/smoothwall/setuid.h
	@install -D $(COMPILE_DIR)/config.h $(PKG_ROOT)/usr/include/smoothwall/config.h
	
	@install -D $(COMPILE_DIR)/smoothcom $(PKG_ROOT)/usr/bin/smoothcom 
	@install -D $(COMPILE_DIR)/smoothd.pm $(PKG_ROOT)/usr/lib/smoothwall/smoothd.pm

	@install -D $(COMPILE_DIR)/sysshutdown.so $(PKG_ROOT)/usr/lib/smoothd/sysshutdown.so 
	@install -D $(COMPILE_DIR)/sysinstall.so $(PKG_ROOT)/usr/lib/smoothd/sysinstall.so 

all: install
	@tar -zcvf $(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz -C $(PKG_ROOT) .
	@tar -zxvf $(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz -C /

clean:
	@make -C $(COMPILE_DIR) clean
	@rm -rf $(PKG_ROOT)
	@rm -f $(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz

download:
	@true
