# Vitest 4 Coverage and Projects Reference

Vitest 4 tightened a few configuration details that commonly break older examples.

## Coverage providers

Choose one:

- `@vitest/coverage-v8` - usually the fastest option
- `@vitest/coverage-istanbul` - useful when Istanbul-specific behavior is needed

Vitest 4 improved V8 coverage accuracy with AST-based remapping, so V8 is now a strong default for most projects.

## Important coverage change

`coverage.all` and `coverage.extensions` are removed in Vitest 4.

Vitest 4 also changed V8 coverage remapping to an AST-based approach, so coverage percentages can legitimately shift after upgrade even when your source code did not change.

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

The key gotcha is inheritance: treat project configs as explicit units. Shared concerns like reporters, coverage, or common setup should be intentionally factored into a base config via `extends: true` or `mergeConfig`, not assumed to flow in automatically.

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

## AI-output optimization note

Vitest 4 includes agent-aware output behavior in some reporting flows. When optimizing for AI or CI summaries, prefer compact summary output over huge raw reports unless a human is actively diagnosing coverage deltas.

## Reference pattern for shared base config

```typescript
import { defineConfig, mergeConfig } from 'vitest/config';

const shared = defineConfig({
  test: {
    restoreMocks: true,
    coverage: {
      provider: 'v8',
    },
  },
});
```
