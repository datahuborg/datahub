GEN_SRC := gen-cpp/DataHub.cpp \
	gen-cpp/datahub_types.cpp 
GEN_OBJ := $(patsubst %.cpp,%.o, $(GEN_SRC))

MY_SRC := DHClient.cpp
MY_OBJ := $(patsubst %.cpp,%.o, $(MY_SRC))

CXXFLAGS := -I$(THRIFT_HOME)/thrift-bin/include -DHAVE_INTTYPES_H -DHAVE_NETINET_IN_H
LDFLAGS := -L$(THRIFT_HOME)/thrift-bin/lib -Wl,-rpath=$(THRIFT_HOME)/thrift-bin/lib

all: DHClient

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -Wall -O2 -g -c $< -o $@

DHClient: $(MY_OBJ) $(GEN_OBJ)
	$(CXX) $^ -o $@ $(LDFLAGS) -lthrift

.PHONY: clean
clean:
	rm -rf gen-cpp *.o DHClient
