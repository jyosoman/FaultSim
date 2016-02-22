CC=g++
CFLAGS=-c -Wall -g
LDFLAGS=
SOURCES=and.cc base.cc main.cc transistor.cc
OBJECTS=$(SOURCES:.cc=.o)
EXECUTABLE=memManaged

all: $(SOURCES) $(EXECUTABLE) 

	    
$(EXECUTABLE): $(OBJECTS) 
	    $(CC) $(LDFLAGS) $(OBJECTS) -o $@

.cpp.o:
	    $(CC) $(CFLAGS) $< -o $@
clean:
	rm $(OBJECTS) $(EXECUTABLE)
