# Vitest 4 Testing Skill

> Write, configure, and debug Vitest 4 test suites with Vite-native patterns.

| | |
|---|---|
| **Status** | Active |
| **Version** | 1.0.0 |
| **Last Updated** | 2026-04-12 |
| **Confidence** | 4/5 |
| **Production Tested** | https://v4.vitest.dev/ |

## What This Skill Does

Provides expert assistance for Vitest 4 projects, from initial `vitest.config.ts` setup through unit, integration, and browser-based test authoring. It focuses on agent-safe execution, type-safe mocking with `vi`, Browser Mode providers, coverage configuration, setup files, and the Vitest 4 migration details that commonly break older test setups.

### Core Capabilities

- Configure `vitest.config.ts` for Node, jsdom, and Browser Mode test suites
- Write Vitest-native tests with `test`, `expect`, and `vi` APIs
- Implement module, function, global, and environment mocks without cross-test leakage
- Configure V8 or Istanbul coverage with Vitest 4-compatible settings
- Set up Browser Mode using Playwright, WebdriverIO, or Preview providers with Vitest 4 provider-factory config
- Migrate deprecated workspace-style configs to `projects`
- Improve AI-generated tests by grounding them in real implementation and config context

## Auto-Trigger Keywords

### Primary Keywords
Exact terms that strongly trigger this skill:
- vitest
- vitest 4
- vitest.config.ts
- vi.mock
- vi.fn
- vi.spyOn
- vitest/browser
- browser mode

### Secondary Keywords
Related terms that may trigger in combination:
- projects config
- v8 coverage
- toMatchScreenshot
- import.meta.vitest
- jsdom test
- test.each
- mocked module
- jest migration

### Error-Based Keywords
Common error messages that should trigger this skill:
- "ReferenceError: jest is not defined"
- "Cannot spy on export"
- "Coverage option \"all\" is not supported"
- "Tests are hanging in watch mode"
- "workspace config is deprecated"
- "Browser provider is missing"
- "Unknown browser provider"

## Known Issues Prevention

| Issue | Root Cause | Solution |
|-------|-----------|----------|
| Tests hang forever | Watch mode used in non-interactive environment | Use `vitest run` |
| Browser spy fails | `vi.spyOn` used on sealed ESM namespace in browser | Use `vi.mock(import('./mod'), { spy: true })` |
| Coverage misses untested files | `coverage.include` omitted | Add explicit source globs |
| Mocks leak across tests | Cleanup flags not enabled | Set `restoreMocks` / `clearMocks` / `unstubEnvs` |
| Multi-project setup breaks | Old workspace terminology/config copied forward | Use `projects` + `defineProject` |
| Browser provider config errors | Vitest 3 string provider examples copied into Vitest 4 | Import provider factories like `playwright()` from the provider package |

## When to Use

### Use This Skill For
- Creating or fixing `vitest.config.ts`
- Writing unit, integration, or browser tests in Vitest 4
- Mocking modules, constructors, globals, env vars, and timers with `vi`
- Setting up coverage reporting in CI or local runs
- Migrating from Jest or older Vitest configs
- Making AI-generated tests more reliable and less hallucination-prone

### Don't Use This Skill For
- Jest-only codebases that are not using Vitest
- End-to-end browser automation outside Vitest Browser Mode
- Test runners that do not share Vite/Vitest configuration

## Version Policy

> [!NOTE]
> This skill targets **Vitest 4+**. It assumes **Node.js 20+** and **Vite 6+**. Browser Mode examples use the Vitest 4 provider-factory API such as `playwright()`. When exact version timing matters, verify feature availability in the official Vitest changelog and provider package docs.

## Quick Usage

```bash
# Install Vitest 4
npm install -D vitest vite

# Run once (agent/CI safe)
npx vitest run

# Run coverage
npx vitest run --coverage

# Initialize Browser Mode setup
npx vitest init browser

# Run a single file
npx vitest run src/example.test.ts
```

## Token Efficiency

| Approach | Estimated Tokens | Time |
|----------|-----------------|------|
| Manual Vitest debugging | ~12,000 | 60-90 min |
| With This Skill | ~6,000 | 20-30 min |
| **Savings** | **50%** | **~40 min** |

## Reference Documentation

For deeper guidance on the most failure-prone areas, see:

| Topic | Reference File | Purpose |
|-------|----------------|---------|
| **Mocking** | [`mocking-reference.md`](references/mocking-reference.md) | Module mocks, hoisting rules, env/global stubs, and safe cleanup |
| **Browser Mode** | [`browser-mode-reference.md`](references/browser-mode-reference.md) | Providers, `vitest/browser` patterns, native event caveats, and spying pitfalls |
| **Coverage & Projects** | [`coverage-projects-reference.md`](references/coverage-projects-reference.md) | Vitest 4 coverage changes, `projects`, and migration-safe config patterns |

See the [References Index](references/README.md) for navigation.

## Environment Heuristic

- **Use `jsdom`** for most component tests, DOM assertions, and fast feedback loops.
- **Use Browser Mode** when native browser APIs, real event behavior, layout, or screenshot assertions are required.

## File Structure

```
vitest-4/
├── SKILL.md        # Quick-start patterns, critical rules, and practical guidance
├── README.md       # This file - discovery and quick reference
└── references/
    ├── README.md                       # Reference index
    ├── mocking-reference.md           # Mocking APIs, hoisting, and cleanup
    ├── browser-mode-reference.md      # Browser Mode provider and test patterns
    └── coverage-projects-reference.md # Coverage/provider/projects guidance
```

## Dependencies

| Package | Version | Verified |
|---------|---------|----------|
| `vitest` | ^4 | 2026-04-12 |
| `vite` | ^6 | 2026-04-12 |
| `node` | >=20 | 2026-04-12 |

> **Preview provider caveat:** `@vitest/browser-preview` can help with local debugging, but it is not a strong CI default because it does not provide the same browser fidelity as Playwright or WebdriverIO.

## Official Documentation

- [Vitest v4 Docs](https://v4.vitest.dev/)
- [LLM Index](https://v4.vitest.dev/llms.txt)
- [Mocking Guide](https://v4.vitest.dev/guide/mocking)
- [Browser Mode Guide](https://v4.vitest.dev/guide/browser)
- [Coverage Guide](https://v4.vitest.dev/guide/coverage)
- [Projects Guide](https://v4.vitest.dev/guide/projects)
- [Writing Tests with AI](https://v4.vitest.dev/guide/learn/writing-tests-with-ai)

## Related Skills

- `github-actions` - CI workflow patterns when running Vitest in GitHub Actions
- `vite` - Vite config guidance when Vitest shares or extends build configuration
- `react-performance` - Useful when Vitest covers React render and interaction regressions

---

**License:** MIT
