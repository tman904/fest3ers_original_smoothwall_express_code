# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = daq

# Deal with snort: get the latest version number dynamically. :)
#
VERSION := $(shell ../../toolcrib/get-snort-ver.sh -v $(PACKAGE))
ifeq ($(VERSION),)
  $(shell echo "get-snort-ver.sh cannot get current $(PACKAGE) version" >&2)
  $(error get-snort-ver.sh cannot get current $(PACKAGE) version)
endif
URL := $(shell ../../toolcrib/get-snort-ver.sh -u $(PACKAGE))
ifeq ($(URL),)
  $(shell echo "get-snort-ver.sh cannot get current $(PACKAGE) URL" >&2)
  $(error get-snort-ver.sh cannot get current $(PACKAGE) URL)
endif

BASE_URL = http://www.snort.org

DIR = $(PACKAGE)-$(VERSION)

CONFIG_OPTS += --disable-bundled-modules --enable-nfq-module \
	      --enable-pcap-module --enable-dump-module 

# You're looking in here because the build system failed to find
# the snort source package or it failed to build.
#
# This makefile should always get the latest version of snort, whatever it is.
# However, the build might fail if the pidfile fix patch is no longer correct.

DOWNLOAD = yes
download:
	@if [ ! -e ../../downloads/$(TARBALL)$(EXTENSION).done ]; then \
	  wget -O ../../downloads/$(TARBALL)$(EXTENSION) $(BASE_URL)$(URL); \
	  if [ $$? -eq 0 ]; then \
	    touch ../../downloads/$(TARBALL)$(EXTENSION).done; \
	  fi; \
	fi


include ../Makefile.rules
