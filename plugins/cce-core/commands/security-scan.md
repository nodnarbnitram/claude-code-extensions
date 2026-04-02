---
description: Run security scans on project files (Python/Go/JS/TS)
argument-hint: [path]
allowed-tools: Bash(*), Glob(*), Read(*)
---

# Security Scan Command

Run language-specific security scanners on the specified path or entire project.

## Task

1. **Determine scan target**:
   - If `$1` is provided, use it as the target path
   - If no argument, scan the entire project (current directory)

2. **Detect languages** in the target path:
   - Use Glob to find file types: `**/*.py`, `**/*.go`, `**/*.{js,jsx,ts,tsx}`
   - Determine which security tools are needed

3. **Run security scans** (using `uvx`/`npx` for on-demand tool execution):
   - **Python files** → Use `bandit` (https://github.com/PyCQA/bandit)
     - Run: `uvx bandit -r $TARGET -f screen` (or `-f json` for JSON output)
   - **Go files** → Use `gosec` (https://github.com/securego/gosec)
     - Check: `gosec -version`
     - Install if missing: `go install github.com/securego/gosec/v2/cmd/gosec@latest`
     - Run: `gosec -fmt=text ./...` (or `-fmt=json`)
   - **JS/TS files** → Use `ultracite` (https://www.ultracite.ai/usage)
     - Run: `npx ultracite check` (checks for security and quality issues)
     - Alternative: `npx ultracite fix` (auto-fixes issues where possible)

4. **If Go tools are missing**:
   - Ask user if they want to install `gosec`

6. **Report findings**:
   - Parse output and summarize security issues by severity
   - Show high/medium/low severity counts
   - List critical findings with file locations
   - Provide recommendations for fixing issues

## Target Path

${1:-.}

## Notes

- Use `uvx` for Python tools (no installation required)
- Use `npx` for JS/TS tools (no installation required)
- For Go tools, check availability and offer installation
- Handle cases where no files of a given type exist
- Provide clear, actionable security recommendations
