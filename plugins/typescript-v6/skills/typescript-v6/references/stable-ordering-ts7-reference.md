# TypeScript 6 `stableTypeOrdering` and TS 7 Context Reference

TypeScript 6 is partly a bridge release toward TypeScript 7. One of the migration tools added in TS 6 is `--stableTypeOrdering`.

## What `--stableTypeOrdering` Is For

```bash
npx tsc --noEmit --stableTypeOrdering
```

Use it when:

- comparing TS 6 and TS 7 behavior
- reducing noisy declaration-output diffs during migration work
- investigating type-order-sensitive inference changes

## What It Is Not For

- normal development builds
- CI defaults for everyday projects
- performance tuning

It can add noticeable type-checking overhead.

## If It Reveals New Errors

That usually means previous inference depended on unstable ordering. The fix is usually to make intent explicit.

```ts
// Prefer explicit annotations when inference starts to wobble
const config: SomeExplicitType = buildConfig();
someFunction<SomeExplicitType>(config);
```

## TS 7 Context

Keep TS 7 context high-level in TS 6 work:

- TS 6 is the practical migration surface today
- TS 7 context matters because TS 6 deprecations are preparing for that future
- Do not treat TS 7 preview behavior as the default answer unless the user explicitly targets it
