# CCE Cloudflare Plugin

Cloudflare Workers, AI, Workflows, and VPC services development for Claude Code.

## Overview

The **cce-cloudflare** plugin provides expert Cloudflare development capabilities across Workers, Workers AI, Workflows, Workers for Platforms, and VPC services. Build edge-first applications with intelligent assistance for the entire Cloudflare Developer Platform.

## Features

- **Cloudflare Workers**: V8 isolate development, runtime APIs, storage selection (KV/D1/R2/Durable Objects)
- **Workers AI**: 50+ models, streaming, RAG, AI Gateway, Vectorize integration
- **Workflows**: Durable execution, Python DAG workflows, step APIs, retry logic
- **Workers for Platforms**: Multi-tenant architectures, dispatch namespaces, dynamic routing
- **VPC Services**: Private API access to AWS/Azure/GCP via cloudflared tunnels

## Plugin Components

### Agents (5)

- **cloudflare-workers-expert**: Core Workers development (runtime, wrangler, storage)
- **cloudflare-workers-ai-expert**: Workers AI models, RAG, streaming, function calling
- **cloudflare-workflows-expert**: Durable workflow orchestration and debugging
- **cloudflare-workers-for-platforms-expert**: Multi-tenant platform infrastructure
- **cloudflare-ai-agents-sdk-expert**: AI Agents SDK for autonomous edge agents

### Skills (1)

- **cloudflare-vpc-services**: Diagnose and create VPC Services for private network access

## Installation

### From Marketplace (Recommended)

```bash
# Add the CCE marketplace
/plugin marketplace add github:nodnarbnitram/claude-code-extensions

# Install Cloudflare plugin
/plugin install cce-cloudflare@cce-marketplace
```

### From Local Source

```bash
git clone https://github.com/nodnarbnitram/claude-code-extensions.git
/plugin marketplace add /path/to/claude-code-extensions
/plugin install cce-cloudflare@cce-marketplace
```

## Usage

### Agents (Automatic Activation)

```bash
> Create a Cloudflare Worker with KV storage
# Uses cloudflare-workers-expert

> Add Workers AI text generation with streaming
# Uses cloudflare-workers-ai-expert

> Implement a durable workflow for order processing
# Uses cloudflare-workflows-expert

> Set up multi-tenant Worker deployment platform
# Uses cloudflare-workers-for-platforms-expert

> Diagnose VPC service dns_error for AWS RDS
# Uses cloudflare-vpc-services skill
```

### Example Workflows

**Building a RAG Application:**
```bash
> Build a RAG application using Workers AI with Vectorize storage
# Agent will use @cf/baai/bge-base-en-v1.5 embeddings + Vectorize
```

**Multi-Tenant Platform:**
```bash
> Create a dispatch namespace for user-deployed Workers
# Sets up Workers for Platforms infrastructure
```

**Private API Access:**
```bash
> Connect my Worker to private RDS database in AWS VPC
# Uses VPC Services skill to configure cloudflared tunnel
```

## Requirements

- **Claude Code**: Latest version
- **Node.js**: 18+ (for wrangler)
- **Cloudflare Account**: With Workers enabled
- **wrangler**: Cloudflare CLI (installed via `npm install -g wrangler`)

## Key Capabilities

- **Edge-First Architecture**: V8 isolates, zero cold starts, global distribution
- **Storage Expertise**: KV, D1, R2, Durable Objects, Vectorize, Hyperdrive
- **AI Integration**: 50+ models, streaming, RAG patterns, AI Gateway
- **Workflow Orchestration**: Durable execution, automatic retries, Python DAGs
- **Platform Development**: Multi-tenancy, dynamic routing, custom limits
- **Private Networking**: VPC Services for AWS/Azure/GCP integration

## License

MIT License - see [LICENSE](../../../LICENSE) for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/nodnarbnitram/claude-code-extensions/issues)
- **Documentation**: [Repository README](../../../README.md)
- **Cloudflare Docs**: [developers.cloudflare.com](https://developers.cloudflare.com)
