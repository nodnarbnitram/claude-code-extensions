# Vitest v4 Pools and Execution Reference

Large or flaky suites often need execution tuning as much as they need better assertions.

## Pool Selection Heuristic

| Pool | Best For | Main Risk |
|------|----------|-----------|
| `forks` | Stability, native modules, mixed infra tests | Slightly slower than threads |
| `threads` | Fast pure-JS suites with safe worker-thread behavior | Native module and runtime compatibility issues |
| `vmThreads` / `vmForks` | Sandbox-style experiments only | Memory leaks and global-object mismatch surprises |

## Recommended Default

Start with `forks` unless you have a measured reason not to. It is the safer default for real-world suites that touch native dependencies, runtime integration layers, or tooling that assumes process isolation.

## Isolation Tradeoff

`isolate: false` can speed up pure Node suites significantly, but only use it when tests are intentionally side-effect-safe and you understand the shared-state risks.

## Persistent Module Cache

For large codebases, `experimental.fsModuleCache` can cut cold-start cost by persisting transformed modules between runs.

## Debugging Heuristic

- Native dependency failures in `threads` → try `forks`
- Memory weirdness in VM pools → remove VM pools first
- Slow cold starts in huge repos → evaluate filesystem module cache
- Random state leakage → review isolation mode before rewriting tests
