# Grafana Billing Metrics Skill

Query key billing metrics from Prometheus and Loki through Grafana's data source proxy API.

## What This Skill Does

- Queries active time series count from Prometheus (primary billing metric)
- Calculates data points per minute (DPM) ingestion rate
- Analyzes cardinality to identify top metrics by series count
- Queries Loki ingestion rate (GB/day)
- Compares metrics across staging and production environments

## Core Capabilities

1. **Prometheus Metrics**: Active series, samples/sec, storage size, cardinality analysis
2. **Loki Metrics**: Ingestion rate, total bytes, active streams, memory chunks
3. **Multi-environment**: Query staging, prod, or both simultaneously
4. **Flexible output**: Human-readable tables or JSON for automation

## Auto-Trigger Keywords

### Primary Keywords
- billing metrics
- cost analysis
- active series
- observability costs

### Secondary Keywords
- prometheus cardinality
- loki ingestion
- storage usage
- grafana usage
- metrics invoice
- time series count
- DPM (data points per minute)

### Error Pattern Keywords
- "high cardinality"
- "ingestion rate too high"
- "storage growing"

## When to Use

- Analyzing observability infrastructure costs
- Investigating high cardinality metrics
- Comparing staging vs production usage
- Preparing for capacity planning
- Debugging ingestion rate issues

## Quick Usage

```bash
# Query all environments
uv run .claude/skills/grafana-billing/scripts/billing_metrics.py

# Query specific environment
uv run .claude/skills/grafana-billing/scripts/billing_metrics.py --env staging

# JSON output for scripting
uv run .claude/skills/grafana-billing/scripts/billing_metrics.py --json

# Only Prometheus metrics
uv run .claude/skills/grafana-billing/scripts/billing_metrics.py --service prometheus
```

## Environment Variables Required

| Variable | Description |
|----------|-------------|
| `GRAFANA_STAGING_API_KEY` | API key for staging Grafana workspace |
| `GRAFANA_PROD_API_KEY` | API key for prod Grafana workspace |

## File Structure

```
grafana-billing/
├── SKILL.md              # Skill instructions for Claude
├── README.md             # This file
├── scripts/
│   ├── billing_metrics.py      # Main CLI
│   ├── grafana_client.py       # Grafana API client
│   ├── prometheus_metrics.py   # Prometheus queries
│   ├── loki_metrics.py         # Loki queries
│   └── formatters.py           # Output formatting
└── references/
    └── billing-metrics.md      # Metric definitions
```

## Dependencies

Managed via uv inline script metadata:
- `httpx` - HTTP client
- `python-dotenv` - Environment variable loading
- `rich` - Table formatting

## Official Documentation

- [Grafana Cloud Metrics Billing](https://grafana.com/docs/grafana-cloud/cost-management-and-billing/understand-your-invoice/metrics-invoice/)
- [Active Series and DPM](https://grafana.com/docs/grafana-cloud/account-management/billing-and-usage/active-series-and-dpm/)
- [Prometheus TSDB Status](https://prometheus.io/docs/prometheus/latest/querying/api/#tsdb-stats)
- [Loki Metrics](https://grafana.com/docs/loki/latest/operations/observability/)

## Related Skills

- `grafana-plugin-scaffolding` - Grafana plugin development
- `kubernetes-operations` - K8s cluster management
