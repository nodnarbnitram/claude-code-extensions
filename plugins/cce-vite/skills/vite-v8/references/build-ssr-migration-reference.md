# Vite 8 Build, SSR, and Migration Reference

Vite 8 unifies more of the dev/build/runtime story around Rolldown and environment-aware execution.

## Rolldown and Oxc Migration

The main migration points are:

- `build.rollupOptions` → `build.rolldownOptions`
- `esbuild` → `oxc`
- legacy HMR/plugin assumptions → environment-aware hooks and filters

## SSR Guidance

SSR issues in Vite 8 are often runtime-boundary issues rather than plain bundling issues. Review:

- `environments`
- `this.environment`
- `ssr.noExternal`
- Module Runner concepts

## Module Runner

Modern Vite SSR/runtime execution is better explained through Module Runner mental models than older `ssrLoadModule`-centric guidance.

## CSS and Build Output

Lightning CSS is the modern default direction, and build behavior should be validated under the same Vite 8 assumptions used in dev.

## Production Checklist

- Run `vite build`
- Run `vite build --ssr <entry>` when SSR applies
- Run `vite preview`
- Validate runtime-specific behavior after externalization decisions
