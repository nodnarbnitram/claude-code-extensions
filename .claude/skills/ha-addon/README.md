# Home Assistant Add-On Development

> Expert guidance for building, configuring, and publishing Home Assistant add-ons with Docker, Supervisor integration, and multi-architecture support.

| | |
|---|---|
| **Status** | Production Ready |
| **Version** | 1.0.0 |
| **Last Updated** | 2025-12-31 |
| **Confidence** | 5/5 |

## What This Skill Does

Develops Home Assistant add-ons from scratch with complete Docker container support, Home Assistant Supervisor API integration, multi-architecture builds, and repository publishing. Covers the full lifecycle: project setup, configuration, Docker builds, S6 overlay services, Supervisor API communication, ingress web UI setup, and publishing to add-on repositories.

### Core Capabilities

- Create add-on project structure with proper directory layouts
- Configure config.yaml with all options, permissions, and architecture support
- Build multi-architecture Docker containers using Home Assistant base images
- Set up S6 overlay services for process management and logging
- Communicate with Home Assistant Supervisor API using bashio helpers
- Configure ingress reverse proxy for web-based add-on UIs
- Validate configuration schemas before publishing
- Package and publish to GitHub-based add-on repositories
- Debug common errors (permission, network, persistence, architecture mismatches)

## Auto-Trigger Keywords

### Primary Keywords

Exact terms that strongly trigger this skill:

- add-on (or addon)
- supervisor (or hassio)
- home assistant docker
- ingress proxy
- bashio helper
- s6 overlay

### Secondary Keywords

Related terms that may trigger in combination:

- homeassistant container
- ha docker configuration
- home assistant service
- supervisor token
- home assistant extension
- docker for home assistant

### Error-Based Keywords

Common error messages that should trigger this skill:

- "Add-on won't start"
- "Supervisor API returns 401"
- "Permission denied on supervisor"
- "Configuration not saving"
- "Unknown architecture"
- "Ingress web UI not accessible"
- "S6 service error"
- "SUPERVISOR_TOKEN not found"

## Known Issues Prevention

| Issue | Root Cause | Solution |
|-------|-----------|----------|
| Add-on fails to start | Missing or non-executable S6 service files | Create `/etc/s6-overlay/s6-rc.d/` with executable `run` scripts |
| Supervisor API 401 errors | Missing or invalid SUPERVISOR_TOKEN | Token automatically injected - verify permissions in config.yaml |
| Data loss after restart | Saving outside `/data/` directory | Always use `bashio::addon::config_path` or hardcode to `/data/` |
| Build fails on architecture | Using unsupported architecture or missing {arch} placeholder | Use only amd64, armv7, aarch64, armhf, i386; use {arch} in image names |
| Ingress returns 502 | Web app not listening or reverse proxy headers missing | Ensure app listens on configured port; set X-Forwarded-* headers |

## When to Use

### Use This Skill For

- Creating a new Home Assistant add-on from scratch
- Configuring Dockerfile with Home Assistant base images
- Setting up Docker container services for Home Assistant
- Adding S6 overlay service management
- Integrating with Home Assistant Supervisor API
- Building web UIs with ingress reverse proxy
- Configuring multi-architecture Docker builds
- Publishing add-ons to GitHub repositories
- Troubleshooting add-on startup and runtime issues

### Don't Use This Skill For

- General Docker concepts (see docker-fundamentals skill instead)
- Home Assistant automation or scripts (use homeassistant-automation skill)
- ESPHome device configuration (use esphome-config-helper skill)
- Kubernetes container orchestration

## Quick Usage

Create a basic add-on:

```bash
# 1. Create directory structure
mkdir -p my-addon/{rootfs,rootfs/etc/s6-overlay/s6-rc.d/my-service}

# 2. Create config.yaml
cat > my-addon/config.yaml << 'EOF'
name: My Add-On
slug: my-addon
version: 1.0.0
arch: [amd64, armv7, aarch64]
permissions: [homeassistant]
EOF

# 3. Create Dockerfile
cat > my-addon/Dockerfile << 'EOF'
FROM ghcr.io/home-assistant/{arch}-base:latest
COPY rootfs /
CMD ["/init"]
EOF

# 4. Create service script
cat > my-addon/rootfs/etc/s6-overlay/s6-rc.d/my-service/run << 'EOF'
#!/command/execlineb -P
/app/my-service
EOF
chmod +x my-addon/rootfs/etc/s6-overlay/s6-rc.d/my-service/run
```

## Token Efficiency

| Approach | Estimated Tokens | Time |
|----------|-----------------|------|
| Manual Implementation | 8,000-12,000 | 2-3 hours |
| With This Skill | 2,000-3,000 | 30-45 minutes |
| **Savings** | **70-75%** | **65-80% faster** |

Savings from pre-built patterns, configuration templates, troubleshooting guides, and architectural best practices.

## File Structure

```
ha-addon/
├── SKILL.md                    # Detailed instructions and patterns
├── README.md                   # This file - discovery and quick reference
├── assets/config.yaml          # Template configuration file
├── assets/Dockerfile           # Template Dockerfile
├── assets/bashio-reference.md  # bashio helper functions reference
└── references/                 # Supporting documentation
    └── supervisor-api.md       # Supervisor API endpoints and examples
```

## Dependencies

| Package | Version | Verified |
|---------|---------|----------|
| Home Assistant | 2024.1+ | 2025-12-31 |
| Docker | 20.10+ | 2025-12-31 |
| Docker buildx | Latest | 2025-12-31 |
| S6 Overlay | 3.x | Included in base images |
| bashio | Latest | Included in base images |

All dependencies except Docker come pre-installed in Home Assistant base images.

## Official Documentation

- [Home Assistant Add-On Development Guide](https://developers.home-assistant.io/docs/add-ons)
- [Add-On Configuration Reference](https://developers.home-assistant.io/docs/add-ons/configuration)
- [Supervisor API Reference](https://developers.home-assistant.io/docs/supervisor/developing)
- [bashio Helper Library](https://github.com/hassio-addons/bashio)
- [S6 Overlay Documentation](https://skarnet.org/software/s6-overlay/)

## Related Skills

- `esphome-config-helper` - ESP32/ESPHome device integration patterns
- `home-assistant-dashboard` - Lovelace dashboard configuration (complementary)
- `frigate-configurator` - NVR system setup (works with add-ons)

---

**License:** MIT

**Skill Purpose:** Reduce add-on development time and prevent common architectural mistakes with proven patterns and troubleshooting guidance.
