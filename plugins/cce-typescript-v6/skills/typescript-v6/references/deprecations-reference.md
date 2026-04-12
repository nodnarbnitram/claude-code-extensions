# TypeScript 6 Deprecations Reference

TypeScript 6 keeps compatibility pressure high so TS 7 does not need to carry legacy configuration forever.

## Deprecated Options You Should Act On

| Deprecated | Replace With |
|------------|--------------|
| `moduleResolution: "node"` / `"node10"` | `"bundler"` for bundled apps or `"nodenext"` for Node.js packages |
| `moduleResolution: "classic"` | Removed in TS 6 — replace with `"bundler"` or `"nodenext"` |
| `target: "es5"` | `"es2015"` minimum, usually something more modern |
| `downlevelIteration` | Remove it |
| `baseUrl` | Use direct `paths` entries |
| `skipDefaultLibCheck` | Removed — use `skipLibCheck` only if you intentionally want broader lib checking skipped |
| legacy non-modern module targets such as AMD/UMD/System/none | Use `esnext`, `preserve`, `commonjs`, or `nodenext` as appropriate |

## `baseUrl` Migration

```json
// Before
{
  "compilerOptions": {
    "baseUrl": "./src",
    "paths": {
      "@app/*": ["app/*"]
    }
  }
}
```

```json
// After
{
  "compilerOptions": {
    "paths": {
      "@app/*": ["./src/app/*"]
    }
  }
}
```

## `ignoreDeprecations` Guidance

```json
{
  "compilerOptions": {
    "ignoreDeprecations": "6.0"
  }
}
```

Use this when the migration has multiple moving pieces and you need a short window to replace deprecated settings. Remove it before the repo treats TS 6 as "done".

## Recommended Strategy

1. Make `types` and `rootDir` explicit first
2. Replace deprecated resolution/module settings next
3. Remove `baseUrl` and other legacy options
4. Keep `ignoreDeprecations: "6.0"` only until the new config is stable
