# Vite 8 Plugin Environment Reference

Vite 8 plugin authoring is increasingly environment-aware.

## Current Environment Access

Use `this.environment` inside plugin hooks when behavior depends on the active runtime.

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
