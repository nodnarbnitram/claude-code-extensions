# TypeScript v6 Plugin

TypeScript 6 guidance for tsconfig migrations, deprecations, module resolution, and modern standard-library types.

## Overview

The **typescript-v6** plugin packages the repository's TypeScript 6 migration guidance into a self-contained Claude Code plugin. It is a **skill-only** package that ships the `typescript-v6` skill without bundling the existing Braintrust or fumadocs agents from `cce-typescript`.

If you want the existing Braintrust or fumadocs agents, install `cce-typescript` separately. This plugin is only for the TypeScript 6 skill.

## Included Components

### Skill

- `typescript-v6`

## Installation

### Plugin Mode

```bash
/plugin marketplace add github:nodnarbnitram/claude-code-extensions
/plugin install typescript-v6@cce-marketplace
```

### Standalone Mode

```bash
git clone https://github.com/nodnarbnitram/claude-code-extensions.git
cd claude-code-extensions
# Install into your project, then select only the typescript-v6 skill from this plugin's content
./install_extensions.py install ~/your-project
```

In standalone installs, keep the scope the same as the plugin package: install/select **only `typescript-v6`** from this plugin's content rather than unrelated TypeScript agents. This package does not replace or bundle `cce-typescript`.

## Use Cases

- Upgrading a project from TypeScript 5.x to TypeScript 6
- Fixing `tsconfig.json` after TS 6 default and deprecation changes
- Choosing between `moduleResolution: "bundler"` and `"nodenext"`
- Migrating deprecated `baseUrl`, `moduleResolution: "node"`, and other legacy settings
- Adopting TS 6-era APIs such as `RegExp.escape`, `Temporal`, `Map.getOrInsert`, and `#/` imports
- Comparing TS 6 and TS 7 behavior with `--stableTypeOrdering`

## Structure

This plugin is self-contained under `plugins/typescript-v6/` with a local `skills/` directory for marketplace installs.

## License

MIT License - see [LICENSE](../../LICENSE) for details.
