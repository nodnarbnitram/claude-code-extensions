# Material Design Fonts for ESP32-S3-BOX-3

This directory contains Material Design fonts referenced by BOX-3 templates and examples.

## Required Fonts

### 1. Roboto-Regular.ttf
**Purpose**: Material Design typography (body text, headings)

**Download**:
- **Google Fonts**: https://fonts.google.com/specimen/Roboto
- **Direct**: https://github.com/google/roboto/releases
- **NPM**: `npm install roboto-fontface`

**Installation**:
```bash
# Download and place in this directory
wget https://github.com/google/roboto/releases/download/v2.138/roboto-unhinted.zip
unzip roboto-unhinted.zip
cp Roboto-Regular.ttf .claude/skills/esphome-box3-builder/assets/fonts/
```

### 2. materialdesignicons-webfont.ttf
**Purpose**: Material Design Icons (UI icons)

**Download**:
- **Official**: https://pictogrammers.com/library/mdi/
- **CDN**: https://cdn.materialdesignicons.com/
- **NPM**: `npm install @mdi/font`

**Installation**:
```bash
# Download from CDN
wget https://cdn.materialdesignicons.com/7.4.47/fonts/materialdesignicons-webfont.ttf
mv materialdesignicons-webfont.ttf .claude/skills/esphome-box3-builder/assets/fonts/

# Or from NPM
npm install @mdi/font
cp node_modules/@mdi/font/fonts/materialdesignicons-webfont.ttf .claude/skills/esphome-box3-builder/assets/fonts/
```

### 3. mdi-codepoints.txt (Optional)
**Purpose**: Icon name → Unicode codepoint reference

**Download**:
```bash
wget https://raw.githubusercontent.com/Templarian/MaterialDesign-Webfont/master/scss/_variables.scss
# Extract codepoints or use pictogrammers.com to search icons
```

## Alternative: Use Google Fonts in ESPHome

ESPHome can download fonts automatically from Google Fonts:

```yaml
font:
  - file: "gfonts://Roboto"  # Downloads automatically
    id: roboto_16
    size: 16
```

**Note**: Google Fonts auto-download does NOT work for Material Design Icons. You must download `materialdesignicons-webfont.ttf` manually.

## Usage in ESPHome Configuration

### Using Local Fonts (Recommended for BOX-3)

```yaml
font:
  # Roboto for text
  - file: .claude/skills/esphome-box3-builder/assets/fonts/Roboto-Regular.ttf
    id: roboto_16
    size: 16

  # Material Design Icons
  - file: .claude/skills/esphome-box3-builder/assets/fonts/materialdesignicons-webfont.ttf
    id: mdi_24
    size: 24
    glyphs: [
      "\U000F0425",  # thermometer
      "\U000F050F",  # water-percent
      "\U000F0493",  # play
      "\U000F03E4",  # pause
    ]
```

### Using Google Fonts Auto-Download

```yaml
font:
  # Auto-download from Google Fonts
  - file: "gfonts://Roboto"
    id: roboto_16
    size: 16

  # Material Design Icons still needs local file
  - file: .claude/skills/esphome-box3-builder/assets/fonts/materialdesignicons-webfont.ttf
    id: mdi_24
    size: 24
    glyphs: ["\U000F0425"]
```

## Icon Codepoint Reference

Common Material Design Icons and their Unicode codepoints:

| Icon Name | Codepoint | Preview |
|-----------|-----------|---------|
| thermometer | `\U000F0425` | 🌡️ |
| water-percent | `\U000F050F` | 💧 |
| play | `\U000F0493` | ▶️ |
| pause | `\U000F03E4` | ⏸️ |
| home | `\U000F0415` | 🏠 |
| settings | `\U000F0493` | ⚙️ |
| check-circle | `\U000F012C` | ✅ |
| alert-circle | `\U000F0029` | ⚠️ |
| wifi | `\U000F05A9` | 📶 |
| bluetooth | `\U000F00AF` | 📶 |

**Find more icons**: https://pictogrammers.com/library/mdi/

## File Sizes

- **Roboto-Regular.ttf**: ~168 KB
- **materialdesignicons-webfont.ttf**: ~1.2 MB (includes 7000+ icons)

**Optimization**: Only include glyphs you need in the `glyphs:` array to reduce compilation time.

## License Information

### Roboto Font
- **License**: Apache License 2.0
- **Source**: Google
- **Commercial use**: Allowed

### Material Design Icons
- **License**: Apache License 2.0 / SIL Open Font License 1.1
- **Source**: Pictogrammers
- **Commercial use**: Allowed

## Troubleshooting

**ESPHome can't find font file**:
- Verify path is relative to ESPHome config file
- Use absolute path if needed
- Check file permissions (readable)

**Icons don't render**:
- Ensure MDI font file downloaded
- Verify codepoint is correct (use pictogrammers.com)
- Add codepoint to `glyphs:` array

**Compilation slow**:
- Reduce number of glyphs in `glyphs:` array
- Only include icons you actually use
- Use smaller font sizes where possible

## Summary

1. **Download fonts** from official sources (Google Fonts, Pictogrammers)
2. **Place in this directory**: `.claude/skills/esphome-box3-builder/assets/fonts/`
3. **Reference in config**: Use relative path from your ESPHome YAML file
4. **Specify glyphs**: Only include icons you need for faster compilation

For usage examples, see the BOX-3 templates in `../templates/`
