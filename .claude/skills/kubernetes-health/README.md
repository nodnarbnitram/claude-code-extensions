# Kubernetes Health

> Dynamic, discovery-driven health diagnostics for Kubernetes clusters

| | |
|---|---|
| **Status** | Active |
| **Version** | 1.0.0 |
| **Last Updated** | 2025-12-09 |
| **Confidence** | 4/5 |
| **Production Tested** | Yes |

## What This Skill Does

- Discovers all installed Kubernetes operators via API discovery
- Dispatches specialized health check agents based on detected APIs
- Aggregates multi-agent results into unified health reports
- Provides weighted health scores (0-100) with status determination
- Generates prioritized recommendations for identified issues

## Auto-Trigger Keywords

### Primary Keywords

- cluster health
- k8s health
- kubernetes health
- kubernetes diagnostics
- cluster diagnostics
- health check
- health assessment

### Secondary Keywords

- node status
- pod health
- deployment health
- operator health
- crossplane health
- argocd health
- cert-manager health
- prometheus health
- api discovery
- cluster status

### Error-Based Keywords

- CrashLoopBackOff
- ImagePullBackOff
- Pending pods
- NotReady nodes
- OutOfSync applications
- certificate expiring
- provider not healthy
- managed resource failed

## When to Use

### Use This Skill When

- Performing routine cluster health assessments
- Troubleshooting cluster-wide issues
- Onboarding to an unfamiliar cluster
- Validating cluster state before/after changes
- Generating health reports for stakeholders

### Don't Use This Skill When

- Debugging a single pod (use kubectl directly)
- Modifying cluster resources (this is read-only)
- Real-time monitoring (this is point-in-time)
- Automatic remediation (agents provide recommendations only)

## Quick Usage

```bash
# Run API discovery
uv run .claude/skills/kubernetes-health/scripts/discover_apis.py

# Get agent dispatch plan
uv run .claude/skills/kubernetes-health/scripts/health_orchestrator.py

# Aggregate results (after agents complete)
uv run .claude/skills/kubernetes-health/scripts/aggregate_report.py
```

## File Structure

```
kubernetes-health/
├── SKILL.md              # Main skill instructions
├── README.md             # This file (auto-trigger keywords)
├── scripts/
│   ├── discover_apis.py      # API discovery engine
│   ├── health_orchestrator.py # Sub-agent mapping
│   └── aggregate_report.py    # Report aggregation
├── references/
│   ├── operator-checks.md     # Per-operator health checks
│   └── health-scoring.md      # Scoring methodology
└── templates/
    └── health-report.json     # Output schema
```

## Dependencies

| Package | Required | Purpose |
|---------|----------|---------|
| kubectl | Yes | Cluster interaction |
| Python 3.11+ | Yes | Script execution |
| uv | Yes | Python script runner |
| kubernetes | No | Advanced API discovery |
