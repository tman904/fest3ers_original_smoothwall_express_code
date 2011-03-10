# Copyright 2004-2010 SmoothWall Ltd

IPTABLES_SRC_DIR:=/build/sources/iptables/iptables-$(IPTABLES_VER)
XTABLES_LIBDIR:=/usr/libexec/xtables

KERNEL_DIR:=/usr/src/linux

CC=gcc 
CXX=g++
COPT_FLAGS:=$(CFLAGS) -g -DDEBUG

CFLAGS:=$(COPT_FLAGS) -DIPTABLES_VERSION=\"$(IPTABLES_VER)\" -Wall -Wunused -I$(IPTABLES_SRC_DIR)/include/ -I.

LDFLAGS      = -rdynamic
LDLIBS       = -ldl -lnsl -liptc -lxtables

PROGS = ipbatch ip6batch

all : $(PROGS)

clean : 
	-rm -f $(PROGS) *.o core

######

ipbatch.o: ipbatch.c $(IPTABLES_SRC_DIR)/include/iptables.h
	$(CC) -c $(CFLAGS) -DXTABLES_LIBDIR=\"$(XTABLES_LIBDIR)\" ipbatch.c -o ipbatch.o
ip6batch.o: ipbatch.c $(IPTABLES_SRC_DIR)/include/iptables.h
	$(CC) -c $(CFLAGS) -DIP6T -DXTABLES_LIBDIR=\"$(XTABLES_LIBDIR)\" ipbatch.c -o ip6batch.o

ipbatch: ipbatch.o $(IPTABLES_SRC_DIR)/iptables.o
	$(CC) $(LDLIBS) $(LDFLAGS) $(CFLAGS) -o $@  $^
ip6batch: ip6batch.o $(IPTABLES_SRC_DIR)/ip6tables.o
	$(CC) $(LDLIBS) $(LDFLAGS) $(CFLAGS) -o $@  $^
