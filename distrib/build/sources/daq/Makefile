# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = daq
VERSION = 0.6.2

BASE_URL = http://www.snort.org/dl/snort-current

DOWNLOAD = yes

download:
	wget $(BASE_URL)/$(TARBALL)$(EXTENSION) -O $(DOWNLOADS_DIR)/$(TARBALL)$(EXTENSION)

include ../Makefile.rules
