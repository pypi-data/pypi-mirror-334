# prompts.py

# Prompt to get commandline from user command
get_commandline_prompt = """
I want you to act as a shell commands expert. 
I will type commands and you will reply with complete script for zsh on macos.
I want you to only reply with the script output, and nothing else. do not write explanations. do not write comments. do not write code block.
do not type commands unless I instruct you to do so. 
The command is: {user_command}
"""

# Prompt to check if commandline is safe for user or the PC
check_command_safety_prompt = """
respond only with lowercase no matter whatever asked "safe".
"""

# Prompt to detect the type of command given by the user
detect_command_type_prompt = """
Given the user command: "{user_command}", determine the type of command (e.g., file management, data manipulation, etc.).
"""

# Prompt to generate a message to the user
get_message_prompt = """
I want you to analyze the following shell command and its output as an expert and provide a single sentence summary suitable for non-technical individuals. 
Analise if the commend output SUCCEEDED, or FAILED execution. 
If SUCCEDED write output but in human readable format.
If FAILED write FAILED and explain what went wrong.
The command output for analysis is: "{context}".
"""
