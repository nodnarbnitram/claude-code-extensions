# JSONPath Patterns for kubectl

Reference for [kubectl JSONPath support](https://kubernetes.io/docs/reference/kubectl/jsonpath/).

## Basic Syntax

```bash
kubectl get <resource> -o jsonpath='{.field.subfield}'
```

## Common Patterns

### Pod Status

```bash
# Pod phase
kubectl get pod <name> -o jsonpath='{.status.phase}'

# Container status
kubectl get pod <name> -o jsonpath='{.status.containerStatuses[0].state}'

# Restart count
kubectl get pod <name> -o jsonpath='{.status.containerStatuses[0].restartCount}'

# Pod IP
kubectl get pod <name> -o jsonpath='{.status.podIP}'

# Node name
kubectl get pod <name> -o jsonpath='{.spec.nodeName}'
```

### Multiple Values

```bash
# Name and status for all pods
kubectl get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.phase}{"\n"}{end}'

# With custom separator
kubectl get pods -o jsonpath='{range .items[*]}{.metadata.name}|{.status.phase}\n{end}'
```

### Filtering

```bash
# Pods with specific label
kubectl get pods -o jsonpath='{.items[?(@.metadata.labels.app=="nginx")].metadata.name}'

# Ready nodes only
kubectl get nodes -o jsonpath='{.items[?(@.status.conditions[?(@.type=="Ready")].status=="True")].metadata.name}'

# Non-running pods
kubectl get pods -o jsonpath='{.items[?(@.status.phase!="Running")].metadata.name}'
```

### Node Information

```bash
# Node capacity
kubectl get nodes -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.capacity.cpu}{"\t"}{.status.capacity.memory}{"\n"}{end}'

# Node conditions
kubectl get nodes -o jsonpath='{.items[*].status.conditions[?(@.type=="Ready")].status}'

# Allocatable resources
kubectl get node <name> -o jsonpath='{.status.allocatable}'
```

### Service & Endpoints

```bash
# Service ClusterIP
kubectl get svc <name> -o jsonpath='{.spec.clusterIP}'

# Service ports
kubectl get svc <name> -o jsonpath='{.spec.ports[*].port}'

# Endpoint addresses
kubectl get endpoints <name> -o jsonpath='{.subsets[*].addresses[*].ip}'
```

### ConfigMaps & Secrets

```bash
# ConfigMap data keys
kubectl get configmap <name> -o jsonpath='{.data}' | jq 'keys'

# Specific ConfigMap value
kubectl get configmap <name> -o jsonpath='{.data.key-name}'

# Secret keys (not values)
kubectl get secret <name> -o jsonpath='{.data}' | jq 'keys'

# Decode secret value
kubectl get secret <name> -o jsonpath='{.data.password}' | base64 -d
```

### Deployments

```bash
# Replica count
kubectl get deployment <name> -o jsonpath='{.spec.replicas}'

# Ready replicas
kubectl get deployment <name> -o jsonpath='{.status.readyReplicas}'

# Container images
kubectl get deployment <name> -o jsonpath='{.spec.template.spec.containers[*].image}'

# Deployment conditions
kubectl get deployment <name> -o jsonpath='{.status.conditions[?(@.type=="Available")].status}'
```

### Events

```bash
# Recent event messages
kubectl get events -o jsonpath='{range .items[*]}{.reason}: {.message}{"\n"}{end}'

# Events for specific object
kubectl get events --field-selector involvedObject.name=<pod> -o jsonpath='{range .items[*]}{.reason}: {.message}{"\n"}{end}'
```

## Output Formatting

### Custom Columns

```bash
kubectl get pods -o custom-columns=NAME:.metadata.name,STATUS:.status.phase,IP:.status.podIP
```

### Sorted Output

```bash
# Sort by creation time
kubectl get pods --sort-by='.metadata.creationTimestamp'

# Sort by restart count
kubectl get pods --sort-by='.status.containerStatuses[0].restartCount'
```

## Tips

1. **Test incrementally**: Start with `'{.metadata}'` then drill down
2. **Use jq for complex parsing**: Pipe JSON output to jq
3. **Escape special characters**: Use `\"` inside jsonpath strings
4. **Range for iteration**: `{range .items[*]}...{end}` for lists
5. **Filters use ?(@)**: `{.items[?(@.field=="value")]}`
