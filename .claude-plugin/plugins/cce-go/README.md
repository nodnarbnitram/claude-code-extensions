# cce-go

Go development plugin enforcing Google Go style guide with Go 1.25+ features and best practices.

## Overview

The `cce-go` plugin provides expert-level Go development assistance through specialized agents that enforce Google's Go style guide, prevent common pitfalls, and promote idiomatic, maintainable code. This plugin is designed for developers who want strict adherence to Go best practices and modern language features.

## Features

### Google Go Style Guide Enforcement

- **Naming Conventions**: MixedCaps only, proper package naming, consistent receiver names
- **Error Handling**: Proper error wrapping with `%w`, early returns, indented error flow
- **Concurrency Patterns**: Explicit goroutine lifetime management, proper context usage
- **Testing Standards**: Table-driven tests WITHOUT assertion libraries (testify/assert forbidden)
- **Interface Design**: Consumer-side interface definitions, concrete return types

### Go 1.25+ Feature Support

- `sync.WaitGroup.Go()` for simpler concurrency patterns
- `testing/synctest` for deterministic concurrent tests
- `hash.Cloner` for efficient hash copying
- `net/http.CrossOriginProtection` for CORS handling
- `tb.Context()` for test contexts

### Code Quality Checks

- Automatic formatting verification with `go fmt`
- Common issue detection with `go vet`
- Race condition detection with `go test -race`
- Goroutine leak prevention
- Error handling completeness
- Variable shadowing detection

## Components

### Agents

#### go-google-style-expert

**Trigger**: Automatically activates when Go files are detected or explicitly invoked for Go code review

**Capabilities**:
- Comprehensive Go codebase analysis
- Style guide violation detection
- Error handling pattern verification
- Concurrency safety checks
- Test quality assessment
- Refactoring recommendations

**Use Cases**:
- Code reviews
- Legacy code modernization
- Style guide migration
- Pre-commit validation
- Learning idiomatic Go patterns

## Installation

### Plugin Mode (Recommended)

```bash
# Add marketplace (if not already added)
claude plugin marketplace add https://github.com/nodnarbnitram/claude-code-extensions

# Install the plugin
claude plugin install cce-go@cce-marketplace

# Verify installation
claude plugin list
```

### Standalone Mode

```bash
# Clone the repository
git clone https://github.com/nodnarbnitram/claude-code-extensions.git
cd claude-code-extensions

# Copy agents to your project
cp -r .claude/agents/specialized/go ~/.claude/agents/specialized/

# Or copy to project-local directory
cp -r .claude/agents/specialized/go /path/to/your/project/.claude/agents/specialized/
```

## Usage

### Automatic Activation

The Go expert agent activates automatically when:
- Go source files (`.go`) are detected in the workspace
- You're working with `go.mod` or Go projects
- You explicitly request Go code review or refactoring

### Manual Invocation

```
> Review my Go code following Google's style guide
> Check this Go package for concurrency issues
> Modernize this Go code to use Go 1.25 features
> Analyze error handling patterns in this repository
```

### Example Workflow

```
> I need to review the user authentication service in ./services/auth/

[go-google-style-expert activates]

The agent will:
1. Scan all .go files in ./services/auth/
2. Check go.mod for Go version compatibility
3. Run go fmt to verify formatting
4. Analyze code against Google style guide
5. Provide detailed violation report with fixes
6. Suggest Go 1.25 improvements where applicable
```

## Core Principles

The plugin enforces these principles in priority order:

1. **Clarity** - Code must be readable and obvious
2. **Simplicity** - Write code, don't design types
3. **Explicit over implicit** - Make intentions clear
4. **Share memory by communicating** - Prefer channels over mutexes
5. **Accept interfaces, return concrete types**

## Common Violations Caught

### Critical Issues

- Unchecked errors (`_, err := someFunc()` without handling)
- Goroutine leaks (unclear lifetime management)
- Custom context types (absolutely forbidden)
- Context stored in struct fields
- Race conditions in concurrent code

### Style Violations

- Underscores in names (`user_name` instead of `userName`)
- "Get" prefix on getters (`GetName()` instead of `Name()`)
- Util/common/helper packages
- Incorrect error wrapping format
- Inconsistent receiver names

### Testing Issues

- Use of assertion libraries (testify, assert)
- Non-table-driven tests
- Missing `t.Helper()` in test helpers
- Incorrect error message format
- Missing test coverage for error paths

## Code Pattern Examples

### Correct Error Handling

```go
// Correct - indented error flow, proper wrapping
if err != nil {
    return fmt.Errorf("operation failed: %w", err)
}
// happy path unindented
```

### Proper Goroutine Management (Go 1.25)

```go
// Modern pattern with WaitGroup.Go()
var wg sync.WaitGroup
wg.Go(func() { processItem() })
wg.Wait()
```

### Context as First Parameter

```go
// Always context first
func Process(ctx context.Context, data []byte) error {
    // implementation
}
```

### Table-Driven Tests

```go
tests := []struct {
    name  string
    input string
    want  string
}{
    {name: "empty", input: "", want: ""},
    {name: "basic", input: "hello", want: "HELLO"},
}
for _, tt := range tests {
    t.Run(tt.name, func(t *testing.T) {
        got := ToUpper(tt.input)
        if got != tt.want {
            t.Errorf("ToUpper(%q) = %q, want %q", tt.input, got, tt.want)
        }
    })
}
```

## Forbidden Patterns

The agent will flag these as critical violations:

```go
// NEVER: Custom context
type MyContext struct { context.Context } // FORBIDDEN

// NEVER: Assertion libraries
assert.Equal(t, expected, actual) // FORBIDDEN

// NEVER: Util packages
package util // FORBIDDEN

// NEVER: Get prefix
func GetName() string // Should be: func Name() string

// NEVER: Ignored errors
result, _ := someFunc() // FORBIDDEN
```

## Output Format

The agent provides structured analysis:

### Summary
- Total files analyzed
- Critical violations count
- Google style compliance percentage
- Go version compatibility

### Detailed Findings
For each violation:
1. **Location**: file:line
2. **Severity**: CRITICAL/WARNING/SUGGESTION
3. **Category**: Naming/Error/Concurrency/Testing/Interface
4. **Current Code**: The problematic code
5. **Correct Pattern**: Fixed code example
6. **Rationale**: Why this matters (from style guide)

### Refactoring Plan
Prioritized list of changes:
1. Critical safety issues (goroutine leaks, ignored errors)
2. Style violations that impact readability
3. Performance improvements
4. Go 1.25 modernization opportunities

## Decision Framework

When multiple patterns are possible, the agent follows this hierarchy:

1. **Safety first** - Prevent goroutine leaks, handle all errors
2. **Clarity over cleverness** - Obvious code beats clever code
3. **Simplicity over abstraction** - Don't over-engineer
4. **Consistency within package** - Match existing patterns
5. **Performance last** - Optimize only after profiling

## Requirements

- Go 1.18+ (for generics support in analysis)
- Go 1.25 recommended (for latest features)
- `go` command available in PATH
- Optional: `staticcheck` for additional linting

## Configuration

No configuration required. The agent enforces Google Go style guide strictly by default.

For project-specific exceptions, add a `.claude/agents/specialized/go/project-overrides.md` file documenting any necessary deviations from the style guide.

## Related Documentation

- [Google Go Style Guide](https://google.github.io/styleguide/go/)
- [Effective Go](https://go.dev/doc/effective_go)
- [Go 1.25 Release Notes](https://go.dev/doc/go1.25)
- [Go Code Review Comments](https://go.dev/wiki/CodeReviewComments)

## Support

For issues, questions, or contributions:
- GitHub Issues: https://github.com/nodnarbnitram/claude-code-extensions/issues
- Repository: https://github.com/nodnarbnitram/claude-code-extensions

## License

MIT License - see [LICENSE](https://github.com/nodnarbnitram/claude-code-extensions/blob/main/LICENSE) file

## Contributing

Contributions welcome! See [CONTRIBUTING.md](https://github.com/nodnarbnitram/claude-code-extensions/blob/main/CONTRIBUTING.md) for guidelines.

---

**Version**: 1.0.0
**Author**: Claude Code Extensions Contributors
**Keywords**: go, golang, google-style, best-practices, go1.25, concurrency, testing
