# ESP32-S3-BOX-3 Hardware Pinout Reference

Complete GPIO pinout, component addresses, and hardware specifications for ESP32-S3-BOX-3.

## GPIO Pinout Summary

| Component | Type | GPIO/Address | Notes |
|-----------|------|--------------|-------|
| **Display** | ILI9342C SPI | CS:5, DC:4, RST:48, CLK:7, MOSI:6 | Reset shared with touch |
| **Touch** | GT911 I²C | SDA:8, SCL:18, INT:3, RST:48 | Address 0x5D or 0x14 |
| **Microphone** | ES7210 I²S | DIN:16, I²C:0x40 | 4-channel ADC, 16kHz |
| **Speaker** | ES8311 I²S | DOUT:15, I²C:0x18 | Mono DAC, 48kHz, needs MCLK |
| **I²S Bus** | Shared | LRCLK:45, BCLK:17, MCLK:2 | Shared by mic and speaker |
| **I²C Bus** | Primary | SDA:8, SCL:18 | For touch, sensors, audio |
| **BME688** | Environmental | I²C:0x77 | Temp, humidity, pressure, gas |
| **IMU** | ICM-42607-P | SPI CS:10 | 6-axis motion sensor |
| **RGB LED** | WS2812 | GPIO39 | Status indicator |
| **USB** | Serial/Power | Built-in | Programming and power |

## Display (ILI9342C)

**Specifications:**
- Resolution: 320x240 pixels
- Interface: SPI
- Color: 16-bit RGB565 (requires PSRAM)
- Refresh: Up to 60Hz

**GPIO Connections:**
- CS: GPIO5
- DC: GPIO4
- RST: GPIO48 (inverted, shared with touch)
- CLK: GPIO7
- MOSI: GPIO6

**Critical Configuration:**
```yaml
display:
  - platform: ili9xxx
    model: S3BOX
    cs_pin: GPIO5
    dc_pin: GPIO4
    reset_pin:
      number: GPIO48
      inverted: true  # CRITICAL
    color_palette: NONE  # 16-bit requires PSRAM
```

**Known Issues:**
- Display flicker → Ensure PSRAM enabled
- Inverted colors → Check `invert_colors` setting
- 2025.2 breaking change: Must use `color_palette: NONE` for 16-bit

## Touchscreen (GT911)

**Specifications:**
- Type: Capacitive multi-touch
- Points: Up to 5 simultaneous
- Interface: I²C
- Resolution: 320x240 coordinates

**GPIO Connections:**
- SDA: GPIO8 (I²C bus_a)
- SCL: GPIO18 (I²C bus_a)
- INT: GPIO3 (interrupt, strapping pin warning)
- RST: GPIO48 (inverted, shared with display)

**I²C Addresses:**
- Primary: 0x5D (INT pin low at boot)
- Alternate: 0x14 (INT pin high at boot)

**Critical Configuration:**
```yaml
touchscreen:
  - platform: gt911
    i2c_id: bus_a
    address: 0x5D
    interrupt_pin:
      number: GPIO3
      ignore_strapping_warning: true  # CRITICAL
    reset_pin:
      number: GPIO48
      inverted: true  # Shared with display
```

**Known Issues:**
- Touch not responding → Check shared reset pin GPIO48 (must be inverted)
- Wrong address → Try 0x5D or 0x14
- Interrupt on strapping pin → Use `ignore_strapping_warning: true`

## Audio (I²S Bus)

**Shared I²S Bus Configuration:**
- LRCLK (Word Select): GPIO45
- BCLK (Bit Clock): GPIO17
- MCLK (Master Clock): GPIO2

**ES7210 Microphone ADC:**
- Interface: I²S + I²C
- I²S DIN: GPIO16
- I²C Address: 0x40
- Sample Rate: 16kHz
- Channels: 4 (using 1)
- Bits: 16-bit
- Gain: 0-42dB (24dB recommended)

**ES8311 Speaker DAC:**
- Interface: I²S + I²C
- I²S DOUT: GPIO15
- I²C Address: 0x18
- Sample Rate: 48kHz
- Channels: Mono
- Bits: 16-bit
- MCLK Required: Yes (CRITICAL)

**Critical Configuration:**
```yaml
i2s_audio:
  - id: i2s_shared
    i2s_lrclk_pin: GPIO45
    i2s_bclk_pin: GPIO17
    i2s_mclk_pin: GPIO2  # CRITICAL for ES8311

audio_dac:
  - platform: es8311
    use_mclk: true  # CRITICAL
    address: 0x18

speaker:
  - platform: i2s_audio
    buffer_duration: 100ms  # Prevents popping
```

**Known Issues:**
- Audio popping → Increase `buffer_duration` to 100ms
- I²S DMA buffer error → Increase buffer size
- No audio → Verify MCLK configured (`use_mclk: true`)
- Sample rate mismatch → 16kHz mic, 48kHz speaker (resampled automatically)

## Sensors

**BME688 Environmental Sensor:**
- Interface: I²C (bus_a)
- Address: 0x77
- Measurements: Temperature, humidity, pressure, gas resistance (VOC)
- Accuracy: ±1°C, ±3% RH, ±1 hPa

**ICM-42607-P IMU:**
- Interface: SPI
- CS: GPIO10
- Measurements: 3-axis accelerometer, 3-axis gyroscope
- Range: ±2/±4/±8/±16g, ±250/±500/±1000/±2000 dps

## RGB LED

**WS2812 Status LED:**
- GPIO: 39
- Chipset: WS2812
- Count: 1 LED
- RGB Order: GRB

**Configuration:**
```yaml
light:
  - platform: esp32_rmt_led_strip
    pin: GPIO39
    num_leds: 1
    rgb_order: GRB
    chipset: WS2812
```

## Power

**USB-C:**
- Voltage: 5V
- Current: Up to 2A recommended (minimum 1A)
- Use: Programming, power, serial communication

**Power Budget:**
- ESP32-S3: ~500mA peak
- Display backlight: ~200mA
- Speaker: ~200-500mA (volume dependent)
- Total: 1-2A recommended supply

## Complete Pin Map Table

| GPIO | Function | Component | Direction | Notes |
|------|----------|-----------|-----------|-------|
| 0 | BOOT | Button | Input | Strapping pin |
| 2 | MCLK | I²S Audio | Output | Master clock for ES8311 |
| 3 | INT | Touch GT911 | Input | Interrupt, ignore strapping warning |
| 4 | DC | Display | Output | Data/command select |
| 5 | CS | Display | Output | Chip select |
| 6 | MOSI | Display SPI | Output | Data out |
| 7 | CLK | Display SPI | Output | Clock |
| 8 | SDA | I²C Bus A | Bidirectional | Touch, sensors, audio config |
| 10 | CS | IMU SPI | Output | ICM-42607-P chip select |
| 15 | DOUT | Speaker I²S | Output | ES8311 audio out |
| 16 | DIN | Microphone I²S | Input | ES7210 audio in |
| 17 | BCLK | I²S Bus | Output | Bit clock |
| 18 | SCL | I²C Bus A | Output | Clock |
| 39 | LED | RGB LED | Output | WS2812 status |
| 45 | LRCLK | I²S Bus | Output | Word select |
| 48 | RST | Display/Touch | Output | Shared reset (inverted) |

## I²C Device Addresses

| Device | Address | Alt Address | Notes |
|--------|---------|-------------|-------|
| GT911 Touch | 0x5D | 0x14 | Depends on INT pin at boot |
| ES7210 ADC | 0x40 | - | Microphone configuration |
| ES8311 DAC | 0x18 | - | Speaker configuration |
| BME688 Sensor | 0x77 | 0x76 | Environmental sensor |

## Known Hardware Issues

**Issue: Display/Touch Reset Pin Conflict**
- **Symptom**: Touch or display not working
- **Cause**: GPIO48 shared between display and touch
- **Solution**: Use `inverted: true` on reset_pin for both

**Issue: I²S DMA Buffer Errors**
- **Symptom**: Audio glitches, crashes
- **Cause**: Insufficient DMA buffer
- **Solution**: Set `buffer_duration: 100ms` in speaker config

**Issue: PSRAM Not Detected**
- **Symptom**: Boot fails, display issues
- **Cause**: PSRAM not configured (2025.2+ requirement)
- **Solution**: Add explicit PSRAM config: `psram: { mode: octal, speed: 80MHz }`

**Issue: UI Freezing During OTA**
- **Symptom**: Display freezes when updating firmware
- **Cause**: Code not executing from PSRAM
- **Solution**: Add `execute_from_psram: true` in esp32.framework.advanced

**Issue: Voice Assistant Crashes**
- **Symptom**: Random reboots when using voice
- **Cause**: Bluetooth interference on ESP32-S3
- **Solution**: Do NOT enable Bluetooth or BLE components

**Issue: Touch GPIO3 Strapping Warning**
- **Symptom**: ESPHome warns about strapping pin
- **Cause**: GPIO3 is used for boot mode selection
- **Solution**: Add `ignore_strapping_warning: true` to interrupt_pin

## Hardware Revisions

**BOX-3 vs BOX vs BOX-Lite:**
- **BOX-3** (latest): ESP32-S3, 16MB PSRAM, better audio
- **BOX**: ESP32-S3, 8MB PSRAM
- **BOX-Lite**: ESP32-S3, 2MB PSRAM, no speaker

Ensure using correct PSRAM mode for your hardware revision.

## Summary

**Critical Pin Configurations:**
- Display reset: GPIO48 inverted
- Touch reset: GPIO48 inverted (same as display)
- Touch interrupt: GPIO3 with `ignore_strapping_warning`
- MCLK: GPIO2 required for ES8311
- I²S buffer: 100ms minimum for stable audio
- PSRAM: Explicit octal mode configuration

**Common Pitfalls:**
- Forgetting `inverted: true` on GPIO48
- Not configuring MCLK for ES8311
- Using small I²S buffer (<100ms)
- Not configuring PSRAM explicitly (2025.2+)
- Enabling Bluetooth (causes crashes)
- Using `color_palette` other than NONE for 16-bit display

**Recommended Reading Order:**
1. This pinout reference (hardware overview)
2. display-lambdas.md (UI implementation)
3. touch-patterns.md (interaction patterns)
4. material-design.md (visual design)
