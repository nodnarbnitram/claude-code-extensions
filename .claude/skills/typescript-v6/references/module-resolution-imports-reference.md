# TypeScript 6 Module Resolution and Imports Reference

The most important TypeScript 6 module-resolution decision is whether the project is primarily a **bundled app** or a **Node.js package/runtime**.

## Choose `bundler` for bundled apps

```json
{
  "compilerOptions": {
    "module": "esnext",
    "moduleResolution": "bundler"
  }
}
```

Use this for Vite, Rollup, esbuild, Webpack, and similar build-driven applications.

## Choose `nodenext` for modern Node.js packages

```json
{
  "compilerOptions": {
    "module": "nodenext",
    "moduleResolution": "nodenext"
  }
}
```

Use this when package exports, ESM/CJS interop, and Node's native resolver should define behavior.

## `#/` Subpath Imports

TypeScript 6 supports Node's `#/`-style subpath imports under `bundler` and `nodenext` resolution modes.

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

## Alias Decision Heuristic

- Use `paths` when you need TypeScript/build-tool aliasing inside a project
- Use package `imports` with `#/` when you want a Node-native, package-internal alias strategy
- Do not mix strategies casually; keep runtime and compiler expectations aligned

## Common Failure Mode

If `#/` imports compile but fail at runtime, the runtime or package metadata likely does not actually support the same alias behavior yet, or the mapping does not match the files the package ships.
