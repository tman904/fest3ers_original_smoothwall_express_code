
CXXFLAGS= $(CFLAGS)
# where to find it - relative path
IPTABLES_SRC_DIR:=../../iptables/iptables-$(IPTABLES_VER)
# where the IPT shared libs live
IPT_LIB_DIR:=/usr/lib/iptables

KERNEL_DIR:=/usr/src/linux

OBJS=
LIB_OBJS=module.o UDSocket.o pid.o setuid.o config.o ipbatch.o ipbatchc.o $(IPTABLES_SRC_DIR)/iptables.o $(IPTABLES_SRC_DIR)/libiptc/libiptc.a
MAIN=main.cpp
LIBS=-ldl /usr/lib/libsmoothd.so 
BIN=smoothd

MODULES=sysshutdown sysinstall sysim #sysiptables

MODULEFLAGS = $(CXXFLAGS) -fPIC -shared -Wl,-soname,$@.so -o $@.so $@.cpp $(LIBS)

all: libsmoothd smoothd $(MODULES) smoothcom ipbatchtest

modules: $(MODULES)

libsmoothd : $(LIB_OBJS)
	$(CXX) -shared -fPIC -o libsmoothd.so $(LIB_OBJS) 
	@install -D ./libsmoothd.so /usr/lib/libsmoothd.so

smoothd: $(OBJS) 
	$(CXX) -o $(BIN) $(DFLAGS) $(MAIN) $(OBJS) $(LIBS)

ipbatchtest: $(OBJS) 
	$(CXX) -o ipbatchtest $(DFLAGS) ipbatchtest.cpp $(OBJS) $(LIBS) 

smoothcom:
	$(CXX) -o smoothcom $(CXXFLAGS) smoothcom.cpp -ldl /usr/lib/libsmoothd.so 

clean:
	rm -f $(OBJS) $(BIN) *.o *.so modules smoothcom

sysshutdown : $(OBJS)  
	$(CXX) $(MODULEFLAGS)
sysiptables : $(OBJS)  
	$(CXX) $(MODULEFLAGS)
sysinstall : $(OBJS)  
	$(CXX) $(MODULEFLAGS)
sysim : $(OBJS)  
	$(CXX) $(MODULEFLAGS)

ipbatchc.o: ipbatch.h 
	$(CC) -c $(CFLAGS) -DIPTABLES_VERSION=\"$(IPTABLES_VER)\" -Wall -Wunused -I$(KERNEL_DIR)/include -I$(IPTABLES_SRC_DIR)/include/ -I. -DIPT_LIB_DIR=\"$(IPT_LIB_DIR)\"  ipbatchc.c 


$(IPTABLES_SRC_DIR)/iptables.o :
	echo "warning: is  " $(IPTABLES_SRC_DIR)/iptables.o  "up to date?"

$(IPTABLES_SRC_DIR)/libiptc/libiptc.a :
	echo "warning: is " $(IPTABLES_SRC_DIR)/libiptc/libiptc.a " up to date?"
