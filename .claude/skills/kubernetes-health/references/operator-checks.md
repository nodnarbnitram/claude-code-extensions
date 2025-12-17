# Operator Health Checks Reference

Detailed health checks for each supported Kubernetes operator.

## Crossplane

### Provider Checks

| Check | kubectl Command | Healthy | Warning | Critical |
|-------|-----------------|---------|---------|----------|
| Provider pods | `kubectl get pods -n crossplane-system -l pkg.crossplane.io/provider` | All Running | Some not Ready | CrashLoopBackOff |
| Provider status | `kubectl get providers.pkg.crossplane.io` | All Healthy | Some Unhealthy | None Healthy |
| Provider revisions | `kubectl get providerrevisions.pkg.crossplane.io` | Active revision exists | Multiple active | No active revision |

### Composition Checks

| Check | kubectl Command | Healthy | Warning | Critical |
|-------|-----------------|---------|---------|----------|
| Composition status | `kubectl get compositions` | All present | Some missing resources | Composition errors |
| XRD status | `kubectl get compositeresourcedefinitions` | All Established | Some Pending | Failed |

### Managed Resource Checks

| Check | kubectl Command | Healthy | Warning | Critical |
|-------|-----------------|---------|---------|----------|
| Ready status | `kubectl get managed -A -o jsonpath='{.items[*].status.conditions}'` | All Ready=True | Some Synced=False | Ready=False |
| Sync status | Filter for Synced condition | All Synced | Some not Synced | None Synced |
| Last reconcile | Check lastTransitionTime | < 5 min ago | < 30 min ago | > 30 min ago |

### Claim Checks

| Check | kubectl Command | Healthy | Warning | Critical |
|-------|-----------------|---------|---------|----------|
| Claim binding | `kubectl get claims -A` | All Bound | Some Pending | Failed |
| Connection secrets | Check secretRef exists | All present | Some missing | None present |

---

## ArgoCD

### Application Checks

| Check | kubectl Command | Healthy | Warning | Critical |
|-------|-----------------|---------|---------|----------|
| Sync status | `kubectl get applications.argoproj.io -A -o jsonpath='{.items[*].status.sync.status}'` | All Synced | OutOfSync | Unknown |
| Health status | `kubectl get applications.argoproj.io -A -o jsonpath='{.items[*].status.health.status}'` | Healthy | Progressing/Suspended | Degraded/Missing |
| Last sync time | Check operationState.finishedAt | < 10 min ago | < 1 hour ago | > 1 hour ago |

### AppProject Checks

| Check | kubectl Command | Healthy | Warning | Critical |
|-------|-----------------|---------|---------|----------|
| Project exists | `kubectl get appprojects.argoproj.io -A` | All defined | Some missing | None defined |
| RBAC configured | Check spec.roles | Roles defined | No roles | - |

### ApplicationSet Checks

| Check | kubectl Command | Healthy | Warning | Critical |
|-------|-----------------|---------|---------|----------|
| Generator status | `kubectl get applicationsets.argoproj.io -A` | All generating | Some errors | All failing |
| Generated apps | Check status.conditions | Apps created | Some pending | None created |

### Controller Checks

| Check | kubectl Command | Healthy | Warning | Critical |
|-------|-----------------|---------|---------|----------|
| Controller pod | `kubectl get pods -n argocd -l app.kubernetes.io/name=argocd-application-controller` | Running | Restarting | CrashLoopBackOff |
| Server pod | `kubectl get pods -n argocd -l app.kubernetes.io/name=argocd-server` | Running | Restarting | CrashLoopBackOff |
| Repo server | `kubectl get pods -n argocd -l app.kubernetes.io/name=argocd-repo-server` | Running | Restarting | CrashLoopBackOff |

---

## Cert-Manager

### Certificate Checks

| Check | kubectl Command | Healthy | Warning | Critical |
|-------|-----------------|---------|---------|----------|
| Certificate status | `kubectl get certificates.cert-manager.io -A` | All Ready=True | Some Pending | Ready=False |
| Expiry (days) | Check status.notAfter | > 30 days | 7-30 days | < 7 days |
| Renewal status | Check status.renewalTime | Scheduled | Overdue | Failed |

### Issuer Checks

| Check | kubectl Command | Healthy | Warning | Critical |
|-------|-----------------|---------|---------|----------|
| Issuer status | `kubectl get issuers.cert-manager.io -A` | All Ready=True | Some not Ready | None Ready |
| ClusterIssuer status | `kubectl get clusterissuers.cert-manager.io` | All Ready=True | Some not Ready | None Ready |
| ACME status | Check status.acme.uri | Registered | - | Registration failed |

### CertificateRequest Checks

| Check | kubectl Command | Healthy | Warning | Critical |
|-------|-----------------|---------|---------|----------|
| Request status | `kubectl get certificaterequests.cert-manager.io -A` | All Approved | Some Pending | Denied |
| Issuance | Check status.conditions | Issued | Pending | Failed |

### Controller Checks

| Check | kubectl Command | Healthy | Warning | Critical |
|-------|-----------------|---------|---------|----------|
| Controller pod | `kubectl get pods -n cert-manager -l app=cert-manager` | Running | Restarting | CrashLoopBackOff |
| Webhook pod | `kubectl get pods -n cert-manager -l app=webhook` | Running | Restarting | CrashLoopBackOff |
| CA Injector | `kubectl get pods -n cert-manager -l app=cainjector` | Running | Restarting | CrashLoopBackOff |

---

## Prometheus Operator

### Prometheus Instance Checks

| Check | kubectl Command | Healthy | Warning | Critical |
|-------|-----------------|---------|---------|----------|
| Prometheus pods | `kubectl get pods -l app.kubernetes.io/name=prometheus` | All Running | Some not Ready | CrashLoopBackOff |
| Prometheus CR | `kubectl get prometheus.monitoring.coreos.com -A` | Reconciled | Pending | Failed |
| Target discovery | Check status.availableReplicas | All available | Some unavailable | None available |

### AlertManager Checks

| Check | kubectl Command | Healthy | Warning | Critical |
|-------|-----------------|---------|---------|----------|
| AlertManager pods | `kubectl get pods -l app.kubernetes.io/name=alertmanager` | All Running | Some not Ready | CrashLoopBackOff |
| AlertManager CR | `kubectl get alertmanager.monitoring.coreos.com -A` | Reconciled | Pending | Failed |
| Config valid | Check status.paused | Not paused | - | Paused/Invalid |

### ServiceMonitor Checks

| Check | kubectl Command | Healthy | Warning | Critical |
|-------|-----------------|---------|---------|----------|
| ServiceMonitors | `kubectl get servicemonitors.monitoring.coreos.com -A` | All present | Some misconfigured | None discovered |
| Target count | Query Prometheus API | Targets found | Some down | All down |

### PrometheusRule Checks

| Check | kubectl Command | Healthy | Warning | Critical |
|-------|-----------------|---------|---------|----------|
| Rules status | `kubectl get prometheusrules.monitoring.coreos.com -A` | All loaded | Some errors | All failed |
| Rule evaluation | Query Prometheus API | Evaluating | Some failing | All failing |

### Operator Checks

| Check | kubectl Command | Healthy | Warning | Critical |
|-------|-----------------|---------|---------|----------|
| Operator pod | `kubectl get pods -n monitoring -l app.kubernetes.io/name=prometheus-operator` | Running | Restarting | CrashLoopBackOff |

---

## Common Patterns

### Condition Checking

Most Kubernetes resources use standard conditions:

```bash
# Get all conditions for a resource
kubectl get <resource> -o jsonpath='{.items[*].status.conditions}'

# Check specific condition
kubectl get <resource> -o jsonpath='{.items[?(@.status.conditions[?(@.type=="Ready")].status=="True")].metadata.name}'
```

### Age/Freshness Checking

```bash
# Get last transition time
kubectl get <resource> -o jsonpath='{.items[*].status.conditions[*].lastTransitionTime}'

# Compare against current time in script
```

### Error Detection

```bash
# Get events for errors
kubectl get events --field-selector type=Warning -A

# Get pod logs for errors
kubectl logs -l app=<label> --tail=100 | grep -i error
```
