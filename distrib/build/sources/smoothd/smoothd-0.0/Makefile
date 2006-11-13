CXXFLAGS= $(CFLAGS)

OBJS=
LIB_OBJS=module.o UDSocket.o pid.o setuid.o config.o
MAIN=main.cpp
LIBS=-ldl /usr/lib/libsmoothd.so 
BIN=smoothd

MODULES=sysshutdown

MODULEFLAGS = $(CXXFLAGS) -fPIC -shared -Wl,-soname,$@.so -o $@.so $@.cpp $(LIBS)

all: libsmoothd smoothd $(MODULES) smoothcom

modules: $(MODULES)

libsmoothd : $(LIB_OBJS)
	$(CXX) -shared -fPIC -o libsmoothd.so $(LIB_OBJS) 
	@install -D ./libsmoothd.so /usr/lib/libsmoothd.so

smoothd: $(OBJS) 
	$(CXX) -o $(BIN) $(DFLAGS) $(MAIN) $(OBJS) $(LIBS)

smoothcom:
	$(CXX) -o smoothcom $(CXXFLAGS) smoothcom.cpp -ldl /usr/lib/libsmoothd.so 

clean:
	rm -f $(OBJS) $(BIN) *.o *.so modules smoothcom



sysshutdown : $(OBJS)  
	$(CXX) $(MODULEFLAGS)
