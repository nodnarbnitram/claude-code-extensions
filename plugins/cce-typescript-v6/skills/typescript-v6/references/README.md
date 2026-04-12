# TypeScript 6 Skill References

Use these references when the main `SKILL.md` is not enough:

| File | Focus |
|------|-------|
| [`defaults-migration-reference.md`](defaults-migration-reference.md) | `types`, `rootDir`, strict/default changes, and upgrade-safe tsconfig patterns |
| [`deprecations-reference.md`](deprecations-reference.md) | Deprecated TS 6 options, replacements, and temporary migration shields |
| [`module-resolution-imports-reference.md`](module-resolution-imports-reference.md) | `bundler` vs `nodenext`, `#/` subpath imports, and path alias decisions |
| [`stdlib-types-reference.md`](stdlib-types-reference.md) | `es2025`, `Temporal`, `RegExp.escape`, and `Map.getOrInsert*` guidance |
| [`stable-ordering-ts7-reference.md`](stable-ordering-ts7-reference.md) | `--stableTypeOrdering`, TS 7 context, and migration-comparison usage |

## Suggested Reading Order

- **Upgrading an existing repo?** Start with `defaults-migration-reference.md`
- **Removing warnings or legacy config?** Start with `deprecations-reference.md`
- **Choosing between `bundler`, `nodenext`, or `#/` imports?** Start with `module-resolution-imports-reference.md`
- **Trying new TS 6 library APIs?** Start with `stdlib-types-reference.md`
- **Comparing TS 6 and TS 7 behavior?** Start with `stable-ordering-ts7-reference.md`

## Official Sources

- [TypeScript 6.0 Release Notes](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-6-0.html)
- [TypeScript Docs](https://www.typescriptlang.org/docs/)
- [TSConfig Reference](https://www.typescriptlang.org/tsconfig/)
