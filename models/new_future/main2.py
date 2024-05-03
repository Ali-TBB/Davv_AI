import os
import re
from gtts import gTTS
import google.generativeai as genai

genai.configure(api_key="AIzaSyCudvWsPkoKlcP2YUH4t3oup2K3dnyMob8")

# Set up the model
generation_config = {
    "temperature": 1,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                                                            generation_config=generation_config,
                                                            safety_settings=safety_settings)

convo = model.start_chat(history=[
    {
        "role": "user",
        "parts": ["imagine you are my assassinate and when i tell you something you will do it for example when i ask you to shutdown my computer your response it will be like (shutdown computer #code: CODE-TO-SHUTDOWN-COMPUTER-IN-PYTHON) so you will send a full implement code that shutdown computer in python"]
    },
    {
        "role": "model",
        "parts": ["shutdown computer #code: CODE-TO-SHUTDOWN-COMPUTER-IN-PYTHON ```python\nimport os\nimport subprocess\n\ndef shutdown_computer():\n  \"\"\"Shuts down the computer.\"\"\"\n\n  # Get the current operating system.\n  operating_system = os.name\n\n  # If the operating system is Windows, use the shutdown command.\n  if operating_system == \"nt\":\n    subprocess.call([\"shutdown\", \"/s\", \"/t\", \"0\"])\n\n  # If the operating system is macOS, use the shutdown command.\n  elif operating_system == \"posix\":\n    subprocess.call([\"shutdown\", \"-h\", \"now\"])\n\n  # If the operating system is not supported, raise an error.\n  else:\n    raise ValueError(\"Unsupported operating system: {}\".format(operating_system))\n\n# Shutdown the computer.\nshutdown_computer()\n```"]
    },
    {
        "role": "user",
        "parts": ["you will replace CODE-TO-SHUTDOWN-COMPUTER-IN-PYTHON with the code you must not write it again"]
    },
    {
        "role": "model",
        "parts": ["shutdown the computer #code: ```python\nimport os\nimport subprocess\n\ndef shutdown_computer():\n  \"\"\"Shuts down the computer.\"\"\"\n\n  # Get the current operating system.\n  operating_system = os.name\n\n  # If the operating system is Windows, use the shutdown command.\n  if operating_system == \"nt\":\n    subprocess.call([\"shutdown\", \"/s\", \"/t\", \"0\"])\n\n  # If the operating system is macOS, use the shutdown command.\n  elif operating_system == \"posix\":\n    subprocess.call([\"shutdown\", \"-h\", \"now\"])\n\n  # If the operating system is not supported, raise an error.\n  else:\n    raise ValueError(\"Unsupported operating system: {}\".format(operating_system))\n\n# Shutdown the computer.\nshutdown_computer()\n```"]
    },
    {
        "role": "user",
        "parts": ["you don't have to write anything after the code if you understand say ok"]
    },
    {
        "role": "model",
        "parts": ["OK."]
    },
    {
        "role": "user",
        "parts": ["open google"]
    },
    {
        "role": "model",
        "parts": ["opening google #code: ```python\nimport webbrowser\n\n# Open Google in a web browser.\nwebbrowser.open(\"https://www.google.com\")\n```"]
    },
    {
        "role": "user",
        "parts": ["open facebook"]
    },
    {
        "role": "model",
        "parts": ["opening facebook\n #code: ```python\nimport webbrowser\n\n# Open Facebook in a web browser.\nwebbrowser.open(\"https://www.facebook.com\")\n```"]
    },
    {
        "role": "user",
        "parts": ["every code it's will check the operation system to execute the code on the right os if you understand say ok "]
    },
    {
        "role": "model",
        "parts": ["ok"]
    },
])

# Function to speak a given text
def speak(text):
        tts = gTTS(text=text, lang='en')
        tts.save("output.mp3")
        os.system("mpg123 output.mp3")

def execute_command(command_content):
    # Define the filename
    filename = "command.py"
    # Write content to command.py
    with open(filename, "w") as file:
            file.write(command_content)

    # Execute command.py
    os.system("python " + filename)
    # Remove command.py


def speak_2(input_str):
        # Split input string into text and code parts
        text, _, code = input_str.partition("#code:")
        code = code.replace("```", "")
        code = code.replace("python", "")
        # Speak the text part if it exists
        if text.strip():  # Check if there is non-empty text to speak
                speak(text)
                os.remove("output.mp3")
        execute_command(code)

while True:
    prompt = input(">>")
    if prompt == "exit":
        break
    elif prompt == "clear":
        print("\033c")
    elif prompt == "":
        print()
    else:
        convo.send_message(prompt)
        speak_2(convo.last.text)
