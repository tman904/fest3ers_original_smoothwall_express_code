include ../Makefile.conf
include ../Makefile.versions

PACKAGE = install
VERSION = 0.0

compile:
	@make -C $(COMPILE_DIR)

install: compile
	@install -D $(COMPILE_DIR)/install/install $(TARGET_DIR)/$(PACKAGE)

all: install
	@true

clean:
	@make -C $(COMPILE_DIR) clean

download:
	@true
