import os
import re
from gtts import gTTS
import google.generativeai as genai
from FileHistory import ChatHistoryHandler



genai.configure(api_key="AIzaSyCudvWsPkoKlcP2YUH4t3oup2K3dnyMob8")
# Set up the model
generation_config = {
    "temperature": 1,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = ChatHistoryHandler("safety_setting.json").history


model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                                                            generation_config=generation_config,
                                                            safety_settings=safety_settings)



history_handler = ChatHistoryHandler("dataset/Run_pross.json")
convo = model.start_chat(history=history_handler.history)

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
