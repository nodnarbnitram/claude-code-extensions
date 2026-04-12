# TypeScript 6 Skill References

Use these references when the main `SKILL.md` is not enough:

| File | Focus |
|------|-------|
| [`migration-v6-reference.md`](migration-v6-reference.md) | Dedicated TS 6 migration checklist, config shifts, and verification loop |
| [`defaults-migration-reference.md`](defaults-migration-reference.md) | `types`, `rootDir`, strict/default changes, and TS 6+ tsconfig patterns |
| [`deprecations-reference.md`](deprecations-reference.md) | Deprecated TS 6 options, replacements, and temporary migration shields |
| [`module-resolution-imports-reference.md`](module-resolution-imports-reference.md) | `bundler` vs `nodenext`, `#/` subpath imports, and path alias decisions |
| [`stdlib-types-reference.md`](stdlib-types-reference.md) | `es2025`, `Temporal`, `RegExp.escape`, and `Map.getOrInsert*` guidance |
| [`workflow-diagnostics-reference.md`](workflow-diagnostics-reference.md) | `tsc --showConfig`, `--explainFiles`, `--traceResolution`, and project-reference debugging |
| [`type-patterns-reference.md`](type-patterns-reference.md) | `satisfies`, exhaustive unions, assertion functions, branded types, and typed results for TS 6+ code |
| [`stable-ordering-ts7-reference.md`](stable-ordering-ts7-reference.md) | `--stableTypeOrdering`, TS 7 context, and migration-comparison usage |

## Suggested Reading Order

- **Upgrading an existing repo?** Start with `migration-v6-reference.md`
- **Need the broader TS 6+ config behavior?** Then read `defaults-migration-reference.md`
- **Removing warnings or legacy config?** Start with `deprecations-reference.md`
- **Choosing between `bundler`, `nodenext`, or `#/` imports?** Start with `module-resolution-imports-reference.md`
- **Trying new TS 6 library APIs?** Start with `stdlib-types-reference.md`
- **Debugging config/file inclusion/resolution?** Start with `workflow-diagnostics-reference.md`
- **Need safer type patterns in TS 6+ code?** Start with `type-patterns-reference.md`
- **Comparing TS 6 and TS 7 behavior?** Start with `stable-ordering-ts7-reference.md`

## Official Sources

- [TypeScript 6.0 Release Notes](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-6-0.html)
- [TypeScript Docs](https://www.typescriptlang.org/docs/)
- [TSConfig Reference](https://www.typescriptlang.org/tsconfig/)
