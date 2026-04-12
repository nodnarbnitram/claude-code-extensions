# Vite v8 Performance and Dev Server Reference

Many Vite performance problems are graph-shape problems, not bundler-flag problems.

## First Things to Check

1. Barrel files that fan out a large import graph
2. Omitted file extensions that force more filesystem work
3. Hot files that would benefit from `server.warmup`
4. Config-loading failures better solved with `--configLoader runner`

## Warmup

Use `server.warmup` for files that are predictably hit during first-load waterfalls. This is especially useful in large applications where startup repeatedly touches the same routes, layouts, or plugin-heavy modules.

## Barrel File Warning

Barrel exports (`index.ts` re-export hubs) are convenient but can explode the graph surface Vite has to traverse. Before micro-tuning bundler config, inspect whether one broad barrel import is pulling in far more code than the page or plugin actually needs.

## Explicit Extensions

Explicit `.ts`, `.tsx`, `.js`, or `.jsx` imports can reduce resolution overhead and ambiguity in large repos.

## Config Loader Heuristic

If config execution behaves strangely in a monorepo or advanced TS setup, try `vite --configLoader runner` before concluding that the config itself is broken.

## Forward-Looking Note

Vite's full-bundle direction exists to reduce network overhead in very large codebases. Treat this as a clue that graph shape and startup waterfalls are first-class performance concerns in modern Vite, not afterthoughts.
