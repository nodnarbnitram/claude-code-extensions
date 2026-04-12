# Vite 8 Skill

> Configure, migrate, and debug Vite 8 projects with Rolldown, Oxc, and environment-aware plugin patterns.

| | |
|---|---|
| **Status** | Active |
| **Version** | 1.0.0 |
| **Last Updated** | 2026-04-12 |
| **Confidence** | 4/5 |
| **Production Tested** | https://vite.dev/ |

## What This Skill Does

Provides expert assistance for Vite 8 projects, from `vite.config.ts` setup through plugin authoring, environment-aware runtime configuration, and Rolldown/Oxc migration. It focuses on the real Vite 8 architecture shift rather than generic bundler advice.

### Core Capabilities

- Configure `vite.config.ts` with Vite 8-era options and conventions
- Migrate legacy Rollup/esbuild-flavored configs to Rolldown/Oxc surfaces
- Author Vite plugins with named environments, hook filters, and environment-aware HMR flows
- Debug SSR/build/runtime issues using Vite 8 mental models such as Module Runner and isolated environments
- Improve production build behavior while keeping dev/build assumptions aligned

## Auto-Trigger Keywords

### Primary Keywords
- vite
- vite 8
- vite.config.ts
- rolldownOptions
- oxc
- environments
- module runner
- hotUpdate

### Secondary Keywords
- lightning css
- ssr.noExternal
- configEnvironment
- this.environment
- hook filters
- rolldown migration
- build target

### Error-Based Keywords
- "rollupOptions is not behaving as expected"
- "esbuild config is deprecated"
- "handleHotUpdate"
- "ssrLoadModule"
- "default import from cjs behaves differently"

## Known Issues Prevention

| Issue | Root Cause | Solution |
|-------|-----------|----------|
| Config feels stuck in older Vite versions | Rollup/esbuild assumptions copied forward | Move to `rolldownOptions` and `oxc` |
| Plugin logic fails in SSR/edge contexts | Plugin assumes only client/SSR | Use named environments and `this.environment` |
| HMR customization is brittle | Legacy HMR APIs carried over | Prefer `hotUpdate` |
| SSR package behavior is inconsistent | Externalization model not reviewed | Check `ssr.noExternal` and runtime boundaries |
| Build output differs unexpectedly from dev | Vite 8 unified engine model not considered | Validate both dev and build with current config |

## When to Use

### Use This Skill For
- Creating or fixing `vite.config.ts`
- Migrating Vite projects to Vite 8 terminology and config surfaces
- Writing or reviewing Vite plugins
- Troubleshooting SSR/runtime/environment-specific behavior
- Improving build config without falling back to outdated Rollup guidance

### Don't Use This Skill For
- Framework-only issues that are actually owned by Next.js/Nuxt/etc internals
- Vitest-specific testing workflows where `vitest-v4` is the better fit

## Version Policy

> [!NOTE]
> This skill targets **Vite 8+**. It assumes the Rolldown/Oxc-era config surface and modern environment APIs. If the repo is intentionally pinned to an older Vite line, verify version-specific support before applying the migration guidance here.

## Quick Usage

```bash
# Start dev server
npx vite dev

# Production build
npx vite build

# SSR build
npx vite build --ssr src/entry-server.ts

# Preview production output
npx vite preview
```

## Token Efficiency

| Approach | Estimated Tokens | Time |
|----------|-----------------|------|
| Manual Vite 8 migration/debugging | ~14,000 | 90-120 min |
| With This Skill | ~7,000 | 30-45 min |
| **Savings** | **50%** | **~60 min** |

## Reference Documentation

For deeper guidance on the most failure-prone areas, see:

| Topic | Reference File | Purpose |
|-------|----------------|---------|
| **Core Config** | [`core-config-reference.md`](references/core-config-reference.md) | CLI, config loading, `rolldownOptions`, `oxc`, and environment config |
| **Plugin Environments** | [`plugin-environment-reference.md`](references/plugin-environment-reference.md) | `this.environment`, `configEnvironment`, `hotUpdate`, and hook filters |
| **Build / SSR / Migration** | [`build-ssr-migration-reference.md`](references/build-ssr-migration-reference.md) | Rolldown/Oxc migration, SSR, Module Runner, and production build guidance |

See the [References Index](references/README.md) for navigation.

## File Structure

```
vite-v8/
├── SKILL.md        # Quick-start patterns, critical rules, and practical guidance
├── README.md       # This file - discovery and quick reference
└── references/
    ├── README.md                          # Reference index
    ├── core-config-reference.md          # Config and CLI patterns
    ├── plugin-environment-reference.md   # Environment-aware plugin authoring
    └── build-ssr-migration-reference.md  # Build, SSR, and migration guidance
```

## Dependencies

| Package | Version | Verified |
|---------|---------|----------|
| `vite` | ^8 | 2026-04-12 |
| `node` | >=20.19 or >=22.12 | 2026-04-12 |

## Official Documentation

- [Vite Docs](https://vite.dev/)
- [LLM Index](https://vite.dev/llms.txt)
- [Config Reference](https://vite.dev/config/)
- [Plugin API](https://vite.dev/guide/api-plugin.html)
- [Build Guide](https://vite.dev/guide/build)
- [SSR Guide](https://vite.dev/guide/ssr)
- [Environment API](https://vite.dev/guide/api-environment)

## Related Skills

- `vitest-v4` - Vitest workflows when the problem is test-runner specific rather than Vite build/runtime specific
- `github-actions` - CI workflow authoring when Vite builds and previews run in GitHub Actions

---

**License:** MIT
