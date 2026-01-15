# Entity Base Classes Reference

Complete reference for Home Assistant entity base classes and properties.

## SensorEntity

### Properties

#### native_value (Required)
- **Type:** Any
- **Description:** Current sensor value
- **Returns:** Sensor measurement or None
- **Example:** `42.5` for temperature, `"on"` for binary value

#### native_unit_of_measurement
- **Type:** str
- **Description:** Unit of measurement for the sensor
- **Example:** `"°C"`, `"W"`, `"%"`

#### state_class
- **Type:** SensorStateClass
- **Values:** `MEASUREMENT`, `TOTAL`, `TOTAL_INCREASING`
- **Description:** Classification of the sensor's numeric value
- **Rules:**
  - `MEASUREMENT`: Instantaneous value (temperature, humidity, power)
  - `TOTAL`: Cumulative value that can reset (water used today)
  - `TOTAL_INCREASING`: Cumulative value that only increases (lifetime energy)

#### device_class
- **Type:** str
- **Description:** Type of measurement
- **Values:** `"temperature"`, `"humidity"`, `"pressure"`, `"power"`, `"energy"`, etc.

### Example

```python
from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.const import UnitOfTemperature

class TemperatureSensor(SensorEntity):
    _attr_device_class = "temperature"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS

    @property
    def native_value(self) -> float | None:
        return self.coordinator.data.get("temperature")
```

## BinarySensorEntity

### Properties

#### is_on (Required)
- **Type:** bool | None
- **Description:** Current binary state
- **True:** Detected/Active
- **False:** Not detected/Inactive
- **None:** Unknown

#### device_class
- **Type:** str
- **Values:** `"motion"`, `"door"`, `"window"`, `"occupancy"`, etc.

### Example

```python
from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass

class MotionSensor(BinarySensorEntity):
    _attr_device_class = BinarySensorDeviceClass.MOTION

    @property
    def is_on(self) -> bool | None:
        return self.coordinator.data.get("motion")
```

## SwitchEntity

### Properties

#### is_on (Required)
- **Type:** bool | None
- **Description:** Current switch state
- **True:** On/Enabled
- **False:** Off/Disabled
- **None:** Unknown

#### turn_on()
- **Type:** async method
- **Description:** Turn on the switch
- **Implementation:** Call API to turn on

#### turn_off()
- **Type:** async method
- **Description:** Turn off the switch
- **Implementation:** Call API to turn off

### Example

```python
from homeassistant.components.switch import SwitchEntity

class MySwitch(SwitchEntity):
    @property
    def is_on(self) -> bool | None:
        return self.coordinator.data.get("state")

    async def async_turn_on(self, **kwargs) -> None:
        await self.coordinator.hass.data[DOMAIN]["api"].turn_on(self.unique_id)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs) -> None:
        await self.coordinator.hass.data[DOMAIN]["api"].turn_off(self.unique_id)
        await self.coordinator.async_request_refresh()
```

## Entity (Base Class)

### Properties

#### unique_id (Required for integration)
- **Type:** str
- **Description:** Unique identifier for the entity
- **Must be:** Stable across restarts
- **Usage:** Prevents duplicate entities

#### device_info
- **Type:** DeviceInfo dict
- **Description:** Links entity to device in device registry
- **Required fields:**
  - `identifiers`: Set of (domain, device_id) tuples
  - `name`: Device name

#### name
- **Type:** str
- **Description:** Entity name
- **Default:** Derived from class name

#### available
- **Type:** bool
- **Description:** Whether entity is available
- **Default:** True

#### should_poll
- **Type:** bool
- **Description:** Whether Home Assistant should poll for updates
- **Default:** True (for non-coordinator entities)
- **Note:** Set to False when using coordinator

#### enabled_default
- **Type:** bool
- **Description:** Whether entity is enabled by default
- **Default:** True

### Lifecycle Hooks

#### async_added_to_hass()
- **Called:** When entity is added to Home Assistant
- **Usage:** Subscribe to coordinator updates
- **Example:**
```python
async def async_added_to_hass(self) -> None:
    await super().async_added_to_hass()
    self.async_on_remove(
        self.coordinator.async_add_listener(self._handle_coordinator_update)
    )
```

#### async_will_remove_from_hass()
- **Called:** Before entity is removed
- **Usage:** Cleanup resources
- **Example:**
```python
async def async_will_remove_from_hass(self) -> None:
    # Cleanup resources
    await super().async_will_remove_from_hass()
```

## Entity Attributes

### States

#### state (Read-only)
- **Type:** str
- **Description:** Current state string
- **Format:** Depends on entity type
- **Example:** `"42.5"` for sensor, `"on"` for switch

#### attributes
- **Type:** dict
- **Description:** Additional attributes for the entity
- **Example:** `{"temperature": 42.5, "humidity": 65}`

## DeviceInfo Structure

```python
from homeassistant.helpers.device_registry import DeviceInfo

device_info = DeviceInfo(
    identifiers={("domain", "device_id")},      # Required
    name="Device Name",                         # Optional
    manufacturer="Manufacturer",                # Optional
    model="Model Name",                         # Optional
    sw_version="1.0.0",                         # Optional
    hw_version="A1",                            # Optional
    serial_number="SERIAL123",                  # Optional
    via_device=("domain", "parent_device_id"), # Optional (for child devices)
    connections={(dr.CONNECTION_NETWORK_MAC, "aa:bb:cc:dd:ee:ff")},
    suggested_area="Living Room",               # Optional
)
```

## Common Patterns

### Coordinator-Based Entity

```python
from homeassistant.helpers.entity_platform import CoordinatorEntity

class CoordinatedSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Sensor"

    @property
    def unique_id(self) -> str:
        return f"{self.coordinator.data['id']}_sensor"

    @property
    def native_value(self) -> float | None:
        return self.coordinator.data.get("value")
```

### State Class Best Practices

```python
# ✅ Correct for instantaneous measurement
_attr_state_class = SensorStateClass.MEASUREMENT
# ✅ Correct for cumulative that resets daily
_attr_state_class = SensorStateClass.TOTAL
# ✅ Correct for cumulative that never resets
_attr_state_class = SensorStateClass.TOTAL_INCREASING
```
