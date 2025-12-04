---
description: Create a specialized agent with specific intent by analyzing documentation URLs
argument-hint: "<intent>" <doc-url> [additional-urls...]
---

# Create Agent from Documentation with Intent

You will create a new specialized agent by analyzing documentation from the provided URLs, guided by a specific intent or purpose.

**Arguments**: $ARGUMENTS

**Important**: The first argument is the **intent/description** of what the agent should do. All remaining arguments are **documentation URLs** to analyze.

## Your Task

Follow these steps to create the agent:

### Step 1: Parse Arguments

Extract from $ARGUMENTS:
- **Intent**: The first argument (everything in quotes or up to the first URL)
- **Documentation URLs**: All remaining arguments

The intent describes the specific purpose or use case for this agent (e.g., "Create a migration assistant agent from incident.io and opsgenie to betterstack").

### Step 2: Analyze Documentation

If multiple URLs are provided, launch **multiple technical-researcher agents in parallel** (one per URL). If only one URL is provided, use a single researcher.

For parallel execution with multiple URLs:
- Launch all technical-researcher agents simultaneously in a single message with multiple Task tool calls
- Each agent should analyze its assigned URL independently
- Combine all research findings before proceeding to Step 3

Each researcher should investigate with the **intent in mind**:
- What technology/framework/library is being documented
- Key concepts, APIs, methods, and patterns **relevant to the stated intent**
- Best practices and conventions
- Common workflows and use cases **that align with the intent**
- Important implementation details that an expert should know
- Migration paths, comparison features, or integration points **if relevant to the intent**
- How this technology differs from alternatives

Request a comprehensive summary suitable for creating a specialized agent focused on the stated intent.

### Step 3: Determine Agent Creation Strategy

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
- **When the intent requires unified knowledge across all URLs** (e.g., migration agents need to understand both source and destination)

**Examples:**
- ✅ Single agent: Intent="migration from X to Y" + docs for X + docs for Y → 1 migration specialist
- ✅ Multiple agents: `workers.cloudflare.com/docs` + `developers.cloudflare.com/d1` + `developers.cloudflare.com/r2` → 3 specialized agents
- ❌ Single agent: `nextjs.org/docs/routing` + `nextjs.org/docs/api-routes` + `nextjs.org/docs/deployment` → 1 comprehensive agent

Based on this analysis and the **stated intent**, proceed to either Step 4A (single agent) or Step 4B (multiple agents).

### Step 4A: Generate Single Consolidated Agent

**Use when:** All URLs document the same technology/framework OR the intent requires unified knowledge across all URLs (like migration, integration, or comparison tasks).

Use the **meta-agent** to create one specialized agent based on all research findings.

Provide the meta-agent with:
- The **stated intent** as the primary goal of this agent
- Complete research findings from all URLs
- Instruction to create an agent that specializes in fulfilling the stated intent
- Request to include \"MUST BE USED\" or \"use PROACTIVELY\" in the description, with clear triggers based on the intent
- Guidance on appropriate tool restrictions for this domain
- Request to incorporate patterns and examples from the documentation
- Emphasis on how the agent should leverage knowledge from all sources to fulfill the intent

The meta-agent should write the agent file to `.claude/agents/specialized/<appropriate-category>/` with a descriptive filename that reflects the intent.

### Step 4B: Generate Multiple Specialized Agents

**Use when:** URLs represent distinct verticals/technologies within a platform AND the intent doesn't require unified knowledge across them.

For each identified vertical/technology, use the **meta-agent** to create a separate specialized agent.

**You can launch multiple meta-agent tasks in parallel** (one per vertical) by including multiple Task tool calls in a single message.

For each meta-agent invocation, provide:
- How the **stated intent** relates to this specific vertical
- Research findings specific to that vertical's URL(s)
- Instruction to create an agent specializing in that specific vertical while supporting the overall intent
- Request to include \"MUST BE USED\" or \"use PROACTIVELY\" in the description
- Guidance on appropriate tool restrictions for this domain
- Request to incorporate patterns and examples from that vertical's documentation
- Clear scope boundaries (what this agent handles vs other related agents)

Each meta-agent should write its agent file to `.claude/agents/specialized/<appropriate-category>/` with a descriptive filename that identifies the specific vertical.

### Step 5: Report Results

**For single agent (Step 4A):**
Provide a summary including:
- The stated intent and how the agent fulfills it
- Key findings from the documentation analysis
- Path to the newly created agent file
- Agent name and description
- When and how this agent should be used (with specific triggers based on the intent)
- Suggested test scenarios to validate the agent against the stated intent

**For multiple agents (Step 4B):**
Provide a summary including:
- The stated intent and how the agent ecosystem fulfills it
- Overview of how the platform was divided into verticals
- For each created agent:
  - Path to the agent file
  - Agent name and description
  - What vertical/technology it covers
  - How it supports the overall intent
  - When and how it should be used
- Suggested test scenarios that would trigger each agent
- Explanation of how the agents complement each other to fulfill the stated intent
