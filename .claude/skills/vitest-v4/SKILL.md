---
name: vitest-v4
description: "Vitest 4+ testing with Vite. Use when configuring vitest.config.ts, writing unit/integration/browser tests, implementing mocks with vi.fn/vi.spyOn/vi.mock, setting up V8 or Istanbul coverage, or migrating from Jest or older Vitest workspace setups. Triggers on vitest, vitest.config.ts, vi.mock, browser mode, vitest/browser, projects, setupFiles, and toMatchScreenshot."
version: 1.0.0
metadata:
  author: Brandon Martin
---

# Vitest 4 Testing Skill

> Write, configure, and debug Vitest 4 test suites with Vite-native patterns.

## Before You Start

**This skill prevents 7+ common Vitest 4 mistakes and saves ~50% tokens.**

| Metric | Without Skill | With Skill |
|--------|--------------|------------|
| Setup Time | ~90 min | ~30 min |
| Common Errors | 7+ | 0 |
| Token Usage | High (trial/error) | Low (known patterns) |

### Known Issues This Skill Prevents

1. Hanging agent runs from using watch mode instead of `vitest run`
2. Broken coverage configs from using removed `coverage.all` or `coverage.extensions`
3. Browser Mode spying failures from sealed ESM namespace objects
4. Mock leakage between tests from missing restore/reset config
5. Invalid multi-project setup from using deprecated `workspace` terminology
6. Wrong APIs from mixing Jest helpers into Vitest tests
7. Flaky browser interactions from using synthetic helpers instead of `vitest/browser`
8. Slow or unstable large suites from choosing the wrong execution pool or isolation mode

## Quick Start

### Step 1: Configure Vitest 4 for agent-safe runs

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    environment: 'node',
    restoreMocks: true,
    clearMocks: true,
    coverage: {
      provider: 'v8',
      include: ['src/**/*.{ts,tsx}'],
    },
  },
});
```

**Why this matters:** Vitest 4 removed `coverage.all` and `coverage.extensions`, and agent/CI environments need one-shot execution plus automatic mock cleanup.

### Step 2: Write tests with Vitest APIs, not Jest APIs

```typescript
import { describe, expect, it, vi } from 'vitest';
import { addUser } from './add-user';
import * as api from './api';

describe('addUser', () => {
  it('returns the created user', async () => {
    vi.spyOn(api, 'createUser').mockResolvedValue({ id: '1', name: 'Ada' });

    await expect(addUser('Ada')).resolves.toEqual({ id: '1', name: 'Ada' });
  });
});
```

**Why this matters:** `vi` is the supported mocking API. Mixing `jest.fn()` or Jest-only patterns causes confusing failures and poor autocomplete.

> **Import rule:** Import `describe`, `it`, `expect`, and `vi` from `vitest` unless the project explicitly enables `globals: true`.

### Step 3: Use the correct runtime command

```bash
vitest run
vitest run --coverage
vitest run path/to/example.test.ts
```

**Why this matters:** `vitest` without `run` starts watch mode by default in development, which is a poor fit for agents, CI, and non-interactive verification.

## Critical Rules

### Always Do

- Use `vitest run` or `vitest --no-watch` for agent and CI workflows
- Prefer `vi.mock(import('./module'))` for type-safe module mocks
- Configure `restoreMocks`, `clearMocks`, or `mockReset` intentionally
- Use `projects` for multi-project configs; the rename began in Vitest 3.2 and older workspace-file usage is removed in Vitest 4
- Use a shared base config when multiple `projects` need common settings; projects do not inherit root config unless you opt in
- Use `coverage.include` to report on untested source files
- Use `page` and `userEvent` from `vitest/browser` in Browser Mode
- Prefer `forks` when native modules or runtime compatibility matter more than raw speed
- Share `vitest.config.ts` and the implementation file when asking AI to generate tests

### Never Do

- Never use `jest.fn`, `jest.spyOn`, or Jest-only globals in Vitest code
- Never rely on removed `coverage.all` or `coverage.extensions` in Vitest 4
- Never use plain watch mode for agent-driven verification
- Never use `vi.spyOn` on native ESM exports in Browser Mode
- Never forget that `vi.mock()` is hoisted before the rest of the file executes
- Never leave env/global stubs un-restored across tests

### Common Mistakes

**Wrong - removed coverage option:**
```typescript
export default defineConfig({
  test: {
    coverage: {
      all: true,
    },
  },
});
```

**Correct - use include globs:**
```typescript
export default defineConfig({
  test: {
    coverage: {
      provider: 'v8',
      include: ['src/**/*.{ts,tsx}'],
    },
  },
});
```

**Why:** Vitest 4 removed `coverage.all` and `coverage.extensions`; `coverage.include` is the supported way to include uncovered files.

**Wrong - Browser Mode spy on sealed export:**
```typescript
import * as math from './math';
import { vi } from 'vitest';

vi.spyOn(math, 'add').mockReturnValue(10);
```

**Correct - use spy-enabled module mock:**
```typescript
import { vi } from 'vitest';

vi.mock(import('./math'), { spy: true });
```

**Why:** Native browser ESM namespace objects are sealed, so direct spies on exports fail in Browser Mode.

## Known Issues Prevention

| Issue | Root Cause | Solution |
|-------|-----------|----------|
| Tests never exit | Watch mode started in a non-interactive session | Use `vitest run` |
| Coverage report misses untested files | `coverage.include` not configured | Add explicit source globs |
| Browser Mode spy throws or does nothing | `vi.spyOn` used on sealed ESM exports | Use `vi.mock(import('./mod'), { spy: true })` |
| Mocks leak between tests | Cleanup flags missing | Enable `restoreMocks` / `clearMocks` / `unstubEnvs` |
| Multi-project config breaks after upgrade | Deprecated workspace terminology or removed workspace-file patterns carried over | Switch to `projects` and `defineProject` |
| Worker or pool config stops working | Old `maxThreads`, `maxForks`, or `poolOptions` carried forward | Migrate to Vitest 4 worker settings such as `maxWorkers` |
| Project-specific config unexpectedly disappears | Root config assumptions are not inherited into `projects` | Use `extends: true`, `mergeConfig`, or a shared base explicitly |
| AI-generated tests use wrong helpers | Jest patterns copied into Vitest | Replace with `vi`, Vitest imports, and Vitest matchers |
| Browser tests hang | Blocking dialogs or wrong user-event utilities | Mock dialogs and use `vitest/browser` helpers |
| Fast pool causes strange native-module failures | `threads` chosen for a suite that needs process isolation | Switch to `forks` or narrow thread usage |

## Bundled Resources

### References

- **Mocking rules and hoisting** → [`references/mocking-reference.md`](references/mocking-reference.md)
- **Browser Mode providers and pitfalls** → [`references/browser-mode-reference.md`](references/browser-mode-reference.md)
- **Coverage and multi-project config** → [`references/coverage-projects-reference.md`](references/coverage-projects-reference.md)
- **Pools, isolation, and persistent cache** → [`references/pools-execution-reference.md`](references/pools-execution-reference.md)
- **Reference index** → [`references/README.md`](references/README.md)

## Configuration Reference

### vitest.config.ts

```typescript
import { defineConfig, defineProject } from 'vitest/config';
import { playwright } from '@vitest/browser-playwright';

export default defineConfig({
  test: {
    projects: [
      defineProject({
        test: {
          name: 'unit',
          include: ['src/**/*.test.ts'],
          environment: 'node',
        },
      }),
      defineProject({
        test: {
          name: 'browser',
          include: ['src/**/*.browser.test.ts'],
          browser: {
            enabled: true,
            provider: playwright(),
            instances: [{ browser: 'chromium' }],
          },
        },
      }),
    ],
    coverage: {
      provider: 'v8',
      include: ['src/**/*.{ts,tsx}'],
    },
    restoreMocks: true,
    unstubEnvs: true,
    setupFiles: ['./test/setup.ts'],
  },
});
```

**Key settings:**
- `test.projects`: Stable multi-project terminology; the rename started in Vitest 3.2, and projects do not automatically inherit every root config value, so shared settings should be factored into a reused base when needed
- `coverage.include`: Required when uncovered source files must appear in the report
- `browser.provider`: In Vitest 4, import the provider factory from the provider package, such as `playwright()`
- `restoreMocks` / `unstubEnvs`: Prevent test pollution across files
- `setupFiles`: Run shared test initialization such as MSW, globals, or polyfills before test files

## Project Structure

```
my-app/
├── src/
│   ├── feature.ts
│   ├── feature.test.ts
│   └── feature.browser.test.ts
├── vitest.config.ts
├── vite.config.ts
└── package.json
```

**Why this matters:** Keeping Node and Browser Mode tests clearly separated makes provider setup, test selection, and troubleshooting much simpler.

**Choose the right environment:** Prefer `jsdom` for most component tests and lightweight DOM assertions. Use Browser Mode when native browser APIs, real layout/event behavior, or screenshot assertions matter.

**Choose the right execution model:** Prefer `forks` for stability and native-module compatibility, especially in mixed or infrastructure-heavy suites. Reach for `threads` only when you know the test environment is safe for worker-thread execution and the extra speed matters.

## Common Patterns

### Type-safe module mock pattern

```typescript
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { getUserName } from './get-user-name';
import * as api from './api';

vi.mock(import('./api'), () => ({
  fetchUser: vi.fn(),
}));

describe('getUserName', () => {
  beforeEach(() => {
    vi.mocked(api.fetchUser).mockReset();
  });

  it('returns the fetched user name', async () => {
    vi.mocked(api.fetchUser).mockResolvedValue({ id: '1', name: 'Ada' });

    await expect(getUserName('1')).resolves.toBe('Ada');
  });
});
```

### Browser Mode interaction pattern

```typescript
import { expect, test } from 'vitest';
import { page, userEvent } from 'vitest/browser';
import { render } from 'vitest-browser-react';
import { Counter } from './counter';

test('increments after click', async () => {
  render(<Counter />);

  await userEvent.click(page.getByRole('button', { name: /increment/i }));

  await expect.element(page.getByText('1')).toBeInTheDocument();
});
```

### In-source testing pattern

```typescript
export function sum(a: number, b: number) {
  return a + b;
}

if (import.meta.vitest) {
  const { it, expect } = import.meta.vitest;

  it('adds numbers', () => {
    expect(sum(1, 2)).toBe(3);
  });
}
```

## Dependencies

### Required

| Package | Version | Purpose |
|---------|---------|---------|
| `vitest` | ^4 | Test runner and assertion/mocking APIs |
| `vite` | ^6 | Shared Vite-powered module pipeline |
| `node` | >=20 | Required runtime for Vitest 4 |

### Optional

| Package | Version | Purpose |
|---------|---------|---------|
| `@vitest/coverage-v8` | ^4 | Fast, accurate coverage with AST remapping |
| `@vitest/coverage-istanbul` | ^4 | Istanbul coverage backend |
| `@vitest/browser-playwright` | ^4 | Playwright provider for Browser Mode |
| `@vitest/browser-webdriverio` | ^4 | WebdriverIO provider for Browser Mode |
| `@vitest/browser-preview` | ^4 | Preview provider for Browser Mode |

## Official Documentation

- [Vitest v4 Docs](https://v4.vitest.dev/)
- [LLM index](https://v4.vitest.dev/llms.txt)
- [Mocking Guide](https://v4.vitest.dev/guide/mocking)
- [Browser Mode Guide](https://v4.vitest.dev/guide/browser)
- [Coverage Guide](https://v4.vitest.dev/guide/coverage)
- [Projects Guide](https://v4.vitest.dev/guide/projects)
- [Writing Tests with AI](https://v4.vitest.dev/guide/learn/writing-tests-with-ai)

## Troubleshooting

### Agent run hangs forever

**Symptoms:** The test process never exits or Claude waits for additional file changes.

**Solution:**
```bash
vitest run
```

### Browser Mode test cannot spy on export

**Symptoms:** `vi.spyOn()` throws, does nothing, or works in Node mode but fails in browser.

**Solution:**
```typescript
vi.mock(import('./module'), { spy: true });
```

### Coverage misses source files with no tests

**Symptoms:** The report only contains files touched by executed tests.

**Solution:**
```typescript
coverage: {
  provider: 'v8',
  include: ['src/**/*.{ts,tsx}'],
}
```

### Legacy worker or pool settings break after upgrade

**Symptoms:** Old `maxThreads`, `maxForks`, `singleThread`, `singleFork`, or `poolOptions` settings stop working after moving to Vitest 4.

**Solution:**
```typescript
test: {
  maxWorkers: 4,
}
```

**Why:** Vitest 4 simplified worker configuration and removed several older pool-specific options.

## Setup Checklist

Before using this skill, verify:

- [ ] Node.js is `>=20`
- [ ] `vite` is `>=6`
- [ ] `vitest.config.ts` or `vite.config.ts` contains a `test` block
- [ ] Agent/CI commands use `vitest run`
- [ ] Coverage provider packages are installed if coverage is enabled
- [ ] Browser provider packages are installed if Browser Mode is enabled
