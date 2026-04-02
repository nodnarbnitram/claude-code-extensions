# ESPHome Troubleshooting Guide

Comprehensive error message lookup table with solutions for compilation errors, runtime issues, configuration problems, and hardware failures.

## Quick Error Lookup

| Error Message | Category | Quick Fix |
|---------------|----------|-----------|
| "Unknown platform" | Config | Check component name spelling |
| "GPIO already in use" | GPIO | Check pin assignments for duplicates |
| "Could not compile" | Compilation | Check YAML syntax, indentation |
| "WiFi connection failed" | Network | Verify SSID/password, check signal |
| "Sensor not found" | Hardware | Check I²C address, verify wiring |
| "OTA upload failed" | OTA | Check device reachable, restart |
| "Invalid pin" | GPIO | Use valid GPIO for platform |
| "YAML syntax error" | Config | Check indentation (2 spaces, no tabs) |
| "API connection timeout" | Network | Check firewall, API encryption key |
| "Flash size too small" | Platform | Reduce features or use larger flash |

---

## Compilation Errors

### Error: "Unknown platform"

**Full Error**:
```
Platform 'xyz' doesn't exist
Unknown platform: xyz
```

**Cause**: Misspelled platform name or unsupported platform

**Solutions**:
1. Check platform spelling in ESPHome documentation
2. Ensure platform exists for component
3. Update ESPHome to latest version (platform may be new)

**Example Fix**:
```yaml
# WRONG
sensor:
  - platform: dht11  # Wrong platform name

# CORRECT
sensor:
  - platform: dht
    model: DHT11  # Specify model instead
```

---

### Error: "GPIO already in use"

**Full Error**:
```
Pin GPIO21 is already in use by component 'i2c'
GPIO21 already used
```

**Cause**: Same GPIO pin assigned to multiple components

**Solutions**:
1. List all GPIO usage in config
2. Find duplicate assignments
3. Reassign one component to different pin
4. Check I²C/SPI default pins not conflicting

**Example Fix**:
```yaml
# WRONG - GPIO21 used twice
i2c:
  sda: GPIO21
  scl: GPIO22

switch:
  - platform: gpio
    pin: GPIO21  # CONFLICT!

# CORRECT - Use different pin
i2c:
  sda: GPIO21
  scl: GPIO22

switch:
  - platform: gpio
    pin: GPIO23  # Different pin
```

---

### Error: "Could not compile"

**Full Error**:
```
Failed to compile firmware
Compilation failed
```

**Causes**:
- YAML syntax error (indentation, missing colon)
- Invalid configuration values
- Missing required fields
- Incompatible component versions

**Solutions**:
1. Run `esphome config device.yaml` to validate YAML
2. Check indentation (use 2 spaces, not tabs)
3. Verify all required fields present
4. Check ESPHome version compatibility
5. Review compilation error logs for specific issue

**Common YAML Syntax Fixes**:
```yaml
# WRONG - Tab indentation
sensor:
→   - platform: dht  # Tab character

# CORRECT - 2 space indentation
sensor:
  - platform: dht  # 2 spaces

# WRONG - Missing colon
sensor
  - platform: dht

# CORRECT - Colon after key
sensor:
  - platform: dht
```

---

### Error: "Invalid pin for platform"

**Full Error**:
```
GPIO34 cannot be used as output on ESP32
Pin GPIO1 is not available on ESP8266
```

**Cause**: Using input-only pin for output, or unavailable pin

**Solutions**:
1. Check GPIO pinout reference for platform
2. Use output-capable pins for switches/LEDs
3. Use input-only pins (GPIO34-39 ESP32) only for sensors
4. Avoid flash pins (GPIO6-11)

**Example Fix**:
```yaml
# WRONG - GPIO34 is input-only on ESP32
switch:
  - platform: gpio
    pin: GPIO34  # Cannot be used as output

# CORRECT - Use output-capable pin
switch:
  - platform: gpio
    pin: GPIO23  # Output-capable
```

**Refer to**: `references/gpio-pinouts.md` for complete pin capabilities

---

### Error: "YAML syntax error"

**Full Error**:
```
expected <block end>, but found '-'
mapping values are not allowed here
```

**Cause**: Invalid YAML syntax (indentation, structure)

**Solutions**:
1. Validate YAML with online validator
2. Check indentation (2 spaces per level)
3. Ensure no tabs (use spaces only)
4. Verify list items start with `-`
5. Check quotes around special characters

**Common YAML Fixes**:
```yaml
# WRONG - Incorrect indentation
sensor:
- platform: dht
  pin: GPIO4

# CORRECT - Consistent 2-space indentation
sensor:
  - platform: dht
    pin: GPIO4

# WRONG - Missing dash for list item
sensor:
  platform: dht
  pin: GPIO4

# CORRECT - Dash for list item
sensor:
  - platform: dht
    pin: GPIO4
```

---

### Error: "Flash size too small"

**Full Error**:
```
Firmware is too large (1234567 bytes), maximum is 1048576 bytes
Sketch too big
```

**Cause**: Firmware exceeds available flash memory

**Solutions**:
1. Reduce features (remove unused components)
2. Disable logger or reduce log level
3. Disable web_server if not needed
4. Use framework: arduino instead of esp-idf (smaller)
5. For ESP8266: Use larger flash size in board config

**Example Fixes**:
```yaml
# Reduce logging
logger:
  level: WARN  # Instead of DEBUG or VERBOSE

# Disable web server
# web_server:  # Comment out if not needed

# Use minimal logger
logger:
  baud_rate: 0  # Disable serial logging
```

---

## Runtime Errors

### Error: "WiFi connection failed"

**Full Error**:
```
WiFi: Can't connect to network 'SSID'
Connection failed
WiFi: Not connected
```

**Causes**:
- Incorrect SSID or password
- Weak WiFi signal
- 5GHz network (ESP8266/ESP32 only support 2.4GHz)
- MAC filtering on router
- DHCP exhausted

**Solutions**:
1. Verify SSID and password in secrets.yaml
2. Check WiFi signal strength (move closer to AP)
3. Ensure using 2.4GHz network (not 5GHz)
4. Check router MAC filter allow list
5. Use static IP if DHCP issues
6. Verify WiFi credentials are in quotes if contain special characters

**Example Fixes**:
```yaml
# Use static IP to avoid DHCP issues
wifi:
  ssid: !secret wifi_ssid
  password: !secret wifi_password
  manual_ip:
    static_ip: 192.168.1.100
    gateway: 192.168.1.1
    subnet: 255.255.255.0

# Quote special characters
# secrets.yaml
wifi_password: "P@ssw0rd!"  # Quote if contains special chars
```

---

### Error: "API connection timeout"

**Full Error**:
```
Connection timeout
Can't connect to ESPHome API
API client connection timeout
```

**Causes**:
- Firewall blocking connection
- Incorrect API encryption key
- Device not reachable on network
- mDNS not working
- Port 6053 blocked

**Solutions**:
1. Verify device IP address (check router DHCP table)
2. Use IP address instead of .local hostname
3. Check API encryption key matches Home Assistant
4. Disable firewall temporarily to test
5. Verify port 6053 not blocked
6. Restart device and Home Assistant

**Example Fixes**:
```yaml
# Ensure API encryption key matches Home Assistant
api:
  encryption:
    key: !secret api_encryption_key  # Must match HA integration

# Use static IP for reliability
wifi:
  manual_ip:
    static_ip: 192.168.1.100
```

**Check connectivity**:
```bash
# Ping device
ping 192.168.1.100

# Check logs
esphome logs device.yaml

# Connect via IP instead of hostname
# In Home Assistant: 192.168.1.100 instead of device.local
```

---

### Error: "Sensor not found"

**Full Error**:
```
I2C: Device not found at address 0x76
Sensor 'xyz' not responding
No sensor detected
```

**Causes**:
- Incorrect I²C address
- Wiring issue (loose connection, wrong pins)
- Sensor not powered
- Pull-up resistors missing (for I²C)
- Incompatible voltage (3.3V vs 5V)

**Solutions**:
1. Use `scan: true` in i2c config to detect devices
2. Check wiring connections
3. Verify correct I²C address (common: 0x76, 0x77 for BME280)
4. Add pull-up resistors (4.7kΩ) on SDA/SCL if needed
5. Check sensor power supply voltage
6. Try different I²C pins

**Example Debugging**:
```yaml
# Enable I2C scan to detect devices
i2c:
  sda: GPIO21
  scl: GPIO22
  scan: true  # Shows detected I2C addresses in logs

sensor:
  - platform: bme280
    address: 0x76  # Try 0x76 or 0x77
    # ...
```

**Check logs**:
```
I2C: Found device at address 0x76  # Sensor detected
I2C: Found device at address 0x77  # Sensor detected
I2C: No devices found  # Check wiring
```

---

### Error: "OTA upload failed"

**Full Error**:
```
OTA update failed
Upload failed
Connection lost during upload
```

**Causes**:
- Device unreachable on network
- Incorrect OTA password
- Insufficient flash space
- Device rebooted during upload
- Weak WiFi signal
- Firewall blocking connection

**Solutions**:
1. Verify device reachable (ping IP address)
2. Check OTA password matches
3. Restart device before OTA update
4. Move device closer to WiFi AP
5. Use wired upload (USB) if OTA keeps failing
6. Clear flash and re-upload via USB

**Example Fixes**:
```yaml
# Ensure OTA configured correctly
ota:
  - platform: esphome
    password: !secret ota_password  # Must match

# Increase safe_mode boot timeout
ota:
  - platform: esphome
    safe_mode: true
    reboot_timeout: 10min  # More time for unstable connections
```

**Recovery steps**:
```bash
# 1. Try OTA update with verbose logging
esphome upload device.yaml --device 192.168.1.100

# 2. If OTA fails, use USB upload
esphome upload device.yaml --device /dev/ttyUSB0

# 3. Last resort: factory reset
# Hold BOOT button, press RESET, release BOOT
# Then upload via USB
```

---

## Configuration Errors

### Error: "Missing required field"

**Full Error**:
```
Required option 'name' not specified
Missing required field: 'pin'
```

**Cause**: Required configuration field not provided

**Solutions**:
1. Check component documentation for required fields
2. Add missing field to configuration
3. Verify field name spelling

**Example Fixes**:
```yaml
# WRONG - Missing name
sensor:
  - platform: dht
    pin: GPIO4

# CORRECT - Name required
sensor:
  - platform: dht
    pin: GPIO4
    temperature:
      name: "Temperature"  # Required
    humidity:
      name: "Humidity"  # Required
```

---

### Error: "Invalid configuration value"

**Full Error**:
```
Invalid value for 'update_interval': '10'
Value must be a time period
```

**Cause**: Configuration value has wrong type or format

**Solutions**:
1. Check expected value type (string, number, boolean)
2. Use correct units for time periods (s, min, h)
3. Quote strings if needed
4. Use correct format for enums

**Example Fixes**:
```yaml
# WRONG - Missing time unit
sensor:
  - platform: dht
    update_interval: 60  # Missing 's'

# CORRECT - Include time unit
sensor:
  - platform: dht
    update_interval: 60s  # Correct

# WRONG - Incorrect enum value
sensor:
  - platform: adc
    attenuation: 11  # Should be 11db

# CORRECT - Use correct enum
sensor:
  - platform: adc
    attenuation: 11db  # Correct
```

---

### Error: "Conflicting ID"

**Full Error**:
```
ID 'sensor_id' is already in use
Duplicate ID: 'my_sensor'
```

**Cause**: Same ID used for multiple components

**Solutions**:
1. Ensure each component has unique ID
2. Search config for duplicate ID names
3. Use descriptive, unique ID names

**Example Fixes**:
```yaml
# WRONG - Duplicate ID
sensor:
  - platform: dht
    id: temp_sensor  # Duplicate!
    temperature:
      name: "Room Temp"

  - platform: bme280
    id: temp_sensor  # Duplicate!
    temperature:
      name: "Outside Temp"

# CORRECT - Unique IDs
sensor:
  - platform: dht
    id: room_temp_sensor  # Unique
    temperature:
      name: "Room Temp"

  - platform: bme280
    id: outside_temp_sensor  # Unique
    temperature:
      name: "Outside Temp"
```

---

## Hardware Issues

### Issue: "Sensor readings are incorrect"

**Symptoms**:
- Temperature reads 0°C or -127°C
- Humidity reads 0%
- Distance sensor reads infinity
- Readings jump erratically

**Causes**:
- Sensor not connected properly
- Pull-up resistors missing (I²C, 1-Wire)
- Voltage mismatch (3.3V vs 5V)
- Sensor failure
- Interference from other devices
- Update interval too fast

**Solutions**:
1. Check all wiring connections
2. Add pull-up resistors (4.7kΩ) for I²C/1-Wire
3. Verify sensor voltage requirements
4. Increase update_interval (>2s for DHT, >30s for BME280)
5. Add filters to smooth readings
6. Move sensor away from interference sources
7. Test sensor with different ESP device

**Example Fixes**:
```yaml
# Add filters to smooth noisy readings
sensor:
  - platform: dht
    pin: GPIO4
    temperature:
      name: "Temperature"
      filters:
        - sliding_window_moving_average:
            window_size: 5
            send_every: 5
        - filter_out: nan  # Filter out invalid readings
    humidity:
      name: "Humidity"
      filters:
        - sliding_window_moving_average:
            window_size: 5
            send_every: 5
        - filter_out: nan
    update_interval: 60s  # Slower = more reliable

# For 1-Wire sensors (DS18B20)
dallas:
  - pin: GPIO4
    update_interval: 60s

sensor:
  - platform: dallas
    filters:
      - filter_out: 85.0  # Filter out sensor error value
      - filter_out: nan
```

---

### Issue: "Device keeps rebooting"

**Symptoms**:
- Device reboots every few seconds
- Boot loop
- Cannot connect to device

**Causes**:
- Power supply insufficient
- Brownout detector triggered
- Watchdog timeout (infinite loop in lambda)
- Memory overflow
- Bad flash
- Incorrect GPIO state at boot

**Solutions**:
1. Use adequate power supply (5V 1A minimum, 2A recommended)
2. Disable brownout detector (ESP32)
3. Check lambdas for infinite loops
4. Reduce memory usage (remove unused components)
5. Reflash firmware via USB
6. Check strapping pins not pulled wrong at boot

**Example Fixes**:
```yaml
# Disable brownout detector (ESP32 only)
esp32:
  board: esp32dev
  framework:
    type: arduino
    version: recommended
  variant: esp32
  # Add this to disable brownout:
  # platformio_options:
  #   board_build.f_cpu: 240000000L
  #   board_build.f_flash: 40000000L
  #   board_build.flash_mode: dio
  #   board_build.partitions: default.csv

# Increase watchdog timeout if needed
ota:
  - platform: esphome
    safe_mode: true
    reboot_timeout: 10min  # More time before reboot
```

**Power supply recommendations**:
- **ESP32**: 5V 1A minimum (2A recommended with peripherals)
- **ESP8266**: 5V 500mA minimum (1A recommended)
- Use dedicated power supply (not USB from computer)
- Add decoupling capacitors (10μF, 100nF) near ESP module

---

### Issue: "Relay not switching"

**Symptoms**:
- Relay clicks but load doesn't switch
- No relay click at all
- Relay switches opposite direction

**Causes**:
- Insufficient drive current
- Inverted logic
- Wrong GPIO pin configuration
- Relay powered from wrong voltage
- Relay coil voltage mismatch

**Solutions**:
1. Use transistor/MOSFET driver for relay coil
2. Check inverted configuration
3. Verify GPIO is output-capable
4. Power relay from external 5V (not ESP)
5. Check relay coil voltage rating
6. Use relay module (has built-in driver circuit)

**Example Fixes**:
```yaml
# Check inverted setting
switch:
  - platform: gpio
    pin:
      number: GPIO23
      inverted: false  # Try true if relay switches opposite
    name: "Relay"

# For active-low relay modules
switch:
  - platform: gpio
    pin:
      number: GPIO23
      inverted: true  # Active-low relay module
    name: "Relay"
    restore_mode: RESTORE_DEFAULT_OFF  # Ensure off at boot
```

**Wiring check**:
```
ESP32      Relay Module
GPIO23 --> IN
GND    --> GND
VCC not connected (relay module powered externally from 5V)
```

---

## Network Issues

### Issue: "Device keeps disconnecting"

**Symptoms**:
- WiFi disconnects every few minutes
- API unavailable intermittently
- Logs show reconnection messages

**Causes**:
- Weak WiFi signal
- Power supply insufficient
- Router DHCP lease timeout
- WiFi power saving mode
- Network congestion
- ESP32 Bluetooth interference (if enabled)

**Solutions**:
1. Move device closer to WiFi AP
2. Use better power supply
3. Configure static IP
4. Disable WiFi power saving
5. Disable Bluetooth on ESP32
6. Use 2.4GHz-only WiFi network

**Example Fixes**:
```yaml
# Disable WiFi power saving
wifi:
  ssid: !secret wifi_ssid
  password: !secret wifi_password
  power_save_mode: NONE  # Disable power saving (ESP32)
  # or
  output_power: 20db  # Increase TX power (ESP32)

# Use static IP for stability
wifi:
  ssid: !secret wifi_ssid
  password: !secret wifi_password
  manual_ip:
    static_ip: 192.168.1.100
    gateway: 192.168.1.1
    subnet: 255.255.255.0

# Increase reboot timeout
api:
  reboot_timeout: 15min  # More time before reboot on disconnect
```

---

## Debugging Techniques

### Enable Verbose Logging

```yaml
logger:
  level: VERBOSE  # DEBUG, VERBOSE, or VERY_VERBOSE
  logs:
    component: VERBOSE  # Log specific component
```

### Use Serial Logging

```bash
# Monitor serial output
esphome logs device.yaml

# Or use platformio
pio device monitor
```

### Enable I²C Scan

```yaml
i2c:
  sda: GPIO21
  scl: GPIO22
  scan: true  # Shows detected I2C devices
```

### Check WiFi Signal

```yaml
sensor:
  - platform: wifi_signal
    name: "WiFi Signal"
    update_interval: 60s
```

### Monitor Uptime

```yaml
sensor:
  - platform: uptime
    name: "Uptime"
```

### Use Safe Mode

```yaml
ota:
  - platform: esphome
    safe_mode: true  # Boots without sensors if errors occur
```

---

## Recovery Procedures

### Factory Reset

1. Hold BOOT button
2. Press RESET button briefly
3. Release BOOT button after 2 seconds
4. Device enters flash mode
5. Upload firmware via USB

### Clear Flash

```bash
# Erase entire flash
esptool.py --port /dev/ttyUSB0 erase_flash

# Then upload firmware
esphome upload device.yaml --device /dev/ttyUSB0
```

### Safe Mode Recovery

If device is stuck in boot loop with OTA enabled:

1. Device will boot into safe mode after failed boots
2. Connect via OTA (device will have .safe suffix)
3. Upload working firmware

---

## Common Error Patterns

### Pattern 1: Boot Loop After OTA

**Symptoms**: Device reboots continuously after OTA update

**Solution**:
1. Wait for safe mode (automatic after ~10 failed boots)
2. Upload previous working firmware
3. Fix issue in new firmware
4. Verify GPIO states at boot

### Pattern 2: I²C Device Not Found

**Symptoms**: `scan: true` shows no devices

**Solution**:
1. Check SDA/SCL connections
2. Add 4.7kΩ pull-up resistors
3. Try different I²C pins
4. Verify sensor power supply
5. Test sensor with Arduino first

### Pattern 3: GPIO Conflict

**Symptoms**: Device boots but feature doesn't work

**Solution**:
1. List all GPIO usage
2. Check I²C/SPI default pins
3. Avoid strapping pins (GPIO0, 2, 12, 15)
4. Use gpio-pinouts.md reference

### Pattern 4: Memory Issues

**Symptoms**: Random crashes, heap warnings in logs

**Solution**:
1. Reduce features
2. Disable web_server
3. Lower logger level
4. Remove unused components
5. Use framework: arduino (smaller than esp-idf)

---

## Summary of Quick Fixes

1. **YAML errors** → Check indentation (2 spaces, no tabs)
2. **GPIO conflicts** → List all pins, check for duplicates
3. **WiFi issues** → Verify credentials, use static IP
4. **I²C not found** → Enable scan, check wiring, add pull-ups
5. **Sensor errors** → Increase update_interval, add filters
6. **OTA fails** → Restart device, use USB upload
7. **Boot loops** → Check power supply, disable brownout
8. **API timeout** → Verify encryption key, use IP not .local

**Always check**:
- Logs with `esphome logs device.yaml`
- GPIO pinout reference
- ESPHome documentation for component

**When stuck**: Start with minimal config, add components one by one to isolate issue
