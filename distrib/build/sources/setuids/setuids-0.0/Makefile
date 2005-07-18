CC=gcc

COMPILE = $(CC) $(CFLAGS)

PROGS = setdmzholes setportfw setxtaccess restartdhcp restartsnort \
	restartsquid smoothiedeath smoothierebirth alcateladslfw \
	installpackage ipsecctrl  restartdnsproxy restartssh \
	setadvnet setipblock restartupnp

all : $(PROGS)

clean : 
	-rm -f $(PROGS) *.o core

######

% : %.c
	$(COMPILE) $< -o $@

setdmzholes : setdmzholes.c
setportfw : setportfw.c
setxtaccess : setxtaccess.c
restartdhcp : restartdhcp.c
restartsnort : restartsnort.c
restartsquid : restartsquid.c
smoothiedeath : smoothiedeath.c
smoothierebirth : smoothierebirth.c
restartdnsproxy : restartdnsproxy.c
restartssh : restartssh.c
alcateladslfw : alcateladslfw.c
setadvnet : setadvnet.c
setipblock : setipblock.c
restartupnp : restartupnp.c
