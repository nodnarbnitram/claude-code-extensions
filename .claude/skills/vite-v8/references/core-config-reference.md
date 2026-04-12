# Vite 8 Core Config Reference

Vite 8 config should reflect the Rolldown/Oxc architecture rather than older Rollup/esbuild-era defaults.

## Core CLI

- `vite dev`
- `vite build`
- `vite build --ssr <entry>`
- `vite preview`

## Config Loading

Vite 8 supports config loading modes such as `bundle`, `runner`, and `native` via `--configLoader` when debugging config execution behavior.

## Preferred Config Surface

```typescript
import { defineConfig } from 'vite';

export default defineConfig({
  build: {
    rolldownOptions: {
      external: ['react'],
    },
  },
  oxc: {
    jsxInject: "import React from 'react'",
  },
  environments: {
    ssr: {},
  },
});
```

## Migration Notes

- Prefer `build.rolldownOptions` over `build.rollupOptions`
- Prefer `oxc` over `esbuild` in new Vite 8 guidance
- Default build targeting follows the Baseline Widely Available browser target
- Lightning CSS is part of the modern Vite 8 direction for CSS processing/minification

## Environment Configuration

Use `environments` when runtime behavior differs meaningfully between client, SSR, edge, or custom execution targets.
