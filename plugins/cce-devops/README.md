# cce-devops

**DevOps Tooling for CI/CD and Infrastructure Management**

Complete DevOps agent suite providing expert guidance for GitHub Actions CI/CD, Helm chart development, ArgoCD GitOps, and Crossplane infrastructure-as-code.

## Overview

The `cce-devops` plugin provides specialized agents for:

- **GitHub Actions CI/CD**: Workflow development, debugging, optimization, security, and custom action creation
- **Helm Charts**: Template development, Go templating, Sprig functions, and chart best practices
- **ArgoCD GitOps**: Installation, security hardening, multi-tenancy, scaling, and operational troubleshooting
- **Crossplane**: Infrastructure provisioning, composition development, AWS resources, and upgrade management

## Agents Included

### GitHub Actions Expert
**Agent:** `github-actions-expert`
**Trigger:** Use when working with `.github/workflows/`, action.yml files, or CI/CD pipeline development

**Capabilities:**
- Workflow YAML development with security best practices
- OIDC authentication for cloud deployments (AWS, Azure, GCP)
- Performance optimization (caching, matrix builds, concurrency)
- Custom action creation (composite, JavaScript, Docker)
- Debugging with diagnostic commands and error analysis
- Migration from other CI/CD platforms

### Helm Template Master
**Agent:** `helm-template-master`
**Trigger:** Use for Helm chart template development, debugging template issues, or working with Go templating

**Capabilities:**
- Go template language and Helm built-in objects
- Sprig function library (70+ functions)
- Helper template patterns (_helpers.tpl)
- Advanced patterns (checksum annotations, secret preservation, conditional resources)
- Template validation and debugging
- values.yaml structure design

### ArgoCD Experts
**Agents:**
- `argocd-operator-expert` - Infrastructure and operational management
- `argocd-developer-expert` - Application deployment patterns
- `argocd-user-expert` - End-user workflows and troubleshooting
- `helm-argocd-applicationset-expert` - ApplicationSet patterns and Helm integration

**Capabilities:**
- Installation and high availability setup
- SSO/OIDC and RBAC configuration
- Multi-tenancy with AppProject isolation
- Sharding and performance tuning
- Backup/disaster recovery procedures
- Application deployment strategies
- Progressive rollouts and sync waves
- Monitoring and troubleshooting

### Crossplane Experts
**Agents:**
- `crossplane-upgrade-agent` - Version upgrades and migration guidance
- `crossplane-aws-rds-expert` - AWS RDS provisioning with Crossplane

**Capabilities:**
- Crossplane installation and configuration
- Composition and XRD development
- Provider configuration (AWS, Azure, GCP)
- Infrastructure resource management
- Version upgrade planning and execution
- AWS RDS database provisioning patterns

## Installation

### Via Plugin System (Recommended)

```bash
# Add marketplace (if not already added)
/plugin marketplace add https://github.com/nodnarbnitram/claude-code-extensions

# Install the plugin
/plugin install cce-devops@cce-marketplace

# Verify installation
/agents  # Should show DevOps agents
```

### Standalone Installation

```bash
# Clone repository
git clone https://github.com/nodnarbnitram/claude-code-extensions.git

# Copy agents to your project or user directory
cp -r claude-code-extensions/.claude/agents/specialized/devops ~/.claude/agents/specialized/
cp -r claude-code-extensions/.claude/agents/specialized/helm ~/.claude/agents/specialized/
cp -r claude-code-extensions/.claude/agents/specialized/argocd ~/.claude/agents/specialized/
cp -r claude-code-extensions/.claude/agents/specialized/crossplane ~/.claude/agents/specialized/
```

## Usage Examples

### GitHub Actions Workflow Development

```
> Create a GitHub Actions workflow for a Node.js app with:
> - Test on multiple Node versions (18, 20, 22)
> - Docker build and push to GHCR
> - AWS deployment using OIDC
> - Proper caching and security practices
```

The `github-actions-expert` agent will create a production-ready workflow with security best practices, performance optimizations, and comprehensive error handling.

### Helm Chart Creation

```
> Create a Helm chart for a FastAPI application with:
> - Deployment with health checks
> - Service and Ingress
> - ConfigMap with checksum-triggered restarts
> - HPA for autoscaling
> - Proper value structure and helpers
```

The `helm-template-master` agent will generate complete templates with Go templating best practices, Sprig functions, and proper indentation handling.

### ArgoCD Setup and Configuration

```
> Set up ArgoCD in HA mode with:
> - 3 replicas for argocd-server
> - Controller sharding for 500+ applications
> - OIDC integration with Okta
> - Multi-tenancy for dev, staging, prod teams
```

The `argocd-operator-expert` agent will provide production-ready configurations with security hardening, RBAC policies, and monitoring setup.

### Crossplane Infrastructure

```
> Create a Crossplane composition for an AWS RDS PostgreSQL database with:
> - VPC and subnet configuration
> - Security group rules
> - Automated backups
> - Multi-AZ deployment
```

The `crossplane-aws-rds-expert` agent will generate compositions, XRDs, and claims with AWS best practices.

## When Agents Activate

All agents in this plugin use **proactive delegation**. They activate automatically when:

- Working with files in `.github/workflows/` (GitHub Actions)
- Editing Helm templates or working with `values.yaml` (Helm)
- Configuring ArgoCD applications, projects, or manifests (ArgoCD)
- Creating Crossplane compositions, XRDs, or claims (Crossplane)
- User explicitly mentions the technology ("create a GitHub Actions workflow", "debug Helm template", etc.)

## Agent Capabilities Matrix

| Agent | CI/CD | Templating | GitOps | IaC | Security | Troubleshooting |
|-------|-------|------------|--------|-----|----------|-----------------|
| github-actions-expert | ✓ | - | - | - | ✓ | ✓ |
| helm-template-master | - | ✓ | - | - | - | ✓ |
| argocd-operator-expert | - | - | ✓ | - | ✓ | ✓ |
| argocd-developer-expert | - | - | ✓ | - | - | ✓ |
| argocd-user-expert | - | - | ✓ | - | - | ✓ |
| helm-argocd-applicationset-expert | - | ✓ | ✓ | - | - | - |
| crossplane-upgrade-agent | - | - | - | ✓ | - | ✓ |
| crossplane-aws-rds-expert | - | - | - | ✓ | ✓ | - |

## Security Features

### GitHub Actions
- Minimal GITHUB_TOKEN permissions
- Script injection prevention patterns
- OIDC authentication (no long-lived credentials)
- Action pinning to commit SHAs
- Safe event trigger selection

### ArgoCD
- SSO/OIDC integration
- Granular RBAC policies
- AppProject-based multi-tenancy
- TLS for all connections
- External secrets management integration

### Crossplane
- Provider credential management
- RBAC for resource creation
- Composition-level security policies
- Secret store integration

## Performance Optimizations

### GitHub Actions
- Dependency caching strategies
- Matrix builds for parallelization
- Concurrency groups for cancellation
- Conditional execution to skip unnecessary work

### ArgoCD
- Controller sharding (consistent-hashing algorithm)
- Repo server parallelization
- Status/operation processor tuning
- Redis compression

### Helm
- Template optimization patterns
- Efficient value lookups
- Minimal resource generation

## Troubleshooting

### Common Issues

**GitHub Actions:**
- Permission denied → Check GITHUB_TOKEN scopes
- Cache not working → Verify cache key includes lock file hash
- Slow workflows → Enable caching, use matrix builds

**Helm:**
- Indentation errors → Use `nindent` instead of `indent`
- Scope loss in range → Use `$` to preserve root context
- Type conversion errors → Always quote environment variable values

**ArgoCD:**
- Sync failures → Check RBAC permissions and AppProject restrictions
- Performance issues → Enable controller sharding and increase status processors
- Git connection issues → Validate credentials and repository access

**Crossplane:**
- Resource not creating → Check provider credentials and RBAC
- Composition not rendering → Validate XRD and composition syntax
- Provider upgrade issues → Follow version-specific upgrade paths

### Getting Help

Each agent provides:
- Structured troubleshooting guides
- Common error patterns and solutions
- Diagnostic commands for debugging
- Validation procedures

Simply describe the issue and the relevant agent will guide you through resolution.

## Technology Versions

**Supported as of January 2025:**
- GitHub Actions: Node 20 runtime, actions/* v4
- Helm: v3.12+
- ArgoCD: v3.1+ (Kubernetes v1.30-v1.33)
- Crossplane: v1.14+

## Contributing

See the main [CONTRIBUTING.md](https://github.com/nodnarbnitram/claude-code-extensions/blob/main/CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](https://github.com/nodnarbnitram/claude-code-extensions/blob/main/LICENSE)

## Related Plugins

- **cce-kubernetes**: Kubernetes cluster operations and health diagnostics
- **cce-cloudflare**: Cloudflare Workers and VPC services
- **cce-core**: Essential hooks, commands, and universal tools

## Support

For issues, questions, or feature requests:
- GitHub Issues: https://github.com/nodnarbnitram/claude-code-extensions/issues
- Documentation: https://github.com/nodnarbnitram/claude-code-extensions
