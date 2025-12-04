# Kubernetes Operations

> Comprehensive kubectl assistance for debugging, resource management, and cluster operations with token-efficient scripts.

| | |
|---|---|
| **Status** | Active |
| **Version** | 1.0.0 |
| **Last Updated** | 2025-11-22 |
| **Confidence** | 4/5 |
| **Production Tested** | Yes |

## What This Skill Does

Provides intelligent assistance for Kubernetes operations using kubectl. Includes token-efficient Python scripts that condense verbose kubectl output into actionable summaries.

### Core Capabilities

- Debug pods with condensed status, events, and logs
- Manage resources (deployments, services, configmaps, secrets)
- Monitor cluster health and resource usage
- Troubleshoot common Kubernetes issues

## Auto-Trigger Keywords

### Primary Keywords
Exact terms that strongly trigger this skill:
- kubectl
- kubernetes
- k8s
- pods
- deployments

### Secondary Keywords
Related terms that may trigger in combination:
- cluster
- namespace
- service
- configmap
- secret
- nodes
- replicas
- rollout

### Error-Based Keywords
Common error messages that should trigger this skill:
- "CrashLoopBackOff"
- "ImagePullBackOff"
- "Pending"
- "OOMKilled"
- "connection refused"
- "no endpoints available"
- "forbidden"

## Known Issues Prevention

| Issue | Root Cause | Solution |
|-------|-----------|----------|
| Wrong cluster context | Not verifying before commands | Always check `kubectl config current-context` |
| Verbose output flooding | Using default kubectl output | Use scripts or jsonpath for minimal output |
| Missing debug info | Incomplete investigation | Use `debug_pod.py` for comprehensive view |
| Secret exposure | Outputting secrets as YAML | Never output secrets in plain text |

## When to Use

### Use This Skill For
- Debugging pod startup issues
- Checking cluster health
- Managing Kubernetes resources
- Troubleshooting service connectivity
- Viewing logs and events

### Don't Use This Skill For
- Creating Helm charts (use helm-chart-scaffolding skill)
- ArgoCD/GitOps workflows (use argocd agents)
- Terraform/IaC for cluster provisioning
- Custom Resource Definition development

## Quick Usage

```bash
# Debug a pod
uv run scripts/debug_pod.py my-pod -n my-namespace

# List resources compactly
uv run scripts/get_resources.py pods -n my-namespace

# Check cluster health
uv run scripts/cluster_health.py
```

## Token Efficiency

| Approach | Estimated Tokens | Time |
|----------|-----------------|------|
| Manual kubectl commands | ~1200 | 5+ min |
| With This Skill | ~400 | 1 min |
| **Savings** | **67%** | **4 min** |

## File Structure

```
kubernetes-operations/
├── SKILL.md        # Detailed instructions and patterns
├── README.md       # This file - discovery and quick reference
├── scripts/        # Token-efficient automation scripts
│   ├── debug_pod.py
│   ├── get_resources.py
│   └── cluster_health.py
├── references/     # Supporting documentation
│   ├── kubectl-cheatsheet.md
│   ├── jsonpath-patterns.md
│   └── debugging-flowchart.md
└── assets/         # Templates and resources
```

## Dependencies

| Package | Version | Verified |
|---------|---------|----------|
| kubectl | 1.25+ | 2024-11-22 |
| jq | 1.6+ | 2024-11-22 |

## Official Documentation

- [kubectl Quick Reference](https://kubernetes.io/docs/reference/kubectl/quick-reference/)
- [JSONPath Support](https://kubernetes.io/docs/reference/kubectl/jsonpath/)
- [Debug Running Pods](https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/)

## Related Skills

- `helm-chart-scaffolding` - Helm chart creation and management
- `k8s-manifest-generator` - Generate Kubernetes YAML manifests
- `gitops-workflow` - ArgoCD/Flux GitOps patterns

---

**License:** MIT
