import google.generativeai as genai
import dspy
import subprocess
import sys
import pkg_resources

# Initialize DSPy model and configure it
def setup_dspy_model():
    model = dspy.LM('gemini-1.5-flash', api_key='AIzaSyDutlHakJqczH-p44CIJQY5ltNAOhv_2kY')  # Gemini or another model
    dspy.configure(lm=model)
    return model

# Function to check and install dependencies
def check_and_install_dependencies():
    required_packages = ['google-generativeai', 'dspy']
    installed_packages = {pkg.key for pkg in pkg_resources.working_set}
    missing_packages = [pkg for pkg in required_packages if pkg not in installed_packages]
    
    if missing_packages:
        print(f"Missing dependencies: {', '.join(missing_packages)}")
        install = input("Would you like to install the missing dependencies? (y/n): ").lower()
        if install == "y":
            subprocess.run([sys.executable, "-m", "pip", "install"] + missing_packages, check=True)
            print("Dependencies installed successfully.")
        else:
            print("Exiting program due to missing dependencies.")
            sys.exit(1)

# Define a DSPy module for generating shell commands based on user input
class CommandGenerator(dspy.Module):
    def __init__(self):
        super().__init__()
        self.generator = dspy.Predict('input -> shell_command: str')

    def forward(self, user_input, iteration=1):
        # Dynamically adjust the prompt for each iteration
        prompt = f"Convert the following natural language request into a valid UNIX/Linux shell command for macOS. Ensure the command is executable, doesn't require user input, and uses no non-default dependencies. Request: {user_input}."
        
        if iteration > 1:
            prompt += f" The previous attempt was unsuccessful. Please fix the command and make it correct."

        # Pass the dynamically created prompt to the model
        response = self.generator(input=prompt)
        return response.shell_command

# Function to execute the shell command and handle errors
def execute_shell_command(command):
    try:
        # Execute the shell command and check for errors
        subprocess.run(command, shell=True, check=True)
        print("Command executed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return False  # Return False to indicate failure
    return True

# Function to automatically fix command or install missing dependencies
def handle_command_execution(command, iteration):
    if not execute_shell_command(command):
        print(f"Command failed on iteration {iteration}. Attempting to fix the command.")
        # Generate a new command to fix the issue
        command_generator = CommandGenerator()
        refined_command = command_generator.forward(command, iteration)
        print(f"Refined Command: {refined_command}")

        # Try executing the refined command again
        if execute_shell_command(refined_command):
            return True
        else:
            print("Could not fix the command. Checking if dependencies are missing...")
            check_for_dependencies_and_fix(refined_command)
            return False
    return True

# Function to check for missing dependencies and install them
def check_for_dependencies_and_fix(command):
    try:
        # Attempt to execute the command to see if any dependencies are missing
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        missing_dependencies = extract_missing_dependencies(e)
        if missing_dependencies:
            install_dependencies(missing_dependencies)
        else:
            print(f"Error: {e}")
            print("Could not resolve the error automatically.")
            return False
    return True

# Function to extract missing dependencies from error message
def extract_missing_dependencies(error):
    missing_deps = []
    if "No module named" in str(error):
        # Parse the error to find missing modules
        missing_deps = [line.split("No module named")[1].strip() for line in str(error).splitlines() if "No module named" in line]
    return missing_deps

# Function to install dependencies
def install_dependencies(dependencies):
    print(f"Missing dependencies: {', '.join(dependencies)}")
    install = input(f"Do you want to install the missing dependencies: {', '.join(dependencies)}? (y/n): ").lower()
    if install == "y":
        subprocess.run([sys.executable, "-m", "pip", "install"] + dependencies, check=True)
        print("Dependencies installed successfully.")
    else:
        print("Exiting program due to missing dependencies.")
        sys.exit(1)

# Define a chat-based function to keep the conversation going
def chat_interface():
    # Set up DSPy model
    setup_dspy_model()

    iteration = 1
    while True:
        # User input
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("Exiting chat...")
            break

        # Generate shell command based on user input
        command_generator = CommandGenerator()
        refined_command = command_generator(user_input, iteration)

        # Print the generated shell command
        print(f"Generated Shell Command (Iteration {iteration}): {refined_command}")

        # Handle the execution of the shell command, retrying if necessary
        if handle_command_execution(refined_command, iteration):
            print("Command executed successfully.")
        else:
            print("Failed to execute the command after retrying. Please check the issue manually.")

        # Ask if user wants to continue with another command
        continue_input = input("Do you want to try another command? (y/n): ").lower()
        if continue_input != "y":
            print("Exiting chat...")
            break

        iteration += 1

# Main execution
if __name__ == "__main__":
    check_and_install_dependencies()  # Check and install dependencies
    chat_interface()  # Start chat interface
