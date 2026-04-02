# Frigate MQTT Topics Reference

## Topic Prefix

All topics are prefixed with the configured `topic_prefix` (default: `frigate`).

Example: `frigate/available` or `frigate/front_door/person`

## Availability Topics

| Topic | Payload | Description |
|-------|---------|-------------|
| `frigate/available` | `online` / `offline` | Frigate availability status |

## Camera Topics

### Camera State

| Topic | Payload | Description |
|-------|---------|-------------|
| `frigate/{camera}/recordings/state` | `ON` / `OFF` | Recording state |
| `frigate/{camera}/snapshots/state` | `ON` / `OFF` | Snapshot state |
| `frigate/{camera}/detect/state` | `ON` / `OFF` | Detection state |
| `frigate/{camera}/motion/state` | `ON` / `OFF` | Motion detection state |
| `frigate/{camera}/improve_contrast/state` | `ON` / `OFF` | Contrast enhancement state |
| `frigate/{camera}/ptz_autotracker/state` | `ON` / `OFF` | PTZ autotracker state |

### Camera Control

| Topic | Payload | Description |
|-------|---------|-------------|
| `frigate/{camera}/recordings/set` | `ON` / `OFF` | Enable/disable recording |
| `frigate/{camera}/snapshots/set` | `ON` / `OFF` | Enable/disable snapshots |
| `frigate/{camera}/detect/set` | `ON` / `OFF` | Enable/disable detection |
| `frigate/{camera}/motion/set` | `ON` / `OFF` | Enable/disable motion detection |
| `frigate/{camera}/improve_contrast/set` | `ON` / `OFF` | Enable/disable contrast |
| `frigate/{camera}/ptz_autotracker/set` | `ON` / `OFF` | Enable/disable autotracker |

### Object Detection

| Topic | Payload | Description |
|-------|---------|-------------|
| `frigate/{camera}/{object}` | Count (integer) | Current object count |
| `frigate/{camera}/{object}/snapshot` | JPEG binary | Latest snapshot with object |

**Example:** `frigate/front_door/person` = `1`

### Motion Detection

| Topic | Payload | Description |
|-------|---------|-------------|
| `frigate/{camera}/motion` | `ON` / `OFF` | Motion currently detected |

### Audio Detection

| Topic | Payload | Description |
|-------|---------|-------------|
| `frigate/{camera}/audio/{audio_type}` | `ON` / `OFF` | Audio event detected |

**Audio Types:** `bark`, `fire_alarm`, `scream`, `speech`, `yell`, etc.

## Event Topics

### New Events

| Topic | Payload | Description |
|-------|---------|-------------|
| `frigate/events` | JSON object | New event notification |

**Event Payload Structure:**
```json
{
  "before": {
    "id": "1234567890.123456-abc123",
    "camera": "front_door",
    "frame_time": 1234567890.123456,
    "snapshot_time": 1234567890.123456,
    "label": "person",
    "sub_label": null,
    "top_score": 0.89,
    "false_positive": false,
    "start_time": 1234567890.123456,
    "end_time": null,
    "score": 0.89,
    "box": [100, 200, 300, 400],
    "area": 40000,
    "ratio": 1.5,
    "region": [0, 0, 640, 480],
    "stationary": false,
    "motionless_count": 0,
    "position_changes": 5,
    "current_zones": ["front_yard"],
    "entered_zones": ["front_yard"],
    "thumbnail": null,
    "has_clip": true,
    "has_snapshot": true
  },
  "after": {
    // Same structure with updated values
  },
  "type": "new"  // "new", "update", or "end"
}
```

### Event Types

| Type | Description |
|------|-------------|
| `new` | Object first detected |
| `update` | Object tracking updated |
| `end` | Object tracking ended |

## Review Topics

| Topic | Payload | Description |
|-------|---------|-------------|
| `frigate/reviews` | JSON object | Review event notification |

## Statistics Topics

| Topic | Payload | Description |
|-------|---------|-------------|
| `frigate/stats` | JSON object | System statistics |

**Stats Payload Example:**
```json
{
  "cpu_usages": {"python_frigate": 15.2},
  "detectors": {
    "coral": {
      "detection_start": 0.0,
      "inference_speed": 8.5,
      "pid": 1234
    }
  },
  "cameras": {
    "front_door": {
      "camera_fps": 5.0,
      "detection_fps": 5.0,
      "capture_pid": 1235,
      "ffmpeg_pid": 1236,
      "process_fps": 5.0
    }
  },
  "service": {
    "uptime": 86400,
    "version": "0.14.0",
    "storage": {
      "/media/frigate/recordings": {
        "free": 500000000000,
        "total": 1000000000000
      }
    }
  }
}
```

## Home Assistant Integration

### Auto-Discovery

Frigate publishes Home Assistant MQTT discovery messages automatically when configured:

```yaml
mqtt:
  enabled: true
  host: 192.168.1.50
```

### Created Entities

| Entity Type | Entity ID Pattern | Description |
|-------------|-------------------|-------------|
| Camera | `camera.{camera}_frigate` | Live camera feed |
| Binary Sensor | `binary_sensor.{camera}_motion` | Motion detection |
| Binary Sensor | `binary_sensor.{camera}_person` | Person detection |
| Binary Sensor | `binary_sensor.{camera}_car` | Car detection |
| Switch | `switch.{camera}_detect` | Detection toggle |
| Switch | `switch.{camera}_recordings` | Recording toggle |
| Switch | `switch.{camera}_snapshots` | Snapshot toggle |
| Sensor | `sensor.{camera}_fps` | Camera FPS |
| Sensor | `sensor.{camera}_detection_fps` | Detection FPS |

## Example Automations

### Notification on Person Detection

```yaml
automation:
  - alias: "Frigate Person Alert"
    trigger:
      - platform: mqtt
        topic: frigate/front_door/person
    condition:
      - condition: template
        value_template: "{{ trigger.payload | int > 0 }}"
    action:
      - service: notify.mobile_app
        data:
          title: "Person Detected"
          message: "Person detected at front door"
          data:
            image: "http://frigate:8971/api/front_door/latest.jpg"
```

### Track Events

```yaml
automation:
  - alias: "Frigate Event Logger"
    trigger:
      - platform: mqtt
        topic: frigate/events
    action:
      - service: logbook.log
        data:
          name: "Frigate"
          message: >
            {{ trigger.payload_json.after.label }} detected on
            {{ trigger.payload_json.after.camera }}
```

### Control Recording

```yaml
# Enable recording
service: mqtt.publish
data:
  topic: frigate/front_door/recordings/set
  payload: "ON"

# Disable detection
service: mqtt.publish
data:
  topic: frigate/front_door/detect/set
  payload: "OFF"
```

## Debugging MQTT

### Subscribe to All Frigate Topics

```bash
mosquitto_sub -h 192.168.1.50 -u user -P password -t "frigate/#" -v
```

### Subscribe to Specific Camera Events

```bash
mosquitto_sub -h 192.168.1.50 -u user -P password -t "frigate/front_door/person" -v
```

### Test Publishing

```bash
mosquitto_pub -h 192.168.1.50 -u user -P password -t "frigate/front_door/detect/set" -m "OFF"
```
