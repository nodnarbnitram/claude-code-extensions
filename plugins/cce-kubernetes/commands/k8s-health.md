---
description: Run comprehensive Kubernetes cluster health diagnostics with dynamic operator discovery
argument-hint: [--operator <name>] [--output json|summary|detailed] [--namespace <ns>]
allowed-tools: Bash(kubectl:*), Task, Skill
---

# Kubernetes Health Diagnostics

Run comprehensive cluster health diagnostics using dynamic API discovery.

## Arguments

- `--operator <name>`: Filter to specific operator (crossplane, argocd, certmanager, prometheus)
- `--output <format>`: Output format (summary, detailed, json). Default: summary
- `--namespace <ns>`: Limit checks to specific namespace

## Workflow

1. **Verify cluster access**
   ```bash
   kubectl config current-context
   kubectl cluster-info --request-timeout=5s
   ```

2. **Confirm cluster** - For production clusters, confirm before proceeding

3. **Run health check** - Invoke the kubernetes-health skill:
   - Discover installed operators via API discovery
   - Dispatch k8s-core-health-agent (always)
   - Dispatch operator-specific agents based on discovery
   - Aggregate results into unified report

4. **Present results** based on output format:
   - **summary**: Overall score, status, top issues, recommendations
   - **detailed**: Full component breakdown with all checks
   - **json**: Raw JSON for programmatic consumption

## Example Usage

```
/k8s-health
/k8s-health --operator crossplane
/k8s-health --output json
/k8s-health --namespace production --output detailed
```

## Output

### Summary Format (default)

```
Cluster Health: prod-eks-us-west-2
Overall: 91/100 - HEALTHY

Components:
  + Core: 98/100 (HEALTHY)
  ~ Crossplane: 72/100 (DEGRADED)
  + ArgoCD: 95/100 (HEALTHY)
  + Cert-Manager: 100/100 (HEALTHY)

Critical Issues: None

Warnings:
  - Crossplane: 2 managed resources not ready

Recommendations:
  1. Check AWS provider credentials
  2. Review managed resource aws-rds-1
```

### JSON Format

```json
{
  "cluster": "prod-eks-us-west-2",
  "timestamp": "2025-12-09T11:05:00Z",
  "overall": {"status": "HEALTHY", "score": 91},
  "components": {...}
}
```

## Invoke

Use the kubernetes-health skill and k8s-health-orchestrator agent to perform the health check based on arguments: $ARGUMENTS
