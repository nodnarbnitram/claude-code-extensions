# Material Design UI Guide for ESP32-S3-BOX-3

Material Design principles, color palette, typography, and layout guidelines for BOX-3 display.

## Color Palette

### Primary Colors
- **Blue**: `Color(33, 150, 243)` - Primary action color
- **Green**: `Color(76, 175, 80)` - Success, positive
- **Orange**: `Color(255, 152, 0)` - Warning, attention
- **Red**: `Color(244, 67, 54)` - Error, critical

### Background Colors
- **Dark Background**: `Color(18, 18, 18)` - Screen background
- **Card Background**: `Color(33, 33, 33)` - Elevated surfaces
- **Light Gray**: `Color(66, 66, 66)` - Buttons, inactive elements

### Text Colors
- **Primary Text**: `Color(255, 255, 255)` - Main content (white)
- **Secondary Text**: `Color(189, 189, 189)` - Supporting text
- **Disabled Text**: `Color(97, 97, 97)` - Inactive elements

## Typography Hierarchy

### Font Sizes
- **Headline**: 20-24px (page titles)
- **Title**: 16-18px (section headers)
- **Body**: 14px (main content)
- **Caption**: 12px (labels, metadata)
- **Small**: 10px (timestamps, footnotes)

### Font Configuration
```yaml
font:
  - file: "gfonts://Roboto"
    id: roboto_24
    size: 24  # Headlines

  - file: "gfonts://Roboto"
    id: roboto_18
    size: 18  # Titles

  - file: "gfonts://Roboto"
    id: roboto_14
    size: 14  # Body

  - file: "gfonts://Roboto"
    id: roboto_12
    size: 12  # Captions

  - file: "gfonts://Roboto"
    id: roboto_10
    size: 10  # Small text
```

## Card Layouts

### Basic Card
```cpp
// Card background (10px margin)
it.filled_rectangle(10, 30, 300, 100, Color(33, 33, 33));

// Card header
it.printf(20, 40, id(roboto_16), "Card Title");

// Card content
it.printf(20, 65, id(roboto_14), "Card content goes here");
```

### Stacked Cards
```cpp
// Top card
it.filled_rectangle(10, 10, 300, 80, Color(33, 33, 33));
it.printf(160, 50, id(roboto_18), TextAlign::CENTER, "Card 1");

// Bottom card
it.filled_rectangle(10, 100, 300, 80, Color(33, 33, 33));
it.printf(160, 140, id(roboto_18), TextAlign::CENTER, "Card 2");
```

## Button Styles

### Filled Button (Primary Action)
```cpp
// Button background (primary color)
it.filled_rectangle(100, 200, 120, 48, Color(33, 150, 243));

// Button text (white)
it.printf(160, 224, id(roboto_14), TextAlign::CENTER, "ACTION");
```

### Outlined Button (Secondary Action)
```cpp
// Button outline
it.rectangle(100, 200, 120, 48, Color(33, 150, 243));

// Button text (primary color)
it.printf(160, 224, id(roboto_14), TextAlign::CENTER, Color(33, 150, 243), "ACTION");
```

### Text Button (Tertiary Action)
```cpp
// No background, just text in primary color
it.printf(160, 224, id(roboto_14), TextAlign::CENTER, Color(33, 150, 243), "action");
```

## Icon Integration

### Material Design Icons Setup
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
      "\U000F0415",  # home
      "\U000F0493",  # settings
    ]
```

### Icon + Text Layout
```cpp
// Icon on left, text on right
it.printf(30, 80, id(mdi_24), "\U000F0425");  // icon
it.printf(60, 85, id(roboto_14), "Temperature");

// Icon above text
it.printf(160, 60, id(mdi_36), TextAlign::CENTER, "\U000F0415");  // icon
it.printf(160, 105, id(roboto_12), TextAlign::CENTER, "Home");
```

## Spacing and Layout

### Margin Guidelines
- **Screen margins**: 10px all sides
- **Card padding**: 10px internal
- **Card spacing**: 10px between cards
- **Button spacing**: 10px between buttons

### Layout Grid (320x240)
```
┌─────────────────────────┐
│ [10px margin]           │ 0-10px
│ ┌───────────────────┐   │
│ │ Header Bar        │   │ 10-40px (30px height)
│ └───────────────────┘   │
│ ┌───────────────────┐   │
│ │                   │   │
│ │ Content Area      │   │ 40-200px (160px height)
│ │                   │   │
│ └───────────────────┘   │
│ ┌───────────────────┐   │
│ │ Bottom Buttons    │   │ 200-240px (40px height)
│ └───────────────────┘   │
│ [10px margin]           │ 230-240px
└─────────────────────────┘
```

## Touch Target Sizing

### Minimum Sizes (Material Design)
- **Minimum touch target**: 48x48px
- **Icon button**: 48x48px
- **Small button**: 60x40px
- **Medium button**: 100x48px
- **Large button**: 140x60px

### Button Layout (Bottom Row)
```cpp
// 3 buttons, equal width
// Button width: (320 - 4*10) / 3 = 93px each

// Button 1: x 10-103
it.filled_rectangle(10, 200, 93, 40, Color(33, 150, 243));

// Button 2: x 113-206
it.filled_rectangle(113, 200, 93, 40, Color(33, 150, 243));

// Button 3: x 216-309
it.filled_rectangle(216, 200, 93, 40, Color(33, 150, 243));
```

## Complete UI Examples

### Thermostat Card
```cpp
// Card background
it.filled_rectangle(10, 30, 300, 140, Color(33, 33, 33));

// Icon
it.printf(30, 50, id(mdi_36), Color(244, 67, 54), "\U000F0425");

// Current temperature (large)
it.printf(160, 80, id(roboto_32), TextAlign::CENTER, "23.5°");

// Status (small)
it.printf(160, 130, id(roboto_12), TextAlign::CENTER, Color(189, 189, 189), "Heating to 24°");

// Mode indicator
it.filled_rectangle(280, 30, 30, 30, Color(244, 67, 54));  // Red = heating
```

### Status Dashboard
```cpp
// WiFi card
it.filled_rectangle(10, 10, 145, 60, Color(33, 33, 33));
it.printf(20, 20, id(mdi_20), "\U000F05A9");  // wifi icon
it.printf(20, 50, id(roboto_12), "%.0f dBm", id(wifi).state);

// Temperature card
it.filled_rectangle(165, 10, 145, 60, Color(33, 33, 33));
it.printf(175, 20, id(mdi_20), "\U000F0425");  // thermometer
it.printf(175, 50, id(roboto_12), "%.1f°C", id(temp).state);

// Humidity card
it.filled_rectangle(10, 80, 145, 60, Color(33, 33, 33));
it.printf(20, 90, id(mdi_20), "\U000F050F");  // water-percent
it.printf(20, 120, id(roboto_12), "%.0f%%", id(hum).state);

// Status card
it.filled_rectangle(165, 80, 145, 60, Color(33, 33, 33));
it.printf(175, 90, id(mdi_20), Color(76, 175, 80), "\U000F012C");  // check-circle
it.printf(175, 120, id(roboto_12), "Online");
```

## Color Usage Guidelines

### Background
- **Dark theme**: Preferred for OLED (reduces burn-in)
- **Screen**: `Color(18, 18, 18)`
- **Cards**: `Color(33, 33, 33)` - slightly elevated

### Actions
- **Primary action**: Blue `Color(33, 150, 243)`
- **Destructive action**: Red `Color(244, 67, 54)`
- **Success**: Green `Color(76, 175, 80)`
- **Warning**: Orange `Color(255, 152, 0)`

### Status Indicators
- **Active/On**: Green `Color(76, 175, 80)`
- **Inactive/Off**: Gray `Color(66, 66, 66)`
- **Alert**: Red `Color(244, 67, 54)`
- **Warning**: Orange `Color(255, 152, 0)`

## Accessibility

### Contrast Ratios
- **Normal text**: Minimum 4.5:1 contrast
- **Large text (>18px)**: Minimum 3:1 contrast
- **White on dark gray**: 15.8:1 (excellent)
- **Light gray on dark**: 7.4:1 (good)

### Touch Targets
- **Minimum**: 48x48px (Material Design guideline)
- **Recommended**: 60x60px for primary actions
- **Spacing**: 8-10px between adjacent targets

## Summary

**Colors**: Dark background (18,18,18), cards (33,33,33), primary blue (33,150,243)
**Typography**: Roboto font, 10-24px sizes
**Cards**: 10px margins, 10px padding, 300px width max
**Buttons**: 48x48px minimum, filled/outlined/text styles
**Icons**: Material Design Icons font, 20-36px sizes
**Layout**: 10px margins, header/content/footer structure
**Touch**: 48x48px minimum, 10px spacing

For display rendering, see display-lambdas.md
For touch interaction, see touch-patterns.md
