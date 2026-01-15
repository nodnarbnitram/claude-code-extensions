# Frigate FFmpeg Presets Reference

## Hardware Acceleration Presets

### Intel Platforms

| Preset | Use Case | Requirements |
|--------|----------|--------------|
| `preset-intel-qsv-h264` | H.264 decode via QSV | Intel gen8+ |
| `preset-intel-qsv-h265` | H.265 decode via QSV | Intel gen8+ |
| `preset-vaapi` | H.264/H.265 via VAAPI | Intel gen1-gen12 |

**Example:**
```yaml
ffmpeg:
  hwaccel_args: preset-intel-qsv-h264
```

### NVIDIA Platforms

| Preset | Use Case | Requirements |
|--------|----------|--------------|
| `preset-nvidia` | H.264/H.265 decode | NVIDIA GPU + Container Toolkit |

**Example:**
```yaml
ffmpeg:
  hwaccel_args: preset-nvidia
```

**Docker Requirements:**
```yaml
services:
  frigate:
    runtime: nvidia
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
```

### AMD Platforms

| Preset | Use Case | Requirements |
|--------|----------|--------------|
| `preset-vaapi` | H.264/H.265 via VAAPI | AMD GPU with radeonsi driver |

**Example:**
```yaml
ffmpeg:
  hwaccel_args: preset-vaapi
```

**Environment Variable:**
```yaml
environment:
  - LIBVA_DRIVER_NAME=radeonsi
```

### Raspberry Pi

| Preset | Use Case | Requirements |
|--------|----------|--------------|
| `preset-rpi-64-h264` | H.264 decode | RPi 4/5, 64-bit OS |
| `preset-rpi-64-h265` | H.265 decode | RPi 4/5, 64-bit OS |

**Requirements:**
- `gpu_mem=128` in `/boot/config.txt`
- Device mapping: `/dev/video10`, `/dev/video11`, `/dev/video12`

## Input Presets

### RTSP Transport

| Preset | Use Case |
|--------|----------|
| `preset-rtsp-restream` | Default RTSP with TCP transport |
| `preset-rtsp-udp` | RTSP with UDP transport |
| `preset-rtsp-blue-iris` | Optimized for Blue Iris |

**Example:**
```yaml
cameras:
  cam1:
    ffmpeg:
      inputs:
        - path: rtsp://camera/stream
          input_args: preset-rtsp-restream
```

### HTTP/MJPEG

| Preset | Use Case |
|--------|----------|
| `preset-http-jpeg-generic` | Generic MJPEG over HTTP |
| `preset-http-reolink` | Reolink HTTP MJPEG |

## Output Presets

### Recording Output

| Preset | Use Case |
|--------|----------|
| `preset-record-generic` | Default recording (no audio) |
| `preset-record-generic-audio-aac` | Recording with AAC audio |
| `preset-record-generic-audio-copy` | Recording with original audio |
| `preset-record-mjpeg` | MJPEG recording |
| `preset-record-ubiquiti` | Ubiquiti camera optimization |

**Example:**
```yaml
cameras:
  cam1:
    ffmpeg:
      output_args:
        record: preset-record-generic-audio-aac
```

## Common Configurations

### Intel System with Audio Recording

```yaml
ffmpeg:
  hwaccel_args: preset-intel-qsv-h264

cameras:
  front_door:
    ffmpeg:
      inputs:
        - path: rtsp://camera/substream
          input_args: preset-rtsp-restream
          roles:
            - detect
        - path: rtsp://camera/mainstream
          input_args: preset-rtsp-restream
          roles:
            - record
      output_args:
        record: preset-record-generic-audio-aac
```

### NVIDIA with go2rtc Restream

```yaml
ffmpeg:
  hwaccel_args: preset-nvidia

go2rtc:
  streams:
    front_door:
      - rtsp://camera/mainstream
      - "ffmpeg:front_door#video=copy#audio=opus"

cameras:
  front_door:
    ffmpeg:
      inputs:
        - path: rtsp://127.0.0.1:8554/front_door
          input_args: preset-rtsp-restream
          roles:
            - detect
            - record
```

### Raspberry Pi with H.265 Camera

```yaml
ffmpeg:
  hwaccel_args: preset-rpi-64-h265

cameras:
  front_door:
    ffmpeg:
      inputs:
        - path: rtsp://camera/h265stream
          input_args: preset-rtsp-restream
          roles:
            - detect
            - record
```

### UDP Transport for Unreliable Networks

```yaml
cameras:
  outdoor_cam:
    ffmpeg:
      inputs:
        - path: rtsp://camera/stream
          input_args: preset-rtsp-udp
          roles:
            - detect
```

## Troubleshooting

### RTSP URL Works in VLC but Not Frigate

Frigate defaults to TCP transport, while VLC auto-switches between UDP and TCP.

**Solution:**
```yaml
input_args: preset-rtsp-udp
```

### No Audio in Recordings

Default presets strip audio to prevent corruption.

**Solution:**
```yaml
output_args:
  record: preset-record-generic-audio-aac
```

### High CPU Despite Hardware Acceleration

1. Verify hardware acceleration is active in Frigate logs
2. Check Docker device mappings are correct
3. Ensure using correct preset for your hardware

### Green/Corrupted Video

Usually indicates wrong codec or resolution mismatch.

**Solutions:**
1. Verify camera actually outputs H.264 or H.265
2. Match `detect.width` and `detect.height` exactly to camera output
3. Try software decoding temporarily to rule out hwaccel issues

## Custom FFmpeg Arguments

For advanced use cases, you can specify raw FFmpeg arguments:

```yaml
cameras:
  cam1:
    ffmpeg:
      inputs:
        - path: rtsp://camera/stream
          input_args:
            - -avoid_negative_ts
            - make_zero
            - -fflags
            - +genpts+discardcorrupt
            - -rtsp_transport
            - tcp
            - -use_wallclock_as_timestamps
            - "1"
```

See [FFmpeg documentation](https://ffmpeg.org/documentation.html) for all available options.
