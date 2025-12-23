# Touch Interaction Patterns for ESP32-S3-BOX-3 GT911

Complete guide to touchscreen binary sensors, gesture detection, and page navigation patterns.

## Touch Binary Sensors

### Button Zone Pattern

```yaml
binary_sensor:
  - platform: touchscreen
    name: "Button Name"
    x_min: 10
    x_max: 150
    y_min: 200
    y_max: 240
    on_press:
      - logger.log: "Button pressed"
    on_release:
      - logger.log: "Button released"
```

### Common Button Sizes

**Material Design minimum touch target: 48x48 pixels**

- Small button: 60x40px
- Medium button: 100x48px
- Large button: 140x60px
- Full-width button: 300x48px

### Button Grid Layout

**3 buttons (bottom row):**
```yaml
binary_sensor:
  # Left button
  - platform: touchscreen
    name: "Button 1"
    x_min: 10
    x_max: 100
    y_min: 200
    y_max: 240

  # Center button
  - platform: touchscreen
    name: "Button 2"
    x_min: 110
    x_max: 210
    y_min: 200
    y_max: 240

  # Right button
  - platform: touchscreen
    name: "Button 3"
    x_min: 220
    x_max: 310
    y_min: 200
    y_max: 240
```

## Gesture Detection

### Swipe Left/Right

```yaml
binary_sensor:
  # Swipe right zone
  - platform: touchscreen
    name: "Swipe Right"
    x_min: 220
    x_max: 320
    y_min: 80
    y_max: 160
    on_press:
      - lambda: |-
          id(current_page) = (id(current_page) + 1) % 3;

  # Swipe left zone
  - platform: touchscreen
    name: "Swipe Left"
    x_min: 0
    x_max: 100
    y_min: 80
    y_max: 160
    on_press:
      - lambda: |-
          id(current_page) = (id(current_page) - 1 + 3) % 3;
```

### Long Press

```yaml
binary_sensor:
  - platform: touchscreen
    name: "Long Press Button"
    x_min: 10
    x_max: 310
    y_min: 100
    y_max: 140
    on_press:
      - delay: 1s  # Long press = 1 second
      - if:
          condition:
            # Still pressed after delay
            lambda: return id(long_press_button).state;
          then:
            - logger.log: "Long press detected"
```

## Page Navigation

### Multi-Page System

**Globals:**
```yaml
globals:
  - id: current_page
    type: int
    initial_value: '0'
```

**Navigation Zones:**
```yaml
binary_sensor:
  # Previous page (left edge)
  - platform: touchscreen
    name: "Page Previous"
    x_min: 0
    x_max: 60
    y_min: 0
    y_max: 240
    on_press:
      - lambda: |-
          id(current_page) = (id(current_page) - 1 + 3) % 3;

  # Next page (right edge)
  - platform: touchscreen
    name: "Page Next"
    x_min: 260
    x_max: 320
    y_min: 0
    y_max: 240
    on_press:
      - lambda: |-
          id(current_page) = (id(current_page) + 1) % 3;

  # Direct page selection (footer buttons)
  - platform: touchscreen
    name: "Go to Page 0"
    x_min: 80
    x_max: 140
    y_min: 210
    y_max: 240
    on_press:
      - lambda: id(current_page) = 0;

  - platform: touchscreen
    name: "Go to Page 1"
    x_min: 140
    x_max: 180
    y_min: 210
    y_max: 240
    on_press:
      - lambda: id(current_page) = 1;

  - platform: touchscreen
    name: "Go to Page 2"
    x_min: 180
    x_max: 240
    y_min: 210
    y_max: 240
    on_press:
      - lambda: id(current_page) = 2;
```

## Value Control Patterns

### Increment/Decrement Buttons

```yaml
binary_sensor:
  # Increase value
  - platform: touchscreen
    name: "Increase"
    x_min: 200
    x_max: 310
    y_min: 100
    y_max: 150
    on_press:
      - lambda: |-
          id(target_value) = id(target_value) + 1;
          if (id(target_value) > 30) id(target_value) = 30;  // max

  # Decrease value
  - platform: touchscreen
    name: "Decrease"
    x_min: 10
    x_max: 120
    y_min: 100
    y_max: 150
    on_press:
      - lambda: |-
          id(target_value) = id(target_value) - 1;
          if (id(target_value) < 10) id(target_value) = 10;  // min
```

### Slider Zone (Continuous Value)

```yaml
binary_sensor:
  - platform: touchscreen
    name: "Volume Slider"
    x_min: 20
    x_max: 300
    y_min: 180
    y_max: 200
    on_press:
      - lambda: |-
          // Get touch X coordinate (0-319)
          auto touch = id(box3_touch).get_touches()[0];
          int x = touch.x;

          // Map to volume (0-100%)
          int volume = (x - 20) * 100 / 280;
          volume = max(0, min(100, volume));

          id(current_volume) = volume;
          ESP_LOGI("touch", "Volume: %d%%", volume);
```

## Toggle Patterns

### On/Off Toggle

```yaml
binary_sensor:
  - platform: touchscreen
    name: "Power Toggle"
    x_min: 100
    x_max: 220
    y_min: 150
    y_max: 200
    on_press:
      - lambda: |-
          id(power_state) = !id(power_state);
          if (id(power_state)) {
            ESP_LOGI("touch", "Turned ON");
          } else {
            ESP_LOGI("touch", "Turned OFF");
          }
```

### Mode Cycling

```yaml
binary_sensor:
  - platform: touchscreen
    name: "Mode Button"
    x_min: 10
    x_max: 310
    y_min: 120
    y_max: 170
    on_press:
      - lambda: |-
          id(mode) = (id(mode) + 1) % 3;  // Cycle through 3 modes
          if (id(mode) == 0) id(mode_text) = "Heat";
          else if (id(mode) == 1) id(mode_text) = "Cool";
          else if (id(mode) == 2) id(mode_text) = "Auto";
```

## Media Player Controls

```yaml
binary_sensor:
  # Play/Pause
  - platform: touchscreen
    name: "Play/Pause"
    x_min: 140
    x_max: 180
    y_min: 250
    y_max: 290
    on_press:
      - media_player.toggle: box_player

  # Previous track
  - platform: touchscreen
    name: "Previous"
    x_min: 60
    x_max: 120
    y_min: 250
    y_max: 290
    on_press:
      - media_player.play_media: !lambda return id(previous_track);

  # Next track
  - platform: touchscreen
    name: "Next"
    x_min: 200
    x_max: 260
    y_min: 250
    y_max: 290
    on_press:
      - media_player.play_media: !lambda return id(next_track);

  # Volume up
  - platform: touchscreen
    name: "Volume Up"
    x_min: 270
    x_max: 310
    y_min: 200
    y_max: 240
    on_press:
      - media_player.volume_up: box_player

  # Volume down
  - platform: touchscreen
    name: "Volume Down"
    x_min: 10
    x_max: 50
    y_min: 200
    y_max: 240
    on_press:
      - media_player.volume_down: box_player
```

## Visual Feedback

### Button Press Indicator

**Display lambda:**
```cpp
lambda: |-
  // Draw button
  if (id(button_pressed).state) {
    it.filled_rectangle(100, 150, 120, 50, Color(33, 150, 243));  // Pressed (blue)
  } else {
    it.filled_rectangle(100, 150, 120, 50, Color(66, 66, 66));    // Normal (gray)
  }
  it.printf(160, 175, id(roboto_16), TextAlign::CENTER, "Press Me");
```

### Touch Ripple Effect

**Using globals:**
```yaml
globals:
  - id: ripple_x
    type: int
    initial_value: '0'
  - id: ripple_y
    type: int
    initial_value: '0'
  - id: ripple_radius
    type: int
    initial_value: '0'
```

**On touch:**
```yaml
on_press:
  - lambda: |-
      auto touch = id(box3_touch).get_touches()[0];
      id(ripple_x) = touch.x;
      id(ripple_y) = touch.y;
      id(ripple_radius) = 1;
  - while:
      condition:
        lambda: return id(ripple_radius) < 50;
      then:
        - lambda: id(ripple_radius) += 5;
        - delay: 50ms
  - lambda: id(ripple_radius) = 0;
```

**Display lambda:**
```cpp
if (id(ripple_radius) > 0) {
  it.circle(id(ripple_x), id(ripple_y), id(ripple_radius), Color(33, 150, 243));
}
```

## Coordinate Reference

**Display: 320x240 pixels**
- Top-left: (0, 0)
- Top-right: (319, 0)
- Bottom-left: (0, 239)
- Bottom-right: (319, 239)
- Center: (160, 120)

**Safe touch zones:**
- Top bar: y 0-40
- Content area: y 40-200
- Bottom buttons: y 200-240

**Edge margins:**
- Left/right: 10px minimum
- Top/bottom: 10px minimum

## Multi-Touch Support

GT911 supports up to **5 simultaneous touch points**.

**Accessing multiple touches:**
```cpp
auto touches = id(box3_touch).get_touches();
for (auto touch : touches) {
  ESP_LOGI("touch", "Touch at (%d, %d)", touch.x, touch.y);
}
```

## Best Practices

1. **Minimum touch target: 48x48 pixels** (Material Design)
2. **Leave 10px margins** around screen edges
3. **Provide visual feedback** on touch (color change, ripple)
4. **Use debouncing** for sensitive actions (delay 100-200ms)
5. **Test touch zones** thoroughly (adjust boundaries as needed)
6. **Group related buttons** (left/center/right, top/bottom)
7. **Consistent placement** (navigation always at bottom, etc.)

## Summary

**Buttons**: `x_min`, `x_max`, `y_min`, `y_max` define touch zone
**Actions**: `on_press`, `on_release` for interaction
**Gestures**: Use zones for swipe left/right
**Pages**: Use global variable + conditional rendering
**Feedback**: Change colors, show ripple, log events
**Minimum size**: 48x48px for touch targets

For display rendering, see display-lambdas.md
For Material Design guidelines, see material-design.md
