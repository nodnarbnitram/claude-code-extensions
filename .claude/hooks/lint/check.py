#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

import json
import sys
import subprocess
import shutil
from pathlib import Path

def check_command_exists(command):
    """Check if a command exists in PATH."""
    return shutil.which(command) is not None

def run_linter(linter_cmd, file_path, linter_name):
    """Run a linter command and report results."""
    try:
        result = subprocess.run(
            linter_cmd,
            capture_output=True,
            text=True
        )

        # Print output if there are issues
        if result.returncode != 0:
            print(f"🔍 {linter_name} found issues in {file_path}:")
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr, file=sys.stderr)

        return result.returncode
    except Exception as e:
        print(f"Error running {linter_name}: {e}", file=sys.stderr)
        return 0

def lint_python(file_path):
    """Lint Python files with ruff."""
    if not check_command_exists('ruff'):
        return 0

    return run_linter(['ruff', 'check', file_path], file_path, 'Ruff')

def lint_go(file_path):
    """Lint Go files with golangci-lint."""
    if not check_command_exists('golangci-lint'):
        return 0

    return run_linter(['golangci-lint', 'run', file_path], file_path, 'golangci-lint')

def lint_js_ts(file_path):
    """Lint JS/TS files with biome or prettier."""
    # Check for biome first
    if check_command_exists('biome'):
        # Check if biome.json exists in project root
        current_dir = Path(file_path).parent
        while current_dir != current_dir.parent:
            if (current_dir / 'biome.json').exists():
                return run_linter(['biome', 'check', file_path], file_path, 'Biome')
            current_dir = current_dir.parent

    # Fall back to prettier
    if check_command_exists('prettier'):
        result = subprocess.run(
            ['prettier', '--check', file_path],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print(f"🔍 Prettier found formatting issues in {file_path}:")
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr, file=sys.stderr)

        return result.returncode

    return 0

def main():
    try:
        # Read JSON input from stdin
        input_data = json.load(sys.stdin)

        # Extract file path
        file_path = input_data.get('tool_input', {}).get('file_path', '')

        # Check if file exists
        if not file_path or not Path(file_path).exists():
            sys.exit(0)

        file_extension = Path(file_path).suffix.lower()

        # Route to appropriate linter based on file extension
        if file_extension == '.py':
            lint_python(file_path)
        elif file_extension == '.go':
            lint_go(file_path)
        elif file_extension in ['.js', '.jsx', '.ts', '.tsx', '.mjs', '.cjs']:
            lint_js_ts(file_path)

        # Always exit 0 to not block the operation
        sys.exit(0)

    except Exception as e:
        # Fail gracefully
        print(f"Error in lint hook: {e}", file=sys.stderr)
        sys.exit(0)

if __name__ == '__main__':
    main()