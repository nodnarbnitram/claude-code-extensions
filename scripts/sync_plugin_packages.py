#!/usr/bin/env python3

from __future__ import annotations

import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent
CLAUDE_ROOT = REPO_ROOT / ".claude"
PLUGINS_ROOT = REPO_ROOT / "plugins"
MARKETPLACE_PATH = REPO_ROOT / ".claude-plugin" / "marketplace.json"

TEXT_EXTENSIONS = {
    ".json",
    ".jsonc",
    ".md",
    ".py",
    ".sh",
    ".txt",
    ".yaml",
    ".yml",
    ".toml",
}

DEFAULT_AUTHOR = {
    "name": "Claude Code Extensions Contributors",
    "url": "https://github.com/nodnarbnitram/claude-code-extensions",
}

DEFAULT_REPOSITORY = "https://github.com/nodnarbnitram/claude-code-extensions"


@dataclass(frozen=True)
class PluginSpec:
    name: str
    description: str
    keywords: list[str]
    assets: list[tuple[str, str]]
    hooks_from_settings: bool = False
    version: str = "1.0.0"


PLUGIN_SPECS: list[PluginSpec] = [
    PluginSpec(
        name="cce-core",
        description="Essential Claude Code extensions: core agents, hooks, commands, and universal tools",
        keywords=["core", "essential", "hooks", "automation", "workflow"],
        hooks_from_settings=True,
        assets=[
            (".claude/agents/core", "agents/core"),
            (".claude/agents/orchestrators", "agents/orchestrators"),
            (".claude/agents/universal", "agents/universal"),
            (".claude/agents/meta-agent.md", "agents/meta-agent.md"),
            (".claude/skills/commit-helper", "skills/commit-helper"),
            (".claude/skills/code-reviewer", "skills/code-reviewer"),
            (".claude/commands/git-commit.md", "commands/git-commit.md"),
            (".claude/commands/git-status.md", "commands/git-status.md"),
            (".claude/commands/prime.md", "commands/prime.md"),
            (".claude/commands/agent-from-docs.md", "commands/agent-from-docs.md"),
            (
                ".claude/commands/agent-intent-from-docs.md",
                "commands/agent-intent-from-docs.md",
            ),
            (".claude/commands/security-scan.md", "commands/security-scan.md"),
            (".claude/commands/wrapup-skillup.md", "commands/wrapup-skillup.md"),
            (".claude/commands/frontend-mode.md", "commands/frontend-mode.md"),
            (".claude/commands/create-skill.md", "commands/create-skill.md"),
            (".claude/hooks", "hooks"),
        ],
    ),
    PluginSpec(
        name="cce-kubernetes",
        description="Kubernetes cluster operations, health diagnostics, and operator-specific agents",
        keywords=["kubernetes", "k8s", "cluster-health"],
        assets=[
            (".claude/agents/specialized/kubernetes", "agents/specialized/kubernetes"),
            (".claude/skills/kubernetes-operations", "skills/kubernetes-operations"),
            (".claude/skills/kubernetes-health", "skills/kubernetes-health"),
            (".claude/commands/k8s-health.md", "commands/k8s-health.md"),
        ],
    ),
    PluginSpec(
        name="cce-cloudflare",
        description="Cloudflare Workers, AI, Workflows, and VPC services development",
        keywords=["cloudflare", "workers", "edge", "ai"],
        assets=[
            (".claude/agents/specialized/cloudflare", "agents/specialized/cloudflare"),
            (
                ".claude/skills/cloudflare-vpc-services",
                "skills/cloudflare-vpc-services",
            ),
        ],
    ),
    PluginSpec(
        name="cce-esphome",
        description="ESPHome IoT development for ESP32/ESP8266 with Home Assistant integration",
        keywords=["esphome", "iot", "esp32", "homeassistant"],
        assets=[
            (".claude/agents/specialized/esphome", "agents/specialized/esphome"),
            (".claude/skills/esphome-config-helper", "skills/esphome-config-helper"),
            (".claude/skills/esphome-box3-builder", "skills/esphome-box3-builder"),
        ],
    ),
    PluginSpec(
        name="cce-homeassistant",
        description="Home Assistant automation, integrations, dashboards, voice, and energy workflows",
        keywords=[
            "homeassistant",
            "home-automation",
            "lovelace",
            "assist",
            "integrations",
        ],
        assets=[
            (
                ".claude/agents/specialized/homeassistant",
                "agents/specialized/homeassistant",
            ),
            (".claude/skills/ha-addon", "skills/ha-addon"),
            (".claude/skills/ha-api", "skills/ha-api"),
            (".claude/skills/ha-automation", "skills/ha-automation"),
            (".claude/skills/ha-dashboard", "skills/ha-dashboard"),
            (".claude/skills/ha-energy", "skills/ha-energy"),
            (".claude/skills/ha-integration", "skills/ha-integration"),
            (".claude/skills/ha-voice", "skills/ha-voice"),
            (".claude/skills/frigate-configurator", "skills/frigate-configurator"),
            (
                ".claude/commands/ha-automation-lint.md",
                "commands/ha-automation-lint.md",
            ),
            (
                ".claude/commands/ha-blueprint-create.md",
                "commands/ha-blueprint-create.md",
            ),
            (
                ".claude/commands/ha-integration-scaffold.md",
                "commands/ha-integration-scaffold.md",
            ),
        ],
    ),
    PluginSpec(
        name="cce-web-react",
        description="React, Next.js, and TanStack Start development",
        keywords=["react", "nextjs", "tanstack"],
        assets=[(".claude/agents/specialized/react", "agents/specialized/react")],
    ),
    PluginSpec(
        name="cce-research",
        description="Deep research coordination: academic papers, technical analysis, data insights, and web intelligence",
        keywords=["research", "academic", "data-analysis", "technical-research"],
        assets=[(".claude/agents/deep-research", "agents/deep-research")],
    ),
    PluginSpec(
        name="cce-web-vue",
        description="Vue.js and Nuxt.js development with Composition API, composables, and SSR/SSG patterns",
        keywords=["vue", "vuejs", "nuxt", "composition-api", "ssr", "ssg"],
        assets=[(".claude/agents/specialized/vue", "agents/specialized/vue")],
    ),
    PluginSpec(
        name="cce-typescript",
        description="TypeScript and frontend tooling including Braintrust testing and fumadocs documentation",
        keywords=["typescript", "frontend", "braintrust", "testing", "documentation"],
        assets=[
            (".claude/agents/specialized/braintrust", "agents/specialized/braintrust"),
            (".claude/agents/specialized/frontend", "agents/specialized/frontend"),
        ],
    ),
    PluginSpec(
        name="cce-go",
        description="Go development following Google Go style guide with Go 1.25+ features and best practices",
        keywords=["go", "golang", "google-style", "best-practices"],
        assets=[(".claude/agents/specialized/go", "agents/specialized/go")],
    ),
    PluginSpec(
        name="cce-anthropic",
        description="Anthropic Claude Agent SDK development for Python and TypeScript autonomous agents",
        keywords=["anthropic", "claude", "agent-sdk", "autonomous-agents"],
        assets=[
            (".claude/agents/specialized/anthropic", "agents/specialized/anthropic")
        ],
    ),
    PluginSpec(
        name="cce-grafana",
        description="Grafana plugin development and billing metrics analysis for Prometheus and Loki",
        keywords=["grafana", "observability", "metrics", "plugins", "billing"],
        assets=[
            (".claude/agents/specialized/grafana", "agents/specialized/grafana"),
            (
                ".claude/skills/grafana-plugin-scaffolding",
                "skills/grafana-plugin-scaffolding",
            ),
            (".claude/skills/grafana-billing", "skills/grafana-billing"),
        ],
    ),
    PluginSpec(
        name="cce-django",
        description="Django backend development suite: models, views, DRF APIs, GraphQL, and ORM optimization",
        keywords=["django", "python", "drf", "graphql", "orm", "backend"],
        assets=[(".claude/agents/specialized/django", "agents/specialized/django")],
    ),
    PluginSpec(
        name="cce-temporal",
        description="Temporal.io workflow development across Python, Go, and TypeScript SDKs with testing and troubleshooting",
        keywords=["temporal", "workflows", "durable-execution", "distributed-systems"],
        assets=[(".claude/agents/specialized/temporal", "agents/specialized/temporal")],
    ),
    PluginSpec(
        name="cce-devops",
        description="DevOps tooling: GitHub Actions, Helm, ArgoCD, and Crossplane for CI/CD and infrastructure",
        keywords=["devops", "ci-cd", "github-actions", "helm", "argocd", "crossplane"],
        assets=[
            (".claude/agents/specialized/devops", "agents/specialized/devops"),
            (".claude/agents/specialized/helm", "agents/specialized/helm"),
            (".claude/agents/specialized/argocd", "agents/specialized/argocd"),
            (".claude/agents/specialized/crossplane", "agents/specialized/crossplane"),
        ],
    ),
    PluginSpec(
        name="cce-ai",
        description="AI/ML development: LLM architecture, prompt engineering, ML ops, and NLP with production deployment focus",
        keywords=["ai", "ml", "llm", "machine-learning", "nlp", "prompt-engineering"],
        assets=[(".claude/agents/specialized/data-ai", "agents/specialized/data-ai")],
    ),
    PluginSpec(
        name="cce-python",
        description="Python CLI development with Typer for type-hint driven applications, validation, and testing",
        keywords=["python", "typer", "cli", "type-hints"],
        assets=[(".claude/agents/specialized/python", "agents/specialized/python")],
    ),
    PluginSpec(
        name="cce-linear",
        description="Linear ticket and project workflows with wrapper scripts for issues, milestones, documents, and PR coordination",
        keywords=["linear", "tickets", "project-management", "triage", "workflow"],
        assets=[
            (".claude/skills/linear", "skills/linear"),
            (".claude/commands/triage.md", "commands/triage.md"),
            (".claude/commands/create-linear-pr.md", "commands/create-linear-pr.md"),
            (".claude/commands/existing-linear.md", "commands/existing-linear.md"),
        ],
    ),
    PluginSpec(
        name="cce-tauri",
        description="Tauri v2 desktop and mobile app development with Rust backend, IPC, capabilities, and security",
        keywords=["tauri", "desktop", "rust", "ipc", "capabilities"],
        assets=[
            (".claude/agents/specialized/tauri", "agents/specialized/tauri"),
            (".claude/skills/tauri-v2", "skills/tauri-v2"),
        ],
    ),
]


def copy_path(src: Path, dest: Path) -> None:
    if not src.exists():
        raise FileNotFoundError(f"Missing source path: {src}")

    if dest.exists():
        if dest.is_dir():
            shutil.rmtree(dest)
        else:
            dest.unlink()

    dest.parent.mkdir(parents=True, exist_ok=True)
    if src.is_dir():
        shutil.copytree(src, dest)
    else:
        shutil.copy2(src, dest)


def copy_agent_assets_flat(src: Path, plugin_root: Path) -> None:
    agents_root = plugin_root / "agents"
    agents_root.mkdir(parents=True, exist_ok=True)

    if src.is_dir():
        for agent_file in src.rglob("*.md"):
            shutil.copy2(agent_file, agents_root / agent_file.name)
        return

    shutil.copy2(src, agents_root / src.name)


def is_text_file(path: Path) -> bool:
    return path.suffix.lower() in TEXT_EXTENSIONS or path.name in {
        "hooks.json",
        "plugin.json",
        "SKILL.md",
        "README.md",
    }


def rewrite_claude_paths(text: str) -> str:
    rewritten = re.sub(r"(?<![\w~/])(?:\./)?\.claude/", "${CLAUDE_PLUGIN_ROOT}/", text)
    rewritten = rewritten.replace(
        "${CLAUDE_PLUGIN_ROOT}/settings.json", "${CLAUDE_PLUGIN_ROOT}/hooks/hooks.json"
    )
    rewritten = rewritten.replace(
        "${CLAUDE_PLUGIN_ROOT}/hooks/hooks.json/hooks/", "${CLAUDE_PLUGIN_ROOT}/hooks/"
    )
    return rewritten


def rewrite_text_files(plugin_root: Path) -> None:
    for path in plugin_root.rglob("*"):
        if not path.is_file() or not is_text_file(path):
            continue
        original = path.read_text()
        updated = rewrite_claude_paths(original)
        if updated != original:
            path.write_text(updated)


def load_existing_manifest(plugin_name: str) -> dict[str, Any]:
    manifest_path = PLUGINS_ROOT / plugin_name / ".claude-plugin" / "plugin.json"
    if manifest_path.exists():
        return json.loads(manifest_path.read_text())
    return {}


def build_manifest(spec: PluginSpec) -> dict[str, Any]:
    existing = load_existing_manifest(spec.name)
    manifest: dict[str, Any] = {
        "name": spec.name,
        "version": existing.get("version", spec.version),
        "description": spec.description,
        "author": existing.get("author", DEFAULT_AUTHOR),
        "homepage": existing.get("homepage", DEFAULT_REPOSITORY),
        "repository": existing.get("repository", DEFAULT_REPOSITORY),
        "license": existing.get("license", "MIT"),
        "keywords": spec.keywords,
    }

    if spec.hooks_from_settings:
        manifest["hooks"] = "./hooks/hooks.json"

    return manifest


def write_manifest(spec: PluginSpec, plugin_root: Path) -> None:
    manifest_dir = plugin_root / ".claude-plugin"
    manifest_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = manifest_dir / "plugin.json"
    manifest_path.write_text(json.dumps(build_manifest(spec), indent=2) + "\n")


def build_core_hooks() -> dict[str, Any]:
    settings = json.loads((CLAUDE_ROOT / "settings.json").read_text())
    hooks = settings["hooks"]

    def rewrite(value: Any) -> Any:
        if isinstance(value, dict):
            return {key: rewrite(inner) for key, inner in value.items()}
        if isinstance(value, list):
            return [rewrite(item) for item in value]
        if isinstance(value, str):
            updated = value.replace(
                "${CLAUDE_PLUGIN_ROOT:-$CLAUDE_PROJECT_DIR}", "${CLAUDE_PLUGIN_ROOT}"
            )
            updated = updated.replace("/.claude/hooks/", "/hooks/")
            return updated
        return value

    return rewrite(hooks)


def write_core_hooks(plugin_root: Path) -> None:
    hooks_dir = plugin_root / "hooks"
    hooks_dir.mkdir(parents=True, exist_ok=True)
    hooks_path = hooks_dir / "hooks.json"
    hooks_path.write_text(json.dumps({"hooks": build_core_hooks()}, indent=2) + "\n")


def sync_plugin(spec: PluginSpec) -> None:
    plugin_root = PLUGINS_ROOT / spec.name
    plugin_root.mkdir(parents=True, exist_ok=True)

    for generated in ["agents", "commands", "skills", "hooks", ".mcp.json"]:
        generated_path = plugin_root / generated
        if generated_path.exists():
            if generated_path.is_dir():
                shutil.rmtree(generated_path)
            else:
                generated_path.unlink()

    for src, dest in spec.assets:
        source_path = REPO_ROOT / src
        if src.startswith(".claude/agents/"):
            copy_agent_assets_flat(source_path, plugin_root)
            continue
        copy_path(source_path, plugin_root / dest)

    if spec.hooks_from_settings:
        write_core_hooks(plugin_root)

    write_manifest(spec, plugin_root)
    rewrite_text_files(plugin_root)


def sync_marketplace() -> None:
    marketplace = json.loads(MARKETPLACE_PATH.read_text())
    marketplace["plugins"] = [
        {
            "name": spec.name,
            "source": f"./plugins/{spec.name}",
            "description": spec.description,
            "version": spec.version,
            "author": {"name": DEFAULT_AUTHOR["name"]},
            "keywords": spec.keywords,
        }
        for spec in PLUGIN_SPECS
    ]
    MARKETPLACE_PATH.write_text(json.dumps(marketplace, indent=2) + "\n")


def main() -> None:
    for spec in PLUGIN_SPECS:
        sync_plugin(spec)
    sync_marketplace()
    print(f"Synced {len(PLUGIN_SPECS)} plugin packages")


if __name__ == "__main__":
    main()
