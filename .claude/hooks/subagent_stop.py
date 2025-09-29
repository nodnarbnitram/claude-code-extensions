#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-dotenv",
# ]
# ///

import argparse
import json
import os
import sys
import subprocess
import random
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional


def get_tts_script_path():
    """
    Determine which TTS script to use based on available API keys.
    Priority order: ElevenLabs > OpenAI > pyttsx3
    """
    # Get current script directory and construct utils/tts path
    script_dir = Path(__file__).parent
    tts_dir = script_dir / "utils" / "tts"
    
    # Check for ElevenLabs API key (highest priority)
    # if os.getenv('ELEVENLABS_API_KEY'):
    #     elevenlabs_script = tts_dir / "elevenlabs_tts.py"
    #     if elevenlabs_script.exists():
    #         return str(elevenlabs_script)
    
    # Check for OpenAI API key (second priority)
    # if os.getenv('OPENAI_API_KEY'):
    #     openai_script = tts_dir / "openai_tts.py"
    #     if openai_script.exists():
    #         return str(openai_script)
    
    # Fall back to pyttsx3 (no API key required)
    pyttsx3_script = tts_dir / "pyttsx3_tts.py"
    if pyttsx3_script.exists():
        return str(pyttsx3_script)
    
    return None


def get_completion_messages():
    """Return list of friendly completion messages."""
    return [
        "Subagent complete!",
        "Subtask done!",
        "Agent finished!",
        "Subagent ready!",
        "Task complete!"
    ]


def get_llm_completion_message(input_data):
    """
    Generate completion message using available LLM services.
    Priority order: Ollama (local) > fallback to random message
    
    Args:
        input_data (dict): Input data from Claude Code containing subagent info
    
    Returns:
        str: Generated or fallback completion message
    """
    # Extract subagent information from input data
    subagent_name = None
    task_info = None
    
    # Try to extract subagent name from various possible fields
    if 'subagent_type' in input_data:
        subagent_name = input_data['subagent_type']
    elif 'agent_type' in input_data:
        subagent_name = input_data['agent_type']
    elif 'tool_name' in input_data:
        subagent_name = input_data['tool_name']
    
    # Try to extract task information
    if 'description' in input_data:
        task_info = input_data['description']
    elif 'task' in input_data:
        task_info = input_data['task']
    elif 'prompt' in input_data:
        task_info = input_data['prompt'][:50] + "..." if len(input_data['prompt']) > 50 else input_data['prompt']
    
    # Get current script directory and construct utils/llm path
    script_dir = Path(__file__).parent
    llm_dir = script_dir / "utils" / "llm"
    
    # Try Ollama script with subagent completion mode
    ollama_script = llm_dir / "ollama.py"
    if ollama_script.exists():
        try:
            cmd = ["uv", "run", str(ollama_script), "--subagent-completion"]
            if subagent_name:
                cmd.append(subagent_name)
            if task_info:
                cmd.append(task_info)
                
            result = subprocess.run(
                cmd, 
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
        except (subprocess.TimeoutExpired, subprocess.SubprocessError):
            pass
    
    # Fallback to random predefined message
    messages = get_completion_messages()
    return random.choice(messages)


def announce_subagent_completion(input_data):
    """Announce subagent completion using the best available TTS service."""
    try:
        tts_script = get_tts_script_path()
        if not tts_script:
            return  # No TTS scripts available
        
        # Get completion message (LLM-generated or fallback)
        completion_message = get_llm_completion_message(input_data)
        
        # Call the TTS script with the completion message
        subprocess.run([
            "uv", "run", tts_script, completion_message
        ], 
        capture_output=True,  # Suppress output
        timeout=10  # 10-second timeout
        )
        
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
        # Fail silently if TTS encounters issues
        pass
    except Exception:
        # Fail silently for any other errors
        pass


def main():
    try:
        # Parse command line arguments
        parser = argparse.ArgumentParser()
        parser.add_argument('--chat', action='store_true', help='Copy transcript to chat.json')
        args = parser.parse_args()
        
        # Read JSON input from stdin
        input_data = json.load(sys.stdin)

        # Ensure log directory exists
        log_dir = os.path.join(os.getcwd(), "logs")
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, "subagent_stop.json")

        # Read existing log data or initialize empty list
        if os.path.exists(log_path):
            with open(log_path, 'r') as f:
                try:
                    log_data = json.load(f)
                except (json.JSONDecodeError, ValueError):
                    log_data = []
        else:
            log_data = []
        
        # Append new data
        log_data.append(input_data)
        
        # Write back to file with formatting
        with open(log_path, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        # Handle --chat switch (same as stop.py)
        if args.chat and 'transcript_path' in input_data:
            transcript_path = input_data['transcript_path']
            if os.path.exists(transcript_path):
                # Read .jsonl file and convert to JSON array
                chat_data = []
                try:
                    with open(transcript_path, 'r') as f:
                        for line in f:
                            line = line.strip()
                            if line:
                                try:
                                    chat_data.append(json.loads(line))
                                except json.JSONDecodeError:
                                    pass  # Skip invalid lines
                    
                    # Write to logs/chat.json
                    chat_file = os.path.join(log_dir, 'chat.json')
                    with open(chat_file, 'w') as f:
                        json.dump(chat_data, f, indent=2)
                except Exception:
                    pass  # Fail silently

        # Announce subagent completion via TTS
        announce_subagent_completion(input_data)

        sys.exit(0)

    except json.JSONDecodeError:
        # Handle JSON decode errors gracefully
        sys.exit(0)
    except Exception:
        # Handle any other errors gracefully
        sys.exit(0)


if __name__ == "__main__":
    main()