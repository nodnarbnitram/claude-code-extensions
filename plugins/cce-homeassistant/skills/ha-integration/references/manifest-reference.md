# manifest.json Reference

Complete reference for Home Assistant integration manifest.json configuration.

## Required Fields

### domain
- **Type:** string
- **Description:** Unique identifier for the integration (lowercase, alphanumeric, underscores only)
- **Example:** `"my_integration"`
- **Constraints:** Must be unique across all Home Assistant integrations

### name
- **Type:** string
- **Description:** Display name shown in Home Assistant UI
- **Example:** `"My Integration"`

### codeowners
- **Type:** array of strings
- **Description:** GitHub usernames of code owners (required for Home Assistant core contributions)
- **Example:** `["@username", "@another_user"]`

## Optional Fields

### version
- **Type:** string (semantic versioning)
- **Description:** Integration version
- **Default:** "0.0.0"
- **Example:** `"1.2.3"`

### homeassistant
- **Type:** string (semantic version)
- **Description:** Minimum Home Assistant version required
- **Default:** "2024.1.0"
- **Example:** `"2024.6.0"`

### config_flow
- **Type:** boolean
- **Description:** Whether integration has config flow UI for setup
- **Default:** false
- **Example:** `true`

### requirements
- **Type:** array of strings
- **Description:** PyPI package dependencies
- **Example:** `["requests>=2.25.0", "python-dateutil"]`

### documentation
- **Type:** string (URL)
- **Description:** Link to integration documentation
- **Example:** `"https://github.com/username/ha-my-integration"`

### issue_tracker
- **Type:** string (URL)
- **Description:** Link to GitHub issues for the integration
- **Example:** `"https://github.com/username/ha-my-integration/issues"`

### quality_scale
- **Type:** string
- **Description:** Quality level of the integration
- **Values:** "internal", "high", "standard"
- **Default:** "standard"

### iot_class
- **Type:** string
- **Description:** Classification of how integration communicates
- **Values:** "assumed_state", "cloud_polling", "cloud_push", "local_polling", "local_push"
- **Example:** `"local_polling"`

### brands
- **Type:** object
- **Description:** Brand information for the integration
- **Example:**
```json
{
  "brands": {
    "mycompany": {
      "name": "My Company",
      "icon": "mdi:icon-name"
    }
  }
}
```

### after_dependencies
- **Type:** array of strings
- **Description:** Domains that must be loaded before this integration
- **Example:** `["http"]`

### before_dependencies
- **Type:** array of strings
- **Description:** Domains that should be loaded after this integration
- **Example:** `["frontend"]`

## Example manifest.json

```json
{
  "domain": "my_integration",
  "name": "My Integration",
  "codeowners": ["@username"],
  "config_flow": true,
  "documentation": "https://github.com/username/ha-my-integration",
  "homeassistant": "2024.1.0",
  "requirements": ["requests>=2.25.0"],
  "version": "1.0.0",
  "issue_tracker": "https://github.com/username/ha-my-integration/issues",
  "iot_class": "local_polling",
  "quality_scale": "high"
}
```

## Best Practices

1. **Domain naming:** Use lowercase with underscores, match directory name
2. **Versions:** Follow semantic versioning (MAJOR.MINOR.PATCH)
3. **Requirements:** Pin major versions, use `>=` for minimum versions
4. **IoT class:** Be accurate - "local_polling" for local network access, "cloud_push" for cloud services
5. **Quality scale:** "standard" for most integrations, "high" for well-tested/maintained
6. **Documentation:** Always provide documentation link to help users
7. **Codeowners:** Essential for Home Assistant core contributions

## Common Mistakes

### ❌ Wrong
```json
{
  "domain": "my-integration",  // ← Hyphens instead of underscores
  "version": "1",               // ← Not semantic versioning
  "requirements": ["requests"]  // ← No version constraint
}
```

### ✅ Correct
```json
{
  "domain": "my_integration",
  "version": "1.0.0",
  "requirements": ["requests>=2.25.0"]
}
```
