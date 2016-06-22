CC        := g++
LD        := g++

MODULES   := base gates logicModels test
SRC_DIR   := $(addprefix src/,$(MODULES))
BUILD_DIR := $(addprefix build/,$(MODULES))

EXECUTABLE=memManaged
SRC       := $(foreach sdir,$(SRC_DIR),$(wildcard $(sdir)/*.cc))
OBJ       := $(patsubst src/%.cc,build/%.o,$(SRC))
INCLUDES  := $(addprefix -I,$(SRC_DIR))

vpath %.cc $(SRC_DIR)

define make-goal
$1/%.o: %.cc
	$(CC) $(INCLUDES) -c $$< -o $$@
endef

.PHONY: all checkdirs clean

all: checkdirs $(EXECUTABLE)

$(EXECUTABLE): $(OBJ)
	$(LD) $^ -o $@


checkdirs: $(BUILD_DIR)

$(BUILD_DIR):
	@mkdir -p $@

clean:
	@rm -rf $(BUILD_DIR)

$(foreach bdir,$(BUILD_DIR),$(eval $(call make-goal,$(bdir))))
