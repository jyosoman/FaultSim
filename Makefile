CC        := g++
LD        := g++

MODULES   := base gates logicModels parser
TESTS	  := test
SRC_DIR   := $(addprefix src/,$(MODULES))
TEST_DIR  := $(addprefix src/,$(TESTS))
TEST_BUILD_DIR  := $(addprefix build/,$(TESTS))
BUILD_DIR := $(addprefix build/,$(MODULES))

SRC       := $(foreach sdir,$(SRC_DIR),$(wildcard $(sdir)/*.cc))
OBJ       := $(patsubst src/%.cc,build/%.o,$(SRC))
INCLUDES  := $(addprefix -I,$(SRC_DIR))
TEST_SRC  := $(foreach sdir,$(TEST_DIR),$(wildcard $(sdir)/*.cc))
TEST_OBJ  := $(patsubst src/%.cc,build/%.o,$(TEST_SRC))
EXECUTABLE:= $(patsubst %.o,%.exe,$(TEST_OBJ))
vpath %.cc $(SRC_DIR)
vpath %.cc $(TEST_DIR)


.PHONY: all checkdirs clean
CFLAGS:=-O3 -DDEBUG
all: checkdirs $(EXECUTABLE)
debug: CFLAGS := -DDEBUG 
debug: all

CFLAGS	  += -Wall -g 
define make-goal
$1/%.o: %.cc
	$(CC) $(INCLUDES) $(CFLAGS) -c $$< -o $$@
endef

$(EXECUTABLE): $(OBJ) $(TEST_OBJ) $(SRC) $(TEST_SRC)
	$(LD) $(OBJ) $(patsubst %.exe,%.o,$@) $(CFLAGS) -o $@ 



checkdirs: $(BUILD_DIR) $(TEST_BUILD_DIR)

$(BUILD_DIR):
	@mkdir -p $@

$(TEST_BUILD_DIR):
	@mkdir -p $@

clean:
	@rm -rf $(BUILD_DIR)
	@rm -rf $(TEST_BUILD_DIR)
	@echo $(TEST_BUILD_DIR) $(BUILD_DIR)
	@echo $(TEST_OBJ)
$(foreach bdir,$(BUILD_DIR),$(eval $(call make-goal,$(bdir))))
$(foreach bdir,$(TEST_BUILD_DIR),$(eval $(call make-goal,$(bdir))))
