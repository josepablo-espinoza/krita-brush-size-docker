# Define variables
TARGET = Krita-Brush-Size-Docker.zip
DIR = brushSizeDocker

# Phony targets
.PHONY: all clean

# Default target
all: $(TARGET)

# Zip target
$(TARGET): $(DIR)/* brushSizeDocker.desktop LICENSE
	@echo $(info Creating zip archive...)
	@mkdir -p tmp/$(DIR)
	@cp -R $(DIR)/* tmp/$(DIR)/
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
