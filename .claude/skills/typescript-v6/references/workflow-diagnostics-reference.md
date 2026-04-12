# TypeScript 6 Workflow and Diagnostics Reference

Verify the compiler state early and often. In TypeScript 6+, that matters more than guessing at source-level fixes.

## Recommended Verification Loop

### 1. Check health before editing

```bash
npx tsc --noEmit
```

Use this as the first pass after a version bump, config rewrite, or unexplained compiler failure.

### 2. Confirm the real merged config

```bash
npx tsc --showConfig
```

Use this when the file says one thing but the compiler behaves like another. It is especially useful when `extends` chains or workspace-level config are involved.

### 3. See why a file is included

```bash
npx tsc --explainFiles
```

Use this to diagnose:

- unexpected `dist/src/...` emit roots
- test files or config files leaking into production builds
- monorepo package boundaries that are wider than expected

### 4. Trace module and type resolution

```bash
npx tsc --traceResolution
```

Use this when debugging:

- `paths` aliases
- `types` package discovery
- `package.json` `exports` / `imports`
- `#/` subpath imports under `bundler` or `nodenext`

## Agent-Safe Workflow

1. update config
2. run `npx tsc --noEmit`
3. if config still feels wrong, run `--showConfig`
4. if file inclusion still feels wrong, run `--explainFiles`
5. if import/type resolution still feels wrong, run `--traceResolution`
6. only then refactor source types or runtime code

## Monorepo / Project References

For package-based repos, make the emitting packages explicit.

```json
{
  "compilerOptions": {
    "composite": true,
    "declaration": true,
    "isolatedDeclarations": true,
    "rootDir": "./src",
    "outDir": "./dist"
  }
}
```

`composite` and `declaration` are not new in TS 6, but they pair well with TS 6's push toward more explicit config and faster incremental tooling.

## Quick Reference

| Command | Use When |
|---------|----------|
| `npx tsc --noEmit` | baseline compiler health check |
| `npx tsc --showConfig` | effective config looks different than expected |
| `npx tsc --explainFiles` | file graph or include/exclude behavior is confusing |
| `npx tsc --traceResolution` | path/type/module resolution is failing |
