# Home Assistant Supervisor API Reference

The Supervisor API allows add-ons to communicate with the Home Assistant system, query add-on status, manage other add-ons, and send notifications.

**Official Documentation:** https://developers.home-assistant.io/docs/supervisor/developing

## Quick Start

All API calls:
- Base URL: `http://supervisor`
- Authentication: `Authorization: Bearer ${SUPERVISOR_TOKEN}` header
- Content-Type: `application/json`
- Response format: JSON

The `SUPERVISOR_TOKEN` environment variable is automatically set by Home Assistant.

## Core Endpoints

### System Information

#### Get Supervisor Info

```bash
curl -X GET \
  -H "Authorization: Bearer ${SUPERVISOR_TOKEN}" \
  http://supervisor/info
```

Response:
```json
{
  "version": "2024.12.0",
  "arch": "amd64",
  "timezone": "Europe/Amsterdam",
  "homeassistant_version": "2024.12.0",
  "machine": "raspberrypi4",
  "update_available": false
}
```

#### Get Home Assistant Info

```bash
curl -X GET \
  -H "Authorization: Bearer ${SUPERVISOR_TOKEN}" \
  http://supervisor/homeassistant/info
```

Response:
```json
{
  "version": "2024.12.0",
  "update_available": true,
  "machine": "raspberrypi4",
  "timezone": "Europe/Amsterdam",
  "logging_level": "INFO"
}
```

### Add-On Management

#### Get Current Add-On Info

Retrieve details about the add-on making the request:

```bash
curl -X GET \
  -H "Authorization: Bearer ${SUPERVISOR_TOKEN}" \
  http://supervisor/addons/self/info
```

Response:
```json
{
  "name": "My Add-On",
  "slug": "my-addon",
  "version": "1.0.0",
  "uuid": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "state": "started",
  "enabled": true,
  "options": {
    "debug": false,
    "log_level": "info"
  }
}
```

#### Get All Add-Ons

```bash
curl -X GET \
  -H "Authorization: Bearer ${SUPERVISOR_TOKEN}" \
  http://supervisor/addons
```

Response:
```json
{
  "addons": [
    {
      "name": "SSH Add-On",
      "slug": "ssh",
      "state": "started",
      "update_available": false
    },
    {
      "name": "My Add-On",
      "slug": "my-addon",
      "state": "started",
      "update_available": false
    }
  ]
}
```

#### Get Specific Add-On Info

```bash
curl -X GET \
  -H "Authorization: Bearer ${SUPERVISOR_TOKEN}" \
  http://supervisor/addons/mysql/info
```

#### Start Add-On

```bash
curl -X POST \
  -H "Authorization: Bearer ${SUPERVISOR_TOKEN}" \
  http://supervisor/addons/mysql/start
```

#### Stop Add-On

```bash
curl -X POST \
  -H "Authorization: Bearer ${SUPERVISOR_TOKEN}" \
  http://supervisor/addons/mysql/stop
```

#### Restart Add-On

```bash
curl -X POST \
  -H "Authorization: Bearer ${SUPERVISOR_TOKEN}" \
  http://supervisor/addons/mysql/restart
```

#### Get Add-On Logs

```bash
curl -X GET \
  -H "Authorization: Bearer ${SUPERVISOR_TOKEN}" \
  http://supervisor/addons/mysql/logs
```

#### Update Add-On Configuration

```bash
curl -X POST \
  -H "Authorization: Bearer ${SUPERVISOR_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "boot": "auto",
    "auto_update": true
  }' \
  http://supervisor/addons/mysql/options
```

## Add-On Lifecycle

### Restart This Add-On

```bash
curl -X POST \
  -H "Authorization: Bearer ${SUPERVISOR_TOKEN}" \
  http://supervisor/addons/self/restart
```

### Stop This Add-On

```bash
curl -X POST \
  -H "Authorization: Bearer ${SUPERVISOR_TOKEN}" \
  http://supervisor/addons/self/stop
```

### Update This Add-On Configuration

```bash
curl -X POST \
  -H "Authorization: Bearer ${SUPERVISOR_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "boot": "auto",
    "auto_update": false,
    "options": {
      "debug": true,
      "log_level": "debug"
    }
  }' \
  http://supervisor/addons/self/options
```

## Home Assistant API

### Get Home Assistant State

Query Home Assistant entity states:

```bash
curl -X GET \
  -H "Authorization: Bearer ${SUPERVISOR_TOKEN}" \
  http://supervisor/homeassistant/api/states
```

### Call Home Assistant Service

```bash
curl -X POST \
  -H "Authorization: Bearer ${SUPERVISOR_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "entity_id": "light.living_room",
    "brightness": 255
  }' \
  http://supervisor/homeassistant/api/services/light/turn_on
```

## Notifications

### Send Notification

Send a notification to Home Assistant UI:

```bash
curl -X POST \
  -H "Authorization: Bearer ${SUPERVISOR_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Add-On",
    "message": "Something important happened",
    "notification_id": "my-addon-event-1",
    "data": {
      "custom_field": "custom_value"
    }
  }' \
  http://supervisor/notifications/create
```

Parameters:
- `title`: Notification title
- `message`: Notification message body
- `notification_id`: Unique identifier to prevent duplicates
- `data`: Optional custom fields

## Logs & Debugging

### Get Add-On Logs

```bash
# Get current add-on logs
curl -X GET \
  -H "Authorization: Bearer ${SUPERVISOR_TOKEN}" \
  http://supervisor/addons/self/logs

# Get other add-on logs
curl -X GET \
  -H "Authorization: Bearer ${SUPERVISOR_TOKEN}" \
  http://supervisor/addons/mysql/logs
```

### Get Supervisor Logs

```bash
curl -X GET \
  -H "Authorization: Bearer ${SUPERVISOR_TOKEN}" \
  http://supervisor/logs
```

## Environment Variables

Home Assistant automatically sets these in add-on containers:

| Variable | Value | Example |
|----------|-------|---------|
| `SUPERVISOR_TOKEN` | Authentication token | `eyJ0...` (JWT) |
| `SUPERVISOR_HOST` | Supervisor hostname | `supervisor` |
| `SUPERVISOR_API_ENDPOINT` | API base URL | `http://supervisor` |

## Error Handling

API responses use standard HTTP status codes:

```bash
# Success (200, 201)
curl -w "\n%{http_code}\n" \
  -X GET \
  -H "Authorization: Bearer ${SUPERVISOR_TOKEN}" \
  http://supervisor/info

# Common errors:
# 200 OK
# 201 Created
# 400 Bad Request (invalid JSON)
# 401 Unauthorized (missing/invalid token)
# 404 Not Found (add-on doesn't exist)
# 500 Internal Error (supervisor error)
```

### Parse Error Response

```bash
response=$(curl -s -X GET \
  -H "Authorization: Bearer ${SUPERVISOR_TOKEN}" \
  http://supervisor/addons/nonexistent/info)

if echo "${response}" | grep -q "error"; then
  error=$(echo "${response}" | jq -r '.error')
  echo "Error: ${error}"
  exit 1
fi
```

## Real-World Examples

### Monitor Another Add-On

```bash
#!/bin/bash
# Check if MySQL is running

TOKEN="${SUPERVISOR_TOKEN}"
ADDON="mysql"

info=$(curl -s -X GET \
  -H "Authorization: Bearer ${TOKEN}" \
  http://supervisor/addons/${ADDON}/info)

state=$(echo "${info}" | jq -r '.state')

if [ "${state}" = "started" ]; then
  echo "MySQL is running"
else
  echo "MySQL is ${state}, starting it..."
  curl -X POST \
    -H "Authorization: Bearer ${TOKEN}" \
    http://supervisor/addons/${ADDON}/start
fi
```

### Send Alert on Startup

```bash
#!/bin/bash
# Notify user when add-on starts

TOKEN="${SUPERVISOR_TOKEN}"

curl -X POST \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Add-On",
    "message": "Started successfully",
    "notification_id": "my-addon-started"
  }' \
  http://supervisor/notifications/create
```

### Get System Information

```bash
#!/bin/bash
# Log system info on startup

TOKEN="${SUPERVISOR_TOKEN}"

info=$(curl -s -X GET \
  -H "Authorization: Bearer ${TOKEN}" \
  http://supervisor/info)

version=$(echo "${info}" | jq -r '.version')
machine=$(echo "${info}" | jq -r '.machine')
timezone=$(echo "${info}" | jq -r '.timezone')

echo "Supervisor: ${version}"
echo "Machine: ${machine}"
echo "Timezone: ${timezone}"
```

### Restart on Configuration Update

```bash
#!/bin/bash
# Watch for configuration changes and restart add-on

TOKEN="${SUPERVISOR_TOKEN}"
ADDON_SLUG="my-addon"

while true; do
  sleep 60

  info=$(curl -s -X GET \
    -H "Authorization: Bearer ${TOKEN}" \
    http://supervisor/addons/${ADDON_SLUG}/info)

  # Check if configuration changed
  # (Implementation depends on your needs)

  # Restart if needed
  # curl -X POST \
  #   -H "Authorization: Bearer ${TOKEN}" \
  #   http://supervisor/addons/${ADDON_SLUG}/restart
done
```

## Using bashio Helpers

bashio provides wrapper functions around these endpoints:

```bash
# Instead of: curl -X GET ... /addons/self/info
bashio::addon::self_info

# Instead of: curl -X POST ... /addons/mysql/restart
bashio::addon::restart "mysql"

# Instead of: curl -X POST ... /notifications/create
bashio::notification::send "Title" "Message"
```

Prefer bashio helpers when available - they handle authentication and parsing automatically.

## Permissions Required

Each endpoint requires specific permissions in config.yaml:

```yaml
permissions:
  homeassistant  # HA state queries, service calls
  hassio         # Supervisor API access
  admin          # System-level operations
  backup         # Backup operations
  manager        # Broader add-on management
```

## Rate Limiting

- No explicit rate limits documented
- Use reasonable intervals (1+ second between API calls)
- Batch operations when possible
- Cache responses to reduce API calls

## Troubleshooting

### "401 Unauthorized"

```bash
# Verify token is set
echo $SUPERVISOR_TOKEN

# Check permissions in config.yaml
# Add 'hassio' if calling Supervisor API endpoints
permissions:
  - hassio
```

### "Connection refused"

```bash
# Verify hostname (always use 'supervisor')
# Verify you're inside the Docker container
# Add hostname 'supervisor' to add-on Docker network
```

### "Invalid JSON response"

```bash
# Verify Content-Type header is set
# Verify JSON payload is valid
# Check API response for error messages:
curl -s ... | jq .
```

## References

- [Supervisor API Docs](https://developers.home-assistant.io/docs/supervisor/developing)
- [bashio Helpers](https://github.com/hassio-addons/bashio)
- [Add-On Development Guide](https://developers.home-assistant.io/docs/add-ons)
