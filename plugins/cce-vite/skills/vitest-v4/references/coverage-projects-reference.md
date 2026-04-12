# Vitest 4 Coverage and Projects Reference

Vitest 4 tightened a few configuration details that commonly break older examples.

## Coverage providers

Choose one:

- `@vitest/coverage-v8` - usually the fastest option
- `@vitest/coverage-istanbul` - useful when Istanbul-specific behavior is needed

Vitest 4 improved V8 coverage accuracy with AST-based remapping, so V8 is now a strong default for most projects.

## Important coverage change

`coverage.all` and `coverage.extensions` are removed in Vitest 4.

Use `coverage.include` instead:

```typescript
coverage: {
  provider: 'v8',
  include: ['src/**/*.{ts,tsx}'],
}
```

Keep `include` focused on real source files. Do not point it at `node_modules`, build output, or broad repo-root globs.

## Projects replace workspace-style config

Vitest 4 uses `projects` as the stable term for multi-project setups. The rename started in Vitest 3.2, and older workspace-file usage is removed in Vitest 4.

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
    maxWorkers: 4,
  },
});
```

Use projects when environments differ meaningfully, like Node vs Browser Mode, or app vs package-level tests in a monorepo.

## Worker migration note

If an older config uses `maxThreads`, `maxForks`, `singleThread`, `singleFork`, or `poolOptions`, migrate those settings to Vitest 4 worker options such as `maxWorkers`.
