#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "typer[all]>=0.12.0",
#     "rich>=13.0.0",
#     "pyyaml>=6.0",
# ]
# ///

"""
Claude Code Extensions Installer

Dynamically installs agents, hooks, commands, and output-styles from this
repository to target projects.
"""

import json
import shutil
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import List, Optional

import typer
import yaml
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.table import Table
from rich.progress import track

# ============================================================================
# Data Models
# ============================================================================

class ExtensionType(str, Enum):
    AGENT = "agent"
    HOOK = "hook"
    COMMAND = "command"
    OUTPUT_STYLE = "output-style"


@dataclass
class Extension:
    """Represents a Claude Code extension."""
    type: ExtensionType
    name: str
    path: Path
    relative_path: Path  # Relative to .claude/
    description: str
    category: Optional[str] = None  # For agents (e.g., "core", "specialized/react")
    dependencies: List[str] = field(default_factory=list)  # For hooks with utils
    metadata: dict = field(default_factory=dict)  # Full frontmatter


@dataclass
class InstallResult:
    """Result of installing an extension."""
    extension: Extension
    success: bool
    action: str  # "installed", "skipped", "overwritten", "failed"
    message: str


# ============================================================================
# Discovery Functions
# ============================================================================

console = Console()


def get_repo_root() -> Path:
    """Get the repository root (where this script is located)."""
    return Path(__file__).parent.resolve()


def parse_frontmatter(file_path: Path) -> dict:
    """Extract YAML frontmatter from a markdown file."""
    try:
        content = file_path.read_text()
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                return yaml.safe_load(parts[1]) or {}
    except Exception as e:
        console.print(f"[yellow]Warning: Could not parse frontmatter in {file_path}: {e}[/yellow]")
    return {}


def detect_hook_dependencies(hook_path: Path) -> List[str]:
    """Detect if a hook imports from utils/."""
    dependencies = []
    try:
        content = hook_path.read_text()
        lines = content.split("\n")

        for line in lines:
            line = line.strip()
            # Look for imports from utils
            if "from utils" in line or "import utils" in line:
                # This hook uses utils - we need to copy the utils directory
                utils_dir = hook_path.parent / "utils"
                if utils_dir.exists():
                    # Find all Python files in utils
                    for util_file in utils_dir.rglob("*.py"):
                        rel_path = util_file.relative_to(hook_path.parent)
                        dependencies.append(str(rel_path))
                break
    except Exception:
        pass

    return dependencies


def discover_agents(repo_path: Path) -> List[Extension]:
    """Discover all agent files in .claude/agents/."""
    agents = []
    agents_dir = repo_path / ".claude" / "agents"

    if not agents_dir.exists():
        return agents

    for agent_file in agents_dir.rglob("*.md"):
        try:
            frontmatter = parse_frontmatter(agent_file)
            name = frontmatter.get("name", agent_file.stem)
            description = frontmatter.get("description", "No description")

            # Determine category from path
            rel_to_agents = agent_file.relative_to(agents_dir)
            category = None
            if len(rel_to_agents.parts) > 1:
                # Has subdirectory, use it as category
                category = str(Path(*rel_to_agents.parts[:-1]))

            agents.append(Extension(
                type=ExtensionType.AGENT,
                name=name,
                path=agent_file,
                relative_path=agent_file.relative_to(repo_path / ".claude"),
                description=description,
                category=category,
                metadata=frontmatter
            ))
        except Exception as e:
            console.print(f"[yellow]Warning: Could not process {agent_file}: {e}[/yellow]")

    return agents


def discover_hooks(repo_path: Path) -> List[Extension]:
    """Discover all hook files in .claude/hooks/ (excluding utils/)."""
    hooks = []
    hooks_dir = repo_path / ".claude" / "hooks"

    if not hooks_dir.exists():
        return hooks

    # Find all .py files recursively, but exclude utils/ directory
    for hook_file in hooks_dir.rglob("*.py"):
        # Skip utils directory
        if "utils" in hook_file.parts:
            continue

        try:
            # Use relative path for name (e.g., "pre_tool_use" or "lint/check")
            rel_to_hooks = hook_file.relative_to(hooks_dir)
            name = str(rel_to_hooks.with_suffix("")).replace("/", "_")
            dependencies = detect_hook_dependencies(hook_file)

            # Try to get description from file
            description = f"Hook: {name}"
            content = hook_file.read_text()
            if '"""' in content:
                doc_start = content.find('"""') + 3
                doc_end = content.find('"""', doc_start)
                if doc_end > doc_start:
                    description = content[doc_start:doc_end].strip().split("\n")[0]

            hooks.append(Extension(
                type=ExtensionType.HOOK,
                name=name,
                path=hook_file,
                relative_path=hook_file.relative_to(repo_path / ".claude"),
                description=description,
                dependencies=dependencies
            ))
        except Exception as e:
            console.print(f"[yellow]Warning: Could not process {hook_file}: {e}[/yellow]")

    return hooks


def discover_commands(repo_path: Path) -> List[Extension]:
    """Discover all command files in .claude/commands/."""
    commands = []
    commands_dir = repo_path / ".claude" / "commands"

    if not commands_dir.exists():
        return commands

    for cmd_file in commands_dir.glob("*.md"):
        try:
            frontmatter = parse_frontmatter(cmd_file)
            name = cmd_file.stem
            description = frontmatter.get("description", "No description")

            commands.append(Extension(
                type=ExtensionType.COMMAND,
                name=name,
                path=cmd_file,
                relative_path=cmd_file.relative_to(repo_path / ".claude"),
                description=description,
                metadata=frontmatter
            ))
        except Exception as e:
            console.print(f"[yellow]Warning: Could not process {cmd_file}: {e}[/yellow]")

    return commands


def discover_output_styles(repo_path: Path) -> List[Extension]:
    """Discover all output-style files in .claude/output-styles/."""
    styles = []
    styles_dir = repo_path / ".claude" / "output-styles"

    if not styles_dir.exists():
        return styles

    for style_file in styles_dir.glob("*.md"):
        try:
            frontmatter = parse_frontmatter(style_file)
            name = frontmatter.get("name", style_file.stem)
            description = frontmatter.get("description", "No description")

            styles.append(Extension(
                type=ExtensionType.OUTPUT_STYLE,
                name=name,
                path=style_file,
                relative_path=style_file.relative_to(repo_path / ".claude"),
                description=description,
                metadata=frontmatter
            ))
        except Exception as e:
            console.print(f"[yellow]Warning: Could not process {style_file}: {e}[/yellow]")

    return styles


def discover_all_extensions(repo_path: Path) -> List[Extension]:
    """Discover all extensions in the repository."""
    extensions = []
    extensions.extend(discover_agents(repo_path))
    extensions.extend(discover_hooks(repo_path))
    extensions.extend(discover_commands(repo_path))
    extensions.extend(discover_output_styles(repo_path))
    return extensions


# ============================================================================
# Settings Management
# ============================================================================

def load_settings(settings_path: Path) -> dict:
    """Load settings.json file."""
    if not settings_path.exists():
        return {
            "$schema": "https://json.schemastore.org/claude-code-settings.json",
            "hooks": {}
        }

    try:
        with open(settings_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        console.print(f"[red]Error loading settings.json: {e}[/red]")
        return {"hooks": {}}


def save_settings(settings_path: Path, settings: dict):
    """Save settings.json file with proper formatting."""
    settings_path.parent.mkdir(parents=True, exist_ok=True)

    with open(settings_path, 'w') as f:
        json.dump(settings, f, indent=2)


def merge_hook_settings(
    target_settings: dict,
    source_settings: dict,
    hooks: List[Extension],
    target_dir: Path
) -> dict:
    """Merge hook configurations from source to target settings.

    Strategy:
    1. For each hook being installed
    2. Find its configuration in source settings.json
    3. Append to target settings (don't duplicate)
    4. Update command paths for target project
    """
    target_hooks = target_settings.setdefault("hooks", {})
    source_hooks = source_settings.get("hooks", {})

    # Map hook names to lifecycle events by examining source settings
    hook_names = {h.name for h in hooks}

    # Process each lifecycle event in source
    for event_name, event_configs in source_hooks.items():
        if event_name not in target_hooks:
            target_hooks[event_name] = []

        # Process each matcher configuration
        for config in event_configs:
            matcher = config.get("matcher", "")
            hooks_list = config.get("hooks", [])

            # Check if any of the hooks in this config are being installed
            relevant_hooks = []
            for hook_config in hooks_list:
                command = hook_config.get("command", "")
                # Check if this command references any of our hooks
                for hook_name in hook_names:
                    if hook_name in command:
                        # Update the command path for target directory
                        updated_command = command.replace(
                            "./.claude/hooks/",
                            str(target_dir / ".claude" / "hooks") + "/"
                        )
                        relevant_hooks.append({
                            **hook_config,
                            "command": updated_command
                        })
                        break

            if relevant_hooks:
                # Check if this matcher already exists in target
                existing_config = None
                for existing in target_hooks[event_name]:
                    if existing.get("matcher", "") == matcher:
                        existing_config = existing
                        break

                if existing_config:
                    # Append to existing matcher
                    existing_hooks_list = existing_config.setdefault("hooks", [])
                    for hook in relevant_hooks:
                        # Don't duplicate
                        if hook not in existing_hooks_list:
                            existing_hooks_list.append(hook)
                else:
                    # Add new matcher configuration
                    target_hooks[event_name].append({
                        "matcher": matcher,
                        "hooks": relevant_hooks
                    })

    return target_settings


# ============================================================================
# Installation Functions
# ============================================================================

def install_extension(
    extension: Extension,
    repo_path: Path,
    target_dir: Path,
    overwrite: bool = False,
    dry_run: bool = False
) -> InstallResult:
    """Install a single extension."""
    target_path = target_dir / ".claude" / extension.relative_path

    # Check if file already exists
    if target_path.exists() and not overwrite:
        return InstallResult(
            extension=extension,
            success=True,
            action="skipped",
            message=f"Already exists: {target_path}"
        )

    if dry_run:
        return InstallResult(
            extension=extension,
            success=True,
            action="would install",
            message=f"Would install to: {target_path}"
        )

    try:
        # Create parent directory
        target_path.parent.mkdir(parents=True, exist_ok=True)

        # Copy the main file
        shutil.copy2(extension.path, target_path)

        action = "overwritten" if target_path.exists() else "installed"
        result = InstallResult(
            extension=extension,
            success=True,
            action=action,
            message=f"Installed to: {target_path}"
        )

        # For hooks, also copy dependencies
        if extension.type == ExtensionType.HOOK and extension.dependencies:
            for dep in extension.dependencies:
                src_dep = repo_path / ".claude" / "hooks" / dep
                dst_dep = target_dir / ".claude" / "hooks" / dep

                if src_dep.exists():
                    dst_dep.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src_dep, dst_dep)

        return result

    except Exception as e:
        return InstallResult(
            extension=extension,
            success=False,
            action="failed",
            message=f"Error: {e}"
        )


def install_extensions(
    extensions: List[Extension],
    repo_path: Path,
    target_dir: Path,
    overwrite: bool = False,
    dry_run: bool = False
) -> List[InstallResult]:
    """Install multiple extensions."""
    results = []

    if not dry_run:
        console.print(f"\n[bold]Installing {len(extensions)} extensions...[/bold]\n")

    for ext in track(extensions, description="Installing..." if not dry_run else "Checking..."):
        result = install_extension(ext, repo_path, target_dir, overwrite, dry_run)
        results.append(result)

    # Handle hooks settings.json merge
    hooks = [e for e in extensions if e.type == ExtensionType.HOOK]
    if hooks and not dry_run:
        source_settings = load_settings(repo_path / ".claude" / "settings.json")
        target_settings = load_settings(target_dir / ".claude" / "settings.json")

        # Backup existing settings
        settings_path = target_dir / ".claude" / "settings.json"
        if settings_path.exists():
            backup_path = settings_path.with_suffix(".json.backup")
            shutil.copy2(settings_path, backup_path)
            console.print(f"[dim]Backed up settings.json to {backup_path}[/dim]")

        # Merge settings
        merged_settings = merge_hook_settings(
            target_settings,
            source_settings,
            hooks,
            target_dir
        )

        save_settings(settings_path, merged_settings)
        console.print("[green]Updated settings.json with hook configurations[/green]")

    return results


# ============================================================================
# UI Functions
# ============================================================================

def display_extensions_table(extensions: List[Extension], title: str = "Available Extensions"):
    """Display extensions in a formatted table."""
    table = Table(title=title, show_header=True, header_style="bold magenta")
    table.add_column("Type", style="cyan", width=12)
    table.add_column("Name", style="green", width=30)
    table.add_column("Category", style="yellow", width=20)
    table.add_column("Description", style="white")

    for ext in sorted(extensions, key=lambda e: (e.type.value, e.category or "", e.name)):
        category = ext.category or "-"
        desc = ext.description[:80] + "..." if len(ext.description) > 80 else ext.description
        table.add_row(ext.type.value, ext.name, category, desc)

    console.print(table)


def display_summary(extensions: List[Extension]):
    """Display a summary of discovered extensions."""
    by_type = {}
    for ext in extensions:
        by_type.setdefault(ext.type.value, []).append(ext)

    summary_lines = []
    for ext_type, items in sorted(by_type.items()):
        if ext_type == "agent":
            # Group agents by category
            by_category = {}
            for agent in items:
                cat = agent.category or "root"
                by_category.setdefault(cat, []).append(agent)

            summary_lines.append(f"• {len(items)} agents")
            for cat in sorted(by_category.keys()):
                summary_lines.append(f"  - {cat}: {len(by_category[cat])}")
        else:
            summary_lines.append(f"• {len(items)} {ext_type}s")

    panel = Panel(
        "\n".join(summary_lines),
        title="[bold]Extension Summary[/bold]",
        border_style="blue"
    )
    console.print(panel)


def display_results(results: List[InstallResult]):
    """Display installation results."""
    by_action = {}
    for result in results:
        by_action.setdefault(result.action, []).append(result)

    console.print("\n[bold]Installation Results:[/bold]\n")

    for action in ["installed", "overwritten", "would install", "skipped", "failed"]:
        if action in by_action:
            items = by_action[action]

            if action == "installed":
                color = "green"
                icon = "✓"
            elif action == "overwritten":
                color = "blue"
                icon = "↻"
            elif action == "would install":
                color = "cyan"
                icon = "→"
            elif action == "skipped":
                color = "yellow"
                icon = "○"
            else:
                color = "red"
                icon = "✗"

            console.print(f"[{color}]{icon} {action.upper()}: {len(items)}[/{color}]")
            for result in items:
                console.print(f"  [{color}]- {result.extension.name}[/{color}]")

    # Summary
    total = len(results)
    successful = sum(1 for r in results if r.success)
    console.print(f"\n[bold]Total: {successful}/{total} successful[/bold]")


def select_extensions_interactive(extensions: List[Extension]) -> List[Extension]:
    """Interactive extension selection."""
    console.print("\n[bold cyan]Interactive Extension Selection[/bold cyan]\n")

    # Ask what to install
    console.print("What would you like to install?")
    console.print("1. All extensions")
    console.print("2. Select by type")
    console.print("3. Select by category (agents only)")
    console.print("4. Individual selection")

    choice = Prompt.ask("Choose an option", choices=["1", "2", "3", "4"], default="1")

    if choice == "1":
        return extensions

    elif choice == "2":
        # Select by type
        available_types = sorted(set(e.type.value for e in extensions))
        console.print("\nAvailable types:")
        for i, t in enumerate(available_types, 1):
            count = sum(1 for e in extensions if e.type.value == t)
            console.print(f"{i}. {t} ({count})")

        selected_nums = Prompt.ask("Select types (comma-separated numbers)").split(",")
        selected_types = [available_types[int(n.strip())-1] for n in selected_nums if n.strip().isdigit()]

        return [e for e in extensions if e.type.value in selected_types]

    elif choice == "3":
        # Select by category (agents only)
        agents = [e for e in extensions if e.type == ExtensionType.AGENT]
        categories = sorted(set(a.category or "root" for a in agents))

        console.print("\nAvailable categories:")
        for i, cat in enumerate(categories, 1):
            count = sum(1 for a in agents if (a.category or "root") == cat)
            console.print(f"{i}. {cat} ({count})")

        selected_nums = Prompt.ask("Select categories (comma-separated numbers)").split(",")
        selected_cats = [categories[int(n.strip())-1] for n in selected_nums if n.strip().isdigit()]

        selected = [a for a in agents if (a.category or "root") in selected_cats]

        # Add non-agent extensions if user wants
        if Confirm.ask("\nAlso install hooks, commands, and output-styles?"):
            selected.extend([e for e in extensions if e.type != ExtensionType.AGENT])

        return selected

    else:
        # Individual selection
        console.print("\nEnter extension names (comma-separated):")
        display_extensions_table(extensions, "Available Extensions")

        names_input = Prompt.ask("Extension names")
        selected_names = [n.strip() for n in names_input.split(",")]

        return [e for e in extensions if e.name in selected_names]


# ============================================================================
# CLI Commands
# ============================================================================

app = typer.Typer(
    name="claude-extensions",
    help="Install Claude Code extensions from this repository to target projects",
    no_args_is_help=True
)


@app.command()
def install(
    target: Optional[Path] = typer.Argument(
        None,
        help="Target project directory (defaults to current directory)",
        exists=True,
        file_okay=False,
        dir_okay=True,
        resolve_path=True
    ),
    extension_type: Optional[str] = typer.Option(
        None,
        "--type", "-t",
        help="Extension type to install (agent, hook, command, output-style, all)"
    ),
    category: Optional[str] = typer.Option(
        None,
        "--category", "-c",
        help="Agent category filter (e.g., core, specialized/react)"
    ),
    interactive: bool = typer.Option(
        True,
        "--interactive/--no-interactive",
        help="Interactive selection mode"
    ),
    overwrite: bool = typer.Option(
        False,
        "--overwrite",
        help="Overwrite existing files"
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Show what would be installed without making changes"
    )
):
    """Install Claude Code extensions to a target project."""

    # Determine paths
    repo_path = get_repo_root()
    target_dir = target or Path.cwd()

    console.print("\n[bold]Claude Code Extensions Installer[/bold]")
    console.print(f"Source: {repo_path}")
    console.print(f"Target: {target_dir}\n")

    # Discover extensions
    console.print("[dim]Discovering extensions...[/dim]")
    extensions = discover_all_extensions(repo_path)

    if not extensions:
        console.print("[red]No extensions found in repository![/red]")
        raise typer.Exit(1)

    display_summary(extensions)

    # Filter by type
    if extension_type and extension_type != "all":
        try:
            ext_type = ExtensionType(extension_type)
            extensions = [e for e in extensions if e.type == ext_type]
        except ValueError:
            console.print(f"[red]Invalid type: {extension_type}[/red]")
            raise typer.Exit(1)

    # Filter by category
    if category:
        extensions = [e for e in extensions if e.category == category]

    # Interactive selection
    if interactive and not dry_run:
        extensions = select_extensions_interactive(extensions)

    if not extensions:
        console.print("[yellow]No extensions selected.[/yellow]")
        raise typer.Exit(0)

    # Show what will be installed
    console.print(f"\n[bold]Will install {len(extensions)} extensions:[/bold]")
    display_extensions_table(extensions, "Selected Extensions")

    # Confirm
    if not dry_run and interactive:
        if not Confirm.ask("\nProceed with installation?"):
            console.print("[yellow]Installation cancelled.[/yellow]")
            raise typer.Exit(0)

    # Install
    results = install_extensions(
        extensions,
        repo_path,
        target_dir,
        overwrite=overwrite,
        dry_run=dry_run
    )

    # Display results
    display_results(results)

    if dry_run:
        console.print("\n[dim]This was a dry run. No changes were made.[/dim]")


@app.command()
def list(
    extension_type: Optional[str] = typer.Option(
        None,
        "--type", "-t",
        help="Filter by extension type"
    ),
    category: Optional[str] = typer.Option(
        None,
        "--category", "-c",
        help="Filter by agent category"
    )
):
    """List available extensions in this repository."""

    repo_path = get_repo_root()
    extensions = discover_all_extensions(repo_path)

    # Apply filters
    if extension_type:
        try:
            ext_type = ExtensionType(extension_type)
            extensions = [e for e in extensions if e.type == ext_type]
        except ValueError:
            console.print(f"[red]Invalid type: {extension_type}[/red]")
            raise typer.Exit(1)

    if category:
        extensions = [e for e in extensions if e.category == category]

    display_summary(extensions)
    display_extensions_table(extensions)


@app.command()
def info(
    name: str = typer.Argument(..., help="Extension name")
):
    """Show detailed information about an extension."""

    repo_path = get_repo_root()
    extensions = discover_all_extensions(repo_path)

    # Find extension
    ext = next((e for e in extensions if e.name == name), None)

    if not ext:
        console.print(f"[red]Extension not found: {name}[/red]")
        raise typer.Exit(1)

    # Display info
    console.print(f"\n[bold cyan]{ext.name}[/bold cyan]")
    console.print(f"Type: {ext.type.value}")
    console.print(f"Path: {ext.path}")
    console.print(f"Description: {ext.description}")

    if ext.category:
        console.print(f"Category: {ext.category}")

    if ext.dependencies:
        console.print(f"Dependencies: {', '.join(ext.dependencies)}")

    if ext.metadata:
        console.print("\n[bold]Metadata:[/bold]")
        for key, value in ext.metadata.items():
            console.print(f"  {key}: {value}")


def main():
    """Entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
