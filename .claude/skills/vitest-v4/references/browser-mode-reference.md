# Vitest 4 Browser Mode Reference

Browser Mode is stable in Vitest 4 and is the right choice when DOM behavior, native browser events, or screenshot assertions matter.

## Provider packages

Install one of:

- `@vitest/browser-playwright`
- `@vitest/browser-webdriverio`
- `@vitest/browser-preview`

`@vitest/browser-preview` is best treated as a local preview/debugging option rather than a CI-grade provider.

## Basic config

```typescript
import { defineConfig } from 'vitest/config';
import { playwright } from '@vitest/browser-playwright';

export default defineConfig({
  test: {
    browser: {
      enabled: true,
      provider: playwright(),
      instances: [{ browser: 'chromium' }],
    },
  },
});
```

In Vitest 4, Browser Mode providers use factory imports from the provider packages. Older string-style provider values belong to pre-v4 examples.

## Interaction helpers

Use helpers from `vitest/browser`, not generic synthetic helpers when native browser realism matters.

```typescript
import { page, userEvent } from 'vitest/browser';
```

This matters because Vitest Browser Mode is designed to work with the real browser runtime rather than a jsdom approximation.

When in doubt, prefer `userEvent` from `vitest/browser` over `@testing-library/user-event` because Vitest's browser helpers are designed to route through the real browser provider instead of simulating everything in-process.

## Screenshot testing

Vitest 4 includes built-in screenshot assertions like `toMatchScreenshot()`. Keep screenshot inputs deterministic and avoid random data or clock-dependent rendering.

Also separate screenshot suites from general interaction suites when provider startup cost or rendering determinism becomes a problem.

## Blocking dialogs

Avoid unmocked `alert`, `confirm`, and `prompt`. These can block browser communication and hang the run.

## Spying caveat

Native ESM namespace objects are sealed in the browser. Use `vi.mock(import('./module'), { spy: true })` instead of `vi.spyOn()` on module exports.

## Locator and assertion pattern

Prefer provider-native locator flows:

```typescript
await expect.element(page.getByRole('button', { name: /save/i })).toBeVisible();
```

Use the `expect.element(...)` wrapper for browser-element assertions rather than assuming standard Node-side matcher semantics.
