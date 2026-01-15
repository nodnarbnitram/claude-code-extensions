# Home Assistant Energy Skill

> Set up Home Assistant energy monitoring with dashboards, solar, grid, and device tracking.

| | |
|---|---|
| **Status** | Active |
| **Version** | 1.0.0 |
| **Last Updated** | 2025-12-31 |
| **Confidence** | 4/5 |
| **Production Tested** | Home Assistant 2023.1+ |

## What This Skill Does

Provides expert guidance for configuring Home Assistant energy monitoring, including energy sensors with proper state classes, utility meters for billing cycles, solar panel tracking, grid monitoring, and device consumption analysis.

### Core Capabilities

- Energy sensor configuration (state_class, device_class, units)
- Utility meter setup for daily/monthly/yearly consumption tracking
- Solar panel production and battery integration
- Grid consumption and return monitoring (separate sensors)
- Device power consumption tracking (smart plugs, CT clamps)
- Statistics and long-term data retention configuration
- Riemann sum integration (converting power to energy)
- Energy dashboard setup and troubleshooting

## Auto-Trigger Keywords

### Primary Keywords
Exact terms that strongly trigger this skill:
- energy dashboard
- energy monitoring
- solar production
- grid consumption
- kWh tracking
- utility meter
- power monitoring
- energy sensors

### Secondary Keywords
Related terms that may trigger in combination:
- state_class
- device_class: energy
- total_increasing
- solar panels
- battery charging
- grid return
- consumption meter
- utility_meter integration
- statistics
- recorder configuration
- self-consumption

### Error-Based Keywords
Common error messages that should trigger this skill:
- "Energy dashboard shows no data"
- "Utility meter not resetting"
- "Solar self-consumption not tracking"
- "Sensor unavailable"
- "Invalid state_class"
- "statistics not generated"

## Known Issues Prevention

| Issue | Root Cause | Solution |
|-------|-----------|----------|
| Energy dashboard blank | Missing `state_class` on sensors | Use `total_increasing` for cumulative meters |
| Utility meter not resetting | Wrong cycle or offset settings | Verify cycle (daily/monthly) and timezone offset |
| Solar not showing in dashboard | Separate battery sensors not configured | Create charge/discharge sensors for batteries |
| Grid flow incorrect | Using bidirectional sensor | Split into consumption and return sensors |
| Statistics missing | Sensors not in recorder's include list | Add energy sensors to recorder configuration |

## When to Use

### Use This Skill For
- Configuring energy sensors with proper state classes and device classes
- Setting up utility meters for consumption tracking by period
- Solar panel production tracking and battery integration
- Grid monitoring (consumption and return flows)
- Individual device energy consumption tracking
- Troubleshooting energy dashboard display issues
- Long-term energy statistics and historical analysis
- Cost tracking with utility meter tariffs
- Riemann sum integration for converting power to energy

### Don't Use This Skill For
- Home Assistant automations and general scripting
- Integration setup for specific device types (covered by device integrations)
- Non-energy sensor configuration
- Dashboard UI design (use ha-dashboard skill)
- Energy cost calculations (covered separately)
- Device pairing and discovery

## Quick Usage

```yaml
# Basic energy sensor with proper configuration
template:
  - sensor:
      - name: "Total Energy"
        unique_id: total_energy
        unit_of_measurement: kWh
        device_class: energy
        state_class: total_increasing
        state: "{{ (states('sensor.meter') | float(0)) }}"

# Utility meter for daily tracking
utility_meter:
  daily_energy:
    source: sensor.total_energy
    cycle: daily
    offset:
      hours: 0
```

## Token Efficiency

| Approach | Estimated Tokens | Time |
|----------|-----------------|------|
| Manual Implementation | ~10000 | 45+ min |
| With This Skill | ~5500 | 15 min |
| **Savings** | **45%** | **30+ min** |

## File Structure

```
ha-energy/
├── SKILL.md                    # Detailed instructions and patterns
├── README.md                   # This file - discovery and quick reference
├── references/                 # Supporting documentation
│   ├── state-class-guide.md               # state_class reference
│   ├── device-class-reference.md          # device_class values
│   ├── utility-meter-patterns.md          # Billing cycle configs
│   ├── energy-dashboard-setup.md          # Step-by-step guide
│   └── solar-integration.md               # Solar and battery setup
└── assets/
    ├── energy-sensors-template.yaml       # Complete sensor template
    ├── utility-meter-examples.yaml        # Meter configurations
    └── energy-dashboard-card.yaml         # Dashboard card YAML
```

## Dependencies

| Package | Version | Verified |
|---------|---------|----------|
| Home Assistant | 2023.1+ | 2025-12-31 |
| Template Integration | Built-in | 2025-12-31 |
| Utility Meter Integration | Built-in | 2025-12-31 |

## Official Documentation

- [Energy Integration Overview](https://www.home-assistant.io/docs/energy/)
- [Electricity Grid Monitoring](https://www.home-assistant.io/docs/energy/electricity-grid/)
- [Solar Panels Integration](https://www.home-assistant.io/docs/energy/solar-panels/)
- [Utility Meter Integration](https://www.home-assistant.io/integrations/utility_meter/)
- [Template Sensor](https://www.home-assistant.io/integrations/template/)
- [Recorder Configuration](https://www.home-assistant.io/integrations/recorder/)

## Related Skills

- `ha-dashboard` - Configure Home Assistant Lovelace dashboards for energy visualization
- `ha-automation` - Create automations based on energy consumption patterns (if available)

---

**License:** MIT
