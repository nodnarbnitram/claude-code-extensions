# CCE Grafana Plugin

Comprehensive Grafana plugin development and observability billing metrics analysis for Claude Code.

## Overview

This plugin provides expert assistance for:
- **Grafana Plugin Development**: Complete lifecycle support for panel, data source, app, and backend plugins
- **Billing Metrics Analysis**: Query and analyze Prometheus and Loki billing metrics from Grafana Cloud
- **SDK Guidance**: Up-to-date documentation access via Context7 for latest Grafana Plugin SDK patterns

## Components

### Agents

#### grafana-plugin-expert
Expert agent for Grafana plugin development with deep knowledge of:
- Plugin architecture (panel, data source, app, backend)
- Grafana Plugin SDK (@grafana/data, @grafana/ui, @grafana/runtime)
- React frontend patterns and Go backend development
- Plugin lifecycle: create, develop, test, sign, publish
- Context7 integration for current SDK documentation

**Auto-triggers on:**
- Grafana plugin development tasks
- Plugin type selection (panel, data source, app)
- SDK usage questions
- Plugin configuration and testing

### Skills

#### grafana-plugin-scaffolding
Automates Grafana plugin project creation using `@grafana/create-plugin`.

**Features:**
- Project scaffolding for all plugin types
- Docker development environment setup with hot-reload
- E2E testing configuration with Playwright
- Plugin configuration management

**Use when:**
- Creating new Grafana plugins
- Setting up development environments
- Configuring Docker Compose for local testing
- Setting up E2E testing infrastructure

**Commands:**
```bash
# Scaffold new plugin (interactive)
npx @grafana/create-plugin@latest

# Start development with hot-reload
docker compose watch

# Run E2E tests
npx playwright test
```

#### grafana-billing
Query and analyze billing metrics from Grafana Cloud Prometheus and Loki instances.

**Features:**
- Query active time series (Prometheus billing dimension)
- Track ingestion rates (samples/sec, GB/day)
- Analyze cardinality (top metrics by series count)
- Compare staging vs production usage
- Storage usage analysis

**Use when:**
- Analyzing observability costs
- Investigating cardinality issues
- Tracking ingestion rate growth
- Comparing environment usage
- Cost optimization planning

**Commands:**
```bash
# Query both environments
uv run .claude/skills/grafana-billing/scripts/billing_metrics.py

# Query specific environment
uv run .claude/skills/grafana-billing/scripts/billing_metrics.py --env prod

# JSON output for automation
uv run .claude/skills/grafana-billing/scripts/billing_metrics.py --json

# Filter to specific service
uv run .claude/skills/grafana-billing/scripts/billing_metrics.py --service prometheus
```

## Installation

### Plugin Mode (Recommended)

```bash
# Add marketplace (if not already added)
/plugin marketplace add /path/to/claude-code-extensions

# Install plugin
/plugin install cce-grafana@cce-marketplace

# Verify installation
/agents  # Should show grafana-plugin-expert
```

Commands are available under the `/cce-grafana:` namespace.

### Standalone Mode

```bash
# Install extensions to project
./install_extensions.py install ~/your-project

# Verify installation
cd ~/your-project && claude
> /agents  # Should show grafana-plugin-expert
```

Commands are available without namespace prefix.

## Usage Examples

### Create a New Panel Plugin

```
Create a new Grafana panel plugin for visualizing time series data with custom aggregations.
```

The agent will:
1. Use the `grafana-plugin-scaffolding` skill to scaffold the project
2. Guide you through plugin type selection
3. Set up the development environment
4. Provide implementation patterns for the panel component

### Analyze Billing Metrics

```
Show me the current Prometheus billing metrics for production and identify any high-cardinality issues.
```

The agent will:
1. Run the billing metrics script for production
2. Display active series, ingestion rates, and storage
3. Highlight top cardinality metrics
4. Suggest optimization opportunities

### Implement a Data Source Backend

```
I need to create a data source plugin with a Go backend that connects to a custom API.
```

The agent will:
1. Scaffold a backend-enabled data source plugin
2. Provide Go implementation patterns using grafana-plugin-sdk-go
3. Show how to implement QueryData and CheckHealth methods
4. Guide on Docker setup for testing

## Key Metrics

### Prometheus Billing Metrics
- **Active Time Series**: Current count of active series (primary billing dimension)
- **Ingestion Rate**: Samples/sec (DPM = samples/sec × 60)
- **Storage**: TSDB on-disk storage bytes
- **Cardinality**: Top metrics by series count

### Loki Billing Metrics
- **Ingestion Rate**: GB/day being ingested
- **Total Bytes**: Cumulative bytes received
- **Active Streams**: Number of active log streams
- **Memory Usage**: Chunks held in memory

## Environment Variables

For billing metrics analysis, set these environment variables:

```bash
export GRAFANA_STAGING_API_KEY="your-staging-api-key"
export GRAFANA_PROD_API_KEY="your-prod-api-key"
```

API keys require:
- Read access to Prometheus and Loki data sources
- Query permissions for billing metrics

## Supported Grafana Version

This plugin supports **Grafana v12.x and later**. For older versions, consult the official Grafana migration guides.

## Plugin Development Workflow

1. **Scaffold**: Use `grafana-plugin-scaffolding` skill
2. **Develop**: Edit components in `src/`, backend in `pkg/`
3. **Test**: Run `npm run dev` and `docker compose watch`
4. **E2E Test**: Run `npx playwright test`
5. **Build**: Run `npm run build` and `mage -v` (backend)
6. **Sign**: Use `npx @grafana/sign-plugin`
7. **Publish**: Submit to Grafana plugin catalog

## References

- [Grafana Plugin Tools Documentation](https://grafana.com/developers/plugin-tools/)
- [Plugin Examples Repository](https://github.com/grafana/grafana-plugin-examples)
- [Plugin Signing Guide](https://grafana.com/docs/grafana/latest/developers/plugins/sign-a-plugin/)
- [Grafana Cloud Billing](https://grafana.com/docs/grafana-cloud/billing-and-usage/)

## Troubleshooting

### Plugin Not Appearing
- Verify `plugin.json` has correct ID format: `orgname-pluginname-type`
- Check Docker volume mounts in `docker-compose.yaml`
- Ensure `npm run dev` completed without errors
- Restart Grafana: `docker compose restart`

### Backend Plugin Errors
- Rebuild Go code: `mage -v`
- Verify binary exists in `dist/`: `gpx_*` or `plugin_start_linux_*`
- Check `plugin.json` has `"backend": true`
- Review Grafana logs: `docker compose logs grafana`

### Billing Metrics Errors
- Verify API keys are set and valid
- Check data source names match configuration
- Ensure API keys have query permissions
- Test individual queries in Grafana Explore

## Contributing

See the main repository [CONTRIBUTING.md](https://github.com/nodnarbnitram/claude-code-extensions/blob/main/CONTRIBUTING.md) for guidelines.

## License

MIT License - See [LICENSE](https://github.com/nodnarbnitram/claude-code-extensions/blob/main/LICENSE)
