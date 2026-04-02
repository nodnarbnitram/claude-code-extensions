# kubectl Cheatsheet

Condensed from [official quick reference](https://kubernetes.io/docs/reference/kubectl/quick-reference/).

## Context & Config

```bash
kubectl config current-context          # Show current context
kubectl config get-contexts             # List all contexts
kubectl config use-context <name>       # Switch context
kubectl config set-context --current --namespace=<ns>  # Set default namespace
```

## Get Resources

```bash
kubectl get <resource> -n <ns>          # List resources
kubectl get <resource> -o wide          # More columns
kubectl get <resource> -o yaml          # YAML output
kubectl get <resource> -o json          # JSON output
kubectl get <resource> --show-labels    # Show labels
kubectl get <resource> -l key=value     # Filter by label
kubectl get <resource> --all-namespaces # All namespaces
```

## Describe & Logs

```bash
kubectl describe <resource> <name> -n <ns>  # Detailed info
kubectl logs <pod> -n <ns>                  # Pod logs
kubectl logs <pod> -c <container>           # Specific container
kubectl logs <pod> --tail=100               # Last 100 lines
kubectl logs <pod> -f                       # Follow logs
kubectl logs <pod> --previous               # Previous container
kubectl logs <pod> --timestamps             # With timestamps
```

## Create & Apply

```bash
kubectl create -f <file.yaml>           # Create from file
kubectl apply -f <file.yaml>            # Apply (create or update)
kubectl apply -f <dir>/                 # Apply all in directory
kubectl apply -k <dir>/                 # Apply with kustomize
kubectl create configmap <name> --from-file=<path>
kubectl create secret generic <name> --from-literal=key=value
```

## Edit & Patch

```bash
kubectl edit <resource> <name> -n <ns>  # Edit in editor
kubectl patch <resource> <name> -p '{"spec":{"replicas":3}}'
kubectl set image deployment/<name> <container>=<image>
```

## Delete

```bash
kubectl delete <resource> <name> -n <ns>
kubectl delete -f <file.yaml>
kubectl delete <resource> --all -n <ns>
kubectl delete pod <name> --force --grace-period=0  # Force delete
```

## Exec & Debug

```bash
kubectl exec -it <pod> -- /bin/sh           # Shell into pod
kubectl exec -it <pod> -c <container> -- /bin/sh  # Specific container
kubectl run debug --rm -it --image=busybox -- /bin/sh  # Debug pod
kubectl cp <pod>:<path> <local-path>        # Copy from pod
kubectl cp <local-path> <pod>:<path>        # Copy to pod
```

## Port Forward

```bash
kubectl port-forward <pod> 8080:80          # Pod
kubectl port-forward svc/<name> 8080:80     # Service
kubectl port-forward deploy/<name> 8080:80  # Deployment
```

## Scaling & Rollouts

```bash
kubectl scale deployment <name> --replicas=3
kubectl autoscale deployment <name> --min=2 --max=10 --cpu-percent=80
kubectl rollout status deployment/<name>
kubectl rollout history deployment/<name>
kubectl rollout undo deployment/<name>
kubectl rollout restart deployment/<name>
```

## Labels & Annotations

```bash
kubectl label <resource> <name> key=value
kubectl label <resource> <name> key-           # Remove label
kubectl annotate <resource> <name> key=value
```

## Resource Usage

```bash
kubectl top nodes
kubectl top pods -n <ns>
kubectl top pods --sort-by=memory
kubectl top pods --sort-by=cpu
```

## Events

```bash
kubectl get events -n <ns>
kubectl get events --sort-by='.lastTimestamp'
kubectl get events --field-selector reason=Failed
```

## Auth & RBAC

```bash
kubectl auth whoami
kubectl auth can-i get pods -n <ns>
kubectl auth can-i --list -n <ns>
kubectl get roles,rolebindings -n <ns>
kubectl get clusterroles,clusterrolebindings
```

## Dry Run

```bash
kubectl apply -f file.yaml --dry-run=client -o yaml
kubectl create deployment <name> --image=<img> --dry-run=client -o yaml
```
