# Copyright 2004-2010 SmoothWall Ltd

include ../Makefile.conf

PACKAGE = git
VERSION = 1.7.4.1

LICENCE_FILE = $(DIR)/COPYING

BASE_URL = http://kernel.org/pub/software/scm/git/

COMPILE = yes
INSTALL = yes

compile: configure
	@make -C $(DIR) NO_PYTHON=yes

install: compile
	@make -C $(DIR) NO_PYTHON=yes DESTDIR=$(PKG_ROOT) install

include ../Makefile.rules
