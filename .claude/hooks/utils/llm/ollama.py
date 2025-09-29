#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "requests",
#     "python-dotenv",
# ]
# ///

import os
import sys
import json
import requests
from dotenv import load_dotenv


def prompt_llm(prompt_text):
    """
    Base Ollama LLM prompting method using local Qwen3 model.

    Args:
        prompt_text (str): The prompt to send to the model

    Returns:
        str: The model's response text, or None if error
    """
    try:
        # Ollama API endpoint (default local)
        url = "http://localhost:11434/api/generate"
        
        payload = {
            "model": "qwen3:0.6b",
            "prompt": prompt_text,
            "stream": False,
            "think": False,
            "options": {
                "temperature": 0.7,
                "num_predict": 50,
                "top_p": 0.9,
            }
        }
        
        response = requests.post(url, json=payload, timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            return result.get("response", "").strip()
    
    except (requests.RequestException, KeyError, ValueError, json.JSONDecodeError):
        pass
    
    return None


def generate_completion_message():
    """
    Generate a completion message using Ollama LLM.

    Returns:
        str: A natural language completion message, or None if error
    """
    load_dotenv()
    
    engineer_name = os.getenv("ENGINEER_NAME", "").strip()

    if engineer_name:
        name_instruction = f"Sometimes (about 30% of the time) include the engineer's name '{engineer_name}' at the BEGINNING of the message only, never at the end."
        examples = f"""Examples of the style: 
- Standard: "Work complete!", "All done!", "Task finished!", "Ready for your next move!"
- Personalized: "{engineer_name}, all set!", "{engineer_name}, we're done!", "{engineer_name}, task complete!", "{engineer_name}, ready!" """
    else:
        name_instruction = ""
        examples = """Examples of the style: "Work complete!", "All done!", "Task finished!", "Ready for your next move!" """

    prompt = f"""Generate a short, friendly completion message for when an AI coding assistant finishes a task. 

Requirements:
- Keep it under 10 words
- Make it positive and future focused
- Use natural, conversational language
- Focus on completion/readiness
- Do NOT include quotes, formatting, or explanations
- Return ONLY the completion message text
{name_instruction}

{examples}

Generate ONE completion message:"""

    response = prompt_llm(prompt)

    # Clean up response - remove quotes and extra formatting
    if response:
        response = response.strip().strip('"').strip("'").strip()
        # Take first line if multiple lines
        response = response.split("\n")[0].strip()

    return response


def generate_subagent_completion_message(subagent_name=None, task_info=None):
    """
    Generate a subagent completion message using Ollama LLM.

    Args:
        subagent_name (str): Name of the completed subagent
        task_info (str): Description of the task completed

    Returns:
        str: A natural language completion message, or None if error
    """
    load_dotenv()
    
    # Build context for the subagent
    if subagent_name and task_info:
        context = f"Subagent '{subagent_name}' completed task: {task_info}"
        examples = f"""Examples:
- "{subagent_name} finished successfully!"
- "{subagent_name} task complete!"
- "{subagent_name} done with {task_info}!"
- "{subagent_name} ready!"
- "Finished {task_info}!" """
    elif subagent_name:
        context = f"Subagent '{subagent_name}' completed its task"
        examples = f"""Examples:
- "{subagent_name} finished!"
- "{subagent_name} complete!"
- "{subagent_name} done!"
- "{subagent_name} ready!"
- "Agent {subagent_name} finished!" """
    else:
        context = "A subagent completed its task"
        examples = """Examples:
- "Subagent complete!"
- "Agent finished!"
- "Subtask done!"
- "Agent ready!"
- "Task complete!" """

    prompt = f"""Generate a short completion message for when a subagent finishes its task.

Context: {context}

Requirements:
- Keep it under 8 words
- Make it brief and informative
- Include the subagent name if provided
- Use natural, conversational language
- Do NOT include quotes, formatting, or explanations
- Return ONLY the completion message text

{examples}

Generate ONE completion message:"""

    response = prompt_llm(prompt)

    # Clean up response - remove quotes and extra formatting
    if response:
        response = response.strip().strip('"').strip("'").strip()
        # Take first line if multiple lines
        response = response.split("\n")[0].strip()
        # Ensure it's not too long
        if len(response) > 50:
            response = response[:47] + "..."

    return response

def main():
    """Command line interface for testing."""
    if len(sys.argv) > 1:
        if sys.argv[1] == "--completion":
            message = generate_completion_message()
            if message:
                print(message)
            else:
                print("Error generating completion message")
        elif sys.argv[1] == "--subagent-completion":
            # Parse optional subagent name and task
            subagent_name = sys.argv[2] if len(sys.argv) > 2 else None
            task_info = sys.argv[3] if len(sys.argv) > 3 else None
            
            message = generate_subagent_completion_message(subagent_name, task_info)
            if message:
                print(message)
            else:
                print("Error generating subagent completion message")
        else:
            prompt_text = " ".join(sys.argv[1:])
            response = prompt_llm(prompt_text)
            if response:
                print(response)
            else:
                print("Error calling Ollama API")
    else:
        print("Usage: ./ollama.py 'your prompt here' or ./ollama.py --completion or ./ollama.py --subagent-completion [subagent_name] [task_info]")


if __name__ == "__main__":
    main()