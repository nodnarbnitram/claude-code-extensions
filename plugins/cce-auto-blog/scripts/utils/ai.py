"""AI invocation utilities for auto-blog plugin."""

import os
import shutil
import subprocess
import sys
from typing import Optional


def get_ai_cli() -> str:
    """Get the AI CLI to use from environment variable."""
    return os.environ.get("BLOG_AI_CLI", "claude")


def check_cli_exists(cli: str) -> bool:
    """Check if CLI command exists in PATH."""
    return shutil.which(cli) is not None


def invoke_ai(
    prompt: str, transcript_content: str, timeout: int = 120
) -> Optional[str]:
    """
    Invoke AI CLI to process prompt with transcript content.

    Args:
        prompt: The instruction prompt for the AI
        transcript_content: The transcript text to summarize
        timeout: Timeout in seconds (default 120)

    Returns:
        AI response text, or None if invocation fails
    """
    cli = get_ai_cli()

    if not check_cli_exists(cli):
        print(f"Warning: AI CLI '{cli}' not found in PATH", file=sys.stderr)
        return None

    try:
        if cli == "opencode":
            cmd = ["opencode", "run", prompt]
        else:
            cmd = ["claude", "-p", prompt, "--dangerously-skip-permissions"]

        result = subprocess.run(
            cmd,
            input=transcript_content,
            capture_output=True,
            text=True,
            timeout=timeout,
        )

        if result.returncode != 0:
            print(
                f"Warning: AI CLI returned non-zero: {result.stderr}", file=sys.stderr
            )
            return None

        return result.stdout.strip()

    except subprocess.TimeoutExpired:
        print(f"Warning: AI CLI timed out after {timeout}s", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Warning: AI invocation failed: {e}", file=sys.stderr)
        return None


def invoke_ai_background(prompt: str, transcript_path: str, output_path: str) -> None:
    """
    Invoke AI CLI in background process (fire-and-forget).

    Used when hook timeout is too short for synchronous AI call.
    Spawns detached subprocess that writes result to output_path.

    Args:
        prompt: The instruction prompt for the AI
        transcript_path: Path to transcript file to read
        output_path: Path to write AI response to
    """
    cli = get_ai_cli()

    if not check_cli_exists(cli):
        return

    # Create wrapper script that reads transcript, calls AI, writes output
    # This allows the hook to exit immediately while AI runs in background
    python_code = f'''
import subprocess
from pathlib import Path

transcript = Path("{transcript_path}").read_text()
cli = "{cli}"
prompt = """{prompt}"""

if cli == "opencode":
    cmd = ["opencode", "run", prompt]
else:
    cmd = ["claude", "-p", prompt, "--dangerously-skip-permissions"]

try:
    result = subprocess.run(cmd, input=transcript, capture_output=True, text=True, timeout=300)
    if result.returncode == 0:
        Path("{output_path}").write_text(result.stdout)
except Exception:
    pass
'''

    subprocess.Popen(
        [sys.executable, "-c", python_code],
        start_new_session=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
