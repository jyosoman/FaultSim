CC        := g++
LD        := g++

CFLAGS	  := -Wall -O3
MODULES   := base gates logicModels parser
TESTS	  := test
SRC_DIR   := $(addprefix src/,$(MODULES))
TEST_DIR  := $(addprefix src/,$(TESTS))
TEST_BUILD_DIR  := $(addprefix build/,$(TESTS))
BUILD_DIR := $(addprefix build/,$(MODULES)) $(TEST_BUILD_DIR)

EXECUTABLE=build/test/main.exe build/test/parseTest.exe
SRC       := $(foreach sdir,$(SRC_DIR),$(wildcard $(sdir)/*.cc))
OBJ       := $(patsubst src/%.cc,build/%.o,$(SRC))
INCLUDES  := $(addprefix -I,$(SRC_DIR))

vpath %.cc $(SRC_DIR)

define make-goal
$1/%.o: %.cc
	$(CC) $(INCLUDES) $(CFLAGS) -c $$< -o $$@
endef

.PHONY: all checkdirs clean

all: checkdirs $(EXECUTABLE)

$(EXECUTABLE): $(OBJ)
	$(LD) $^ $(CFLAGS) -o $@ $(patsubst build/test/%.exe,src/test/%.cc,$@)



checkdirs: $(BUILD_DIR)

$(BUILD_DIR):
	@mkdir -p $@

clean:
	@rm -rf $(BUILD_DIR)

$(foreach bdir,$(BUILD_DIR),$(eval $(call make-goal,$(bdir))))
