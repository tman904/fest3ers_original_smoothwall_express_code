# Makefile for iptableproc
# (c) 2006 Martin Houston <martin.houston@smoothwall.net>
# Released under the GPL.
# using the 2.6 kbuild facility

SRC_DIR = $(shell pwd;)
ifndef KERNEL_DIR
KERNEL_DIR := /usr/src/linux-2.6.16.21-0.25-obj/i386/default
endif

obj-m += iptableproc.o

iptableproc-objs := procside.o iptables.o seqstuff.o

all:
	make -C $(KERNEL_DIR) M=$(SRC_DIR) modules

clean:
	make -C $(KERNEL_DIR) M=$(SRC_DIR) clean
	
install:
	make -C $(KERNEL_DIR) M=$(SRC_DIR) install
	


