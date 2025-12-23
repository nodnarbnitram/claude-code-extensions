# GPIO Pinout Reference for ESPHome

Complete GPIO reference for ESP32 and ESP8266 platforms with safe pin recommendations, strapping pin warnings, and pin capabilities.

## ESP32 GPIO Pinout

### Safe GPIO Pins (Recommended for General Use)

These pins are safe for most applications and won't interfere with boot:

**Digital I/O (Input/Output):**
- GPIO4, GPIO5, GPIO12, GPIO13, GPIO14, GPIO16, GPIO17, GPIO18, GPIO19, GPIO21, GPIO22, GPIO23, GPIO25, GPIO26, GPIO27, GPIO32, GPIO33

**ADC Capable (Analog Input):**
- GPIO32, GPIO33, GPIO34, GPIO35, GPIO36, GPIO39 (VP), GPIO38 (VN)

**Touch Capable:**
- GPIO0, GPIO2, GPIO4, GPIO12, GPIO13, GPIO14, GPIO15, GPIO27, GPIO32, GPIO33

**PWM Capable:**
- All GPIO pins can be used for PWM (16 channels available)

### Strapping Pins (Use with Caution)

These pins affect boot behavior and should be used carefully:

**GPIO0** (BOOT button)
- Pulled HIGH at boot
- LOW at boot = Flash mode
- Can be used after boot, but avoid pulling LOW on power-up
- Often connected to onboard button

**GPIO2** (Built-in LED on many boards)
- Must be LOW for ESP32 to enter download mode
- Must be floating or HIGH at boot for normal operation
- Safe to use after boot
- Often connected to onboard LED

**GPIO5**
- Strapping pin
- Must be HIGH during boot for SDIO Slave mode
- Generally safe to use after boot

**GPIO12** (MTDI)
- Flash voltage selector
- LOW = 3.3V Flash, HIGH = 1.8V Flash
- Use with caution if you have 3.3V flash (most boards)
- Can be used after boot

**GPIO15** (MTDO)
- Outputs PWM signal at boot
- Strapping pin for debug output
- Must be HIGH at boot for normal operation
- Use with caution

### Input-Only Pins

These pins can ONLY be used as inputs (no OUTPUT mode):

- GPIO34, GPIO35, GPIO36, GPIO39 (VP), GPIO38 (VN)
- Do not have internal pull-up or pull-down resistors
- Useful for analog sensors (ADC)

### Pins to Avoid

**Do NOT use for critical applications:**

**GPIO6-GPIO11** (SPI Flash)
- Connected to integrated SPI flash
- Using these will cause crashes
- Includes: GPIO6, GPIO7, GPIO8, GPIO9, GPIO10, GPIO11

**GPIO1** (TX0)
- Serial TX pin
- Avoid if you need serial logging

**GPIO3** (RX0)
- Serial RX pin
- Avoid if you need serial logging

### Default I²C Pins

- **SDA**: GPIO21
- **SCL**: GPIO22

Can be changed in configuration:
```yaml
i2c:
  sda: GPIO21
  scl: GPIO22
```

### Default SPI Pins

- **MOSI**: GPIO23
- **MISO**: GPIO19
- **CLK**: GPIO18
- **CS**: User-defined (often GPIO5)

### Default UART Pins

**UART0** (USB Serial):
- TX: GPIO1
- RX: GPIO3

**UART1** (Available):
- TX: GPIO10 (not recommended - SPI Flash)
- RX: GPIO9 (not recommended - SPI Flash)

**UART2** (Recommended for external serial):
- TX: GPIO17
- RX: GPIO16

### ESP32 DevKit Pin Mapping

Common pin labels on ESP32 DevKit boards:

| Label | GPIO | Notes |
|-------|------|-------|
| D0 | GPIO0 | BOOT button, strapping pin |
| D1 | GPIO1 | TX0, avoid if using serial |
| D2 | GPIO2 | Built-in LED, strapping pin |
| D3 | GPIO3 | RX0, avoid if using serial |
| D4 | GPIO4 | Safe |
| D5 | GPIO5 | Strapping pin |
| D12 | GPIO12 | Strapping pin (flash voltage) |
| D13 | GPIO13 | Safe |
| D14 | GPIO14 | Safe |
| D15 | GPIO15 | Strapping pin |
| D16 | GPIO16 | Safe (RX2) |
| D17 | GPIO17 | Safe (TX2) |
| D18 | GPIO18 | Safe (SPI CLK) |
| D19 | GPIO19 | Safe (SPI MISO) |
| D21 | GPIO21 | Safe (I2C SDA) |
| D22 | GPIO22 | Safe (I2C SCL) |
| D23 | GPIO23 | Safe (SPI MOSI) |
| D25 | GPIO25 | Safe (DAC1) |
| D26 | GPIO26 | Safe (DAC2) |
| D27 | GPIO27 | Safe |
| D32 | GPIO32 | Safe (ADC) |
| D33 | GPIO33 | Safe (ADC) |
| D34 | GPIO34 | Input only (ADC) |
| D35 | GPIO35 | Input only (ADC) |
| D36 | GPIO36 (VP) | Input only (ADC) |
| D39 | GPIO39 (VN) | Input only (ADC) |

---

## ESP8266 GPIO Pinout

### Safe GPIO Pins (Recommended)

**Digital I/O (Input/Output):**
- GPIO4 (D2), GPIO5 (D1), GPIO12 (D6), GPIO13 (D7), GPIO14 (D5)

**PWM Capable:**
- GPIO4 (D2), GPIO5 (D1), GPIO12 (D6), GPIO13 (D7), GPIO14 (D5)

**ADC Capable:**
- A0 (single ADC pin, 0-1V range)

### Strapping Pins (Use with Caution)

**GPIO0** (D3, FLASH button)
- Must be HIGH at boot for normal operation
- LOW at boot = Flash mode
- Can be used after boot (often as button input with pull-up)

**GPIO2** (D4, Built-in LED)
- Must be HIGH at boot
- Often connected to onboard LED (inverted)
- Safe to use after boot

**GPIO15** (D8)
- Must be LOW at boot
- Pulled LOW with resistor on most boards
- Can be used after boot

### Pins to Avoid

**GPIO6-GPIO11** (SPI Flash)
- Connected to integrated SPI flash
- Using these will cause crashes

**GPIO1** (TX)
- Serial TX pin
- Avoid if you need serial logging

**GPIO3** (RX)
- Serial RX pin
- Avoid if you need serial logging

**GPIO16** (D0, Wake pin)
- Used for deep sleep wake
- No interrupt support
- No pull-up/pull-down resistors
- Use only for wake from deep sleep or simple output

### Default I²C Pins

- **SDA**: GPIO4 (D2)
- **SCL**: GPIO5 (D1)

Can be changed in configuration:
```yaml
i2c:
  sda: GPIO4
  scl: GPIO5
```

### Default SPI Pins

**Hardware SPI:**
- **MOSI**: GPIO13 (D7)
- **MISO**: GPIO12 (D6)
- **CLK**: GPIO14 (D5)
- **CS**: User-defined (often GPIO15/D8)

### ESP8266 NodeMCU Pin Mapping

Common pin labels on NodeMCU boards:

| Label | GPIO | Notes |
|-------|------|-------|
| D0 | GPIO16 | Wake pin, limited functionality |
| D1 | GPIO5 | Safe (I2C SCL) |
| D2 | GPIO4 | Safe (I2C SDA) |
| D3 | GPIO0 | FLASH button, strapping pin |
| D4 | GPIO2 | Built-in LED, strapping pin |
| D5 | GPIO14 | Safe (SPI CLK) |
| D6 | GPIO12 | Safe (SPI MISO) |
| D7 | GPIO13 | Safe (SPI MOSI) |
| D8 | GPIO15 | Strapping pin, must be LOW at boot |
| TX | GPIO1 | Serial TX, avoid |
| RX | GPIO3 | Serial RX, avoid |
| A0 | ADC0 | Analog input (0-1V) |

---

## GPIO Configuration Examples

### Basic Digital Output (LED)

```yaml
switch:
  - platform: gpio
    pin: GPIO23  # ESP32 safe pin
    name: "LED"
```

### Digital Input (Button with Pull-Up)

```yaml
binary_sensor:
  - platform: gpio
    pin:
      number: GPIO4  # ESP32 safe pin
      mode: INPUT_PULLUP
      inverted: true
    name: "Button"
```

### Digital Input (Button with Pull-Down)

```yaml
binary_sensor:
  - platform: gpio
    pin:
      number: GPIO4
      mode: INPUT_PULLDOWN
    name: "Button"
```

### PWM Output (Dimmable LED)

```yaml
output:
  - platform: ledc  # ESP32
    pin: GPIO25
    id: pwm_output

light:
  - platform: monochromatic
    output: pwm_output
    name: "Dimmable Light"
```

### Analog Input (ESP32)

```yaml
sensor:
  - platform: adc
    pin: GPIO32  # ESP32 ADC pin
    name: "Analog Sensor"
    attenuation: 11db  # Allows 0-3.3V range
    update_interval: 60s
```

### Analog Input (ESP8266)

```yaml
sensor:
  - platform: adc
    pin: A0  # ESP8266 only has one ADC
    name: "Analog Sensor"
    update_interval: 60s
```

---

## GPIO Conflict Prevention

### Common GPIO Conflicts

**I²C + Individual GPIO:**
- Don't use GPIO21/GPIO22 (ESP32) or GPIO4/GPIO5 (ESP8266) for other purposes if using I²C

**SPI + Individual GPIO:**
- Don't use default SPI pins (GPIO18, GPIO19, GPIO23 on ESP32) for other purposes if using SPI

**Serial Logging + GPIO1/GPIO3:**
- If you need GPIO1 or GPIO3, disable serial logging

**Strapping Pins at Boot:**
- Avoid external pull-ups/pull-downs on GPIO0, GPIO2, GPIO12, GPIO15 (ESP32) during boot

### How to Avoid Conflicts

1. **List all GPIO usage** in your configuration
2. **Check for duplicates** - same pin used twice
3. **Check I²C/SPI defaults** - ensure not conflicting
4. **Avoid strapping pins** for critical sensors
5. **Test boot behavior** - ensure device boots reliably

### GPIO Conflict Example (Bad)

```yaml
# BAD: GPIO21 used twice
i2c:
  sda: GPIO21  # Uses GPIO21
  scl: GPIO22

switch:
  - platform: gpio
    pin: GPIO21  # CONFLICT! Already used by I²C SDA
    name: "Relay"
```

### GPIO Conflict Fixed (Good)

```yaml
# GOOD: Use different pin for relay
i2c:
  sda: GPIO21
  scl: GPIO22

switch:
  - platform: gpio
    pin: GPIO23  # Safe pin, no conflict
    name: "Relay"
```

---

## Quick Pin Selection Guide

### Need Digital Output?
**ESP32**: GPIO4, GPIO5, GPIO13, GPIO14, GPIO16-19, GPIO21-23, GPIO25-27, GPIO32-33
**ESP8266**: GPIO4 (D2), GPIO5 (D1), GPIO12 (D6), GPIO13 (D7), GPIO14 (D5)

### Need Digital Input?
**ESP32**: Same as digital output + GPIO34-36, GPIO39
**ESP8266**: Same as digital output + GPIO0 (D3) with pull-up

### Need PWM?
**ESP32**: All output-capable pins
**ESP8266**: GPIO4 (D2), GPIO5 (D1), GPIO12 (D6), GPIO13 (D7), GPIO14 (D5)

### Need Analog Input?
**ESP32**: GPIO32-36, GPIO39
**ESP8266**: A0 only

### Need I²C?
**ESP32**: Default GPIO21 (SDA), GPIO22 (SCL)
**ESP8266**: Default GPIO4/D2 (SDA), GPIO5/D1 (SCL)

### Need SPI?
**ESP32**: Default GPIO23 (MOSI), GPIO19 (MISO), GPIO18 (CLK)
**ESP8266**: Default GPIO13/D7 (MOSI), GPIO12/D6 (MISO), GPIO14/D5 (CLK)

---

## Platform-Specific Notes

### ESP32 Advantages
- More GPIO pins (34+ vs 11)
- Multiple ADC channels (18 vs 1)
- Touch sensor support
- DAC support (GPIO25, GPIO26)
- More UART/I²C/SPI buses

### ESP8266 Limitations
- Fewer GPIO pins (11 usable)
- Only 1 ADC pin (A0)
- No DAC
- No touch sensors
- Limited number of interrupts

### When to Use ESP32 vs ESP8266
**Use ESP32 when:**
- Need more GPIO pins
- Need multiple ADC inputs
- Using touch sensors
- Complex projects with many peripherals

**Use ESP8266 when:**
- Budget constrained
- Simple projects (few sensors/switches)
- Lower power consumption needed
- Smaller physical size required

---

## Summary

**ESP32 Safe Pins**: GPIO4, GPIO5, GPIO13, GPIO14, GPIO16-19, GPIO21-23, GPIO25-27, GPIO32-33

**ESP8266 Safe Pins**: GPIO4 (D2), GPIO5 (D1), GPIO12 (D6), GPIO13 (D7), GPIO14 (D5)

**Avoid**: GPIO0, GPIO2, GPIO6-11, GPIO15 for critical applications

**Default I²C (ESP32)**: GPIO21 (SDA), GPIO22 (SCL)

**Default I²C (ESP8266)**: GPIO4/D2 (SDA), GPIO5/D1 (SCL)

**Always check**: Boot behavior, strapping pins, and conflicts before finalizing design
