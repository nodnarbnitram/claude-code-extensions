# Vite 8 Build, SSR, and Migration Reference

Vite 8 unifies more of the dev/build/runtime story around Rolldown and environment-aware execution.

## Rolldown and Oxc Migration

The main migration points are:

- `build.rollupOptions` → `build.rolldownOptions`
- `esbuild` → `oxc`
- legacy HMR/plugin assumptions → environment-aware hooks and filters

Also watch for older config snippets that still talk about esbuild CSS minification or Rollup-specific extension points as the preferred path. In Vite 8, those examples are often historically accurate but strategically wrong.

## SSR Guidance

SSR issues in Vite 8 are often runtime-boundary issues rather than plain bundling issues. Review:

- `environments`
- `this.environment`
- `ssr.noExternal`
- Module Runner concepts

## Module Runner

Modern Vite SSR/runtime execution is better explained through Module Runner mental models than older `ssrLoadModule`-centric guidance.

When SSR debugging feels like “the bundle built but runtime is wrong,” it is often a Module Runner or environment-boundary problem rather than a bundling one.

## CSS and Build Output

Lightning CSS is the modern default direction, and build behavior should be validated under the same Vite 8 assumptions used in dev.

## Rollup Hook Caveat

Some Rollup hooks behave differently under Rolldown-era execution, especially assumptions about parallelism or dev-only parsing behavior. Do not assume every historical Rollup performance trick still maps 1:1.

## Production Checklist

- Run `vite build`
- Run `vite build --ssr <entry>` when SSR applies
- Run `vite preview`
- Validate runtime-specific behavior after externalization decisions
