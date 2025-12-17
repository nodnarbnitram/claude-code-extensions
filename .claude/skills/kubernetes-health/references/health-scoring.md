# Health Scoring Methodology

This document defines how health scores are calculated for Kubernetes cluster health reports.

## Score Ranges

| Status | Score Range | Criteria |
|--------|-------------|----------|
| **HEALTHY** | 90-100 | All checks pass, no warnings or errors |
| **DEGRADED** | 60-89 | Some warnings present, no critical issues |
| **CRITICAL** | 0-59 | Critical issues affecting availability or functionality |

## Check Categories

Each health check belongs to one of four categories with assigned weights:

| Category | Weight | Description | Examples |
|----------|--------|-------------|----------|
| **Availability** | 40% | Is the component running and accessible? | Pod running, node ready, endpoint reachable |
| **Configuration** | 25% | Is the component properly configured? | Valid specs, proper limits, correct settings |
| **Freshness** | 20% | Is data/state up-to-date? | Recent sync, up-to-date revision, fresh reconcile |
| **Resources** | 15% | Are resources within limits? | CPU/memory usage, storage capacity, quota usage |

## Check Status Scoring

Individual checks contribute to the component score based on their status:

| Check Status | Score Contribution | Description |
|--------------|-------------------|-------------|
| **OK** | 100 points | Check passed completely |
| **WARNING** | 70 points | Check passed with warnings |
| **ERROR** | 30 points | Check failed |

## Component Score Calculation

Component score is calculated as a weighted average of all checks:

```
component_score = Σ(check_score × category_weight) / Σ(category_weight)
```

### Example Calculation

Given a component with these checks:

| Check | Category | Status | Score |
|-------|----------|--------|-------|
| Pod running | availability | OK | 100 |
| Config valid | configuration | WARNING | 70 |
| Last sync | freshness | OK | 100 |
| CPU usage | resources | OK | 100 |

Calculation:
```
weighted_sum = (100 × 0.40) + (70 × 0.25) + (100 × 0.20) + (100 × 0.15)
             = 40 + 17.5 + 20 + 15
             = 92.5

total_weight = 0.40 + 0.25 + 0.20 + 0.15 = 1.0

component_score = 92.5 / 1.0 = 92.5 → HEALTHY
```

## Overall Score Calculation

The overall cluster health score is a weighted average of all component scores:

```
overall_score = Σ(component_score × component_weight) / Σ(component_weight)
```

### Component Weights

| Component | Weight | Rationale |
|-----------|--------|-----------|
| **Core** | 1.0 | Core Kubernetes health is always critical |
| **Crossplane** | 0.8 | Infrastructure-as-code, important but not always critical |
| **ArgoCD** | 0.8 | GitOps deployments, important for delivery |
| **Cert-Manager** | 0.8 | TLS certificates, security-relevant |
| **Prometheus** | 0.8 | Monitoring, important for observability |

### Example Overall Calculation

Given these component scores:

| Component | Score | Weight |
|-----------|-------|--------|
| Core | 98 | 1.0 |
| Crossplane | 72 | 0.8 |
| ArgoCD | 95 | 0.8 |

Calculation:
```
weighted_sum = (98 × 1.0) + (72 × 0.8) + (95 × 0.8)
             = 98 + 57.6 + 76
             = 231.6

total_weight = 1.0 + 0.8 + 0.8 = 2.6

overall_score = 231.6 / 2.6 = 89.1 → DEGRADED
```

## Status Determination Rules

### CRITICAL Status Triggers

A component is **CRITICAL** (score < 60) when any of:
- Core pods are not running (CrashLoopBackOff, Failed)
- No replicas available
- Controller/operator pod down
- Data loss or corruption detected

### DEGRADED Status Triggers

A component is **DEGRADED** (score 60-89) when any of:
- Some pods restarting frequently
- Stale data (last sync > threshold)
- Configuration warnings
- Resource pressure (approaching limits)

### HEALTHY Status Criteria

A component is **HEALTHY** (score 90-100) when:
- All pods running and ready
- All configurations valid
- Data is fresh (recent sync/reconcile)
- Resources within normal limits
- No warnings or errors in recent events

## Severity Classification

Issues are classified by severity for prioritization:

| Severity | Description | Examples |
|----------|-------------|----------|
| **Critical** | Immediate action required | Service down, data at risk |
| **High** | Action needed soon | Performance degraded, approaching limits |
| **Medium** | Should be addressed | Warnings, suboptimal config |
| **Low** | Nice to fix | Minor inefficiencies |

## Recommendations Priority

Recommendations are sorted by:
1. Severity (Critical → Low)
2. Impact (more components affected first)
3. Effort (quick wins first)

```python
def sort_recommendations(recommendations):
    severity_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
    return sorted(
        recommendations,
        key=lambda r: (
            severity_order.get(r["severity"], 4),
            -r.get("impact_count", 1),
            r.get("effort_minutes", 60)
        )
    )
```
