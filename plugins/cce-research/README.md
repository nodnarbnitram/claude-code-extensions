# CCE Research Plugin

**Deep research coordination: academic papers, technical analysis, data insights, and web intelligence**

## Overview

The CCE Research plugin provides a comprehensive suite of specialized research agents that work in coordinated teams to conduct thorough, multi-faceted investigations. Whether you need academic literature reviews, current web intelligence, technical code analysis, or quantitative data insights, this plugin orchestrates expert researchers to deliver comprehensive findings.

## Key Features

- **Coordinated Research Team**: Strategic orchestration across multiple specialist researchers
- **Multi-Source Intelligence**: Academic papers, web content, code repositories, and statistical data
- **Temporal Awareness**: All agents track dates and prioritize recent, relevant information
- **Structured Output**: JSON-formatted findings with citations, confidence levels, and quality assessments
- **Private Repository Access**: Technical researcher can analyze both public and private GitHub repositories

## Agents Included

### 1. Research Coordinator (`research-coordinator`)

**The strategic orchestrator for complex research tasks**

- Analyzes research requirements and allocates tasks to specialists
- Defines iteration strategies (1-3 rounds) based on complexity
- Sets quality thresholds and success criteria
- Plans integration of diverse findings
- Outputs comprehensive JSON execution plans

**Use when**: You have a complex research question requiring multiple perspectives or deep investigation.

**Capabilities**:
- Strategic task allocation based on specialist strengths
- Iteration planning for comprehensive coverage
- Quality assurance and success criteria definition
- Integration planning for multi-researcher findings

### 2. Academic Researcher (`academic-researcher`)

**Specialist for scholarly sources and peer-reviewed literature**

- Searches academic databases (ArXiv, PubMed, Google Scholar)
- Evaluates peer-reviewed papers and research quality
- Analyzes citations and bibliometric data
- Identifies research gaps and future directions
- Extracts research methodologies and limitations

**Use proactively for**:
- Research paper analysis
- Literature reviews
- Citation tracking
- Academic methodology evaluation

**Output includes**:
- Key findings with confidence levels
- Research methodology analysis
- Citation networks and seminal works
- Quality indicators (journal impact, peer review status)
- Properly formatted academic citations

### 3. Web Researcher (`web-researcher`)

**Expert in current news, industry reports, and real-time web intelligence**

- Gathers breaking news and current events
- Analyzes industry reports and market trends
- Tracks company announcements and press releases
- Monitors public sentiment and social discussions
- Evaluates regulatory updates and policy changes

**Use proactively for**:
- Current news and industry reports
- Real-time information gathering
- Market trends and competitive intelligence
- Breaking developments and announcements

**Output includes**:
- Executive summary with temporal context
- Key findings with source citations and dates
- Source quality analysis (credibility, publication date)
- Trend identification (current, emerging, long-term)
- Temporal analysis of recent developments
- Information gaps and conflicting sources

### 4. Technical Researcher (`technical-researcher`)

**Specialist in code repositories, technical documentation, and implementation analysis**

- Analyzes GitHub repositories (public and private)
- Reviews API documentation and technical specs
- Evaluates code quality and architecture
- Tracks version histories and breaking changes
- Assesses community adoption and maintenance status

**Use for**:
- Code repository analysis
- Technical documentation review
- Implementation examples and best practices
- Private repository access (using `gh` CLI and `git`)

**Capabilities**:
- **Private repository access**: Uses `gh` CLI for quick file reads, `git clone` for comprehensive analysis
- Architecture and design pattern evaluation
- Security considerations and testing coverage
- Community activity assessment
- Version currency and update frequency tracking

**Output (JSON format)**:
- Repository statistics and metrics
- Code quality assessment
- Technical insights and patterns
- Implementation recommendations
- Community insights and adoption trends
- Temporal analysis (maintenance health, ecosystem maturity)

### 5. Data Analyst (`data-analyst`)

**Quantitative analysis and statistical insights specialist**

- Identifies numerical data from statistical databases
- Performs comprehensive statistical analysis
- Creates meaningful comparisons and benchmarks
- Identifies trends, correlations, and outliers
- Suggests appropriate data visualizations

**Use for**:
- Quantitative analysis
- Statistical insights
- Data-driven research
- Trend analysis and forecasting

**Capabilities**:
- Descriptive statistics and trend analysis
- Comparative benchmarking
- Correlation analysis and outlier detection
- Data quality assessment
- Visualization recommendations

**Output (JSON format)**:
- Key metrics with confidence levels
- Trend analysis with rate of change
- Comparisons with statistical significance
- Data-driven insights and implications
- Visualization suggestions
- Data quality assessment

## Installation

### Via Plugin Manager

```bash
# Add the CCE marketplace (if not already added)
/plugin marketplace add /path/to/claude-code-extensions

# Install the research plugin
/plugin install cce-research@cce-marketplace
```

### Manual Installation

Clone the repository and the agents will be available:

```bash
git clone https://github.com/nodnarbnitram/claude-code-extensions.git
cd claude-code-extensions
```

The agents are in `.claude/agents/deep-research/`.

## Usage

### Command Namespacing

When installed as a plugin, agents appear with the prefix `cce-research:` in the agents list. When used standalone (cloned repository), agents have no prefix.

| Installation Mode | Agent Names |
|-------------------|-------------|
| **Plugin** | `cce-research:research-coordinator`, `cce-research:academic-researcher`, etc. |
| **Standalone** | `research-coordinator`, `academic-researcher`, etc. |

### Example Workflows

#### 1. Complex Research Investigation

```
> I need comprehensive research on quantum computing's impact on cryptography
```

Claude will invoke the **research-coordinator** to:
1. Analyze the complexity and identify knowledge domains
2. Allocate tasks to specialists:
   - **academic-researcher**: Peer-reviewed papers on quantum algorithms
   - **web-researcher**: Current industry developments and announcements
   - **technical-researcher**: Quantum computing frameworks and implementations
   - **data-analyst**: Statistical analysis of algorithm performance
3. Define integration plan for synthesizing findings

#### 2. Academic Literature Review

```
> Review recent papers on transformer architecture optimizations
```

Claude will invoke **academic-researcher** to:
- Search academic databases for recent publications
- Evaluate paper quality and citations
- Extract key methodologies and findings
- Identify research gaps

#### 3. Technology Assessment

```
> Analyze the current state of Rust web frameworks
```

Claude will invoke **technical-researcher** to:
- Search GitHub for popular Rust web frameworks
- Analyze repository statistics and maintenance status
- Review documentation and code quality
- Assess community adoption and trends

#### 4. Market Data Analysis

```
> What are the growth trends in cloud computing spending?
```

Claude will invoke **data-analyst** to:
- Identify authoritative data sources
- Extract statistical data
- Calculate growth rates and trends
- Provide visualization recommendations

#### 5. Current Events Research

```
> What are the latest developments in AI regulation?
```

Claude will invoke **web-researcher** to:
- Search for recent news and announcements
- Track regulatory changes and policy updates
- Analyze source credibility and recency
- Identify emerging trends

## Key Principles

All research agents follow these core principles:

1. **Temporal Awareness**: Always establish current date/time context at the start
2. **Source Quality**: Evaluate credibility, recency, and reliability
3. **Structured Output**: Consistent JSON formatting with citations
4. **Confidence Levels**: Explicit uncertainty acknowledgment
5. **Comprehensive Coverage**: Multi-source validation and cross-referencing
6. **Actionable Insights**: Focus on decision-relevant findings

## Advanced Features

### Private Repository Access

The **technical-researcher** can access private GitHub repositories using:

**GitHub CLI (`gh`)**:
```bash
# View repository details
gh repo view owner/repo

# Read file contents
gh api repos/owner/repo/contents/path/to/file --jq .content | base64 -d

# Search code in private repo
gh search code --repo owner/repo "search term"
```

**Git CLI**:
```bash
# Clone for comprehensive analysis
git clone https://github.com/owner/repo.git
```

### Multi-Iteration Research

The research-coordinator can plan 1-3 iteration rounds:

- **Single pass**: Well-defined, focused topics
- **2 iterations**: Topics requiring initial exploration then deep dive
- **3 iterations**: Complex topics needing discovery, analysis, and synthesis phases

### Integration Strategies

The coordinator plans how findings will be synthesized:

- **Complementary**: Different aspects of the same topic
- **Comparative**: Multiple perspectives on contentious issues
- **Sequential**: Building upon each other's findings
- **Validating**: Cross-checking facts across sources

## Configuration

No additional configuration required. All agents use inherited tools and models from your Claude Code settings.

### Tool Access

Research agents use these tools:
- `Read`, `Write`, `Edit`: File operations for storing findings
- `WebSearch`, `WebFetch`: Web and academic search capabilities
- `Bash`: Running `date` for temporal context, `gh`/`git` for repository access
- `Task`: For complex multi-step research workflows
- `mcp__context7`, `mcp__Ref`: MCP integrations (if available)

## Troubleshooting

### Agent Not Triggering

Ensure your prompt includes clear research intent:
- Use keywords like "research", "analyze", "investigate", "review"
- Specify the domain (academic, technical, market, current events)

### Private Repository Access Fails

For technical-researcher:
1. Ensure `gh` CLI is authenticated: `gh auth status`
2. Verify repository access permissions
3. Check network connectivity

### Output Format Issues

All agents output structured JSON. If you need different formats:
- Ask agents to format findings as markdown reports
- Request specific sections or summaries

## Contributing

This plugin is part of the [claude-code-extensions](https://github.com/nodnarbnitram/claude-code-extensions) project.

To contribute:
1. Fork the repository
2. Add/modify agents in `.claude/agents/deep-research/`
3. Update plugin.json and README.md
4. Submit a pull request

## License

MIT License - See repository LICENSE file

## Version History

- **1.0.0** (2025-12-23): Initial release
  - 5 specialized research agents
  - Coordinated multi-researcher workflows
  - Temporal awareness and recency tracking
  - Private repository access
  - Structured JSON output formats

## Support

- **Issues**: [GitHub Issues](https://github.com/nodnarbnitram/claude-code-extensions/issues)
- **Discussions**: [GitHub Discussions](https://github.com/nodnarbnitram/claude-code-extensions/discussions)
- **Documentation**: [Repository README](https://github.com/nodnarbnitram/claude-code-extensions)

---

**Part of the Claude Code Extensions ecosystem** - Modular plugins for every tech stack
