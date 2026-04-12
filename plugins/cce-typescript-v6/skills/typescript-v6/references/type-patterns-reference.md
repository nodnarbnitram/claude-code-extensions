# TypeScript 6+ Type Patterns Reference

These patterns are **not new in TS 6**, but they are especially useful in TypeScript 6+ projects when the codebase exposes unclear contracts, widened literals, or incomplete unions.

## `satisfies` for Config and Option Objects

```ts
const compilerMode = {
  moduleResolution: 'bundler',
  strict: true,
} satisfies {
  moduleResolution: 'bundler' | 'nodenext';
  strict: boolean;
};
```

Use this when you want validation without widening away the useful literal types.

## Exhaustive Union Handling

```ts
type ResolutionMode = 'bundler' | 'nodenext' | 'preserve';

function describeMode(mode: ResolutionMode) {
  switch (mode) {
    case 'bundler':
      return 'bundled app';
    case 'nodenext':
      return 'node-style runtime';
    case 'preserve':
      return 'mixed emit strategy';
    default: {
      const exhaustive: never = mode;
      return exhaustive;
    }
  }
}
```

Use this when config, runtime, or state unions change and you need the compiler to prove coverage.

## Assertion Functions

```ts
function assertNodeTypes(types: string[] | undefined): asserts types is string[] {
  if (!types || !types.includes('node')) {
    throw new Error('Expected Node types to be configured');
  }
}
```

Use assertion functions when migration checks need to narrow unknown or optional data from config readers, CLI inputs, or JSON loading.

## Branded IDs and Nominal Separation

```ts
type Brand<T, B extends string> = T & { readonly __brand: B };
type PackageName = Brand<string, 'PackageName'>;
```

This is useful when migration tooling or repo scripts pass around multiple plain strings that should not be mixed up.

## Result Pattern for Type-Safe Operations

```ts
type Result<T, E = Error> =
  | { success: true; value: T }
  | { success: false; error: E };
```

Use this when upgrade helpers or config loaders need explicit success/error control flow instead of exceptions.

## Quick Reference

| Pattern | Use When |
|---------|----------|
| `satisfies` | config or option objects should stay literal-precise |
| exhaustive `never` | unions changed and every branch must be handled |
| assertion functions | optional/unknown values must be narrowed safely |
| branded types | plain strings/IDs should not be mixed accidentally |
| `Result<T, E>` | upgrade helpers need explicit typed success/failure |
