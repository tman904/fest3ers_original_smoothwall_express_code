# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = libwww-perl
VERSION = 5.64

BASE_URL = http://lwp.linpro.no/lwp/


CONFIGURE = yes

configure: $(DIR)/
	@(cd $(DIR); perl Makefile.PL -n ) 

include ../Makefile.rules
