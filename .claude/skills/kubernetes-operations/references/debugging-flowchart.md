# Kubernetes Debugging Flowchart

Decision tree for common pod issues.

## Pod Not Starting

```
Pod Status?
├── Pending
│   ├── Check: kubectl describe pod <name>
│   ├── Look for: "Events" section
│   └── Common causes:
│       ├── Insufficient resources → Check node capacity, adjust requests/limits
│       ├── No matching nodes → Check nodeSelector, affinity, tolerations
│       ├── PVC not bound → Check PVC status and StorageClass
│       └── Image pull issues → Check imagePullSecrets
│
├── ContainerCreating
│   ├── Check: kubectl describe pod <name>
│   └── Common causes:
│       ├── Image pull error → Verify image name and registry auth
│       ├── ConfigMap/Secret missing → Verify referenced resources exist
│       └── Volume mount issues → Check PVC and volume configuration
│
├── CrashLoopBackOff
│   ├── Check: kubectl logs <name> --previous
│   ├── Check: kubectl describe pod <name> (exit code)
│   └── Common causes:
│       ├── Exit code 1 → Application error, check logs
│       ├── Exit code 137 → OOMKilled, increase memory limit
│       ├── Exit code 143 → SIGTERM, check liveness probe
│       └── Missing config → Check env vars and mounts
│
├── ImagePullBackOff
│   ├── Check: kubectl describe pod <name>
│   └── Common causes:
│       ├── Image not found → Verify image:tag exists
│       ├── Auth error → Check imagePullSecrets
│       └── Network error → Check registry connectivity
│
└── Running but not working
    ├── Check: kubectl logs <name>
    ├── Check: kubectl exec -it <name> -- /bin/sh
    └── Common causes:
        ├── Readiness probe failing → Check probe config and endpoint
        ├── Wrong command/args → Verify entrypoint
        └── Missing dependencies → Check service connectivity
```

## Service Not Accessible

```
Can't reach service?
│
├── Check service exists
│   kubectl get svc <name> -n <ns>
│
├── Check endpoints
│   kubectl get endpoints <name> -n <ns>
│   └── Empty? → Pod labels don't match service selector
│
├── Check pod labels match selector
│   kubectl get svc <name> -o jsonpath='{.spec.selector}'
│   kubectl get pods -l <selector> -n <ns>
│
├── Test from within cluster
│   kubectl run debug --rm -it --image=busybox -- wget -qO- http://<svc>:<port>
│
└── Check NetworkPolicy
    kubectl get networkpolicy -n <ns>
    └── Blocking traffic? → Update policy or test without it
```

## High Resource Usage

```
Resource issues?
│
├── Check current usage
│   kubectl top pods -n <ns>
│   kubectl top nodes
│
├── OOMKilled containers
│   ├── Check: kubectl describe pod <name> (look for OOMKilled)
│   ├── Solution: Increase memory limits
│   └── Investigate: Profile application memory usage
│
├── CPU throttling
│   ├── Check: kubectl describe pod <name> (look for CPU limits)
│   └── Solution: Increase CPU limits or optimize application
│
└── Node pressure
    ├── Check: kubectl describe node <name>
    ├── Look for: MemoryPressure, DiskPressure, PIDPressure
    └── Solution: Add nodes, evict pods, or clean up disk
```

## Quick Diagnosis Commands

```bash
# 1. Get overview
kubectl get pods -n <ns> -o wide

# 2. Check specific pod
kubectl describe pod <name> -n <ns>

# 3. Get logs
kubectl logs <name> -n <ns> --tail=100

# 4. Get previous logs (if restarting)
kubectl logs <name> -n <ns> --previous

# 5. Check events
kubectl get events -n <ns> --sort-by='.lastTimestamp' | tail -20

# 6. Shell into pod
kubectl exec -it <name> -n <ns> -- /bin/sh

# 7. Check resource usage
kubectl top pod <name> -n <ns>
```

## Exit Code Reference

| Code | Signal | Meaning |
|------|--------|---------|
| 0 | - | Success |
| 1 | - | General error |
| 126 | - | Command not executable |
| 127 | - | Command not found |
| 128+n | Signal n | Killed by signal |
| 137 | SIGKILL (9) | OOMKilled or force killed |
| 143 | SIGTERM (15) | Graceful termination |
| 255 | - | Exit status out of range |
