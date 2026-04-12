# Vitest 4 Skill References

Use these references when the main `SKILL.md` is not enough:

| File | Focus |
|------|-------|
| [`mocking-reference.md`](mocking-reference.md) | `vi.mock`, `vi.fn`, `vi.spyOn`, env/global stubs, hoisting, and cleanup rules |
| [`browser-mode-reference.md`](browser-mode-reference.md) | Provider setup, `vitest/browser`, event realism, screenshots, and Browser Mode caveats |
| [`coverage-projects-reference.md`](coverage-projects-reference.md) | V8/Istanbul coverage setup, `coverage.include`, and multi-project config |
| [`pools-execution-reference.md`](pools-execution-reference.md) | forks vs threads, isolation tradeoffs, fs module cache, and large-suite execution tuning |

## Suggested Reading Order

- **Writing or fixing mocks?** Start with `mocking-reference.md`
- **Running tests in a real browser?** Start with `browser-mode-reference.md`
- **Fixing coverage or multi-project config?** Start with `coverage-projects-reference.md`
- **Tuning speed or debugging runner instability?** Start with `pools-execution-reference.md`

## Official Sources

- [Vitest v4 Docs](https://v4.vitest.dev/)
- [LLM Index](https://v4.vitest.dev/llms.txt)
- [Writing Tests with AI](https://v4.vitest.dev/guide/learn/writing-tests-with-ai)
