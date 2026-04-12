# TypeScript 6 Migration Reference

Use this reference when a project is moving from TypeScript 5.x-era assumptions into TypeScript 6 behavior.

## High-Impact Migration Changes

### 1. Re-check ambient globals

Projects that rely on Node.js, test, Worker, or Bun globals should make `types` explicit instead of relying on broad ambient discovery.

```json
{
  "compilerOptions": {
    "types": ["node", "jest"]
  }
}
```

### 2. Make `rootDir` explicit

```json
{
  "compilerOptions": {
    "rootDir": "./src",
    "outDir": "./dist"
  },
  "include": ["src/**/*"]
}
```

This avoids surprising emit-path shifts such as `dist/src/...`.

### 3. Replace deprecated config early

Look for old settings like:

- `moduleResolution: "node"` / `"node10"`
- `baseUrl`
- `downlevelIteration`
- `target: "es5"`

Move to `bundler` or `nodenext`, direct `paths`, and more modern targets first.

### 4. Use the compiler before editing code

```bash
npx tsc --noEmit
npx tsc --showConfig
npx tsc --explainFiles
npx tsc --traceResolution
```

These commands usually explain the upgrade faster than rewriting source files blindly.

### 5. Keep `ignoreDeprecations` temporary

```json
{
  "compilerOptions": {
    "ignoreDeprecations": "6.0"
  }
}
```

Use it to create breathing room, then remove it once the real replacements land.

## Migration Checklist

- [ ] `rootDir` is explicit if sources live below the `tsconfig.json`
- [ ] `types` is explicit where ambient globals matter
- [ ] `moduleResolution` is `bundler` or `nodenext`
- [ ] deprecated options are removed or scheduled for removal
- [ ] `tsc --showConfig` and `tsc --explainFiles` were used if behavior is still surprising
- [ ] runtime support for `Temporal`, `RegExp.escape`, and `Map.getOrInsert*` was checked separately

## Quick Reference

| Change Area | What To Check |
|-------------|---------------|
| Ambient globals | `types` entries |
| Emit layout | `rootDir`, `outDir`, `include` |
| Module resolution | `bundler` vs `nodenext` |
| Legacy config | `baseUrl`, `downlevelIteration`, ES5-era targets |
| Debugging | `--showConfig`, `--explainFiles`, `--traceResolution` |
