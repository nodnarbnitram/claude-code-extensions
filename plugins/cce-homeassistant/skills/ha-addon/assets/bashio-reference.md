# bashio Helper Functions Reference

bashio is a set of bash helper functions included in Home Assistant base images. It simplifies common operations for add-ons, eliminating the need to hardcode paths or directly call APIs.

**GitHub:** https://github.com/hassio-addons/bashio
**Included in:** All official Home Assistant base images

## Quick Start

Use bashio in your S6 service scripts (`rootfs/etc/s6-overlay/s6-rc.d/*/run`):

```bash
#!/command/execlineb -P
foreground { bashio::log::info "Starting my service" }
/app/my-service
```

Or in standard bash scripts (S6 newer versions):

```bash
#!/bin/bash
source /usr/lib/bashio.sh
bashio::log::info "Service started"
```

## Logging Functions

All logging goes to Home Assistant logs (visible in UI).

### Basic Logging

```bash
bashio::log::info "Informational message"
bashio::log::notice "Important notice"
bashio::log::warning "Warning message"
bashio::log::error "Error message"
bashio::log::debug "Debug message (only if debug enabled)"
bashio::log::red "Red colored text"
bashio::log::green "Green colored text"
bashio::log::yellow "Yellow colored text"
```

### With Context

```bash
# Include add-on UUID for debugging
bashio::log::info "[$(bashio::addon::id)] Service started"

# Include configuration value
bashio::log::info "Using log_level: $(bashio::addon::option 'log_level')"
```

## Configuration Access

### Read Options

```bash
# Get single option
OPTION="$(bashio::addon::option 'debug')"

# Get option with default fallback
OPTION="$(bashio::addon::option 'log_level' 'info')"

# Check if option is true
if bashio::addon::option 'debug'; then
  bashio::log::debug "Debug mode enabled"
fi

# Read JSON configuration
CONFIG="$(bashio::addon::option 'server')"
HOST="$(bashio::jq "${CONFIG}" '.host')"
PORT="$(bashio::jq "${CONFIG}" '.port')"
```

### Get Paths

```bash
# Configuration data path (persisted)
CONFIG_PATH="$(bashio::addon::config_path)"

# Temporary directory
TEMP_PATH="/tmp"

# Add-on UUID (unique identifier)
ADDON_UUID="$(bashio::addon::id)"

# Home Assistant configuration directory
HA_CONFIG="/config"
```

## Supervisor API Access

### Addon Information

```bash
# Get current add-on info
bashio::addon::self_info

# Get all add-ons
bashio::supervisor::addons

# Check if other add-on is installed
bashio::addon::installed "my-other-addon"

# Get specific add-on info
bashio::addon::info "slug-name"
```

### Addon Lifecycle

```bash
# Restart this add-on
bashio::addon::restart

# Stop this add-on
bashio::addon::stop

# Start another add-on
bashio::addon::start "mysql"

# Reload addon (update config)
bashio::addon::reload
```

### Supervisor Info

```bash
# System information
bashio::supervisor::info

# Home Assistant information
bashio::homeassistant::info

# Check Supervisor version
VERSION="$(bashio::supervisor::version)"

# Get update available
bashio::supervisor::update_available
```

### Notifications

```bash
# Send notification to user
bashio::notification::send "Warning" "Something went wrong"

# With more options
curl -X POST \
  -H "Authorization: Bearer ${SUPERVISOR_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Add-On",
    "message": "Something happened",
    "notification_id": "my-addon-1",
    "data": {
      "custom_field": "value"
    }
  }' \
  http://supervisor/notifications/create
```

## Validation Functions

### Check Conditions

```bash
# Check if string is empty
if bashio::var::is_empty "${MY_VAR}"; then
  bashio::log::error "Variable is empty"
fi

# Check if string equals another
if bashio::var::equals "${MY_VAR}" "expected_value"; then
  bashio::log::info "Match!"
fi

# Check if array contains element
if bashio::var::in_array "${VALUE}" "${ARRAY[@]}"; then
  bashio::log::info "Found in array"
fi

# Check if file exists
if bashio::fs::file_exists "/data/config.json"; then
  bashio::log::info "Config found"
fi

# Check if directory exists
if bashio::fs::directory_exists "/data/backups"; then
  bashio::log::info "Backup directory found"
fi
```

## JSON/YAML Processing

### JSON Utilities

```bash
# Parse JSON field
VALUE="$(bashio::jq "${JSON_DATA}" '.field_name')"

# Parse nested JSON
HOST="$(bashio::jq "${JSON_DATA}" '.server.host')"

# Parse array
ITEM="$(bashio::jq "${JSON_DATA}" '.items[0]')"

# Parse with default
VALUE="$(bashio::jq "${JSON_DATA}" '.optional_field // "default"')"

# Pretty print JSON
bashio::jq "${JSON_DATA}"
```

### YAML Utilities

```bash
# Read from YAML configuration
bashio::yaml::read_object "/config/automations.yaml"
```

## Real-World Examples

### Example 1: Read Config and Log

```bash
#!/command/execlineb -P
foreground {
  bashio::log::info "Add-on starting..."
}
foreground {
  define DEBUG "$(bashio::addon::option 'debug')"
  bashio::log::info "Debug mode: ${DEBUG}"
}
foreground {
  define CONFIG_PATH "$(bashio::addon::config_path)"
  bashio::log::info "Using config path: ${CONFIG_PATH}"
}
# Run service
/app/my-service
```

### Example 2: API Communication

```bash
#!/bin/bash
source /usr/lib/bashio.sh

# Get add-on configuration
CONFIG_PATH="$(bashio::addon::config_path)"

# Read custom config
if [ -f "${CONFIG_PATH}/settings.json" ]; then
  SETTINGS="$(cat "${CONFIG_PATH}/settings.json")"
  API_KEY="$(bashio::jq "${SETTINGS}" '.api_key')"
else
  bashio::log::warning "Settings not found, using defaults"
  API_KEY=""
fi

# Communicate with Home Assistant
HASS_INFO="$(bashio::homeassistant::info)"
VERSION="$(bashio::jq "${HASS_INFO}" '.version')"
bashio::log::info "Home Assistant version: ${VERSION}"

# Run service
/app/my-service --api-key="${API_KEY}"
```

### Example 3: Health Check Loop

```bash
#!/bin/bash
source /usr/lib/bashio.sh

# Start service in background
/app/my-service &
SERVICE_PID=$!

bashio::log::info "Service started with PID ${SERVICE_PID}"

# Monitor service
while true; do
  if ! kill -0 "${SERVICE_PID}" 2>/dev/null; then
    bashio::log::error "Service died unexpectedly"
    exit 1
  fi

  if ! curl -f http://localhost:8080/health > /dev/null 2>&1; then
    bashio::log::warning "Health check failed"
  fi

  sleep 30
done

trap "kill ${SERVICE_PID}" SIGTERM
```

## Common Patterns

### Pattern: Configuration Validation

```bash
# Ensure required options are set
if bashio::var::is_empty "$(bashio::addon::option 'api_key')"; then
  bashio::log::error "api_key is required"
  exit 1
fi

bashio::log::info "Configuration valid"
```

### Pattern: Debug Mode Toggle

```bash
if bashio::addon::option 'debug'; then
  # Enable debug logging
  export DEBUG=1
  bashio::log::debug "Debug mode enabled"
else
  export DEBUG=0
fi
```

### Pattern: Directory Initialization

```bash
CONFIG_PATH="$(bashio::addon::config_path)"

# Create required directories
mkdir -p "${CONFIG_PATH}/data"
mkdir -p "${CONFIG_PATH}/logs"

bashio::log::info "Initialized directories in ${CONFIG_PATH}"
```

## Important Notes

### Always Available Environment Variables

Automatically set by Home Assistant:

- `SUPERVISOR_TOKEN` - API authentication token
- `SUPERVISOR_HOST` - Supervisor API host (always `supervisor`)
- `ADDON_UUID` - Unique identifier for this add-on

### Using SUPERVISOR_TOKEN

For direct API calls when bashio helpers don't exist:

```bash
curl -X GET \
  -H "Authorization: Bearer ${SUPERVISOR_TOKEN}" \
  http://supervisor/addons/installed
```

### S6 Overlay Integration

bashio is automatically sourced in S6 scripts. For standard executables:

```bash
# Source bashio in your script
source /usr/lib/bashio.sh

# Now bashio functions are available
bashio::log::info "Ready to go"
```

### Error Handling

bashio functions use exit codes:

```bash
if bashio::addon::self_info > /dev/null 2>&1; then
  bashio::log::info "Successfully retrieved info"
else
  bashio::log::error "Failed to get info"
fi
```

## Troubleshooting

### "bashio: command not found"

**Problem:** bashio not available

**Solution:**
```bash
# Check location
ls -la /usr/lib/bashio.sh

# Source it explicitly
source /usr/lib/bashio.sh
```

### "SUPERVISOR_TOKEN not set"

**Problem:** Token not available in scripts

**Solution:**
- Token is set by Home Assistant automatically
- Make sure you're running inside the Docker container
- Check add-on permissions in config.yaml

### "Permission denied" on API calls

**Problem:** Insufficient permissions

**Solution:**
```yaml
# Add required permissions to config.yaml
permissions:
  - homeassistant    # For HA core access
  - hassio          # For Supervisor API
  - admin           # For system access
```

## Additional Resources

- [bashio GitHub Repository](https://github.com/hassio-addons/bashio)
- [bashio Function Documentation](https://github.com/hassio-addons/bashio/blob/master/README.md)
- [Home Assistant Supervisor API](https://developers.home-assistant.io/docs/supervisor/developing)
- [S6 Overlay Init System](https://skarnet.org/software/s6-overlay/)
