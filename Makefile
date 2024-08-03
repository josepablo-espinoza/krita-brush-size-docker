# Define variables
TARGET = Krita-Brush-Size-Docker.zip
DIR = brushSizeDocker

# Phony targets
.PHONY: all clean

# Default target
all: $(TARGET)

# Zip target
$(TARGET): $(DIR)/brushSizeDocker.py $(DIR)/__init__.py $(DIR)/Manual.html brushSizeDocker.desktop LICENSE
	@echo $(info Creating zip archive...)
	@mkdir -p tmp/$(DIR)
	@cp $(DIR)/brushSizeDocker.py tmp/$(DIR)/
	@cp $(DIR)/__init__.py tmp/$(DIR)/
	@cp $(DIR)/Manual.html tmp/$(DIR)/
	@cp LICENSE tmp/$(DIR)/
	@cp brushSizeDocker.desktop tmp/
	@cd tmp && zip -r ../$(TARGET) .
	@rm -rf tmp
	@echo $(info Zip archive created: $(TARGET))

# Clean target
clean:
	@echo "Cleaning up..."
	@rm -f $(TARGET)
	@rm -rf tmp
	@echo "Cleanup complete."