CC        := g++
LD        := g++

MODULES   := base gates logicModels parser
TESTS	  := test
SRC_DIR   := $(addprefix src/,$(MODULES))
TEST_DIR  := $(addprefix src/,$(TESTS))
PYTEST_DIR:= src/pythonTesting
TEST_BUILD_DIR  := $(addprefix build/,$(TESTS))
BUILD_DIR := $(addprefix build/,$(MODULES))
PYTEST_BUILD_DIR:=build/pythonTesting

SRC       := $(foreach sdir,$(SRC_DIR),$(wildcard $(sdir)/*.cc))
OBJ       := $(patsubst src/%.cc,build/%.o,$(SRC))
INCLUDES  := $(addprefix -I,$(SRC_DIR))
TEST_SRC  := $(foreach sdir,$(TEST_DIR),$(wildcard $(sdir)/*.cc))
PYTEST_SRC  := $(foreach sdir,$(PYTEST_DIR),$(wildcard $(sdir)/*.cc))
TEST_OBJ  := $(patsubst src/%.cc,build/%.o,$(TEST_SRC))
PYSHAREDLIB  := $(patsubst src/%.cc,build/%.so,$(PYTEST_SRC))
EXECUTABLE:= $(patsubst %.o,%.exe,$(TEST_OBJ))
vpath %.cc $(SRC_DIR)
vpath %.cc $(TEST_DIR)


.PHONY: all checkdirs clean
CFLAGS:=   -std=c++11 -O3
all: checkdirs $(EXECUTABLE) $(PYSHAREDLIB) $(SRC)
debug: CFLAGS := -DDEBUG 
debug: all

CFLAGS	  += -Wall 

$(OBJ):$(SRC)
	$(CC) $(INCLUDES) $(CFLAGS) -fPIC -c $(patsubst build/%.o,src/%.cc,$@) -o $@

$(TEST_OBJ):$(SRC) $(TEST_SRC)
	$(CC) $(INCLUDES) $(CFLAGS) -fPIC -c $(patsubst build/%.o,src/%.cc,$@) -o $@

$(EXECUTABLE): $(OBJ) $(TEST_OBJ)
	$(LD) $(OBJ) $(patsubst %.exe,%.o,$@) $(CFLAGS) -o $@ 

$(PYSHAREDLIB): $(OBJ) $(PYTEST_SRC) $(PYTEST_BUILD_DIR)
	$(LD)  $(OBJ) $(INCLUDES) $(patsubst build/%.so,src/%.cc,$@) $(CFLAGS) -shared -fPIC -o $@ 



checkdirs: $(BUILD_DIR) $(TEST_BUILD_DIR) $(PYTEST_BUILD_DIR)

$(BUILD_DIR):
	@mkdir -p $@

$(TEST_BUILD_DIR):
	@mkdir -p $@
$(PYTEST_BUILD_DIR):
	@mkdir -p $@


clean:
	@rm -rf $(BUILD_DIR)
	@rm -rf $(TEST_BUILD_DIR)
	@echo $(TEST_BUILD_DIR) $(BUILD_DIR)

