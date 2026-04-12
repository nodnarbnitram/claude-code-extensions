# Vite 8 Plugin Environment Reference

Vite 8 plugin authoring is increasingly environment-aware.

## Current Environment Access

Use `this.environment` inside plugin hooks when behavior depends on the active runtime.

This is a real architectural shift away from simplistic `ssr` booleans. When a plugin touches multiple runtimes, environment identity should drive the design.

## Environment-Specific Config

```typescript
export default function myPlugin() {
  return {
    name: 'my-plugin',
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

## HMR Direction

Prefer `hotUpdate` for modern, environment-aware HMR customization rather than building new logic around `handleHotUpdate`.

## Hook Filters

Use hook filters to reduce unnecessary cross-runtime work when plugins run across Rust↔JS boundaries.

```typescript
transform: {
  filter: {
    id: /\.(ts|tsx)$/,
  },
  handler(code, id) {
    return { code, map: null };
  },
}
```

## Shared Build Plugins

When a plugin must be shared across environments during build, review `sharedDuringBuild` or related builder-sharing settings instead of assuming old single-pipeline behavior.

## Rolldown Detection

When debugging plugin compatibility, `this.meta.rolldownVersion` can help detect whether the plugin is running under the new engine assumptions.

## Module Type Hint

If a `load` or `transform` hook turns non-JS content into executable JS, return `moduleType: 'js'` so Rolldown can classify it correctly.
