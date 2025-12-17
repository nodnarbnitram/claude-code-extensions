# Grafana Plugin Types Guide

Choosing the right plugin type for your use case (Grafana v12.x+).

## Plugin Type Overview

| Type | Purpose | Frontend | Backend | Complexity |
|------|---------|----------|---------|------------|
| Panel | Custom visualizations | React | None | Low-Medium |
| Data Source | Connect to external data | React | Optional Go | Medium-High |
| App | Full applications | React | Optional Go | High |

## Panel Plugins

### When to Use
- Custom visualization not available in core Grafana
- Specialized chart types (treemaps, network graphs, custom gauges)
- Industry-specific displays (trading, IoT, etc.)
- Data presentation with custom interactions

### Capabilities
- Receive data from any data source
- Configurable options panel
- Theme-aware styling
- Variable support
- Time range awareness
- Annotations support

### Limitations
- Cannot fetch data directly (uses data sources)
- No server-side processing
- Single visualization per panel

### Architecture
```
┌─────────────────────────────────────────┐
│             Grafana Dashboard           │
├─────────────────────────────────────────┤
│  ┌───────────────────────────────────┐  │
│  │         Panel Plugin               │  │
│  │  ┌─────────────────────────────┐  │  │
│  │  │     React Component         │  │  │
│  │  │  - Receives data frames     │  │  │
│  │  │  - Renders visualization    │  │  │
│  │  │  - Handles options          │  │  │
│  │  └─────────────────────────────┘  │  │
│  └───────────────────────────────────┘  │
│              ▲                           │
│              │ Data Frames               │
│              │                           │
│  ┌───────────────────────────────────┐  │
│  │         Data Source                │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

### Example Use Cases
- Custom heatmap with specific color schemes
- Network topology visualization
- Floor plan with sensor overlays
- Trading candlestick charts with custom indicators

## Data Source Plugins

### When to Use
- Connect Grafana to a new data backend
- Custom API integration
- Proprietary database connectivity
- Specialized query languages

### Frontend-Only Data Sources
Best for:
- REST APIs accessible from browser
- APIs with CORS enabled
- Simple authentication (API keys, OAuth)
- No need for alerting

### Backend Data Sources
Required for:
- Alerting support
- APIs not accessible from browser (internal networks)
- Complex authentication (mTLS, NTLM)
- Binary protocols
- Streaming data
- Heavy data processing

### Capabilities
- Custom query editor
- Configuration UI
- Health checks
- Annotations
- Variables
- Alerting (backend only)
- Streaming (backend only)

### Architecture
```
Frontend-Only:
┌────────────────┐     ┌────────────────┐     ┌────────────────┐
│    Browser     │────▶│ Grafana Proxy  │────▶│  External API  │
│  Query Editor  │     │  (routes.json) │     │                │
└────────────────┘     └────────────────┘     └────────────────┘

Backend:
┌────────────────┐     ┌────────────────┐     ┌────────────────┐
│    Browser     │────▶│ Grafana Server │────▶│  External API  │
│  Query Editor  │     │  (Go Plugin)   │     │                │
└────────────────┘     └────────────────┘     └────────────────┘
```

### Example Use Cases
- Custom metrics store (InfluxDB-like)
- REST API wrapper (Jira, ServiceNow)
- Database (custom SQL dialect)
- IoT platform integration

## App Plugins

### When to Use
- Full application within Grafana
- Multiple pages/views needed
- Custom workflows
- Configuration UIs
- Integration hubs

### Capabilities
- Multiple pages with routing
- Custom navigation
- Include other plugins (panels, data sources)
- Configuration pages
- Backend API endpoints (optional)
- Role-based access control

### Limitations
- Higher complexity
- More maintenance overhead
- Larger bundle sizes

### Architecture
```
┌─────────────────────────────────────────────────────┐
│                    App Plugin                        │
├─────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │
│  │   Page 1    │  │   Page 2    │  │   Page 3    │  │
│  │   (Home)    │  │ (Dashboard) │  │  (Config)   │  │
│  └─────────────┘  └─────────────┘  └─────────────┘  │
├─────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐                   │
│  │ Nested Panel│  │Nested DS    │  (Optional)       │
│  │   Plugin    │  │  Plugin     │                   │
│  └─────────────┘  └─────────────┘                   │
├─────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────┐    │
│  │           Backend Component (Optional)       │    │
│  │      - Custom API endpoints                  │    │
│  │      - Background processing                 │    │
│  └─────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────┘
```

### Example Use Cases
- Incident management system
- Infrastructure catalog
- Cost management dashboard
- MLOps platform
- Custom admin interface

## Decision Matrix

### Choose Panel Plugin When:
- [x] Need custom visualization
- [x] Data comes from existing data sources
- [x] No server-side processing needed
- [x] Single view is sufficient

### Choose Data Source Plugin When:
- [x] Need to connect to new data backend
- [x] Custom query language needed
- [x] Specific authentication requirements
- [x] Want to use data in standard panels

### Choose App Plugin When:
- [x] Need multiple pages
- [x] Building a complete application
- [x] Custom workflows required
- [x] Need to bundle multiple plugin types

### Add Backend When:
- [x] Need alerting support
- [x] API not browser-accessible
- [x] Complex authentication needed
- [x] Heavy data processing
- [x] Binary protocols
- [x] Streaming data

## Hybrid Approaches

### App with Nested Data Source
Common for integration platforms where you need:
- Configuration UI (app pages)
- Data connectivity (data source)
- Custom visualizations (optional nested panels)

### Data Source with Enhanced Query Editor
When you need:
- Rich query building experience
- Query templates/snippets
- Query analysis/optimization suggestions

### Panel with Backend Processing
Currently not directly supported - consider:
- Using a backend data source for processing
- Creating an app plugin if more control needed

## Migration Considerations

### Frontend DS → Backend DS
Reasons to migrate:
- Add alerting support
- Access internal APIs
- Improve security (hide credentials)
- Handle complex protocols

### Panel → App
Reasons to upgrade:
- Need configuration pages
- Multiple related visualizations
- Custom navigation required

### Standalone → Nested
Bundle related plugins in an app when:
- They work together
- Share configuration
- Simplify user installation
