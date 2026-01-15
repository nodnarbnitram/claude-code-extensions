"""Sensor platform for Home Assistant integration."""
from typing import Any

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import MyDataUpdateCoordinator
from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up sensor platform from config entry.

    Args:
        hass: Home Assistant instance
        entry: Config entry
        async_add_entities: Callback to add entities
    """
    coordinator: MyDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    # Create sensor entities
    sensors = [
        MySensor(coordinator, 0),
        MySensor(coordinator, 1),
    ]

    async_add_entities(sensors)


class MySensor(SensorEntity):
    """Custom sensor entity."""

    _attr_device_class = "temperature"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS

    def __init__(self, coordinator: MyDataUpdateCoordinator, idx: int) -> None:
        """Initialize sensor.

        Args:
            coordinator: Data coordinator
            idx: Sensor index
        """
        self.coordinator = coordinator
        self._idx = idx

    @property
    def unique_id(self) -> str:
        """Return unique ID for the entity.

        Returns:
            Unique identifier
        """
        # Use a stable identifier from coordinator data
        device_id = self.coordinator.data.get("id", "unknown")
        return f"{device_id}_sensor_{self._idx}"

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information.

        Returns:
            Device information dictionary
        """
        device_id = self.coordinator.data.get("id", "unknown")
        return DeviceInfo(
            identifiers={(DOMAIN, device_id)},
            name=self.coordinator.data.get("name", "My Device"),
            manufacturer="My Company",
            model="Model Name",
        )

    @property
    def name(self) -> str:
        """Return entity name.

        Returns:
            Entity name
        """
        return f"Temperature Sensor {self._idx}"

    @property
    def native_value(self) -> float | None:
        """Return sensor value.

        Returns:
            Current sensor value or None
        """
        try:
            data = self.coordinator.data.get("sensors", [])
            if self._idx < len(data):
                return float(data[self._idx]["temperature"])
        except (KeyError, TypeError, ValueError):
            pass
        return None

    @property
    def available(self) -> bool:
        """Return if entity is available.

        Returns:
            True if available
        """
        return self.coordinator.last_update_success

    async def async_added_to_hass(self) -> None:
        """Connect to coordinator when added to hass.

        This ensures entity updates when coordinator updates.
        """
        await super().async_added_to_hass()
        self.async_on_remove(
            self.coordinator.async_add_listener(self._handle_coordinator_update)
        )

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from coordinator.

        This is called when the coordinator updates.
        """
        self.async_write_ha_state()
