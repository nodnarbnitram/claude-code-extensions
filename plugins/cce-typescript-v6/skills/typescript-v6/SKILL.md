---
name: typescript-v6
description: "TypeScript 6.0 guidance for tsconfig migrations, default changes, deprecations, module resolution, and modern standard-library types. Use when upgrading from TypeScript 5.x, debugging TypeScript 6 compiler changes, configuring tsconfig.json, or adopting TS 6 features like `#/` subpath imports, `RegExp.escape`, `Temporal`, and `--stableTypeOrdering`. Triggers on typescript 6, ts 6, tsconfig.json, stableTypeOrdering, moduleResolution bundler, nodenext, ignoreDeprecations, rootDir, types array, and subpath imports."
version: 1.0.0
metadata:
  author: Brandon Martin
---

# TypeScript 6 Skill

> Upgrade, configure, and debug TypeScript 6 projects with migration-safe defaults and modern module/runtime guidance.

## Before You Start

**This skill is for TypeScript 6.0-specific changes and migrations, not generic TypeScript tutoring.**

| Metric | Without Skill | With Skill |
|--------|--------------|------------|
| Upgrade Investigation Time | ~90 min | ~30 min |
| Common tsconfig Regressions | 5+ | 0-1 |
| Token Usage | High (manual diffing) | Low (release-note-grounded guidance) |

### Known Issues This Skill Prevents

1. Surprise build failures from missing `types` entries after upgrading
2. Unexpected `dist/src/...` output because `rootDir` was never explicit
3. Deprecated `moduleResolution node` or `baseUrl` settings surviving into a TS 6 migration
4. Confusion about when to use `bundler` vs `nodenext`
5. Overusing `ignoreDeprecations: "6.0"` as a long-term fix instead of a temporary migration aid
6. Misunderstanding `--stableTypeOrdering` as a production performance flag instead of a TS 6→7 comparison tool

## Quick Start

### Step 1: Make the migration-sensitive options explicit

```json
{
  "compilerOptions": {
    "rootDir": "./src",
    "outDir": "./dist",
    "types": ["node"],
    "strict": true
  },
  "include": ["src/**/*"]
}
```

**Why this matters:** TypeScript 6 changes enough defaults and behaviors that previously implicit configuration can become noisy or ambiguous. In many upgrades, `rootDir` and `types` are the two most common settings to make explicit first.

### Step 2: Pick module resolution deliberately

```json
{
  "compilerOptions": {
    "module": "esnext",
    "moduleResolution": "bundler"
  }
}
```

**Why this matters:** TypeScript 6 deprecates `moduleResolution: "node"`/`"node10"`. Bundled apps should usually choose `bundler`, while Node.js packages should usually choose `nodenext`.

### Step 3: Use TS 6-era APIs only when the target/lib/runtime really supports them

```ts
const escaped = RegExp.escape('(hello)');

const value = new Map<string, number>().getOrInsert('count', 0);

const tomorrow = Temporal.Now.instant().add({ hours: 24 });
```

**Why this matters:** TypeScript 6 can type new platform APIs before every runtime ships them. Distinguish **compiler types available** from **runtime support available**.

## Critical Rules

### Always Do

- Make `rootDir` explicit before or during a TS 6 upgrade if your sources are nested below the `tsconfig.json`
- Make the `types` array explicit for Node, test runners, Workers, Bun, or other global type providers when the project relies on those ambient globals
- Prefer `moduleResolution: "bundler"` for bundled web apps and `moduleResolution: "nodenext"` for modern Node.js packages
- Treat `ignoreDeprecations: "6.0"` as a short-term migration escape hatch, not the destination
- Use `paths` directly instead of relying on deprecated `baseUrl`
- Verify runtime support before recommending `Temporal`, `getOrInsert`, or `RegExp.escape`
- Use `--stableTypeOrdering` only when comparing TS 6 and TS 7 behavior or investigating ordering-sensitive issues

### Never Do

- Never recommend deprecated `moduleResolution: "node"` / `"node10"` as the forward-looking path
- Never leave `types` implicit if a project depends on `@types/node`, test globals, or platform globals
- Never assume `ignoreDeprecations: "6.0"` will keep working in TypeScript 7
- Never present TS 7 preview context as if it were already the default compiler runtime
- Never imply that TypeScript types guarantee runtime availability for new ECMAScript APIs

### Common Mistakes

**Wrong - relying on pre-TS 6 ambient type loading:**
```json
{
  "compilerOptions": {
    "outDir": "./dist"
  }
}
```

**Correct - declare what global types the project actually needs:**
```json
{
  "compilerOptions": {
    "outDir": "./dist",
    "types": ["node"]
  }
}
```

**Why:** TS 6 no longer treats the entire `@types` universe as an implicit default. Explicit `types` improves performance and predictability.

**Wrong - keep deprecated path alias setup unchanged:**
```json
{
  "compilerOptions": {
    "baseUrl": "./src",
    "paths": {
      "@app/*": ["app/*"]
    }
  }
}
```

**Correct - inline the source prefix in `paths`:**
```json
{
  "compilerOptions": {
    "paths": {
      "@app/*": ["./src/app/*"]
    }
  }
}
```

**Why:** `baseUrl` is deprecated in TS 6. The forward-looking setup is direct `paths` entries.

**Wrong - use `stableTypeOrdering` as a normal build flag:**
```bash
tsc --stableTypeOrdering --build
```

**Correct - use it only for comparison/debugging:**
```bash
tsc --noEmit --stableTypeOrdering
```

**Why:** The flag exists to reduce TS 6 vs TS 7 output noise. It can meaningfully slow type-checking and is not intended as a permanent default.

## Known Issues Prevention

| Issue | Root Cause | Solution |
|-------|-----------|----------|
| `process` / `describe` / `fs` suddenly missing | The project relied on ambient type discovery that is no longer safe to assume during TS 6 migration work | Add explicit entries like `"types": ["node", "jest"]` |
| Output moves to `dist/src/...` | The project relied on inferred source-root behavior that TS 6 migration work often needs to replace with explicit config | Set `rootDir` explicitly, usually `./src` |
| Upgrade warnings explode | Deprecated module resolution or emit-era options survived from older configs | Migrate to `bundler` or `nodenext`; remove deprecated options |
| `#/` imports do not resolve | Runtime or resolution mode does not match TS 6 support requirements | Use Node 20+ support with `moduleResolution: "bundler"` or `"nodenext"` |
| New ES APIs compile but fail at runtime | TS lib types are present, runtime support is not | Verify runtime compatibility and polyfill strategy separately |
| Type ordering changes create noisy diffs | TS 6/TS 7 ordering differs during migration experiments | Use `--stableTypeOrdering` temporarily |

## Bundled Resources

### References

- **Defaults and migration fixes** → [`references/defaults-migration-reference.md`](references/defaults-migration-reference.md)
- **Deprecations and replacements** → [`references/deprecations-reference.md`](references/deprecations-reference.md)
- **Module resolution and `#/` imports** → [`references/module-resolution-imports-reference.md`](references/module-resolution-imports-reference.md)
- **New library types and APIs** → [`references/stdlib-types-reference.md`](references/stdlib-types-reference.md)
- **`stableTypeOrdering` and TS 7 context** → [`references/stable-ordering-ts7-reference.md`](references/stable-ordering-ts7-reference.md)
- **Reference index** → [`references/README.md`](references/README.md)

## Configuration Reference

### Bundled application baseline

```json
{
  "compilerOptions": {
    "target": "es2025",
    "module": "esnext",
    "moduleResolution": "bundler",
    "lib": ["es2025", "dom"],
    "rootDir": "./src",
    "outDir": "./dist",
    "strict": true,
    "noUncheckedSideEffectImports": true
  },
  "include": ["src/**/*"]
}
```

**Key settings:**
- `rootDir`: Prevents accidental `dist/src/...` nesting
- `types`: Add it explicitly only when the project actually depends on Node/test/platform globals
- `moduleResolution: "bundler"`: Best fit for Vite/esbuild/Rollup/Webpack-style app builds
- `target: "es2025"` / `lib: ["es2025", ...]`: Gives access to TS 6-era built-in types such as `RegExp.escape`

### Node package baseline

```json
{
  "compilerOptions": {
    "target": "es2022",
    "module": "nodenext",
    "moduleResolution": "nodenext",
    "lib": ["es2022"],
    "rootDir": "./src",
    "outDir": "./dist",
    "types": ["node"],
    "strict": true
  },
  "include": ["src/**/*"]
}
```

**Key settings:**
- `nodenext`: Use when the package's runtime semantics should follow modern Node.js ESM/CJS rules
- Explicit `.js` import specifiers and `package.json` module settings still matter; TS 6 does not remove that responsibility

## Project Structure

```
my-ts-project/
├── src/
├── dist/
├── package.json
└── tsconfig.json
```

**Why this matters:** TS 6 rewards explicit, boring project structure. Most upgrade pain comes from old implicit config behavior, not from source code syntax.

## Common Patterns

### Direct `paths` migration

```json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

Use this instead of keeping deprecated `baseUrl` around.

### `#/` subpath imports for package-internal aliases

```json
{
  "name": "my-package",
  "type": "module",
  "imports": {
    "#/*": "./dist/*"
  }
}
```

```ts
import * as utils from '#/utils.js';
```

Use this when your package/runtime already supports Node's `imports` field and you want package-native aliases instead of bundler-only conventions. Keep the exact mapping aligned with the files the package actually ships.

### Temporary migration shield

```json
{
  "compilerOptions": {
    "ignoreDeprecations": "6.0"
  }
}
```

Use this only long enough to unblock the migration. Plan to remove it before TS 7.

## Troubleshooting

### "Cannot find name 'process'" / "Cannot find name 'describe'"

Add the appropriate `types` entries and install the matching `@types/*` package if needed.

### Output path changed unexpectedly

Set `rootDir` explicitly. This is one of the most common TS 6 upgrade regressions.

### Deprecated option warnings keep appearing

Migrate away from deprecated settings; use `ignoreDeprecations: "6.0"` only while the real replacement work is still in progress.

### `RegExp.escape` / `Temporal` / `getOrInsert` compile but fail in production

Check runtime support. TS 6 can expose types before every target environment implements the runtime API.

## Setup Checklist

- [ ] `rootDir` is explicit if source files live below the `tsconfig.json`
- [ ] `types` is explicit for Node, tests, Workers, Bun, or other ambient platforms
- [ ] `moduleResolution` is `bundler` or `nodenext`, not deprecated `node` / `node10`
- [ ] Deprecated `baseUrl` / `downlevelIteration` / ES5-era settings are removed or scheduled for removal
- [ ] `ignoreDeprecations: "6.0"` is temporary and tracked
- [ ] New TS 6 APIs are validated against actual runtime support
- [ ] `--stableTypeOrdering` is only used for migration comparisons, not normal builds

## Official Documentation

- [TypeScript 6.0 Release Notes](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-6-0.html)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [TSConfig Reference](https://www.typescriptlang.org/tsconfig/)
- [Compiler Options Reference](https://www.typescriptlang.org/docs/handbook/compiler-options.html)
- [Choosing Compiler Options](https://www.typescriptlang.org/docs/handbook/modules/guides/choosing-compiler-options.html)
