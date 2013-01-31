# Copyright 2004-2010 SmoothWall Ltd

CC=gcc
CFLAGS=-O2 -Wall

COMPILE=$(CC) $(VERSION_DEFINES) $(CFLAGS)

PROGS=raidautorun iowrap

all : $(PROGS)

clean : 
	@rm -f $(PROGS) *.o core

######

%.o : %.c
	$(COMPILE) -c $< -o $@

iowrap: iowrap.o
	$(COMPILE) $< -o $@
raidautorun: raidautorun.o
	$(COMPILE) $< -o $@
