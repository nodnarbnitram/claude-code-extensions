# Display Lambda Rendering Cookbook for ESP32-S3-BOX-3

Complete guide to ILI9xxx display lambda rendering with text, shapes, icons, and multi-page UI patterns.

## Display Lambda Basics

The display lambda is a C++ code block that runs on each display update to render the UI.

**Basic Structure:**
```cpp
lambda: |-
  // C++ code here - runs every update_interval
  it.printf(x, y, id(font), "Text");
```

## Text Rendering

### Simple Text

```cpp
// Basic text at position
it.printf(10, 20, id(roboto_16), "Hello World");

// Centered text
it.printf(160, 120, id(roboto_16), TextAlign::CENTER, "Centered");

// Right-aligned text
it.printf(310, 20, id(roboto_16), TextAlign::TOP_RIGHT, "Right");
```

### Text Alignment Options

- `TextAlign::TOP_LEFT` (default)
- `TextAlign::TOP_CENTER`
- `TextAlign::TOP_RIGHT`
- `TextAlign::CENTER_LEFT`
- `TextAlign::CENTER` (both H and V)
- `TextAlign::CENTER_RIGHT`
- `TextAlign::BOTTOM_LEFT`
- `TextAlign::BOTTOM_CENTER`
- `TextAlign::BOTTOM_RIGHT`

### Dynamic Text (Sensor Values)

```cpp
// Temperature from sensor
if (id(temp_sensor).has_state()) {
  it.printf(20, 40, id(roboto_14), "Temp: %.1f°C", id(temp_sensor).state);
}

// String from global variable
it.printf(20, 60, id(roboto_14), "%s", id(status_text).c_str());

// Formatted with multiple values
it.printf(20, 80, id(roboto_12), "%.1f°C / %.1f%%",
  id(temp).state, id(humidity).state);
```

## Shapes

### Rectangles

```cpp
// Filled rectangle (x, y, width, height, color)
it.filled_rectangle(10, 30, 300, 80, COLOR_ON);

// Outlined rectangle
it.rectangle(10, 30, 300, 80, COLOR_ON);

// Card background
it.filled_rectangle(10, 30, 300, 100, Color(33, 33, 33));  // Dark gray
```

### Lines

```cpp
// Horizontal line (x1, y1, x2, y2, color)
it.line(10, 100, 310, 100, COLOR_ON);

// Vertical line
it.line(160, 10, 160, 230, COLOR_ON);

// Diagonal line
it.line(10, 10, 310, 230, COLOR_ON);
```

### Circles

```cpp
// Filled circle (x, y, radius, color)
it.filled_circle(160, 120, 50, COLOR_ON);

// Outlined circle
it.circle(160, 120, 50, COLOR_ON);
```

## Colors

### Built-in Colors

```cpp
COLOR_ON    // White (or configured on color)
COLOR_OFF   // Black (or configured off color)
```

### Custom RGB Colors

```cpp
Color(255, 0, 0)      // Red
Color(0, 255, 0)      // Green
Color(0, 0, 255)      // Blue
Color(255, 255, 0)    // Yellow
Color(128, 128, 128)  // Gray
Color(33, 33, 33)     // Dark gray (Material Design)
```

### Material Design Color Palette

```cpp
// Primary colors
Color(33, 150, 243)   // Blue
Color(76, 175, 80)    // Green
Color(255, 152, 0)    // Orange
Color(244, 67, 54)    // Red

// Background colors
Color(18, 18, 18)     // Dark background
Color(33, 33, 33)     // Card background
Color(255, 255, 255)  // White background
```

## Icons (Material Design Icons)

### Icon Setup

**Font configuration:**
```yaml
font:
  - file: .claude/skills/esphome-box3-builder/assets/fonts/materialdesignicons-webfont.ttf
    id: mdi_24
    size: 24
    glyphs: [
      "\U000F0425",  # thermometer
      "\U000F050F",  # water-percent
      "\U000F0493",  # play
      "\U000F03E4",  # pause
      "\U000F0 415",  # home
    ]
```

### Icon Rendering

```cpp
// Render icon
it.printf(30, 50, id(mdi_24), "\U000F0425");  // thermometer

// Icon with text
it.printf(30, 50, id(mdi_24), "\U000F0425");
it.printf(60, 53, id(roboto_14), "23.5°C");
```

**Common Icon Codepoints** (see assets/fonts/mdi-codepoints.txt):
- Thermometer: `\U000F0425`
- Water Percent: `\U000F050F`
- Play: `\U000F0493`
- Pause: `\U000F03E4`
- Home: `\U000F0415`
- Settings: `\U000F0493`
- Power: `\U000F0425`

## Multi-Page UI

### Page System Setup

**Globals:**
```yaml
globals:
  - id: current_page
    type: int
    initial_value: '0'
```

**Display Lambda:**
```cpp
lambda: |-
  // Common header on all pages
  it.filled_rectangle(0, 0, 320, 30, Color(33, 150, 243));
  it.printf(160, 5, id(roboto_16), TextAlign::TOP_CENTER, "BOX-3");

  // Page-specific content
  if (id(current_page) == 0) {
    // Page 0: Home
    it.printf(160, 80, id(roboto_20), TextAlign::CENTER, "Home");
    if (id(temp).has_state()) {
      it.printf(160, 120, id(roboto_16), TextAlign::CENTER, "%.1f°C", id(temp).state);
    }
  } else if (id(current_page) == 1) {
    // Page 1: Settings
    it.printf(160, 80, id(roboto_20), TextAlign::CENTER, "Settings");
    it.printf(20, 120, id(roboto_14), "Volume: %d%%", (int)(id(volume).state * 100));
  } else if (id(current_page) == 2) {
    // Page 2: Status
    it.printf(160, 80, id(roboto_20), TextAlign::CENTER, "Status");
    it.printf(20, 120, id(roboto_14), "WiFi: %.0f dBm", id(wifi_signal).state);
  }

  // Page indicators (dots)
  for (int i = 0; i < 3; i++) {
    if (i == id(current_page)) {
      it.filled_circle(140 + i * 20, 220, 5, COLOR_ON);
    } else {
      it.circle(140 + i * 20, 220, 5, COLOR_ON);
    }
  }
```

### Page Navigation

**Touch zones:**
```yaml
binary_sensor:
  - platform: touchscreen
    name: "Previous Page"
    x_min: 0
    x_max: 100
    y_min: 200
    y_max: 240
    on_press:
      - lambda: |-
          id(current_page) = (id(current_page) - 1 + 3) % 3;

  - platform: touchscreen
    name: "Next Page"
    x_min: 220
    x_max: 320
    y_min: 200
    y_max: 240
    on_press:
      - lambda: |-
          id(current_page) = (id(current_page) + 1) % 3;
```

## Complete UI Examples

### Thermostat UI

```cpp
lambda: |-
  // Background
  it.fill(Color(18, 18, 18));

  // Header card
  it.filled_rectangle(10, 10, 300, 60, Color(33, 33, 33));
  it.printf(160, 25, id(roboto_20), TextAlign::CENTER, "Thermostat");

  // Temperature display card
  it.filled_rectangle(10, 80, 300, 100, Color(33, 33, 33));
  if (id(current_temp).has_state()) {
    it.printf(160, 120, id(roboto_32), TextAlign::CENTER, "%.1f°", id(current_temp).state);
  }
  it.printf(160, 160, id(roboto_14), TextAlign::CENTER, "Current");

  // Target temperature card
  it.filled_rectangle(10, 190, 145, 40, Color(33, 33, 33));
  it.printf(82, 210, id(roboto_16), TextAlign::CENTER, "Target: %.0f°", id(target_temp).state);

  // Mode indicator
  it.filled_rectangle(165, 190, 145, 40, Color(33, 150, 243));
  it.printf(237, 210, id(roboto_16), TextAlign::CENTER, "%s", id(mode_text).c_str());
```

### Media Player UI

```cpp
lambda: |-
  // Album art placeholder
  it.filled_rectangle(60, 30, 200, 200, Color(33, 33, 33));
  it.printf(160, 120, id(mdi_48), TextAlign::CENTER, "\U000F040D");  // music icon

  // Song title
  it.printf(160, 10, id(roboto_14), TextAlign::TOP_CENTER, "%s", id(song_title).c_str());

  // Play/pause button
  if (id(is_playing)) {
    it.printf(160, 250, id(mdi_36), TextAlign::CENTER, "\U000F03E4");  // pause
  } else {
    it.printf(160, 250, id(mdi_36), TextAlign::CENTER, "\U000F0493");  // play
  }

  // Previous/next buttons
  it.printf(80, 250, id(mdi_36), TextAlign::CENTER, "\U000F04AE");   // skip-previous
  it.printf(240, 250, id(mdi_36), TextAlign::CENTER, "\U000F04AD");  // skip-next
```

## Performance Tips

**Minimize Redraws:**
```cpp
// Only redraw when values change
static float last_temp = 0;
if (id(temp).state != last_temp) {
  // Redraw temperature area
  last_temp = id(temp).state;
}
```

**Use Static Variables:**
```cpp
// Remember state across lambda calls
static int animation_frame = 0;
animation_frame = (animation_frame + 1) % 60;
```

**Conditional Rendering:**
```cpp
// Only render if sensor has valid data
if (id(sensor).has_state()) {
  // Render sensor value
}
```

## Coordinate System

- Origin (0, 0) is **top-left corner**
- X increases **right** (0-319)
- Y increases **down** (0-239)
- Display size: **320x240 pixels**

**Safe rendering area:**
- Leave 10px margin: (10, 10) to (310, 230)
- Touch zones: Minimum 48x48px (Material Design guideline)

## Summary

**Text**: Use `it.printf()` with TextAlign for positioning
**Shapes**: `filled_rectangle()`, `rectangle()`, `line()`, `circle()`
**Colors**: `Color(R, G, B)` or `COLOR_ON`/`COLOR_OFF`
**Icons**: MDI font with Unicode codepoints
**Multi-Page**: Use globals and conditional rendering
**Touch Integration**: See touch-patterns.md

For Material Design guidelines, see material-design.md
For touch interaction, see touch-patterns.md
