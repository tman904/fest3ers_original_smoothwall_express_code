
CXXFLAGS = $(CFLAGS)

OBJS=
LIB_OBJS = module.o UDSocket.o pid.o setuid.o config.o ipbatch.o
MAIN = main.cpp
LIBS = -ldl /usr/lib/libsmoothd.so 
BIN = smoothd

MODULES = sysshutdown sysinstall sysim sysp3scan sysalcatel sysdhcpd sysdnsproxy \
	sysntpd syssnort syssquid syssshd sysupnpd sysadvnet sysipblock \
	sysxtaccess sysupdown sysipsec systimeset sysiptables systraffic syssip sysclamav \
	systimedaccess

MODULEFLAGS = $(CXXFLAGS) -shared -Wl,-soname,$@.so -o $@.so $@.cpp $(LIBS)

all: libsmoothd smoothd $(MODULES) smoothcom

modules: $(MODULES)

libsmoothd : $(LIB_OBJS)
	$(CXX) -shared  -o libsmoothd.so $(LIB_OBJS) 
	@install -D ./libsmoothd.so /usr/lib/libsmoothd.so

smoothd: $(OBJS) 
	$(CXX) -o $(BIN) $(DFLAGS) $(MAIN) $(OBJS) $(LIBS)

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
sysp3scan : $(OBJS)  
	$(CXX) $(MODULEFLAGS)
sysalcatel : $(OBJS)  
	$(CXX) $(MODULEFLAGS)
sysdhcpd : $(OBJS)  
	$(CXX) $(MODULEFLAGS)
sysdnsproxy : $(OBJS)  
	$(CXX) $(MODULEFLAGS)
sysntpd : $(OBJS)  
	$(CXX) $(MODULEFLAGS)
syssnort : $(OBJS)  
	$(CXX) $(MODULEFLAGS)
syssquid : $(OBJS)  
	$(CXX) $(MODULEFLAGS)
syssshd : $(OBJS)  
	$(CXX) $(MODULEFLAGS)
sysupnpd : $(OBJS)  
	$(CXX) $(MODULEFLAGS)
sysadvnet : $(OBJS)  
	$(CXX) $(MODULEFLAGS)
sysipblock : $(OBJS)  
	$(CXX) $(MODULEFLAGS)
sysxtaccess : $(OBJS)  
	$(CXX) $(MODULEFLAGS)
sysupdown : $(OBJS)  
	$(CXX) $(MODULEFLAGS)
sysipsec : $(OBJS)  
	$(CXX) $(MODULEFLAGS)
systimeset : $(OBJS)  
	$(CXX) $(MODULEFLAGS)
sysiptabes : $(OBJS)  
	$(CXX) $(MODULEFLAGS)
systraffic : $(OBJS)  
	$(CXX) $(MODULEFLAGS)
syssip : $(OBJS)  
	$(CXX) $(MODULEFLAGS)
sysclamav : $(OBJS)
	$(CXX) $(MODULEFLAGS)
systimedaccess : $(OBJS)
	$(CXX) $(MODULEFLAGS)
