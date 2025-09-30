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

### Step 2: Generate the Agent

Use the **meta-agent** to create a new specialized agent based on the research findings.

Provide the meta-agent with:
- Complete research findings from Step 1
- Instruction to create an agent that specializes in this technology
- Request to include "MUST BE USED" or "use PROACTIVELY" in the description
- Guidance on appropriate tool restrictions for this domain
- Request to incorporate patterns and examples from the documentation

The meta-agent should write the agent file to `.claude/agents/specialized/<appropriate-category>/` with a descriptive filename.

### Step 3: Report Results

Provide a summary including:
- Key findings from the documentation analysis
- Path to the newly created agent file
- Agent name and description
- When and how this agent should be used
- Suggested test scenarios to validate the agent