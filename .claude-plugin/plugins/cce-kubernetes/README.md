# CCE Kubernetes Plugin

Kubernetes cluster operations, health diagnostics, and operator-specific agents.

## Overview

The **cce-kubernetes** plugin provides comprehensive Kubernetes support including dynamic cluster health diagnostics, kubectl operations, and operator-specific health checks for ArgoCD, Crossplane, cert-manager, and Prometheus.

## Features

- **Dynamic Health Checks**: API discovery detects installed operators and runs specialized diagnostics
- **Operator Support**: ArgoCD, Crossplane, cert-manager, Prometheus Operator
- **kubectl Operations**: Debugging, logs, describe, exec, port-forward
- **Resource Management**: Deployments, services, configmaps, secrets, scaling, rollouts
- **Token-Efficient**: Scripts use bash commands, not verbose tool output

## Plugin Components

### Agents (6)

**Orchestrator:**
- **k8s-health-orchestrator**: Dynamic API discovery and health orchestration

**Specialized Health Agents:**
- **k8s-core-health-agent**: Nodes, pods, deployments, services, PVCs
- **k8s-argocd-health-agent**: Applications, AppProjects, ApplicationSets, sync status
- **k8s-crossplane-health-agent**: Providers, compositions, claims, managed resources
- **k8s-certmanager-health-agent**: Certificates, Issuers, certificate expiry
- **k8s-prometheus-health-agent**: Prometheus instances, AlertManagers, ServiceMonitors

### Skills (2)

- **kubernetes-operations**: kubectl debugging and resource management scripts
- **kubernetes-health**: Comprehensive cluster diagnostics

### Commands (1)

- `/cce-kubernetes:health`: Run complete cluster health assessment

## Installation

### From Marketplace (Recommended)

```bash
# Add the CCE marketplace
/plugin marketplace add github:nodnarbnitram/claude-code-extensions

# Install Kubernetes plugin
/plugin install cce-kubernetes@cce-marketplace
```

### From Local Source

```bash
git clone https://github.com/nodnarbnitram/claude-code-extensions.git
/plugin marketplace add /path/to/claude-code-extensions
/plugin install cce-kubernetes@cce-marketplace
```

## Usage

### Command

```bash
/cce-kubernetes:health
# Runs dynamic API discovery and comprehensive health checks
# Automatically detects ArgoCD, Crossplane, cert-manager, Prometheus
```

### Skills (User-Invoked)

```bash
/kubernetes-operations
# Interactive kubectl operation menu (debug, logs, describe, exec, port-forward)

/kubernetes-health
# Full cluster health diagnostic
```

### Agents (Automatic Activation)

```bash
> Check if my ArgoCD applications are healthy
# Uses k8s-argocd-health-agent

> Debug the failing deployment in namespace prod
# Uses kubernetes-operations skill

> Check certificate expiry dates
# Uses k8s-certmanager-health-agent

> Verify Crossplane managed resources are ready
# Uses k8s-crossplane-health-agent
```

### Example Workflows

**Complete Cluster Health:**
```bash
/cce-kubernetes:health
# Output:
# ✅ Core resources healthy
# ✅ ArgoCD: 15 apps synced
# ⚠️  Crossplane: 2 managed resources degraded
# ✅ cert-manager: All certs valid
```

**Debugging Pods:**
```bash
> Show logs for failing pods in namespace my-app
# Uses kubectl logs with error filtering
```

**Resource Scaling:**
```bash
> Scale deployment api-server to 5 replicas
# Uses kubectl scale
```

## Requirements

- **Claude Code**: Latest version
- **kubectl**: Configured with cluster access
- **Kubeconfig**: Valid context for target cluster
- **Optional Operators**: ArgoCD, Crossplane, cert-manager, Prometheus

## Health Check Coverage

**Core Resources:**
- Nodes (ready, disk pressure, memory pressure)
- Pods (phase, restarts, readiness)
- Deployments (replicas, conditions)
- Services (endpoints, selector matching)
- PersistentVolumeClaims (binding status)

**ArgoCD:**
- Application sync status and health
- AppProject quotas and restrictions
- ApplicationSet generation status

**Crossplane:**
- Provider installation and health
- Composition definitions
- Claims and managed resource status

**cert-manager:**
- Certificate ready status
- Issuer ready status
- Certificate expiry warnings

**Prometheus:**
- Prometheus instance status
- AlertManager replicas
- ServiceMonitor target discovery

## License

MIT License - see [LICENSE](../../../LICENSE) for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/nodnarbnitram/claude-code-extensions/issues)
- **Documentation**: [Repository README](../../../README.md)
