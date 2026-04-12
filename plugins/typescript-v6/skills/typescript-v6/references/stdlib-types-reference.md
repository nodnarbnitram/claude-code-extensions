# TypeScript 6 Standard Library Types Reference

TypeScript 6 adds or promotes several useful standard-library types. The compiler can understand them before every runtime ships them, so verify runtime support separately.

## `es2025`

```json
{
  "compilerOptions": {
    "target": "es2025",
    "lib": ["es2025", "dom"]
  }
}
```

This gives access to TS 6-era built-in types such as `RegExp.escape` and other APIs moved from `esnext` into `es2025`.

## `RegExp.escape`

```ts
function buildWordMatcher(word: string) {
  const escaped = RegExp.escape(word);
  return new RegExp(`\\b${escaped}\\b`, 'g');
}
```

Use this instead of hand-rolled regex escaping.

## `Temporal`

Use `Temporal` with `esnext`/`esnext.temporal` typing support when the environment and project actually intend to adopt it.

```ts
const tomorrow = Temporal.Now.instant().add({ hours: 24 });
```

## `Map.getOrInsert` / `getOrInsertComputed`

```ts
const counts = new Map<string, number>();

counts.getOrInsert('retries', 0);
counts.getOrInsertComputed('cache-key', () => expensiveDefault());
```

These are nice ergonomics wins, but they are still subject to runtime support constraints.

## DOM Iterables Simplification

TypeScript 6 folds iterable DOM support into `dom`, so modern browser-focused projects often no longer need a separate `dom.iterable` entry.
