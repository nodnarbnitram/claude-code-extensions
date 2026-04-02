"""Config flow for Home Assistant integration."""
from typing import Any, Dict, Optional
import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigEntry
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN


class MyIntegrationConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle config flow for my_integration."""

    VERSION = 1
    MINOR_VERSION = 1

    async def async_step_user(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Handle user initiation of config flow.

        Args:
            user_input: Input from user

        Returns:
            Flow result with form or entry creation
        """
        errors = {}

        if user_input is not None:
            # Check for existing entry
            await self.async_set_unique_id(user_input.get("host"))
            self._abort_if_unique_id_configured()

            # Validate user input
            try:
                # TODO: Add validation logic
                # - Test connection
                # - Validate credentials
                # - Fetch initial config
                pass
            except Exception as exc:  # pylint: disable=broad-except
                errors["base"] = "invalid_auth"

            if not errors:
                return self.async_create_entry(
                    title=user_input.get("name", "My Integration"),
                    data=user_input,
                )

        # Show form to user
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("name"): str,
                    vol.Required("host"): str,
                    vol.Optional("api_key"): str,
                }
            ),
            errors=errors,
        )

    async def async_step_reauth(
        self, user_input: Dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle reauth upon API authentication error.

        Args:
            user_input: Input from user

        Returns:
            Flow result with form or entry creation
        """
        config_entry = self.hass.config_entries.async_get_entry(
            self.context["entry_id"]
        )

        if user_input is not None:
            config_entry.data = {**config_entry.data, **user_input}
            self.hass.config_entries.async_update_entry(config_entry)
            return self.async_abort(reason="reauth_successful")

        return self.async_show_form(
            step_id="reauth",
            data_schema=vol.Schema({vol.Required("api_key"): str}),
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: ConfigEntry,
    ) -> "MyIntegrationOptionsFlow":
        """Return options flow."""
        return MyIntegrationOptionsFlow(config_entry)


class MyIntegrationOptionsFlow:
    """Options flow for my_integration."""

    def __init__(self, config_entry: ConfigEntry) -> None:
        """Initialize options flow.

        Args:
            config_entry: The config entry
        """
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Manage integration options.

        Args:
            user_input: Input from user

        Returns:
            Flow result with form or entry creation
        """
        if user_input is not None:
            return FlowResult(
                type="create_entry",
                data=user_input,
            )

        current_options = self.config_entry.options
        return FlowResult(
            type="form",
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        "refresh_rate",
                        default=current_options.get("refresh_rate", 5),
                    ): int,
                }
            ),
        )
