# Home Assistant API Integration

> Master Home Assistant's REST and WebSocket APIs for external integration, state management, and real-time communication.

| | |
|---|---|
| **Status** | Production Ready |
| **Version** | 1.0.0 |
| **Last Updated** | 2025-12-31 |
| **Confidence** | 5/5 |
| **Home Assistant Version** | 2021.1+ |

## What This Skill Does

This skill provides comprehensive guidance for integrating with Home Assistant's REST and WebSocket APIs. It covers authentication, state management, service calls, event subscriptions, and real-time communication patterns. Includes code examples in Python (requests, aiohttp), JavaScript (fetch, WebSocket), and cURL for common operations.

### Core Capabilities

- **REST API Integration** - HTTP endpoints for states, services, events, history, config, and templates
- **WebSocket API Mastery** - Real-time event subscriptions, service calls, state queries with persistent connections
- **Authentication Setup** - Long-Lived Access Token creation, Bearer token management, security best practices
- **State Management** - Reading, creating, updating entity states with proper attribute handling
- **Service Calls** - Discovering and calling Home Assistant services with correct domain/service routing
- **Error Handling** - Comprehensive error response patterns (401, 404, 502, etc.) with recovery strategies

## Auto-Trigger Keywords

### Primary Keywords
These terms strongly trigger this skill:
- REST API
- WebSocket
- API endpoint
- service call
- access token
- Bearer token
- subscribe_events
- Home Assistant API
- entity state
- service domain

### Secondary Keywords
Related terms that may trigger in combination:
- authentication
- state management
- API integration
- integration code
- HTTP client
- external integration
- state subscription
- real-time events
- Home Assistant integration
- API endpoint documentation

### Error-Based Keywords
Common error messages that should trigger this skill:
- "401 Unauthorized"
- "404 Not Found"
- "HTTP 502 Bad Gateway"
- "auth_required"
- "WebSocket closed"
- "Bearer token"
- "entity not found"
- "service call failed"
- "state format"
- "token invalid"

## Known Issues Prevention

| Issue | Root Cause | Solution |
|-------|-----------|----------|
| 401 Authorization errors | Token invalid, expired, or missing Bearer prefix | Create new token in Settings; verify "Bearer " prefix in Authorization header (exact spacing) |
| WebSocket immediate close | Missing auth_required handling or timeout | Respond to auth_required message within 10 seconds with Bearer token |
| State attribute confusion | Mixing entity state string with attributes object | Remember: state is always a string (e.g., "on", "23.5"); attributes contain metadata |
| Service call silent failure | Incorrect domain/service format or wrong entity_id | Verify with `GET /api/services/{domain}`; use entity_id in JSON payload, not path |
| Connection timeouts | Home Assistant unreachable or firewall blocking | Verify URL (http not https), port 8123 open, HA instance running and accessible |

## When to Use

### Use This Skill For
- Making HTTP REST API calls to Home Assistant (get/set states, call services)
- Establishing WebSocket connections for real-time event monitoring
- Setting up authentication with Long-Lived Access Tokens
- Debugging API integration issues (404, 401, 502 errors)
- Writing Python (requests, aiohttp) or JavaScript (fetch, WebSocket) integration code
- Understanding service discovery and schema
- Managing entity states programmatically
- Implementing automated Home Assistant interactions

### Don't Use This Skill For
- Building Home Assistant automations (use Automation skill instead)
- Creating Home Assistant custom integrations (use Integration skill)
- Configuring Home Assistant dashboard cards (use ha-dashboard skill)
- Voice assistant configuration (use ha-voice skill)
- Low-level ESPHome device configuration

## Quick Usage

```bash
# Set up environment
export HA_URL="http://192.168.1.100:8123"
export HA_TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# Get all entity states
curl -X GET "${HA_URL}/api/states" \
  -H "Authorization: Bearer ${HA_TOKEN}"

# Call a service
curl -X POST "${HA_URL}/api/services/light/turn_on" \
  -H "Authorization: Bearer ${HA_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "light.living_room", "brightness": 200}'
```

## Token Efficiency

| Approach | Estimated Tokens | Time |
|----------|-----------------|------|
| Manual API Discovery | 2500+ | 20-30 minutes |
| With This Skill | 800-1200 | 2-5 minutes |
| **Savings** | **~65% less** | **~80% faster** |

The skill provides pre-written code examples, error handling patterns, and authentication setup that would otherwise require multiple API docs reads and trial-and-error debugging.

## File Structure

```
ha-api/
├── SKILL.md              # Detailed instructions, API reference, code examples
├── README.md             # This file - discovery and quick reference
├── references/           # Supporting documentation
│   ├── REST_API_REFERENCE.md
│   ├── WEBSOCKET_API_REFERENCE.md
│   ├── AUTHENTICATION.md
│   └── SERVICE_CATALOG.md
└── assets/               # Code templates
    ├── python_rest_example.py
    ├── python_websocket_example.py
    ├── javascript_rest_example.js
    └── javascript_websocket_example.js
```

## Dependencies

| Package | Language | Version | Verified |
|---------|----------|---------|----------|
| requests | Python | 2.25+ | 2025-12-31 |
| aiohttp | Python | 3.8+ | 2025-12-31 |
| fetch | JavaScript | Native API | 2025-12-31 |
| WebSocket | JavaScript | Native API | 2025-12-31 |

Install Python packages:
```bash
pip install requests aiohttp
```

## Official Documentation

- [Home Assistant REST API](https://developers.home-assistant.io/docs/api/rest)
- [Home Assistant WebSocket API](https://developers.home-assistant.io/docs/api/websocket)
- [Home Assistant Authentication](https://developers.home-assistant.io/docs/auth_api)
- [Home Assistant Integration API](https://www.home-assistant.io/integrations/api/)
- [Home Assistant Developer Documentation](https://developers.home-assistant.io/)

## Related Skills

- `ha-dashboard` - Configure Home Assistant Lovelace dashboards and cards
- `ha-voice` - Set up voice assistants and voice interaction
- `esphome-config-helper` - Configure ESPHome devices that integrate with Home Assistant

---

**License:** MIT

**Maintainer:** Claude Code Extensions Contributors

**Last Verified:** 2025-12-31 with Home Assistant 2025.1.0
