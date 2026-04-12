# Vitest 4 Mocking Reference

Vitest 4 uses the `vi` utility for mocks, spies, stubs, and timers. Prefer Vitest-native patterns over Jest-compatible muscle memory.

## Core APIs

- `vi.fn()` - create a mock function
- `vi.spyOn(obj, 'method')` - spy on a property or method in Node/jsdom mode
- `vi.mock(import('./module'), factory)` - mock a module with type-safe imports
- `vi.stubEnv('NAME', 'value')` - stub env values
- `vi.stubGlobal('fetch', mock)` - stub globals

## Architecture Note

Vitest 4 runs on Vite's native Module Runner rather than the older `vite-node` executor model. That matters because seemingly odd mocking or path-resolution behavior is often runner-related, not just test-code related.

## Type-safe module mock pattern

```typescript
import { vi } from 'vitest';
import * as api from './api';

vi.mock(import('./api'), () => ({
  fetchUser: vi.fn(),
}));

vi.mocked(api.fetchUser).mockResolvedValue({ id: '1', name: 'Ada' });
```

## Hoisting rule

`vi.mock()` is hoisted. Treat it like a file-level declaration, not normal runtime code.

If local variables are needed before the mock factory runs, reach for `vi.hoisted()` instead of trying to outsmart hoisting with ordinary top-level state.

```typescript
const { mockToken } = vi.hoisted(() => ({
  mockToken: 'test-token',
}));
```

### Bad pattern

```typescript
const token = makeToken();

vi.mock(import('./auth'), () => ({
  getToken: () => token,
}));
```

### Better pattern

```typescript
const mockedGetToken = vi.fn();

vi.mock(import('./auth'), () => ({
  getToken: mockedGetToken,
}));
```

## Cleanup strategy

Prefer config-driven cleanup whenever possible:

```typescript
test: {
  restoreMocks: true,
  clearMocks: true,
  unstubEnvs: true,
  unstubGlobals: true,
}
```

Use per-test cleanup only when a project intentionally leaves some state intact.

## Importing the real implementation

Use `vi.importActual()` when you need a partial mock that preserves most of the original module:

```typescript
vi.mock(import('./math'), async () => {
  const actual = await vi.importActual<typeof import('./math')>('./math');

  return {
    ...actual,
    add: vi.fn(() => 10),
  };
});
```

## Non-hoisted mocking

Use `vi.doMock()` when the mock must be created later at runtime rather than hoisted at module load time.

## Constructor behavior

Vitest 4 improved constructor-aware spying and mocking. This matters in class-heavy code because `new` calls now behave more predictably under `vi.spyOn()` / `vi.fn()` than many older examples suggest.

## Module directories

When debugging custom module resolution behavior, know that older `VITE_NODE_DEPS_MODULE_DIRECTORIES` references have moved to `VITEST_MODULE_DIRECTORIES` in the new architecture.

## Timers

For timer-driven code, prefer explicit fake timer control:

```typescript
vi.useFakeTimers();
vi.advanceTimersByTime(1000);
vi.useRealTimers();
```

## Constructors in Vitest 4

Vitest 4 supports constructor-aware `vi.fn()` and `vi.spyOn()` behavior, which makes class-heavy mocks less awkward than older releases.

## Browser Mode caveat

Do **not** rely on `vi.spyOn(moduleNamespace, 'exportedFn')` in Browser Mode. Browser ESM namespace objects are sealed.

Use:

```typescript
vi.mock(import('./module'), { spy: true });
```

instead of:

```typescript
vi.spyOn(moduleNamespace, 'exportedFn');
```
