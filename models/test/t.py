import subprocess

def Run():
    try:
        # Read the command from the specified file
        with open("command.py", "r") as file:
            command_content = file.read().strip()
        # Execute the command using subprocess
        subprocess.run(["python", "command.py"])
    except Exception as e:
        print(f"An error occurred while running the command: {e}")
        # Pass the error to the Error method
        print(str(e))
Run()