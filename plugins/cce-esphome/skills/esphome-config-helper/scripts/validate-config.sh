#!/usr/bin/env bash
# ESPHome Configuration Validation Script
# Validates YAML syntax and compiles firmware to check for errors

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if config file provided
if [ -z "$1" ]; then
    echo -e "${RED}Error: No configuration file specified${NC}"
    echo "Usage: $0 <config.yaml>"
    echo "Example: $0 my-device.yaml"
    exit 1
fi

CONFIG_FILE="$1"

# Check if file exists
if [ ! -f "$CONFIG_FILE" ]; then
    echo -e "${RED}Error: Configuration file not found: $CONFIG_FILE${NC}"
    exit 1
fi

# Check if esphome command is available
if ! command -v esphome &> /dev/null; then
    echo -e "${RED}Error: esphome command not found${NC}"
    echo "Install with: pip3 install esphome"
    exit 1
fi

echo -e "${YELLOW}=== ESPHome Configuration Validation ===${NC}"
echo ""

# Step 1: Validate YAML syntax and configuration
echo -e "${YELLOW}Step 1: Validating YAML syntax and configuration...${NC}"
if esphome config "$CONFIG_FILE"; then
    echo -e "${GREEN}✓ Configuration is valid${NC}"
    echo ""
else
    echo -e "${RED}✗ Configuration validation failed${NC}"
    echo -e "${RED}Fix the errors above and try again${NC}"
    exit 1
fi

# Step 2: Compile firmware
echo -e "${YELLOW}Step 2: Compiling firmware...${NC}"
echo -e "${YELLOW}(This may take a few minutes on first run)${NC}"
if esphome compile "$CONFIG_FILE"; then
    echo -e "${GREEN}✓ Firmware compiled successfully${NC}"
    echo ""
else
    echo -e "${RED}✗ Compilation failed${NC}"
    echo -e "${RED}Fix the errors above and try again${NC}"
    exit 1
fi

# Success
echo -e "${GREEN}=== Validation Complete ===${NC}"
echo -e "${GREEN}✓ Configuration is valid${NC}"
echo -e "${GREEN}✓ Firmware compiles without errors${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "  1. Flash device: esphome upload $CONFIG_FILE"
echo "  2. Monitor logs: esphome logs $CONFIG_FILE"
echo ""
