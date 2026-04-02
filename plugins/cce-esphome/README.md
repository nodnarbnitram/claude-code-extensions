# CCE ESPHome Plugin

ESPHome IoT development for ESP32/ESP8266 with Home Assistant integration.

## Overview

The **cce-esphome** plugin provides comprehensive ESPHome development support, from basic device configuration to advanced ESP32-S3-BOX-3 voice assistant builds. Covers networking, automation, components, Home Assistant integration, and hardware-specific patterns.

## Features

- **Device Support**: ESP32, ESP8266, ESP32-S3, RP2040
- **100+ Components**: Sensors, outputs, displays, binary sensors, switches, lights, climate
- **Voice Assistant**: ESP32-S3-BOX-3 audio pipeline (I2S, ES7210 ADC, ES8311 DAC)
- **Home Assistant Integration**: Bidirectional communication, entity sync, service calls
- **Networking**: WiFi, Ethernet, mDNS, API encryption, OTA updates
- **Automation**: Triggers, conditions, actions, lambdas, scripts, state machines

## Plugin Components

### Agents (6)

- **esphome-core**: Core concepts, YAML configuration, device fundamentals
- **esphome-components**: 100+ component library (sensors, displays, lights, climate)
- **esphome-networking**: WiFi, Ethernet, mDNS, API encryption, OTA, MQTT
- **esphome-automations**: Automation logic, triggers, conditions, lambdas, scripts
- **esphome-homeassistant**: Home Assistant integration and bidirectional communication
- **esphome-box3**: ESP32-S3-BOX-3 hardware specialist (audio pipeline, display, touch, voice)

### Skills (2)

- **esphome-config-helper**: Rapid ESPHome YAML generation and validation
- **esphome-box3-builder**: ESP32-S3-BOX-3 templates and voice assistant configs

## Installation

### From Marketplace (Recommended)

```bash
# Add the CCE marketplace
/plugin marketplace add github:nodnarbnitram/claude-code-extensions

# Install ESPHome plugin
/plugin install cce-esphome@cce-marketplace
```

### From Local Source

```bash
git clone https://github.com/nodnarbnitram/claude-code-extensions.git
/plugin marketplace add /path/to/claude-code-extensions
/plugin install cce-esphome@cce-marketplace
```

## Usage

### Skills (User-Invoked)

```bash
/esphome-config-helper
# Interactive config generation with device selection and component wizard

/esphome-box3-builder
# ESP32-S3-BOX-3 voice assistant template generation
```

### Agents (Automatic Activation)

```bash
> Create ESPHome config for ESP32 with temperature sensor
# Uses esphome-core + esphome-components

> Add WiFi with static IP and OTA updates
# Uses esphome-networking

> Implement automation to turn on light at sunset
# Uses esphome-automations

> Sync Home Assistant sensor states to ESPHome
# Uses esphome-homeassistant

> Configure ESP32-S3-BOX-3 audio pipeline for voice assistant
# Uses esphome-box3
```

### Example Workflows

**Basic ESP32 Sensor:**
```bash
/esphome-config-helper
# Generates complete YAML with WiFi, OTA, API, and sensors
```

**Voice Assistant on BOX-3:**
```bash
/esphome-box3-builder
# Complete voice assistant with I2S audio, ILI9xxx display, GT911 touch
```

**Home Assistant Integration:**
```bash
> Import Home Assistant sun.sun entity for sunrise/sunset automations
# Sets up homeassistant.sensor platform
```

## Requirements

- **Claude Code**: Latest version
- **ESPHome**: 2024.x+ recommended
- **Python**: 3.9+ (for ESPHome CLI)
- **Home Assistant**: For integration features (optional)

## Hardware Coverage

- **ESP32**: All variants (ESP32, ESP32-S2, ESP32-S3, ESP32-C3)
- **ESP8266**: NodeMCU, Wemos D1 Mini, etc.
- **ESP32-S3-BOX-3**: Audio (I2S/ES7210/ES8311), ILI9xxx display, GT911 touch
- **RP2040**: Raspberry Pi Pico W

## Component Categories

- **Sensors**: Temperature, humidity, motion, light, energy monitoring
- **Binary Sensors**: GPIO, touch, presence detection
- **Switches**: GPIO control, template switches
- **Lights**: RGB, RGBW, addressable LEDs (WS2812)
- **Climate**: Thermostats, IR remote control
- **Displays**: OLED, TFT, e-paper with lambda rendering
- **Voice**: Microphone, speaker, voice assistant

## License

MIT License - see [LICENSE](../../../LICENSE) for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/nodnarbnitram/claude-code-extensions/issues)
- **Documentation**: [Repository README](../../../README.md)
- **ESPHome Docs**: [esphome.io](https://esphome.io)
