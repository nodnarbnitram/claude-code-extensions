# View Types Reference

Complete guide to Home Assistant Lovelace view layouts with selection criteria.

## View Type Comparison

| View Type | Best For | Cards | Layout | Mobile |
|-----------|----------|-------|--------|--------|
| **Masonry** | General dashboards | Multiple | Auto-columns | Good |
| **Panel** | Single focus (maps, media) | 1 | Full-width | Excellent |
| **Sections** | Organized grids | Multiple | Drag-drop grid | Excellent |
| **Sidebar** | Two-column layouts | Multiple | Main + sidebar | Good |

## Masonry View (Default)

Auto-arranging columns that adapt to screen width. Cards flow into columns based on available space.

**Best for:**
- General-purpose dashboards
- Mixed card types and sizes
- Quick setup without manual positioning

**Configuration:**

```yaml
views:
  - title: Home
    # type: masonry  # Optional, this is the default
    path: home
    icon: mdi:home
    cards:
      - type: entities
        title: Lights
        entities:
          - light.living_room
          - light.bedroom
      - type: weather-forecast
        entity: weather.home
        forecast_type: daily
      - type: gauge
        entity: sensor.temperature
        name: Temperature
```

**Behavior:**
- Cards automatically arranged in columns
- Column count adjusts to screen width
- Card order follows YAML order (top-to-bottom, left-to-right)
- Cards with `getCardSize()` method influence placement

## Panel View

Single card displayed full-width. Perfect for maps, media players, or any content that benefits from maximum space.

**Best for:**
- Map displays
- Camera feeds
- Large media players
- Custom full-screen cards

**Configuration:**

```yaml
views:
  - title: Map
    type: panel
    path: map
    icon: mdi:map
    cards:
      - type: map
        entities:
          - device_tracker.phone
          - zone.home
          - zone.work
        aspect_ratio: 16:9
        default_zoom: 12
```

**Important:** Panel view only displays the first card. Additional cards are ignored.

**Common Panel Cards:**
- `map` - Location tracking
- `picture-elements` - Interactive floorplans
- `iframe` - Embedded content
- `media-control` - Large media player
- `calendar` - Full calendar view

## Sections View (New Default)

Grid-based layout with drag-and-drop support in UI mode. Organizes cards into named sections.

**Best for:**
- Organized, structured dashboards
- Room-by-room layouts
- Mobile-first design
- Users who prefer UI editing

**Configuration:**

```yaml
views:
  - title: Dashboard
    type: sections
    path: dashboard
    icon: mdi:view-dashboard
    max_columns: 4
    sections:
      - title: Living Room
        cards:
          - type: tile
            entity: light.living_room
          - type: tile
            entity: climate.living_room
          - type: tile
            entity: media_player.living_room

      - title: Bedroom
        cards:
          - type: tile
            entity: light.bedroom
          - type: tile
            entity: fan.bedroom

      - title: Security
        cards:
          - type: tile
            entity: lock.front_door
          - type: tile
            entity: binary_sensor.motion
```

**Section Options:**

```yaml
sections:
  - title: Section Name
    type: grid                  # Default section type
    column_span: 2              # Span multiple columns
    cards: []
```

**Card Grid Options (for custom cards):**

```javascript
// In custom card
getGridOptions() {
  return {
    rows: 2,        // Height in grid units
    columns: 6,     // Width in grid units (max 6)
    min_rows: 1,    // Minimum height
    max_rows: 4     // Maximum height
  };
}
```

## Sidebar View

Two-column layout with main content area and sidebar. Useful for dashboards with primary content and supplementary information.

**Best for:**
- Control panels with status sidebar
- Media dashboards with queue/playlist sidebar
- Room controls with sensor readings sidebar

**Configuration:**

```yaml
views:
  - title: Overview
    type: sidebar
    path: overview
    icon: mdi:view-split-vertical
    cards:
      # Main area cards (default position)
      - type: weather-forecast
        entity: weather.home
        forecast_type: daily

      - type: entities
        title: Quick Controls
        entities:
          - light.living_room
          - climate.thermostat
          - media_player.tv

      # Sidebar cards (explicit position)
      - type: entities
        title: Sensors
        view_layout:
          position: sidebar
        entities:
          - sensor.temperature
          - sensor.humidity
          - sensor.air_quality

      - type: logbook
        view_layout:
          position: sidebar
        entities:
          - binary_sensor.front_door
        hours_to_show: 12
```

**Card Positioning:**

```yaml
# Place card in sidebar
- type: entities
  view_layout:
    position: sidebar
  entities: [...]

# Place card in main area (default)
- type: entities
  view_layout:
    position: main
  entities: [...]
```

**Sidebar Behavior:**
- Main area: ~70% width on desktop
- Sidebar: ~30% width on desktop
- Mobile: Sidebar stacks below main content

## View Common Properties

All view types share these properties:

```yaml
views:
  - title: View Title          # Tab title (required)
    path: view-path            # URL path (recommended)
    icon: mdi:home             # Tab icon
    theme: theme_name          # Apply specific theme
    background: /local/bg.jpg  # Background image
    visible:                   # Visibility conditions
      - user: admin
    subview: false             # Hide from navigation bar

    # Type-specific
    type: masonry              # masonry, panel, sections, sidebar
    cards: []                  # Card list
```

## Visibility Control

Control who sees a view:

```yaml
views:
  - title: Admin
    path: admin
    visible:
      - user: admin_user_id
      - user: another_admin

  - title: Guest View
    path: guest
    visible: false             # Hidden from all users in navigation
```

## Subviews

Views accessible only via navigation, not in tab bar:

```yaml
views:
  - title: Room Details
    path: room-details
    subview: true
    cards:
      - type: entities
        entities:
          - light.bedroom
```

Navigate to subview:
```yaml
tap_action:
  action: navigate
  navigation_path: /lovelace/room-details
```

## Selection Guide

**Choose Masonry when:**
- You want quick setup
- Card positions don't matter much
- You have varied card sizes

**Choose Panel when:**
- You need full-width display
- Showing maps, cameras, or embedded content
- Single-focus views

**Choose Sections when:**
- You want organized, structured layouts
- You prefer UI-based editing
- Mobile experience is priority
- You're setting up new dashboards (recommended default)

**Choose Sidebar when:**
- You need two distinct content areas
- Main controls with status/info sidebar
- Desktop-focused dashboards

## Migration Tips

**From Masonry to Sections:**
1. Group related cards conceptually
2. Create sections for each group
3. Move cards into appropriate sections
4. Adjust `max_columns` for screen width

**From UI to YAML:**
1. Use three-dot menu > "Raw configuration editor"
2. Copy YAML and save to file
3. Enable YAML mode in configuration.yaml
