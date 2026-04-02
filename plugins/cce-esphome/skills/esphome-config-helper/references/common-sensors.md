# Common Sensor Configurations for ESPHome

Top 20 sensor configurations with wiring diagrams, platform selection guidance, and complete working examples.

## Temperature & Humidity Sensors

### 1. DHT22 (Temperature & Humidity)

**Platform**: `dht`
**Connection**: Single GPIO pin with pull-up resistor
**Accuracy**: ±0.5°C, ±2% RH
**Cost**: Low
**Reliability**: Moderate (prone to reading failures)

**Wiring**:
```
DHT22    ESP32/ESP8266
VCC  --> 3.3V
DATA --> GPIO4 (with 4.7kΩ pull-up to 3.3V)
GND  --> GND
```

**Configuration**:
```yaml
sensor:
  - platform: dht
    pin: GPIO4
    model: DHT22  # or DHT11, DHT21, AM2302
    temperature:
      name: "Temperature"
      filters:
        - sliding_window_moving_average:
            window_size: 5
            send_every: 5
    humidity:
      name: "Humidity"
      filters:
        - sliding_window_moving_average:
            window_size: 5
            send_every: 5
    update_interval: 60s
```

**Notes**:
- Use 4.7kΩ pull-up resistor on DATA line
- Update interval should be >2s (avoid too frequent readings)
- Use filters to smooth noisy readings
- Consider BME280 for more reliable operation

---

### 2. BME280 (Temperature, Humidity, Pressure)

**Platform**: `bme280`
**Connection**: I²C or SPI
**Accuracy**: ±1°C, ±3% RH, ±1 hPa
**Cost**: Moderate
**Reliability**: High (recommended over DHT22)

**Wiring (I²C)**:
```
BME280   ESP32       ESP8266
VCC  --> 3.3V        3.3V
GND  --> GND         GND
SDA  --> GPIO21      GPIO4 (D2)
SCL  --> GPIO22      GPIO5 (D1)
```

**Configuration**:
```yaml
i2c:
  sda: GPIO21  # ESP32, use GPIO4 for ESP8266
  scl: GPIO22  # ESP32, use GPIO5 for ESP8266
  scan: true

sensor:
  - platform: bme280
    temperature:
      name: "Temperature"
      oversampling: 16x
    humidity:
      name: "Humidity"
      oversampling: 16x
    pressure:
      name: "Pressure"
      oversampling: 16x
    address: 0x76  # or 0x77
    update_interval: 60s
```

**Notes**:
- I²C address is usually 0x76 or 0x77 (check with `scan: true`)
- Update interval >30s to prevent self-heating
- More reliable than DHT22, worth the extra cost
- Use oversampling to improve accuracy

---

### 3. DS18B20 (Waterproof Temperature)

**Platform**: `dallas`
**Connection**: 1-Wire protocol, single GPIO
**Accuracy**: ±0.5°C
**Cost**: Low
**Reliability**: High
**Special**: Waterproof versions available

**Wiring**:
```
DS18B20  ESP32/ESP8266
VCC  --> 3.3V
DATA --> GPIO4 (with 4.7kΩ pull-up to 3.3V)
GND  --> GND
```

**Configuration**:
```yaml
dallas:
  - pin: GPIO4

sensor:
  - platform: dallas
    address: 0x1c0000031edd2a28  # Use actual address from logs
    name: "Temperature"
    resolution: 12  # 9, 10, 11, or 12 bits
    update_interval: 60s
```

**Notes**:
- Requires 4.7kΩ pull-up resistor on DATA line
- Address auto-discovered on first boot (check logs)
- Multiple DS18B20 sensors can share same pin (1-Wire bus)
- Waterproof versions ideal for outdoor/pool/aquarium

---

### 4. SHT3x (High Accuracy Temperature & Humidity)

**Platform**: `sht3xd`
**Connection**: I²C
**Accuracy**: ±0.2°C, ±2% RH
**Cost**: Moderate
**Reliability**: Very High

**Wiring (I²C)**:
```
SHT3x    ESP32       ESP8266
VCC  --> 3.3V        3.3V
GND  --> GND         GND
SDA  --> GPIO21      GPIO4 (D2)
SCL  --> GPIO22      GPIO5 (D1)
```

**Configuration**:
```yaml
i2c:
  sda: GPIO21
  scl: GPIO22
  scan: true

sensor:
  - platform: sht3xd
    temperature:
      name: "Temperature"
    humidity:
      name: "Humidity"
    address: 0x44  # or 0x45
    update_interval: 60s
```

**Notes**:
- Superior accuracy compared to DHT22 and BME280
- I²C address is 0x44 or 0x45
- Very stable readings over time
- Higher cost but worth it for precision applications

---

## Motion & Presence Sensors

### 5. HC-SR501 PIR (Motion Sensor)

**Platform**: `gpio` (binary_sensor)
**Connection**: Single GPIO pin
**Range**: Up to 7 meters
**Cost**: Very Low
**Reliability**: High

**Wiring**:
```
HC-SR501  ESP32/ESP8266
VCC   --> 5V (or 3.3V depending on module)
OUT   --> GPIO14
GND   --> GND
```

**Configuration**:
```yaml
binary_sensor:
  - platform: gpio
    pin: GPIO14
    name: "Motion Sensor"
    device_class: motion
    filters:
      - delayed_off: 100ms  # Debounce
```

**Notes**:
- Some modules support 5V, others 3.3V (check datasheet)
- Adjustable sensitivity and time delay (potentiometers on module)
- Output HIGH when motion detected
- Use delayed_off filter to prevent flickering

---

### 6. RCWL-0516 (Microwave Motion Sensor)

**Platform**: `gpio` (binary_sensor)
**Connection**: Single GPIO pin
**Range**: Up to 7 meters through walls
**Cost**: Low
**Reliability**: High

**Wiring**:
```
RCWL-0516  ESP32/ESP8266
VIN   --> 5V
OUT   --> GPIO14
GND   --> GND
```

**Configuration**:
```yaml
binary_sensor:
  - platform: gpio
    pin: GPIO14
    name: "Microwave Motion Sensor"
    device_class: motion
    filters:
      - delayed_off: 500ms
```

**Notes**:
- Detects motion through walls, glass, plastic
- More sensitive than PIR (can detect small movements)
- Requires 5V power
- May have false triggers (WiFi, microwave ovens)

---

## Light Sensors

### 7. BH1750 (Ambient Light Sensor)

**Platform**: `bh1750`
**Connection**: I²C
**Range**: 1-65535 lux
**Cost**: Low
**Reliability**: High

**Wiring (I²C)**:
```
BH1750   ESP32       ESP8266
VCC  --> 3.3V        3.3V
GND  --> GND         GND
SDA  --> GPIO21      GPIO4 (D2)
SCL  --> GPIO22      GPIO5 (D1)
ADDR --> GND         GND (for 0x23)
```

**Configuration**:
```yaml
i2c:
  sda: GPIO21
  scl: GPIO22

sensor:
  - platform: bh1750
    name: "Illuminance"
    address: 0x23  # 0x23 (ADDR=GND) or 0x5C (ADDR=VCC)
    update_interval: 60s
```

**Notes**:
- Accurate lux measurements (better than LDR)
- I²C address: 0x23 (ADDR=GND) or 0x5C (ADDR=VCC)
- Low power consumption
- Ideal for automatic lighting control

---

### 8. TSL2561 (Light Sensor with IR)

**Platform**: `tsl2561`
**Connection**: I²C
**Range**: 0.1-40,000 lux
**Cost**: Moderate
**Reliability**: High

**Wiring (I²C)**:
```
TSL2561  ESP32       ESP8266
VCC  --> 3.3V        3.3V
GND  --> GND         GND
SDA  --> GPIO21      GPIO4 (D2)
SCL  --> GPIO22      GPIO5 (D1)
```

**Configuration**:
```yaml
i2c:
  sda: GPIO21
  scl: GPIO22

sensor:
  - platform: tsl2561
    name: "Illuminance"
    address: 0x39  # 0x29, 0x39, or 0x49
    update_interval: 60s
```

**Notes**:
- Dual spectrum (visible + IR)
- Better for outdoor use (compensates for IR)
- I²C address: 0x29, 0x39, or 0x49
- More expensive than BH1750

---

## Distance Sensors

### 9. HC-SR04 (Ultrasonic Distance Sensor)

**Platform**: `ultrasonic`
**Connection**: 2 GPIO pins (trigger + echo)
**Range**: 2-400 cm
**Cost**: Very Low
**Reliability**: Moderate

**Wiring**:
```
HC-SR04  ESP32/ESP8266
VCC   --> 5V
TRIG  --> GPIO12
ECHO  --> GPIO14 (with voltage divider if using 5V module)
GND   --> GND
```

**Configuration**:
```yaml
sensor:
  - platform: ultrasonic
    trigger_pin: GPIO12
    echo_pin: GPIO14
    name: "Distance"
    update_interval: 60s
    timeout: 3m  # Maximum measurement timeout
    filters:
      - filter_out: nan
      - median:
          window_size: 7
          send_every: 4
```

**Notes**:
- 5V modules require voltage divider on ECHO (5V → 3.3V)
- Affected by temperature and humidity
- Use filters to smooth readings
- Not suitable for very short distances (<2cm)

---

### 10. VL53L0X (ToF Laser Distance Sensor)

**Platform**: `vl53l0x`
**Connection**: I²C
**Range**: 3-200 cm
**Cost**: Moderate
**Reliability**: High

**Wiring (I²C)**:
```
VL53L0X  ESP32       ESP8266
VCC  --> 3.3V        3.3V
GND  --> GND         GND
SDA  --> GPIO21      GPIO4 (D2)
SCL  --> GPIO22      GPIO5 (D1)
```

**Configuration**:
```yaml
i2c:
  sda: GPIO21
  scl: GPIO22

sensor:
  - platform: vl53l0x
    name: "Distance"
    address: 0x29
    update_interval: 1s
    long_range: true  # Up to 2m (less accurate)
```

**Notes**:
- Time-of-Flight laser (very accurate)
- Not affected by ambient light or object color
- I²C address: 0x29
- long_range mode extends to 2m but reduces accuracy

---

## Air Quality Sensors

### 11. BME680 (Air Quality, Temp, Humidity, Pressure)

**Platform**: `bme680`
**Connection**: I²C or SPI
**Accuracy**: ±1°C, ±3% RH, ±1 hPa
**Cost**: Moderate-High
**Reliability**: High

**Wiring (I²C)**:
```
BME680   ESP32       ESP8266
VCC  --> 3.3V        3.3V
GND  --> GND         GND
SDA  --> GPIO21      GPIO4 (D2)
SCL  --> GPIO22      GPIO5 (D1)
```

**Configuration**:
```yaml
i2c:
  sda: GPIO21
  scl: GPIO22

sensor:
  - platform: bme680
    temperature:
      name: "Temperature"
    humidity:
      name: "Humidity"
    pressure:
      name: "Pressure"
    gas_resistance:
      name: "Gas Resistance"
    address: 0x76  # or 0x77
    update_interval: 60s
```

**Notes**:
- Gas resistance indicates air quality (VOC)
- Requires burn-in period (48 hours for stable readings)
- I²C address: 0x76 or 0x77
- Superior to BME280 for air quality monitoring

---

### 12. SGP30 (eCO2 and TVOC Sensor)

**Platform**: `sgp30`
**Connection**: I²C
**Measurements**: eCO2 (400-60,000 ppm), TVOC (0-60,000 ppb)
**Cost**: Moderate
**Reliability**: High

**Wiring (I²C)**:
```
SGP30    ESP32       ESP8266
VCC  --> 3.3V        3.3V
GND  --> GND         GND
SDA  --> GPIO21      GPIO4 (D2)
SCL  --> GPIO22      GPIO5 (D1)
```

**Configuration**:
```yaml
i2c:
  sda: GPIO21
  scl: GPIO22

sensor:
  - platform: sgp30
    eco2:
      name: "eCO2"
      accuracy_decimals: 1
    tvoc:
      name: "TVOC"
      accuracy_decimals: 1
    address: 0x58
    update_interval: 1s
    compensation:
      temperature_source: temp_sensor_id  # Optional
      humidity_source: humidity_sensor_id  # Optional
```

**Notes**:
- Requires 12-hour burn-in for accurate readings
- Baseline calibration improves over time
- Compensation with temp/humidity improves accuracy
- Fixed I²C address: 0x58

---

## Energy Monitoring

### 13. INA219 (Current/Voltage/Power Sensor)

**Platform**: `ina219`
**Connection**: I²C
**Range**: 0-26V, ±3.2A (with 0.1Ω shunt)
**Cost**: Low
**Reliability**: High

**Wiring (I²C)**:
```
INA219   ESP32       ESP8266
VCC  --> 3.3V        3.3V
GND  --> GND         GND
SDA  --> GPIO21      GPIO4 (D2)
SCL  --> GPIO22      GPIO5 (D1)
```

**Configuration**:
```yaml
i2c:
  sda: GPIO21
  scl: GPIO22

sensor:
  - platform: ina219
    address: 0x40
    shunt_resistance: 0.1 ohm
    current:
      name: "Current"
    power:
      name: "Power"
    bus_voltage:
      name: "Bus Voltage"
    shunt_voltage:
      name: "Shunt Voltage"
    max_voltage: 26V
    max_current: 3.2A
    update_interval: 60s
```

**Notes**:
- Measures DC current, voltage, and power
- Shunt resistor value affects max current
- I²C address: 0x40-0x4F (configurable)
- Ideal for battery monitoring, solar panels

---

### 14. PZEM-004T (AC Power Monitor)

**Platform**: `pzemac` or `pzemdc`
**Connection**: UART
**Range**: 80-260V, 0-100A
**Cost**: Moderate
**Reliability**: High

**Wiring (UART)**:
```
PZEM-004T  ESP32
5V     --> 5V
TX     --> GPIO16 (RX2)
RX     --> GPIO17 (TX2)
GND    --> GND
```

**Configuration**:
```yaml
uart:
  id: uart_bus
  tx_pin: GPIO17
  rx_pin: GPIO16
  baud_rate: 9600

sensor:
  - platform: pzemac
    current:
      name: "Current"
    voltage:
      name: "Voltage"
    power:
      name: "Power"
    energy:
      name: "Energy"
    frequency:
      name: "Frequency"
    power_factor:
      name: "Power Factor"
    update_interval: 60s
```

**Notes**:
- AC power monitoring (mains voltage)
- Separate CT (current transformer) for current measurement
- PZEM-004T v3.0 uses UART (older versions use different protocol)
- Dangerous if not installed correctly (mains voltage)

---

## Environmental Sensors

### 15. MH-Z19 (CO2 Sensor)

**Platform**: `mhz19`
**Connection**: UART
**Range**: 0-5000 ppm CO2
**Cost**: Moderate
**Reliability**: High

**Wiring (UART)**:
```
MH-Z19   ESP32
VIN  --> 5V
TX   --> GPIO16 (RX2)
RX   --> GPIO17 (TX2)
GND  --> GND
```

**Configuration**:
```yaml
uart:
  id: uart_bus
  tx_pin: GPIO17
  rx_pin: GPIO16
  baud_rate: 9600

sensor:
  - platform: mhz19
    co2:
      name: "CO2"
    temperature:
      name: "Temperature"
    update_interval: 60s
    automatic_baseline_calibration: false
```

**Notes**:
- Requires 24-hour warm-up for accurate readings
- Automatic baseline calibration should be disabled for accurate readings
- Manual calibration in fresh air (400 ppm) recommended
- Preheating time: 3 minutes

---

### 16. SDS011 (Particulate Matter Sensor)

**Platform**: `sds011`
**Connection**: UART
**Range**: PM2.5 and PM10 (0-999.9 μg/m³)
**Cost**: Moderate
**Reliability**: High

**Wiring (UART)**:
```
SDS011   ESP32
5V   --> 5V
TX   --> GPIO16 (RX2)
RX   --> GPIO17 (TX2)
GND  --> GND
```

**Configuration**:
```yaml
uart:
  id: uart_bus
  tx_pin: GPIO17
  rx_pin: GPIO16
  baud_rate: 9600

sensor:
  - platform: sds011
    pm_2_5:
      name: "PM2.5"
    pm_10_0:
      name: "PM10"
    update_interval: 5min
    rx_only: false  # Set to true if you only connect RX
```

**Notes**:
- Measures fine dust particles (PM2.5 and PM10)
- Laser-based sensor (very accurate)
- Fan can be controlled (sleep mode to extend life)
- Use longer update_interval to extend fan life

---

## Other Common Sensors

### 17. Pulse Counter (Water/Gas/Electricity Meter)

**Platform**: `pulse_counter`
**Connection**: Single GPIO pin
**Cost**: Free (uses existing meter)
**Reliability**: High

**Wiring**:
```
Pulse Output  ESP32/ESP8266
Signal    --> GPIO14 (with pull-up if needed)
GND       --> GND
```

**Configuration**:
```yaml
sensor:
  - platform: pulse_counter
    pin: GPIO14
    name: "Water Usage"
    unit_of_measurement: "L/min"
    filters:
      - multiply: 0.5  # Convert pulses to liters (depends on meter)
    total:
      name: "Total Water Usage"
      unit_of_measurement: "L"
      filters:
        - multiply: 0.5
```

**Notes**:
- Works with utility meters that have pulse output
- Calibration factor depends on meter (pulses per liter/kWh)
- Can monitor water, gas, electricity consumption
- Use internal_filter to debounce noisy signals

---

### 18. Rotary Encoder

**Platform**: `rotary_encoder`
**Connection**: 2 GPIO pins (CLK + DT)
**Cost**: Very Low
**Reliability**: High

**Wiring**:
```
Encoder  ESP32/ESP8266
CLK  --> GPIO12
DT   --> GPIO14
SW   --> GPIO13 (optional button)
+    --> 3.3V
GND  --> GND
```

**Configuration**:
```yaml
sensor:
  - platform: rotary_encoder
    name: "Rotary Encoder"
    pin_a: GPIO12
    pin_b: GPIO14
    resolution: 1  # 1, 2, or 4 (steps per detent)
    min_value: 0
    max_value: 100
    publish_initial_value: true

binary_sensor:
  - platform: gpio
    pin:
      number: GPIO13
      mode: INPUT_PULLUP
      inverted: true
    name: "Encoder Button"
```

**Notes**:
- Mechanical encoders may need debouncing
- resolution depends on encoder type (usually 1 or 2)
- Optional button (SW pin) for click detection
- Can be used for volume control, dimming, menu navigation

---

### 19. AHT10/AHT20 (Temperature & Humidity)

**Platform**: `aht10`
**Connection**: I²C
**Accuracy**: ±0.3°C, ±2% RH
**Cost**: Low
**Reliability**: High

**Wiring (I²C)**:
```
AHT10/20  ESP32       ESP8266
VCC   --> 3.3V        3.3V
GND   --> GND         GND
SDA   --> GPIO21      GPIO4 (D2)
SCL   --> GPIO22      GPIO5 (D1)
```

**Configuration**:
```yaml
i2c:
  sda: GPIO21
  scl: GPIO22

sensor:
  - platform: aht10
    temperature:
      name: "Temperature"
    humidity:
      name: "Humidity"
    update_interval: 60s
```

**Notes**:
- Good alternative to DHT22 (more reliable)
- Fixed I²C address: 0x38
- Lower cost than BME280
- Newer AHT20 is drop-in replacement

---

### 20. Analog Input (Generic)

**Platform**: `adc`
**Connection**: Single ADC pin
**Range**: 0-3.3V (ESP32 with attenuation), 0-1V (ESP8266)
**Cost**: Free
**Reliability**: High

**Wiring**:
```
Sensor Output  ESP32           ESP8266
Signal     --> GPIO32 (ADC)    A0
GND        --> GND             GND
```

**Configuration (ESP32)**:
```yaml
sensor:
  - platform: adc
    pin: GPIO32  # Any ADC-capable pin
    name: "Analog Input"
    attenuation: 11db  # 0db (0-1V), 2.5db (0-1.5V), 6db (0-2V), 11db (0-3.3V)
    update_interval: 60s
    filters:
      - calibrate_linear:
          - 0.0 -> 0.0
          - 3.3 -> 100.0  # Map voltage to meaningful units
```

**Configuration (ESP8266)**:
```yaml
sensor:
  - platform: adc
    pin: A0  # Only ADC pin on ESP8266
    name: "Analog Input"
    update_interval: 60s
    filters:
      - multiply: 3.3  # Convert to voltage (0-1V range)
```

**Notes**:
- ESP32 has 18 ADC pins, ESP8266 has only 1 (A0)
- Use attenuation on ESP32 to adjust input range
- Use calibrate_linear filter to map voltage to sensor units
- Requires external voltage divider if sensor output >3.3V

---

## Sensor Selection Guide

### Temperature/Humidity
- **Budget**: DHT22 (GPIO, ±0.5°C)
- **Recommended**: BME280 (I²C, ±1°C, includes pressure)
- **High Accuracy**: SHT3x (I²C, ±0.2°C)
- **Waterproof**: DS18B20 (1-Wire, ±0.5°C)

### Motion Detection
- **Indoor**: HC-SR501 PIR (GPIO, 7m range)
- **Through Walls**: RCWL-0516 Microwave (GPIO, 7m through obstacles)

### Light Level
- **Budget/Accurate**: BH1750 (I²C, 1-65535 lux)
- **Outdoor/IR Compensation**: TSL2561 (I²C, dual spectrum)

### Distance Measurement
- **Budget**: HC-SR04 Ultrasonic (GPIO, 2-400cm)
- **Accurate**: VL53L0X ToF Laser (I²C, 3-200cm)

### Air Quality
- **Budget**: MQ-series Gas Sensors (analog, specific gases)
- **Recommended**: BME680 (I²C, VOC/gas resistance)
- **CO2 Specific**: MH-Z19 (UART, 0-5000 ppm)
- **Particulate Matter**: SDS011 (UART, PM2.5/PM10)

### Energy Monitoring
- **DC Power**: INA219 (I²C, 0-26V, 0-3.2A)
- **AC Power**: PZEM-004T (UART, 80-260V, 0-100A)

### Connection Type Comparison
- **GPIO**: Simplest, one pin, limited accuracy (PIR, DHT22)
- **I²C**: Multiple sensors on 2 pins, accurate (BME280, BH1750)
- **1-Wire**: Multiple sensors on 1 pin (DS18B20)
- **SPI**: Fast, requires 4 pins (displays, high-speed sensors)
- **UART**: Serial communication, requires 2 pins (PZEM, MH-Z19)
- **Analog (ADC)**: Voltage measurement, requires calibration (potentiometers, LDR)

---

## Summary

**Most Versatile**: BME280 (temp/humidity/pressure, I²C, reliable)

**Best Motion**: HC-SR501 PIR (low cost, reliable, easy)

**Best Light**: BH1750 (accurate lux, I²C, low cost)

**Best Air Quality**: BME680 (comprehensive, I²C, includes VOC)

**Best Distance**: VL53L0X (accurate, I²C, not affected by ambient light)

**Best for Beginners**: DHT22, HC-SR501, BH1750 (simple GPIO/I²C, low cost)

**Most Reliable**: I²C sensors (BME280, BH1750, SHT3x, VL53L0X)
