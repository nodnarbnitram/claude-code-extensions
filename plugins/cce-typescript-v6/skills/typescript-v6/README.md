# TypeScript 6 Skill

> Build and operate TypeScript 6+ projects with modern tsconfig patterns, compiler diagnostics, and release-note-grounded guidance.

| | |
|---|---|
| **Status** | Active |
| **Version** | 1.0.0 |
| **Last Updated** | 2026-04-12 |
| **Confidence** | 4/5 |
| **Primary Source** | https://www.typescriptlang.org/docs/handbook/release-notes/typescript-6-0.html |

## What This Skill Does

Provides expert assistance for TypeScript 6+ development and configuration work. It focuses on the compiler changes and workflows that most often break or confuse real projects: explicit `types`, explicit `rootDir`, deprecated resolution/module settings, `#/` imports, newer ES library typings surfaced in TS 6, and the TS 6→TS 7 bridge tools such as `ignoreDeprecations` and `stableTypeOrdering`. It also includes practical compiler-verification workflow and TS-safe type-pattern guidance that fit TypeScript 6+ projects without pretending older generic advice is TS 6-specific.

### Core Capabilities

- Configure `tsconfig.json` intentionally for TypeScript 6+ projects
- Choose between `bundler` and `nodenext` module-resolution strategies without falling back to deprecated `node` / `node10`
- Fix common regressions caused by `types` and `rootDir` changes
- Migrate deprecated `baseUrl`, ES5-era targets, and legacy module settings to forward-looking replacements
- Explain and apply TypeScript 6-era library typings and patterns such as `#/` subpath imports, `RegExp.escape`, `Temporal`, and `Map.getOrInsert`
- Use compiler diagnostics like `--showConfig`, `--explainFiles`, and `--traceResolution` before changing source code blindly
- Apply TS-safe patterns such as `satisfies`, exhaustive unions, and assertion functions when the codebase reveals type ambiguity
- Use `--stableTypeOrdering` and TS 7 preview context responsibly during migration work

## Auto-Trigger Keywords

### Primary Keywords
- typescript 6
- ts 6
- ignoreDeprecations
- stableTypeOrdering
- types array
- noUncheckedSideEffectImports
- moduleResolution node is deprecated
- baseUrl is deprecated
- tsc --showConfig
- tsc --traceResolution
- tsc --explainFiles

### Secondary Keywords
- subpath imports
- #/ imports
- RegExp.escape
- Temporal API
- getOrInsert
- baseUrl migration
- downlevelIteration
- es2025

### Error-Based Keywords
- "Cannot find name 'process'"
- "Cannot find name 'describe'"
- "moduleResolution node is deprecated"
- "output is going to dist/src"
- "baseUrl is deprecated"
- "stableTypeOrdering"

## Known Issues Prevention

| Issue | Root Cause | Solution |
|-------|-----------|----------|
| Node or test globals disappear | The project relied on ambient type discovery that is no longer safe to assume during TS 6 migration work | Add explicit `types` entries |
| Emit path shifts into `dist/src/...` | The project relied on inferred source-root behavior that TS 6 migration work often needs to replace with explicit config | Set `rootDir` explicitly |
| TS 6 upgrade floods logs with warnings | Deprecated options survived from older configs | Replace them or temporarily gate them with `ignoreDeprecations: "6.0"` |
| Aliases do not work across environments | Bundler-only and Node-native alias strategies got mixed together | Pick `paths`, `imports`, and module resolution consistently |
| New ES APIs compile but break in runtime | Type-level support was mistaken for runtime support | Verify the runtime separately |

## When to Use

### Use This Skill For
- Building or maintaining a TypeScript 6+ codebase
- Fixing `tsconfig.json` in an active TypeScript 6+ project
- Choosing modern module resolution for bundlers or Node.js
- Migrating deprecated options such as `baseUrl` and `moduleResolution: "node"`
- Adopting TS 6-era standard-library types and platform APIs

### Don't Use This Skill For
- Generic TypeScript language tutoring unrelated to TS 6 changes
- Framework-specific runtime behavior that belongs to Next.js, Vite, Tauri, etc.
- TypeScript compiler API migration work for TS 7-native internals beyond high-level context

## Version Policy

> [!NOTE]
> This skill targets **TypeScript 6+** with special attention to the TypeScript 6.0 default/deprecation changes. It includes **TS 7 context only as comparison guidance**, not as the primary implementation target. When exact feature timing or runtime availability matters, verify it against the official release notes and TSConfig docs.

## Quick Usage

```bash
# Check the current project with an explicit TS 6 compiler
npx tsc --noEmit

# Compare type ordering behavior for TS 6 vs TS 7 migration work
npx tsc --noEmit --stableTypeOrdering

# Temporary migration shield while you remove deprecated options
# (do not keep this forever)
# "ignoreDeprecations": "6.0"
```

## Token Efficiency

| Approach | Estimated Tokens | Time |
|----------|-----------------|------|
| Manual TS 6+ docs diffing | ~12,000 | 60-90 min |
| With This Skill | ~6,000 | 20-30 min |
| **Savings** | **50%** | **~40 min** |

## Reference Documentation

For deeper guidance on the most failure-prone areas, see:

| Topic | Reference File | Purpose |
|-------|----------------|---------|
| **TS 6 Migration** | [`migration-v6-reference.md`](references/migration-v6-reference.md) | Handle the highest-impact changes when moving into TS 6 |
| **Defaults & Configuration** | [`defaults-migration-reference.md`](references/defaults-migration-reference.md) | Fix `types`, `rootDir`, and other TS 6+ configuration behavior |
| **Deprecations** | [`deprecations-reference.md`](references/deprecations-reference.md) | Replace deprecated TS 6 options with durable alternatives |
| **Module Resolution & Imports** | [`module-resolution-imports-reference.md`](references/module-resolution-imports-reference.md) | Choose `bundler` vs `nodenext`, and use `#/` imports correctly |
| **Standard Library Types** | [`stdlib-types-reference.md`](references/stdlib-types-reference.md) | Use `es2025`, `Temporal`, `RegExp.escape`, and upsert methods responsibly |
| **Workflow & Diagnostics** | [`workflow-diagnostics-reference.md`](references/workflow-diagnostics-reference.md) | Use compiler commands to verify config, file inclusion, and module resolution |
| **Type Patterns** | [`type-patterns-reference.md`](references/type-patterns-reference.md) | Apply `satisfies`, exhaustive unions, assertions, and typed results in TS 6+ code |
| **TS 6→7 Migration Context** | [`stable-ordering-ts7-reference.md`](references/stable-ordering-ts7-reference.md) | Apply `stableTypeOrdering`, preview TS 7 differences, and avoid false assumptions |

See the [References Index](references/README.md) for navigation.

## File Structure

```
typescript-v6/
├── SKILL.md                              # Quick-start patterns, critical rules, and upgrade guidance
├── README.md                             # This file - discovery and quick reference
└── references/
    ├── README.md                         # Reference index
    ├── migration-v6-reference.md         # Dedicated TypeScript 6 migration guide
    ├── defaults-migration-reference.md   # TS 6+ defaults and configuration behavior
    ├── deprecations-reference.md         # Deprecated options and replacements
    ├── module-resolution-imports-reference.md # bundler/nodenext and `#/` imports
    ├── stdlib-types-reference.md         # New platform/library types in TS 6
    ├── workflow-diagnostics-reference.md # Compiler commands for migration debugging
    ├── type-patterns-reference.md        # TS-safe patterns for TS 6+ code
    └── stable-ordering-ts7-reference.md  # `stableTypeOrdering` and TS 7 context
```

## Dependencies

| Package | Version | Verified |
|---------|---------|----------|
| `typescript` | ^6 | 2026-04-12 |
| `node` | >=20 recommended for modern TS 6 + native subpath-import workflows | 2026-04-12 |

## Official Documentation

- [TypeScript 6.0 Release Notes](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-6-0.html)
- [TypeScript Docs](https://www.typescriptlang.org/docs/)
- [TSConfig Reference](https://www.typescriptlang.org/tsconfig/)
- [Compiler Options Reference](https://www.typescriptlang.org/docs/handbook/compiler-options.html)
- [Choosing Compiler Options](https://www.typescriptlang.org/docs/handbook/modules/guides/choosing-compiler-options.html)

## Related Skills

- `vite-v8` - Useful when TypeScript 6 config changes live inside a Vite 8 project
- `vitest-v4` - Useful when TS 6 upgrades affect test globals, coverage config, or `vitest.config.ts`
- `github-actions` - CI workflow updates when `tsc --noEmit` or migration checks run in GitHub Actions

---

**License:** MIT
