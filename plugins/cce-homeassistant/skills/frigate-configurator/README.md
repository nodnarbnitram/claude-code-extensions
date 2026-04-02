# Frigate NVR Configuration Expert

> Configure Frigate NVR with optimized YAML, object detection, recording, zones, and hardware acceleration.

| | |
|---|---|
| **Status** | Active |
| **Version** | 1.0.0 |
| **Last Updated** | 2025-12-27 |
| **Confidence** | 5/5 |
| **Production Tested** | https://docs.frigate.video/ |

## What This Skill Does

This skill provides expert-level assistance for configuring and troubleshooting Frigate NVR, an AI-powered network video recorder with real-time object detection.

### Core Capabilities

- Generate optimized Frigate YAML configurations for any camera setup
- Configure object detectors (Coral TPU, OpenVINO, ONNX, CPU)
- Set up hardware-accelerated video decoding (Intel QSV/VAAPI, NVIDIA, AMD, Raspberry Pi)
- Configure recording with intelligent retention policies
- Create zones for location-aware detection and speed estimation
- Troubleshoot common issues (bus errors, green video, high CPU)
- Integrate with Home Assistant via MQTT
- Configure go2rtc for WebRTC live streaming
- Set up advanced features: face recognition, LPR, audio detection, GenAI descriptions

## Auto-Trigger Keywords

### Primary Keywords
Exact terms that strongly trigger this skill:
- frigate
- frigate config
- frigate yaml
- frigate nvr
- frigate camera
- frigate detector
- frigate recording
- frigate zones
- coral tpu
- edgetpu

### Secondary Keywords
Related terms that may trigger in combination:
- object detection nvr
- ai camera recording
- rtsp object detection
- home assistant camera
- nvr configuration
- video surveillance ai
- birdseye view
- motion mask
- detection zone
- go2rtc

### Error-Based Keywords
Common error messages that should trigger this skill:
- "Fatal Python error: Bus error"
- "database is locked"
- "shm_size"
- "green video frigate"
- "coral not detected"
- "mqtt connection failed"
- "camera offline frigate"
- "no objects detected"
- "recording not working frigate"
- "high cpu usage frigate"

## Known Issues Prevention

| Issue | Root Cause | Solution |
|-------|-----------|----------|
| Bus Error | Insufficient shared memory | Set `shm-size: 256mb` in docker-compose |
| Database Locked | SQLite on network storage | Use local storage for database |
| Green/Distorted Video | Wrong resolution in config | Match camera's actual output resolution |
| Coral Not Detected | Missing device passthrough | Add `/dev/bus/usb` to Docker devices |
| High CPU Usage | Missing hardware acceleration | Configure hwaccel preset |
| No Audio in Recordings | Default audio stripping | Use `preset-record-generic-audio-aac` |

## When to Use

### Use This Skill For
- Initial Frigate NVR setup and configuration
- Adding new cameras to existing Frigate installation
- Configuring Coral TPU or OpenVINO detectors
- Setting up recording with retention policies
- Creating detection zones and motion masks
- Troubleshooting camera connectivity issues
- Optimizing performance and reducing CPU usage
- Integrating Frigate with Home Assistant
- Configuring hardware acceleration (Intel/NVIDIA/AMD/RPi)
- Setting up go2rtc for live streaming

### Don't Use This Skill For
- General RTSP camera troubleshooting (not Frigate-specific)
- Home Assistant automations (use ha-dashboard skill)
- Generic Docker troubleshooting
- Network configuration unrelated to Frigate
- Non-Frigate NVR software (ZoneMinder, Blue Iris, etc.)

## Quick Usage

```yaml
# Minimal Frigate config with Coral TPU
mqtt:
  enabled: false

detectors:
  coral:
    type: edgetpu
    device: usb

cameras:
  front_door:
    ffmpeg:
      inputs:
        - path: rtsp://user:pass@192.168.1.100:554/stream1
          roles:
            - detect
    detect:
      width: 1280
      height: 720
      fps: 5
```

## Token Efficiency

| Approach | Estimated Tokens | Time |
|----------|-----------------|------|
| Manual Implementation | ~15,000 | 2-4 hours |
| With This Skill | ~6,000 | 30-45 min |
| **Savings** | **60%** | **75%** |

## File Structure

```
frigate-configurator/
├── SKILL.md        # Detailed instructions and patterns
├── README.md       # This file - discovery and quick reference
├── templates/      # Docker-compose and config templates
│   ├── docker-compose.yml
│   ├── config-minimal.yml
│   └── config-full.yml
├── references/     # Supporting documentation
│   ├── detector-comparison.md
│   ├── ffmpeg-presets.md
│   └── mqtt-topics.md
└── scripts/        # Validation utilities
    └── validate-config.sh
```

## Dependencies

| Package | Version | Verified |
|---------|---------|----------|
| Frigate | 0.14+ | 2025-12-27 |
| Docker | 20.10+ | 2025-12-27 |
| docker-compose | 2.0+ | 2025-12-27 |

## Official Documentation

- [Frigate Documentation](https://docs.frigate.video/)
- [Configuration Reference](https://docs.frigate.video/configuration/reference)
- [Object Detectors](https://docs.frigate.video/configuration/object_detectors)
- [Hardware Acceleration](https://docs.frigate.video/configuration/hardware_acceleration_video)
- [Troubleshooting FAQs](https://docs.frigate.video/troubleshooting/faqs)

## Related Skills

- `ha-dashboard` - Home Assistant Lovelace dashboard configuration
- `esphome-config-helper` - ESPHome device configuration

---

**License:** MIT
