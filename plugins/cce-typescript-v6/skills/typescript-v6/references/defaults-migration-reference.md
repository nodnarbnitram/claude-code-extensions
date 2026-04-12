# TypeScript 6 Defaults and Migration Reference

TypeScript 6 is a migration-heavy release because several assumptions that used to stay implicit often need to become explicit during real upgrades.

## Highest-Impact Upgrade Checks

### 1. Make `types` explicit

If a project depends on Node.js globals, a test runner, Workers, or Bun globals, add the exact type packages it needs instead of relying on ambient discovery.

```json
{
  "compilerOptions": {
    "types": ["node", "jest"]
  }
}
```

This improves both performance and predictability compared with older "load everything from `@types`" assumptions.

### 2. Make `rootDir` explicit

If the source tree lives under `src/`, TypeScript 6 upgrades often need this:

```json
{
  "compilerOptions": {
    "rootDir": "./src",
    "outDir": "./dist"
  },
  "include": ["src/**/*"]
}
```

Without it, some projects can see emitted files shift from `dist/index.js` to `dist/src/index.js`.

### 3. Keep `strict` deliberate

If the project already uses strict mode, keep it explicit. If the repo truly needs looser semantics during a staged migration, say so explicitly instead of assuming older defaults.

```json
{
  "compilerOptions": {
    "strict": false
  }
}
```

### 4. Keep `target` / `lib` intentional

Use modern library types only when the project can support them.

```json
{
  "compilerOptions": {
    "target": "es2025",
    "lib": ["es2025", "dom"]
  }
}
```

## Migration Baselines

### Bundled web app

```json
{
  "compilerOptions": {
    "target": "es2025",
    "module": "esnext",
    "moduleResolution": "bundler",
    "lib": ["es2025", "dom"],
    "rootDir": "./src",
    "outDir": "./dist",
    "strict": true
  },
  "include": ["src/**/*"]
}
```

Add a `types` array here only if the app or its tooling actually needs Node/test/platform globals.

### Node package

```json
{
  "compilerOptions": {
    "target": "es2022",
    "module": "nodenext",
    "moduleResolution": "nodenext",
    "lib": ["es2022"],
    "rootDir": "./src",
    "outDir": "./dist",
    "types": ["node"],
    "strict": true
  },
  "include": ["src/**/*"]
}
```

## Temporary Escape Hatch

```json
{
  "compilerOptions": {
    "ignoreDeprecations": "6.0"
  }
}
```

Use this only to buy time while you remove deprecated settings. Do not treat it as a permanent upgrade strategy.
