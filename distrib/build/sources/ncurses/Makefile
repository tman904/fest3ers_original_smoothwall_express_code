include ../Makefile.conf

PACKAGE = ncurses
VERSION = 5.4

BASE_URL = ftp://ftp.gnu.org/gnu/ncurses/

ifeq ($(BUILDENV), 1)
CONFIG_OPTS = --with-shared \
    --without-debug --without-ada --enable-overwrite
endif

include ../Makefile.rules
