---
name: typescript-v6
description: "TypeScript 6+ guidance for project development, tsconfig configuration, diagnostics, module resolution, deprecations, and modern standard-library typings. Use when building or maintaining TypeScript 6+ projects, debugging compiler behavior, or working through TS 6-specific defaults and tooling such as `#/` subpath imports, `ignoreDeprecations`, `RegExp.escape`, `Temporal`, and `--stableTypeOrdering`. Triggers on typescript 6, ts 6, stableTypeOrdering, ignoreDeprecations, types array, noUncheckedSideEffectImports, baseUrl deprecated, moduleResolution node deprecated, and subpath imports."
version: 1.0.0
metadata:
  author: Brandon Martin
---

# TypeScript 6 Skill

> Build, configure, and debug TypeScript 6+ projects with precise compiler guidance and modern module/runtime patterns.

## Before You Start

**This skill is for real TypeScript 6+ project work: daily development, configuration, debugging, and upgrades.**

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
7. Missing Node/test globals because TS 6+ projects often need explicit `types` entries
8. New side-effect import errors because TS 6 applies stricter side-effect import checking

## Quick Start

### Step 1: Make the important options explicit

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

**Why this matters:** TypeScript 6 changed enough defaults and behaviors that explicit configuration now matters more in everyday work. `rootDir` and `types` are two of the most important settings to keep intentional.

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

### Step 3: Use TS 6-era library typings only when the target/lib/runtime really supports them

```ts
const escaped = RegExp.escape('(hello)');

const value = new Map<string, number>().getOrInsert('count', 0);

const tomorrow = Temporal.Now.instant().add({ hours: 24 });
```

**Why this matters:** TypeScript 6 can type new platform APIs before every runtime ships them. Distinguish **compiler types available** from **runtime support available**.

### Step 4: Verify config and resolution before changing code

```bash
npx tsc --noEmit
npx tsc --showConfig
npx tsc --explainFiles
```

**Why this matters:** TS 6+ projects often fail because the effective config or included file graph is not what the project expects. Validate that first, then refactor.

## Critical Rules

### Always Do

- Make `rootDir` explicit when your sources are nested below the `tsconfig.json`
- Make the `types` array explicit for Node, test runners, Workers, Bun, or other global type providers when the project relies on those ambient globals
- Prefer `moduleResolution: "bundler"` for bundled web apps and `moduleResolution: "nodenext"` for modern Node.js packages
- Treat `ignoreDeprecations: "6.0"` as a short-term migration escape hatch, not the destination
- Use `paths` directly instead of relying on deprecated `baseUrl`
- Make `types` explicit when the project truly depends on Node, test, Worker, or Bun globals
- Treat side-effect imports as intentionally checked and fix their paths deliberately
- Verify runtime support before recommending `Temporal`, `getOrInsert`, or `RegExp.escape`
- Use `--stableTypeOrdering` only when comparing TS 6 and TS 7 behavior or investigating ordering-sensitive issues
- Use `satisfies`, exhaustive `never` checks, and assertion functions when TS 6+ code exposes type ambiguity that should be made explicit
- Re-run `tsc --noEmit` after config changes and again after type-pattern refactors

### Never Do

- Never recommend deprecated `moduleResolution: "node"` / `"node10"` as the forward-looking path
- Never recommend removed `moduleResolution: "classic"` as a fallback path
- Never leave `types` implicit if a project depends on `@types/node`, test globals, or platform globals
- Never assume `ignoreDeprecations: "6.0"` will keep working in TypeScript 7
- Never present TS 7 preview context as if it were already the default compiler runtime
- Never imply that TypeScript types guarantee runtime availability for new ECMAScript APIs
- Never import pre-TS 6 tsconfig advice that still uses `skipDefaultLibCheck`, `downlevelIteration`, or old AMD/UMD/SystemJS examples

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

**Why:** In TS 6+, explicit `types` improves performance and predictability when the project depends on ambient globals.

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

**Wrong - type widening hides the real config contract:**
```ts
const compilerMode = {
  moduleResolution: 'bundler',
  strict: true,
};
```

**Correct - keep literals checked without widening:**
```ts
const compilerMode = {
  moduleResolution: 'bundler',
  strict: true,
} satisfies {
  moduleResolution: 'bundler' | 'nodenext';
  strict: boolean;
};
```

**Why:** `satisfies` is not new in TS 6, but it is one of the cleanest ways to make config and option objects precise without losing inference.

**Wrong - union handling silently misses a new case:**
```ts
type ResolutionMode = 'bundler' | 'nodenext' | 'preserve';

function describeMode(mode: ResolutionMode) {
  if (mode === 'bundler') return 'bundled app';
  return 'node-style runtime';
}
```

**Correct - exhaustive union handling:**
```ts
type ResolutionMode = 'bundler' | 'nodenext' | 'preserve';

function describeMode(mode: ResolutionMode) {
  switch (mode) {
    case 'bundler':
      return 'bundled app';
    case 'nodenext':
      return 'node-style runtime';
    case 'preserve':
      return 'mixed emit strategy';
    default: {
      const exhaustive: never = mode;
      return exhaustive;
    }
  }
}
```

**Why:** TypeScript 6+ projects often rely on unions for config, platform, and runtime state. Exhaustive `never` checks make missing cases obvious.

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
| Side-effect imports suddenly error | Side-effect import checking is stricter in TS 6+ projects | Fix typos, add explicit files, or tighten import paths intentionally |
| `#/` imports do not resolve | Runtime or resolution mode does not match TS 6 support requirements | Use Node 20+ support with `moduleResolution: "bundler"` or `"nodenext"` |
| New ES APIs compile but fail at runtime | TS lib types are present, runtime support is not | Verify runtime compatibility and polyfill strategy separately |
| Type ordering changes create noisy diffs | TS 6/TS 7 ordering differs during migration experiments | Use `--stableTypeOrdering` temporarily |

## Bundled Resources

### References

- **Dedicated TS 6 migration guide** → [`references/migration-v6-reference.md`](references/migration-v6-reference.md)
- **Defaults and configuration behavior** → [`references/defaults-migration-reference.md`](references/defaults-migration-reference.md)
- **Deprecations and replacements** → [`references/deprecations-reference.md`](references/deprecations-reference.md)
- **Module resolution and `#/` imports** → [`references/module-resolution-imports-reference.md`](references/module-resolution-imports-reference.md)
- **New library types and APIs** → [`references/stdlib-types-reference.md`](references/stdlib-types-reference.md)
- **Verification workflow and diagnostics** → [`references/workflow-diagnostics-reference.md`](references/workflow-diagnostics-reference.md)
- **Type-safe patterns for TS 6+ code** → [`references/type-patterns-reference.md`](references/type-patterns-reference.md)
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

### Monorepo/project-reference check

```json
{
  "compilerOptions": {
    "composite": true,
    "declaration": true,
    "isolatedDeclarations": true,
    "rootDir": "./src",
    "outDir": "./dist"
  }
}
```

Use this when packages emit `.d.ts` files or participate in project references. `isolatedDeclarations` is not TS 6-exclusive, but it fits the stricter, more explicit TS 6+ workflow well.

## Verification Workflow

```bash
npx tsc --noEmit
npx tsc --showConfig
npx tsc --explainFiles
npx tsc --traceResolution
```

**When to use each command:**
- `--noEmit`: First-pass health check after config or type changes
- `--showConfig`: Confirm the effective merged config before debugging phantom settings
- `--explainFiles`: Understand why a file is in the program or why a file graph changed
- `--traceResolution`: Debug `paths`, package exports, `types`, or `#/` import resolution

## Troubleshooting

### "Cannot find name 'process'" / "Cannot find name 'describe'"

Add the appropriate `types` entries and install the matching `@types/*` package if needed.

### Output path changed unexpectedly

Set `rootDir` explicitly. This is one of the most common TS 6 upgrade regressions.

### Deprecated option warnings keep appearing

Migrate away from deprecated settings; use `ignoreDeprecations: "6.0"` only while the real replacement work is still in progress.

### New side-effect import errors appear in TS 6+

Inspect the import path and whether the file is intended as a side-effect-only module. TS 6 applies stricter checking here, so old typos or vague side-effect imports can surface now.

### `RegExp.escape` / `Temporal` / `getOrInsert` compile but fail in production

Check runtime support. TS 6 can expose types before every target environment implements the runtime API.

## Setup Checklist

- [ ] `rootDir` is explicit if source files live below the `tsconfig.json`
- [ ] `types` is explicit for Node, tests, Workers, Bun, or other ambient platforms
- [ ] `moduleResolution` is `bundler` or `nodenext`, not deprecated `node` / `node10`
- [ ] Removed `classic` resolution, `skipDefaultLibCheck`, and `downlevelIteration` are not lingering in copied config
- [ ] Deprecated `baseUrl` / `downlevelIteration` / ES5-era settings are removed or scheduled for removal
- [ ] `tsc --showConfig` and `tsc --explainFiles` were used if the upgrade behavior is still surprising
- [ ] `ignoreDeprecations: "6.0"` is temporary and tracked
- [ ] New TS 6 APIs are validated against actual runtime support
- [ ] `--stableTypeOrdering` is only used for migration comparisons, not normal builds

## Official Documentation

- [TypeScript 6.0 Release Notes](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-6-0.html)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [TSConfig Reference](https://www.typescriptlang.org/tsconfig/)
- [Compiler Options Reference](https://www.typescriptlang.org/docs/handbook/compiler-options.html)
- [Choosing Compiler Options](https://www.typescriptlang.org/docs/handbook/modules/guides/choosing-compiler-options.html)
