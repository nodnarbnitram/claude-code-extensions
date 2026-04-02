# Config Flow Patterns Reference

Advanced patterns for Home Assistant config flow implementation.

## Basic Config Flow Structure

```python
from homeassistant.config_entries import ConfigFlow
import voluptuous as vol

class MyConfigFlow(ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """User-initiated config flow."""
        if user_input is not None:
            # Process input
            return self.async_create_entry(title="...", data=user_input)

        # Show form
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({...})
        )
```

## Validation Patterns

### Basic Validation

```python
async def async_step_user(self, user_input=None):
    errors = {}

    if user_input is not None:
        try:
            # Validate input
            await self._validate_input(user_input)
        except ValueError as err:
            errors["base"] = "invalid_value"
        except ConnectionError as err:
            errors["base"] = "cannot_connect"
        except AuthenticationError as err:
            errors["base"] = "invalid_auth"

        if not errors:
            return self.async_create_entry(title="...", data=user_input)

    return self.async_show_form(
        step_id="user",
        data_schema=...,
        errors=errors
    )
```

### Volume Schema Validation

```python
import voluptuous as vol

vol.Schema({
    vol.Required("host"): vol.All(str, vol.Length(min=5, max=100)),
    vol.Required("port"): vol.Range(min=1, max=65535),
    vol.Optional("name"): str,
})
```

### Custom Validators

```python
def validate_hostname(value: str) -> str:
    """Validate hostname format."""
    if not all(c.isalnum() or c in '-.' for c in value):
        raise vol.Invalid("Invalid hostname")
    return value

vol.Schema({
    vol.Required("host"): validate_hostname,
})
```

## Multi-Step Flows

### Two-Step Flow

```python
async def async_step_user(self, user_input=None):
    """First step: get basic info."""
    if user_input is not None:
        self.data = user_input
        return await self.async_step_advanced()

    return self.async_show_form(
        step_id="user",
        data_schema=vol.Schema({
            vol.Required("host"): str,
        })
    )

async def async_step_advanced(self, user_input=None):
    """Second step: get advanced settings."""
    if user_input is not None:
        return self.async_create_entry(
            title=self.data["host"],
            data={**self.data, **user_input}
        )

    return self.async_show_form(
        step_id="advanced",
        data_schema=vol.Schema({
            vol.Optional("port", default=8080): int,
        })
    )
```

## Reauth Flow

### Handling Expired Credentials

```python
async def async_step_reauth(self, user_input=None):
    """Handle reauth upon API authentication error."""
    config_entry = self.hass.config_entries.async_get_entry(
        self.context["entry_id"]
    )

    errors = {}

    if user_input is not None:
        try:
            await self._validate_input({
                **config_entry.data,
                **user_input
            })
        except AuthenticationError:
            errors["base"] = "invalid_auth"

        if not errors:
            self.hass.config_entries.async_update_entry(
                config_entry,
                data={**config_entry.data, **user_input}
            )
            return self.async_abort(reason="reauth_successful")

    return self.async_show_form(
        step_id="reauth",
        data_schema=vol.Schema({
            vol.Required("api_key"): str,
        }),
        errors=errors,
    )
```

## Options Flow

### Basic Options Flow

```python
class MyOptionsFlow:
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage options."""
        if user_input is not None:
            return self.async_create_entry(
                title="",
                data=user_input
            )

        current_options = self.config_entry.options
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Optional(
                    "refresh_rate",
                    default=current_options.get("refresh_rate", 5)
                ): int,
                vol.Optional(
                    "enable_advanced",
                    default=current_options.get("enable_advanced", False)
                ): bool,
            })
        )

@staticmethod
@callback
def async_get_options_flow(config_entry):
    return MyOptionsFlow(config_entry)
```

## Single Instance Flow

### Prevent Multiple Instances

```python
async def async_step_user(self, user_input=None):
    """Prevent multiple instances."""
    # Check for existing entry
    await self.async_set_unique_id(user_input.get("host"))
    self._abort_if_unique_id_configured()

    # Rest of flow...
```

## Import Flow

### Importing from YAML

```python
async def async_step_import(self, import_data):
    """Import from configuration.yaml."""
    return await self.async_step_user(import_data)
```

## Error Messages

### Standard Error Strings

```python
# Authentication errors
errors["base"] = "invalid_auth"       # Wrong credentials
errors["base"] = "invalid_apikey"     # Invalid API key

# Connection errors
errors["base"] = "cannot_connect"     # Cannot reach host
errors["base"] = "connection_timeout" # Timeout

# Validation errors
errors["base"] = "invalid_value"      # Invalid input value
errors["base"] = "already_configured" # Entry already exists

# Custom errors (define in strings.json)
errors["base"] = "custom_error"
```

## Discovery Flow

### Discovering Devices

```python
async def async_step_discovery_confirm(self, discovery_info=None):
    """Confirm discovered device."""
    if user_input is not None:
        return self.async_create_entry(
            title=discovery_info["name"],
            data=discovery_info
        )

    return self.async_show_form(
        step_id="discovery_confirm",
        description_placeholders={
            "name": discovery_info["name"]
        }
    )
```

## Advanced Validators

### Enum Validation

```python
vol.In(["option1", "option2", "option3"])
```

### URL Validation

```python
vol.Url()
```

### Email Validation

```python
vol.Email()
```

### Custom Async Validator

```python
async def validate_async(value):
    """Validate with async operation."""
    # Can use await here
    result = await some_async_call(value)
    if not result:
        raise vol.Invalid("Invalid")
    return value

# Use in schema
vol.Schema({
    vol.Required("field"): validate_async,
})
```

## Context Handling

### Storing Context

```python
self.context["reason"] = "user"  # Store custom context
self.context["entry_id"] = "..."  # For reauth flows
```

### Retrieving Context

```python
reason = self.context.get("reason")
entry_id = self.context.get("entry_id")
```

## Translations and Descriptions

### Using Placeholder Descriptions

```python
return self.async_show_form(
    step_id="user",
    data_schema=...,
    description_placeholders={
        "device_name": "My Device",
        "manufacturer": "ACME Corp"
    }
)
```

### Error Messages (in strings.json)

```json
{
  "error": {
    "invalid_auth": "Invalid authentication credentials",
    "cannot_connect": "Failed to connect to device",
    "custom_error": "Custom error message"
  }
}
```
