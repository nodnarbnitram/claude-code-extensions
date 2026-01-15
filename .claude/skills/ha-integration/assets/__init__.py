"""Home Assistant custom integration."""
import asyncio
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .coordinator import MyDataUpdateCoordinator

DOMAIN = "my_integration"
PLATFORMS = ["sensor"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the integration from config entry.

    Args:
        hass: Home Assistant instance
        entry: Config entry created by config flow

    Returns:
        True if setup was successful
    """
    hass.data.setdefault(DOMAIN, {})

    # Create and setup coordinator
    coordinator = MyDataUpdateCoordinator(hass, entry)

    try:
        await coordinator.async_config_entry_first_refresh()
    except ConfigEntryNotReady as err:
        raise ConfigEntryNotReady("Failed to fetch initial data") from err

    hass.data[DOMAIN][entry.entry_id] = coordinator

    # Forward setup to platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry.

    Args:
        hass: Home Assistant instance
        entry: Config entry to unload

    Returns:
        True if unload was successful
    """
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
