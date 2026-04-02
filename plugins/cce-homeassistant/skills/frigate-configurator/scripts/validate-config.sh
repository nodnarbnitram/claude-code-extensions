#!/bin/bash
# Frigate Configuration Validator
# Validates Frigate YAML configuration for common issues
#
# Usage: ./validate-config.sh /path/to/config.yml
#
# Checks performed:
#   - YAML syntax validation
#   - Required fields presence
#   - Common misconfiguration patterns
#   - Resolution format validation
#   - Credential exposure warnings

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

CONFIG_FILE="${1:-config.yml}"

if [[ ! -f "$CONFIG_FILE" ]]; then
    echo -e "${RED}Error: Configuration file not found: $CONFIG_FILE${NC}"
    echo "Usage: $0 /path/to/config.yml"
    exit 1
fi

echo "Validating Frigate configuration: $CONFIG_FILE"
echo "================================================"

ERRORS=0
WARNINGS=0

# Check for YAML validity
echo -n "Checking YAML syntax... "
if command -v python3 &> /dev/null; then
    if python3 -c "import yaml; yaml.safe_load(open('$CONFIG_FILE'))" 2>/dev/null; then
        echo -e "${GREEN}OK${NC}"
    else
        echo -e "${RED}FAILED${NC}"
        echo "  YAML syntax error detected. Run: python3 -c \"import yaml; yaml.safe_load(open('$CONFIG_FILE'))\""
        ((ERRORS++))
    fi
else
    echo -e "${YELLOW}SKIPPED${NC} (python3 not available)"
fi

# Check for cameras section
echo -n "Checking for cameras section... "
if grep -q "^cameras:" "$CONFIG_FILE"; then
    echo -e "${GREEN}OK${NC}"
else
    echo -e "${RED}MISSING${NC}"
    echo "  Configuration must have a 'cameras:' section"
    ((ERRORS++))
fi

# Check for detect settings in cameras
echo -n "Checking detect settings... "
if grep -q "detect:" "$CONFIG_FILE"; then
    echo -e "${GREEN}OK${NC}"
else
    echo -e "${YELLOW}WARNING${NC}"
    echo "  No detect settings found. Cameras need detect width/height/fps configured"
    ((WARNINGS++))
fi

# Check for hardcoded credentials
echo -n "Checking for exposed credentials... "
if grep -Eq "rtsp://[^{]*:[^{]*@" "$CONFIG_FILE"; then
    echo -e "${YELLOW}WARNING${NC}"
    echo "  Hardcoded RTSP credentials detected. Consider using environment variables:"
    echo "  rtsp://{FRIGATE_USER}:{FRIGATE_PASSWORD}@camera_ip:554/stream"
    ((WARNINGS++))
else
    echo -e "${GREEN}OK${NC}"
fi

# Check for localhost in MQTT config
echo -n "Checking MQTT host configuration... "
if grep -Eq "host:.*localhost|host:.*127\.0\.0\.1" "$CONFIG_FILE"; then
    echo -e "${RED}ERROR${NC}"
    echo "  MQTT host set to localhost. This won't work in Docker containers."
    echo "  Use the actual host IP address instead."
    ((ERRORS++))
else
    echo -e "${GREEN}OK${NC}"
fi

# Check for unreasonably high detect resolution
echo -n "Checking detect resolution... "
if grep -Eq "width:\s*(1920|2560|3840|4096)" "$CONFIG_FILE"; then
    if grep -B5 "width:\s*(1920|2560|3840|4096)" "$CONFIG_FILE" | grep -q "detect:"; then
        echo -e "${YELLOW}WARNING${NC}"
        echo "  High detect resolution detected (>1280). This wastes detector capacity."
        echo "  Recommended: 1280x720 or lower for detection"
        ((WARNINGS++))
    else
        echo -e "${GREEN}OK${NC}"
    fi
else
    echo -e "${GREEN}OK${NC}"
fi

# Check for detect fps > 10
echo -n "Checking detect FPS... "
if grep -Eq "fps:\s*([1-9][0-9]|[2-9][0-9])" "$CONFIG_FILE"; then
    if grep -B5 "fps:\s*([1-9][0-9]|[2-9][0-9])" "$CONFIG_FILE" | grep -q "detect:"; then
        echo -e "${YELLOW}WARNING${NC}"
        echo "  Detect FPS may be too high (>10). Recommended: 5 fps for most use cases"
        ((WARNINGS++))
    else
        echo -e "${GREEN}OK${NC}"
    fi
else
    echo -e "${GREEN}OK${NC}"
fi

# Check for detectors section
echo -n "Checking detectors configuration... "
if grep -q "^detectors:" "$CONFIG_FILE"; then
    echo -e "${GREEN}OK${NC}"
else
    echo -e "${YELLOW}WARNING${NC}"
    echo "  No detectors section found. Will use CPU detection (not recommended for production)"
    ((WARNINGS++))
fi

# Check for record enabled but no retain
echo -n "Checking recording retention... "
if grep -q "enabled:\s*[Tt]rue" "$CONFIG_FILE" && grep -q "^record:" "$CONFIG_FILE"; then
    if ! grep -q "retain:" "$CONFIG_FILE"; then
        echo -e "${YELLOW}WARNING${NC}"
        echo "  Recording enabled but no retention policy set. Storage may fill up."
        ((WARNINGS++))
    else
        echo -e "${GREEN}OK${NC}"
    fi
else
    echo -e "${GREEN}OK${NC}"
fi

# Summary
echo ""
echo "================================================"
echo "Validation Summary"
echo "================================================"

if [[ $ERRORS -eq 0 && $WARNINGS -eq 0 ]]; then
    echo -e "${GREEN}All checks passed!${NC}"
    exit 0
elif [[ $ERRORS -eq 0 ]]; then
    echo -e "${YELLOW}$WARNINGS warning(s) found${NC}"
    echo "Configuration should work but review warnings above."
    exit 0
else
    echo -e "${RED}$ERRORS error(s), $WARNINGS warning(s) found${NC}"
    echo "Please fix errors before deploying."
    exit 1
fi
