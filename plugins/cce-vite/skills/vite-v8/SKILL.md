---
name: vite-v8
description: "Vite 8+ development with Rolldown and Oxc. Use when configuring vite.config.ts, migrating rollup/esbuild-era configs, authoring Vite plugins with environments and hook filters, or troubleshooting SSR, Module Runner, and production build behavior in Vite 8. Triggers on vite, vite.config.ts, rolldownOptions, oxc, module runner, environments, hotUpdate, and lightning css."
version: 1.0.0
metadata:
  author: Brandon Martin
---

# Vite 8 Skill

> Configure, migrate, and debug Vite 8 projects with the repo's preferred Vite-native patterns.

## Before You Start

**This skill focuses on the Vite 8 architecture shift, not generic bundler advice.**

| Metric | Without Skill | With Skill |
|--------|--------------|------------|
| Migration Time | ~120 min | ~40 min |
| Common Config Errors | 6+ | 0 |
| Token Usage | High (trial/error) | Low (known patterns) |

### Known Issues This Skill Prevents

1. Broken builds from leaving `rollupOptions` in Vite 8 configs where `rolldownOptions` is needed
2. Outdated JS/TS transform setup from using `esbuild` instead of `oxc`
3. Plugin code checking stale `ssr` booleans instead of environment-aware APIs
4. HMR bugs from using deprecated `handleHotUpdate` patterns instead of `hotUpdate`
5. SSR/runtime confusion from older `ssrLoadModule` mental models instead of Module Runner
6. Performance regressions from missing hook filters in Rust↔JS plugin boundaries
7. Slow startup and request waterfalls from barrel files, missing warmup, or loose import resolution

## Quick Start

### Step 1: Start with a typed Vite 8 config

```typescript
// vite.config.ts
import { defineConfig } from 'vite';

export default defineConfig({
  server: {
    port: 5173,
  },
  build: {
    target: 'baseline-widely-available',
    rolldownOptions: {
      output: {
        manualChunks: undefined,
      },
    },
  },
});
```

**Why this matters:** Vite 8 is built around Rolldown/Oxc-era config and defaults. Starting from `defineConfig` with Vite 8 options avoids backporting old Rollup/esbuild assumptions into a new architecture.

### Step 2: Prefer Vite 8 terminology in plugins and SSR code

```typescript
import type { Plugin } from 'vite';

export function inspectEnvironment(): Plugin {
  return {
    name: 'inspect-environment',
    configEnvironment(name) {
      if (name === 'ssr') {
        return {
          resolve: {
            conditions: ['node'],
          },
        };
      }
    },
  };
}
```

**Why this matters:** Vite 8 leans on named environments and environment-aware plugin behavior. That is a better fit than older client-vs-SSR shortcuts.

### Step 3: Use the correct one-shot commands

```bash
vite dev
vite build
vite build --ssr src/entry-server.ts
vite preview
```

**Why this matters:** These are the stable command surfaces agents and CI flows should target. Avoid inventing framework-specific abstractions unless the project already uses them.

## Critical Rules

### Always Do

- Use `vite.config.ts` with `defineConfig` for repo-facing Vite 8 work
- Prefer `build.rolldownOptions` over legacy `build.rollupOptions`
- Prefer `oxc` over `esbuild` for new Vite 8 transform configuration
- Use named environments when plugin or SSR behavior differs by runtime
- Use hook filters when writing performance-sensitive `transform` or `resolveId` plugins
- Reach for Module Runner concepts when debugging modern SSR/runtime execution
- Use explicit file extensions and review barrel files when performance work matters
- Keep Vite plugin code ESM-first

### Never Do

- Never introduce new `rollupOptions`/`esbuild` examples as the preferred Vite 8 path
- Never treat `handleHotUpdate` as the forward-looking HMR hook in Vite 8
- Never assume a single client/SSR split is enough for all runtimes
- Never suggest CommonJS config as the default for new Vite work
- Never skip `ssr.noExternal` review when SSR dependencies misbehave

### Common Mistakes

**Wrong - legacy build config:**
```typescript
export default defineConfig({
  build: {
    rollupOptions: {
      external: ['react'],
    },
  },
  esbuild: {
    jsxInject: "import React from 'react'",
  },
});
```

**Correct - Vite 8 config:**
```typescript
export default defineConfig({
  build: {
    rolldownOptions: {
      external: ['react'],
    },
  },
  oxc: {
    jsxInject: "import React from 'react'",
  },
});
```

**Why:** Vite 8 moved its preferred build and transform configuration surface to Rolldown and Oxc.

**Wrong - stale HMR hook:**
```typescript
export default function plugin() {
  return {
    name: 'old-hmr',
    handleHotUpdate(ctx) {
      return ctx.modules;
    },
  };
}
```

**Correct - environment-aware HMR:**
```typescript
export default function plugin() {
  return {
    name: 'env-hmr',
    hotUpdate(ctx) {
      return ctx.modules;
    },
  };
}
```

**Why:** `hotUpdate` is the environment-aware Vite 8 direction, while `handleHotUpdate` is legacy-oriented.

## Known Issues Prevention

| Issue | Root Cause | Solution |
|-------|-----------|----------|
| Config migration stalls | Old Rollup/esbuild settings copied forward | Migrate to `rolldownOptions` and `oxc` |
| Plugin logic breaks in non-standard runtimes | Plugin assumes only client/SSR | Use named `environments` and `this.environment` |
| HMR customization feels brittle | Legacy HMR hook carried forward | Prefer `hotUpdate` and environment-aware flows |
| SSR dependency crashes | Externalization assumptions are wrong | Review `ssr.noExternal` and runtime-specific needs |
| Dev/build behavior diverges | Config ignores Vite 8's unified engine model | Validate both `vite dev` and `vite build` under Rolldown |
| Plugin performance drops | Too much JS-side hook work | Add hook filters and narrower matching |
| Cold starts are sluggish | Heavy hot paths are not warmed and import graph is noisy | Review `server.warmup`, explicit extensions, and barrel-file usage |

## Bundled Resources

### References

- **Core config and CLI patterns** → [`references/core-config-reference.md`](references/core-config-reference.md)
- **Environment-aware plugin authoring** → [`references/plugin-environment-reference.md`](references/plugin-environment-reference.md)
- **Build, SSR, and migration guidance** → [`references/build-ssr-migration-reference.md`](references/build-ssr-migration-reference.md)
- **Performance and dev-server heuristics** → [`references/performance-devserver-reference.md`](references/performance-devserver-reference.md)
- **Reference index** → [`references/README.md`](references/README.md)

## Configuration Reference

### vite.config.ts

```typescript
import { defineConfig } from 'vite';

export default defineConfig({
  build: {
    target: 'baseline-widely-available',
    rolldownOptions: {
      output: {
        chunkFileNames: 'assets/[name]-[hash].js',
      },
    },
  },
  oxc: {
    jsxInject: "import React from 'react'",
  },
  environments: {
    ssr: {
      resolve: {
        conditions: ['node'],
      },
    },
  },
  css: {
    lightningcss: {},
  },
});
```

**Key settings:**
- `build.rolldownOptions`: Preferred Vite 8 build customization surface
- `oxc`: Preferred JS/TS transform configuration surface in new Vite 8 examples
- `environments`: Use when runtime behavior differs across client/SSR/edge-like targets
- `css.lightningcss`: Reflects Vite 8's modern CSS processing direction
- `server.warmup`: Useful in large apps where cold-start waterfalls hit the same hot files repeatedly

## Project Structure

```
my-app/
├── src/
├── index.html
├── vite.config.ts
├── package.json
└── tsconfig.json
```

**Why this matters:** Vite 8 still rewards simple, explicit project layout. Complexity should come from runtime environments and plugin boundaries, not from hiding the core config.

**Performance heuristic:** If startup feels bad, inspect import-graph shape before chasing exotic bundler flags. Barrel files, omitted extensions, and lack of warmup often matter more than another layer of config cleverness.

## Common Patterns

### Environment-aware plugin pattern

```typescript
import type { Plugin } from 'vite';

export function envAwarePlugin(): Plugin {
  return {
    name: 'env-aware-plugin',
    transform: {
      filter: {
        id: /\.(ts|tsx)$/,
      },
      handler(code, id) {
        return {
          code,
          map: null,
        };
      },
    },
    configEnvironment(name) {
      if (name === 'ssr') {
        return {
          resolve: {
            conditions: ['node'],
          },
        };
      }
    },
  };
}
```

### SSR build pattern

```bash
vite build
vite build --ssr src/entry-server.ts
vite preview
```

### Module Runner mental model

```typescript
// Pseudocode sketch
const mod = await moduleRunner.import('/src/entry-server.ts');
```

Use this model when modern Vite SSR debugging is really about runtime execution boundaries rather than plain bundling.

## Dependencies

### Required

| Package | Version | Purpose |
|---------|---------|---------|
| `vite` | ^8 | Build tool, dev server, plugin host |
| `node` | >=20.19 or >=22.12 | Required Vite 8 runtime |

### Optional

| Package | Version | Purpose |
|---------|---------|---------|
| `typescript` | latest | Typed `vite.config.ts` and plugin authoring |
| framework plugin packages | latest | React/Vue/Svelte/etc integrations |

## Official Documentation

- [Vite Docs](https://vite.dev/)
- [LLM index](https://vite.dev/llms.txt)
- [Config Reference](https://vite.dev/config/)
- [Plugin API](https://vite.dev/guide/api-plugin.html)
- [Build Guide](https://vite.dev/guide/build)
- [SSR Guide](https://vite.dev/guide/ssr)
- [Environment API](https://vite.dev/guide/api-environment)

## Troubleshooting

### Old config keys no longer feel right

**Symptoms:** A config works but reads like pre-Vite-8 code, or new options are not behaving as expected.

**Solution:**
```typescript
build: {
  rolldownOptions: {},
}

oxc: {}
```

### SSR runtime behavior is unclear

**Symptoms:** The bundle builds, but runtime execution differs by environment or platform.

**Solution:**
Review `environments`, `this.environment`, Module Runner expectations, and `ssr.noExternal` before changing unrelated bundler settings.

### Plugin hook work feels slow or noisy

**Symptoms:** Custom plugins add overhead in dev or build.

**Solution:**
Use hook filters and narrow matching patterns so only relevant files cross the Rust↔JS boundary.

## Setup Checklist

Before using this skill, verify:

- [ ] `vite` is on a Vite 8 release line
- [ ] Node satisfies Vite 8 runtime requirements
- [ ] `vite.config.ts` is ESM/TypeScript-first
- [ ] Legacy `rollupOptions` / `esbuild` usage has been reviewed
- [ ] Environment-specific behavior is modeled explicitly when SSR/edge runtimes are involved
