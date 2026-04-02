# Grafana Plugin Signing and Publishing Guide

Guide to signing and publishing Grafana plugins (v12.x+).

## Overview

Grafana plugins must be signed before distribution. There are three signature levels:

| Level | Who Can Sign | Distribution |
|-------|--------------|--------------|
| Private | Any Grafana Cloud user | Internal use only |
| Community | Registered developers | Grafana catalog |
| Commercial | Grafana Labs partners | Grafana catalog |

## Prerequisites

1. **Grafana Cloud Account**: https://grafana.com/auth/sign-up
2. **Plugin ID registered** with your organization
3. **Node.js 18+** installed
4. **Plugin built** (`npm run build`)

## Plugin ID Requirements

Your plugin ID must follow the format:
```
<org>-<name>-<type>
```

Examples:
- `mycompany-weather-panel`
- `acmecorp-metrics-datasource`
- `cooltools-admin-app`

**Important**: Once published, the plugin ID cannot be changed.

## Signing Process

### Step 1: Generate Access Policy Token

1. Log in to https://grafana.com
2. Go to **My Account** → **Access Policies**
3. Create new token with scope: `plugins:write`
4. Copy the token (shown only once)

### Step 2: Set Environment Variable

```bash
export GRAFANA_ACCESS_POLICY_TOKEN=your-token-here
```

Or create `.env` file (don't commit this!):
```
GRAFANA_ACCESS_POLICY_TOKEN=your-token-here
```

### Step 3: Run Sign Plugin

```bash
# Interactive signing
npx @grafana/sign-plugin@latest

# Or specify root URL for private plugins
npx @grafana/sign-plugin@latest --rootUrls https://grafana.mycompany.com
```

### Step 4: Verify Signature

The signing process creates/updates `MANIFEST.txt` in your `dist/` folder:

```bash
cat dist/MANIFEST.txt
# Should show plugin metadata and signature
```

## Signature Types

### Private Signature

For internal/private use only:
- Specify `--rootUrls` with your Grafana instance URLs
- Plugin only works on specified URLs
- No catalog submission required

```bash
npx @grafana/sign-plugin@latest \
  --rootUrls https://grafana.mycompany.com,https://grafana-staging.mycompany.com
```

### Community Signature

For public distribution:
- No `--rootUrls` (works on any Grafana instance)
- Requires catalog submission
- Free to use

### Commercial Signature

For commercial plugins:
- Requires Grafana Labs partnership
- Enhanced support and visibility
- Licensing options available

## Publishing to Grafana Catalog

### Pre-Publication Checklist

- [ ] Plugin ID follows naming convention
- [ ] `plugin.json` has all required fields:
  - `id`, `type`, `name`
  - `info.author.name`
  - `info.version` (valid semver)
  - `info.updated` (ISO date)
  - `info.description`
  - `info.logos.small` and `info.logos.large`
- [ ] README.md with installation and usage instructions
- [ ] CHANGELOG.md with version history
- [ ] LICENSE file
- [ ] Screenshots in `src/img/` folder
- [ ] Plugin signed (MANIFEST.txt exists)

### Submission Process

1. **Create GitHub Release**
   ```bash
   # Tag your version
   git tag v1.0.0
   git push origin v1.0.0

   # Create release with signed dist as asset
   zip -r your-plugin-1.0.0.zip dist/
   gh release create v1.0.0 your-plugin-1.0.0.zip
   ```

2. **Submit to Grafana**
   - Go to https://grafana.com/orgs/your-org/plugins
   - Click "Submit Plugin"
   - Provide GitHub repository URL
   - Fill in additional details
   - Submit for review

3. **Review Process**
   - Grafana team reviews submission
   - May request changes
   - Typically 1-2 weeks for approval

### Updating Published Plugins

1. Update version in `plugin.json`
2. Update CHANGELOG.md
3. Build and sign: `npm run build && npx @grafana/sign-plugin@latest`
4. Create new GitHub release
5. Grafana automatically detects new versions

## Automated Signing (CI/CD)

### GitHub Actions Example

```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build

      - name: Sign plugin
        run: npx @grafana/sign-plugin@latest
        env:
          GRAFANA_ACCESS_POLICY_TOKEN: ${{ secrets.GRAFANA_ACCESS_POLICY_TOKEN }}

      - name: Package plugin
        run: |
          mv dist/ myorg-myplugin-panel/
          zip -r myorg-myplugin-panel-${{ github.ref_name }}.zip myorg-myplugin-panel/

      - name: Create Release
        uses: softprops/action-gh-release@v1
        with:
          files: myorg-myplugin-panel-${{ github.ref_name }}.zip
```

### GitLab CI Example

```yaml
release:
  stage: release
  image: node:20
  only:
    - tags
  script:
    - npm ci
    - npm run build
    - npx @grafana/sign-plugin@latest
    - mv dist/ myorg-myplugin-panel/
    - zip -r myorg-myplugin-panel-${CI_COMMIT_TAG}.zip myorg-myplugin-panel/
  artifacts:
    paths:
      - myorg-myplugin-panel-${CI_COMMIT_TAG}.zip
  variables:
    GRAFANA_ACCESS_POLICY_TOKEN: $GRAFANA_ACCESS_POLICY_TOKEN
```

## Distribution Without Catalog

For private plugins not submitted to the catalog:

### Option 1: Direct Installation

```bash
# Download and extract to plugins directory
cd /var/lib/grafana/plugins
unzip myorg-myplugin-panel.zip

# Add to allow list
# grafana.ini
[plugins]
allow_loading_unsigned_plugins = myorg-myplugin-panel

# Restart Grafana
systemctl restart grafana-server
```

### Option 2: Provisioning

```yaml
# provisioning/plugins/plugins.yaml
apiVersion: 1
plugins:
  - type: panel
    name: myorg-myplugin-panel
    url: https://github.com/myorg/myplugin/releases/download/v1.0.0/myorg-myplugin-panel-1.0.0.zip
```

### Option 3: Docker Volume

```yaml
# docker-compose.yaml
services:
  grafana:
    image: grafana/grafana:latest
    volumes:
      - ./plugins/myorg-myplugin-panel:/var/lib/grafana/plugins/myorg-myplugin-panel
    environment:
      - GF_PLUGINS_ALLOW_LOADING_UNSIGNED_PLUGINS=myorg-myplugin-panel
```

## Troubleshooting

### Signing Fails

```
Error: Plugin not found
```
- Verify plugin ID matches your Grafana Cloud organization
- Check token has `plugins:write` scope

```
Error: Invalid manifest
```
- Ensure `dist/` contains valid build
- Check `plugin.json` is valid JSON

### Plugin Shows "Unsigned"

- Verify MANIFEST.txt exists in dist/
- Check signature matches plugin ID
- For private plugins, verify rootUrls match current Grafana URL

### Catalog Submission Rejected

Common reasons:
- Missing required files (README, LICENSE)
- Plugin.json validation errors
- Security issues in code
- Insufficient documentation

## Resources

- **Signing Documentation**: https://grafana.com/developers/plugin-tools/publish-a-plugin/sign-a-plugin
- **Publishing Guide**: https://grafana.com/developers/plugin-tools/publish-a-plugin/publish-a-plugin
- **Plugin Guidelines**: https://grafana.com/developers/plugin-tools/publish-a-plugin/plugin-guidelines
- **Grafana Cloud**: https://grafana.com/products/cloud/
