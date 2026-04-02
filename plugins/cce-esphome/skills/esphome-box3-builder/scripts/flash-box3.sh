#!/usr/bin/env bash
# ESP32-S3-BOX-3 Flash Script
# Validates, compiles, and flashes BOX-3 specific firmware

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

if [ -z "$1" ]; then
    echo -e "${RED}Error: No configuration file specified${NC}"
    echo "Usage: $0 <config.yaml>"
    exit 1
fi

CONFIG_FILE="$1"

if [ ! -f "$CONFIG_FILE" ]; then
    echo -e "${RED}Error: Configuration file not found: $CONFIG_FILE${NC}"
    exit 1
fi

if ! command -v esphome &> /dev/null; then
    echo -e "${RED}Error: esphome command not found${NC}"
    echo "Install with: pip3 install esphome"
    exit 1
fi

echo -e "${YELLOW}=== ESP32-S3-BOX-3 Flash Workflow ===${NC}"
echo ""

# Step 1: Validate
echo -e "${YELLOW}Step 1: Validating configuration...${NC}"
if esphome config "$CONFIG_FILE"; then
    echo -e "${GREEN}✓ Configuration valid${NC}"
else
    echo -e "${RED}✗ Configuration invalid${NC}"
    exit 1
fi

# Step 2: Compile
echo -e "${YELLOW}Step 2: Compiling firmware...${NC}"
if esphome compile "$CONFIG_FILE"; then
    echo -e "${GREEN}✓ Firmware compiled${NC}"
else
    echo -e "${RED}✗ Compilation failed${NC}"
    exit 1
fi

# Step 3: Flash
echo -e "${YELLOW}Step 3: Flashing BOX-3...${NC}"
echo -e "${YELLOW}Connect BOX-3 via USB and press ENTER${NC}"
read

# Auto-detect port
if [ -e /dev/ttyACM0 ]; then
    PORT=/dev/ttyACM0
elif [ -e /dev/ttyUSB0 ]; then
    PORT=/dev/ttyUSB0
else
    echo -e "${RED}Error: No USB device found${NC}"
    exit 1
fi

echo -e "${YELLOW}Using port: $PORT${NC}"

if esphome upload "$CONFIG_FILE" --device "$PORT"; then
    echo -e "${GREEN}✓ Flash successful${NC}"
else
    echo -e "${RED}✗ Flash failed${NC}"
    exit 1
fi

# Step 4: Monitor logs
echo -e "${GREEN}=== Flash Complete ===${NC}"
echo -e "${YELLOW}Monitor logs? (y/n)${NC}"
read -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    esphome logs "$CONFIG_FILE"
fi
