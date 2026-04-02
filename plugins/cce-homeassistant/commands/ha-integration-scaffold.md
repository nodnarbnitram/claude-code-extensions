---
description: Generate boilerplate for a new Home Assistant custom integration
argument-hint: <domain> [--with-config-flow] [--platforms sensor,switch,...]
allowed-tools: Write, Bash
---

# Home Assistant Integration Scaffold

Generate boilerplate files for a new Home Assistant custom integration.

**Arguments**: $ARGUMENTS

**Important**:
- First argument: **domain** (kebab-case identifier, e.g., `my-integration`)
- Optional flags:
  - `--with-config-flow`: Include config_flow.py for UI-based configuration
  - `--platforms`: Comma-separated list of platforms (e.g., `sensor,switch,light`)

## Your Task

Follow these steps to scaffold the Home Assistant integration:

### Step 1: Parse Arguments

Extract from $ARGUMENTS:
- **Domain**: The first argument (kebab-case identifier, e.g., `my-integration`)
- **Config Flow Flag**: Check for `--with-config-flow` (optional)
- **Platforms**: Extract from `--platforms sensor,switch,...` (optional)

Examples:
- `/ha-integration-scaffold my-device`
- `/ha-integration-scaffold weather-api --with-config-flow`
- `/ha-integration-scaffold smart-lights --platforms sensor,switch,light`
- `/ha-integration-scaffold iot-hub --with-config-flow --platforms sensor,binary_sensor`

### Step 2: Validate Domain

- Must be kebab-case (lowercase letters and hyphens only)
- Convert underscores to hyphens if needed
- Store as both kebab-case (domain) and snake_case (for Python module name)
  - Domain: `my-integration`
  - Python module: `my_integration`

### Step 3: Generate manifest.json

Create `custom_components/<domain>/manifest.json` with:

```json
{
  "domain": "domain-name",
  "name": "Domain Name",
  "codeowners": ["@username"],
  "config_entries_only": true,
  "documentation": "https://github.com/username/ha-domain-name",
  "homeassistant": "2024.1.0",
  "iot_class": "cloud_polling",
  "issue_tracker": "https://github.com/username/ha-domain-name/issues",
  "requirements": [],
  "version": "1.0.0"
}
```

**Key points**:
- `domain`: Use the kebab-case version (e.g., `my-integration`)
- `name`: Title-case version (e.g., `My Integration`)
- `homeassistant`: Set to a recent stable version (e.g., `2024.1.0`)
- `iot_class`: Choose appropriate class:
  - `local_polling`: Local network, polling
  - `cloud_polling`: Cloud API, polling
  - `local_push`: Local network, push updates
  - `cloud_push`: Cloud API, push updates
- `config_entries_only`: Set to `true` (required for modern integrations)
- `requirements`: Empty array initially (add dependencies as needed)

### Step 4: Generate __init__.py

Create `custom_components/<domain>/__init__.py` with:

```python
"""The {name} integration."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

DOMAIN = "{domain}"
PLATFORMS: list[Platform] = []


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up {name} from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {}

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
```

**Key points**:
- Use `{domain}` placeholder (replace with actual domain)
- Use `{name}` placeholder (replace with title-case name)
- `PLATFORMS` list will be populated based on `--platforms` flag
- Include async setup/unload entry methods
- Include proper type hints

### Step 5: Generate config_flow.py (if --with-config-flow)

If `--with-config-flow` is specified, create `custom_components/<domain>/config_flow.py`:

```python
"""Config flow for {name} integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required("host"): str,
        vol.Optional("name", default="My Device"): str,
    }
)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for {name}."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            # TODO: Validate the user input
            # Add entry
            return self.async_create_entry(
                title=user_input.get("name", "My Device"), data=user_input
            )

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )
```

**Key points**:
- Include voluptuous schema for configuration validation
- Implement `async_step_user` for initial setup
- Include TODO comment for validation logic
- Set appropriate `VERSION` number

Also create `custom_components/<domain>/const.py`:

```python
"""Constants for the {name} integration."""
from __future__ import annotations

DOMAIN = "{domain}"
```

### Step 6: Generate Platform Stubs (if --platforms specified)

For each platform in `--platforms sensor,switch,...`, create a stub file `custom_components/<domain>/<platform>.py`:

```python
"""<Platform Title> platform for {name} integration."""
from __future__ import annotations

import logging

from homeassistant.components.<platform> import <PlatformClass>
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

_LOGGER = logging.getLogger(__name__)

DOMAIN = "{domain}"


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up {name} {platform} platform."""
    # TODO: Implement entity setup
    pass
```

**Key points**:
- Platform mapping (sensor → SensorEntity, switch → SwitchEntity, light → LightEntity, etc.)
- Use proper Home Assistant import paths
- Include async_setup_entry function
- Add TODO comment for implementation

### Step 7: Directory Structure

Create the following directory structure:

```
custom_components/
└── <domain>/
    ├── __init__.py
    ├── manifest.json
    ├── const.py                 (if --with-config-flow)
    ├── config_flow.py           (if --with-config-flow)
    └── <platform>.py            (one per platform in --platforms)
```

### Step 8: Output Summary

Generate a summary report including:
- Path to created integration directory
- Domain name (kebab-case)
- Integration name (title-case)
- Files created:
  - manifest.json
  - __init__.py
  - const.py (if config flow included)
  - config_flow.py (if config flow included)
  - List of platform files created
- Next steps for development:
  - Replace TODO comments with actual implementation
  - Add device coordinator if polling external APIs
  - Implement entity properties (device_class, state_class, native_value)
  - Add configuration validation in config_flow
  - Register devices with device registry
  - Test with Home Assistant development instance

## Important Notes

- **Python Module Naming**: The domain uses kebab-case, but Python module paths use snake_case (automatic conversion)
- **Manifest Domain**: Always use the kebab-case version in manifest.json `"domain"` field
- **Config Flow**: Only include if integration needs UI-based configuration
- **Platforms**: Each platform gets its own file under the integration directory
- **Type Hints**: All generated code uses Python type hints for clarity
- **Async/Await**: All Home Assistant integration code is async
- **Constants**: Store integration domain in const.py when config_flow is included
