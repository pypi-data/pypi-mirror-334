import os
import platform
import sys
import subprocess
import time
import threading
from dotenv import load_dotenv
from .config import settings, Colors
from .openai_api import generate_shell_command, is_command_safe
from .utils import colorize

MAX_RETRIES = 500  # Limit retries to prevent infinite loops
TIMEOUT = 10000    # Maximum time (in seconds) before killing a command

def load_env_vars():
    load_dotenv()
    return os.getenv("GEMINI_API_KEY")  # Updated to use Gemini API key

def read_config():
    return settings["command_execution_confirmation"], settings["security_check"], settings["gemini_model_config"]

def recognize_operating_system():
    return platform.system()

def read_user_command():
    return " ".join(sys.argv[1:])

def execute_command_with_interaction(shell_command, timeout=TIMEOUT):
    """
    Executes a command while handling interactive prompts, timeouts, and showing real-time output.
    - Ensures the command doesn't hang indefinitely.
    - Returns both stdout and stderr for AI analysis if it fails.
    """
    print(colorize(f"EXECUTING: {shell_command}", Colors.OKGREEN))

    process = subprocess.Popen(
        shell_command,
        shell=True,
        executable='/bin/bash',
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE,
        text=True
    )

    try:
        # 🚀 Use communicate() instead of manual threading to capture output
        stdout, stderr = process.communicate(timeout=timeout)

        print(stdout.strip())  # Print real-time output

    except subprocess.TimeoutExpired:
        print(colorize("⏳ Timeout reached! Terminating process...", Colors.FAIL))
        process.terminate()
        process.wait()
        return None, "Process timed out."

    finally:
        process.stdout.close()  # 🚀 Ensure streams are closed
        process.stderr.close()
        process.wait()  # 🚀 Prevent zombie processes

    if process.returncode != 0:
        raise subprocess.CalledProcessError(process.returncode, shell_command, output=stdout, stderr=stderr)

    return stdout, stderr


def execute_with_retry(user_command, shell_command, security_check, gemini_api_key, gemini_model_config, command_execution_confirmation, operating_system, retry_count=0):
    """
    Executes a command and retries intelligently if it fails.
    - Provides AI with full error context to generate improved commands.
    - Detects errors related to missing dependencies, incorrect paths, and permissions.
    - Stops retrying after reaching MAX_RETRIES.
    """
    try:
        execute_command_with_interaction(shell_command)
        print(colorize("✅ Command executed successfully!", Colors.OKGREEN))
        return  # Exit function if successful

    except subprocess.CalledProcessError as e:
        error_message = e.stderr.strip() if e.stderr else str(e)
        print(colorize(f"❌ ERROR: Command execution failed.\n🔍 Exact Error: {error_message}", Colors.FAIL))
        print(colorize(f"💀 Failed Command: {shell_command}", Colors.WARNING))

        # If max retries reached, stop
        if retry_count >= MAX_RETRIES:
            print(colorize("⚠️ Max retries reached. Aborting execution.", Colors.FAIL))
            return

        print(colorize("🔄 Retrying with AI-generated improvements...", Colors.WARNING))

        # Generate a new fixed command with full error context
        retry_prompt = (
            f"User's original request: '{user_command}'.\n"
            f"Previously generated command that failed: '{shell_command}'.\n"
            f"Exact error message from execution: '{error_message}'.\n"
            "Generate a **fixed** UNIX/Linux shell command that correctly achieves the user's goal, avoids previous errors, and ensures correct paths, dependencies, and permissions.\n"
            "Important:\n"
            "- If the error indicates a missing command, provide the correct installation command.\n"
            "- If the error involves permission issues, add 'sudo' if necessary.\n"
            "- If the error is due to an existing directory, add '--skip-existing' if supported.\n"
            "- Make sure the fixed command is executable on macOS and Linux."
        )

        new_shell_command = generate_shell_command(retry_prompt, gemini_api_key, gemini_model_config)

        print(colorize(f"🆕 New AI-generated command: {new_shell_command}", Colors.OKCYAN))

        # Retry with the improved command
        execute_with_retry(user_command, new_shell_command, security_check, gemini_api_key, gemini_model_config, command_execution_confirmation, operating_system, retry_count + 1)

def main():
    # Load environment variables
    gemini_api_key = load_env_vars()  # Use Gemini API key

    # Read config settings
    command_execution_confirmation, security_check, gemini_model_config = read_config()

    # Recognize the operating system
    operating_system = recognize_operating_system()

    # Read user command
    user_command = read_user_command()

    # Convert natural language to a shell command
    shell_command = generate_shell_command(user_command, gemini_api_key, gemini_model_config)
    print(f"DEBUG: Generated shell command: {shell_command}")  # Debugging output

    # Process and execute the command with retry mechanism
    execute_with_retry(user_command, shell_command, security_check, gemini_api_key, gemini_model_config, command_execution_confirmation, operating_system)

if __name__ == "__main__":
    main()
