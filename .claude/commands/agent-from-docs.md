---
description: Create a specialized agent by analyzing documentation URLs
argument-hint: <doc-url> [additional-urls...]
---

# Create Agent from Documentation

You will create a new specialized agent by analyzing documentation from the provided URLs.

**Documentation URLs**: $ARGUMENTS

## Your Task

Follow these steps to create the agent:

### Step 1: Analyze Documentation

If multiple URLs are provided, launch **multiple technical-researcher agents in parallel** (one per URL). If only one URL is provided, use a single researcher.

For parallel execution with multiple URLs:
- Launch all technical-researcher agents simultaneously in a single message with multiple Task tool calls
- Each agent should analyze its assigned URL independently
- Combine all research findings before proceeding to Step 2

Each researcher should investigate:
- What technology/framework/library is being documented
- Key concepts, APIs, methods, and patterns
- Best practices and conventions
- Common workflows and use cases
- Important implementation details that an expert should know
- How this technology differs from alternatives

Request a comprehensive summary suitable for creating a specialized agent.

### Step 1.5: Determine Agent Creation Strategy

After gathering all research findings, analyze whether to create one or multiple agents:

**Create MULTIPLE agents when URLs represent distinct verticals/technologies:**
- Different core APIs or services (e.g., Cloudflare Workers vs D1 vs R2)
- Separate deployment models or runtime environments
- Distinct problem domains within a platform
- Independent tools/products that happen to share a brand

**Create a SINGLE agent when URLs cover the same technology:**
- Different aspects of one framework (e.g., Next.js routing + data fetching + deployment)
- Progressive documentation depth on one topic
- Multiple guides for the same library/tool

**Examples:**
- ✅ Multiple agents: `workers.cloudflare.com/docs` + `developers.cloudflare.com/d1` + `developers.cloudflare.com/r2` → 3 specialized agents
- ❌ Single agent: `nextjs.org/docs/routing` + `nextjs.org/docs/api-routes` + `nextjs.org/docs/deployment` → 1 comprehensive agent

Based on this analysis, proceed to either Step 2A (single agent) or Step 2B (multiple agents).

### Step 2A: Generate Single Consolidated Agent

**Use when:** All URLs document the same technology/framework.

Use the **meta-agent** to create one specialized agent based on all research findings.

Provide the meta-agent with:
- Complete research findings from all URLs
- Instruction to create an agent that specializes in this technology
- Request to include "MUST BE USED" or "use PROACTIVELY" in the description
- Guidance on appropriate tool restrictions for this domain
- Request to incorporate patterns and examples from the documentation

The meta-agent should write the agent file to `.claude/agents/specialized/<appropriate-category>/` with a descriptive filename.

### Step 2B: Generate Multiple Specialized Agents

**Use when:** URLs represent distinct verticals/technologies within a platform.

For each identified vertical/technology, use the **meta-agent** to create a separate specialized agent.

**You can launch multiple meta-agent tasks in parallel** (one per vertical) by including multiple Task tool calls in a single message.

For each meta-agent invocation, provide:
- Research findings specific to that vertical's URL(s)
- Instruction to create an agent specializing in that specific vertical
- Request to include "MUST BE USED" or "use PROACTIVELY" in the description
- Guidance on appropriate tool restrictions for this domain
- Request to incorporate patterns and examples from that vertical's documentation
- Clear scope boundaries (what this agent handles vs other related agents)

Each meta-agent should write its agent file to `.claude/agents/specialized/<appropriate-category>/` with a descriptive filename that identifies the specific vertical (e.g., `cloudflare-workers-expert.md`, `cloudflare-d1-expert.md`).

### Step 3: Report Results

**For single agent (Step 2A):**
Provide a summary including:
- Key findings from the documentation analysis
- Path to the newly created agent file
- Agent name and description
- When and how this agent should be used
- Suggested test scenarios to validate the agent

**For multiple agents (Step 2B):**
Provide a summary including:
- Overview of how the platform was divided into verticals
- For each created agent:
  - Path to the agent file
  - Agent name and description
  - What vertical/technology it covers
  - When and how it should be used
- Suggested test scenarios that would trigger each agent
- Explanation of how the agents complement each other