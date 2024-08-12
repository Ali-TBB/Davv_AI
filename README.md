
# Davv_AI

Davv_AI is an AI-powered assistant designed to simplify tasks across various operating systems. It offers an intuitive interface for interaction and includes a streaming record feature that you can activate and start recording by simply saying "Hi Google."

## How it Works

Davv_AI interprets natural language commands and converts them into Python code using the Gemini AI API. Here's how it operates:

1. **Natural Language Interpretation**: You input commands in plain language, such as "open Google."
2. **Code Generation**: Davv_AI interprets these commands and generates the corresponding Python code automatically.
3. **Execution**: The generated code is executed seamlessly, performing the requested task across any operating system.
4. **Error Handling**: If any errors occur during execution, Davv_AI attempts to diagnose and fix them automatically, ensuring a smoother user experience.
5. **Interface Interaction**: You can interact with the interface through voice commands or text input, making it more accessible and user-friendly.
6. **Project Handling**: Davv_AI can handle larger projects, such as creating a Snake game or developing a shopping website. It will generate the necessary files and code, allowing you to focus on customization and refinement.
7. **Streaming Record Feature**: Activate the streaming record feature, Once activated, you can start recording by simply saying "Hi Google". This feature is particularly helpful for visually impaired users, enabling them to interact with the computer more effectively. For example, they can perform tasks like opening Google, searching for music on YouTube, playing the first song, or even shutting down the computer. The feature provides real-time feedback, making these actions more accessible and manageable.

## Installation

To install Davv_AI, follow these steps:

1. **Clone the Repository**:

   ```
   git clone https://github.com/Ali-TBB/Davv_AI.git
   ```

2. **Navigate to the Project Directory**:

   ```
   cd Davv_AI
   ```

3. **Install Dependencies**:

   ```
   pip install -r requirements.txt
   ```

4. **Setup Gemini AI API**:

   - Sign up for a Gemini AI API account and obtain your API key.
   - Set your API key as a variable in the `.env` file.
   - Alternatively, you can enter your API key when prompted after running the program.

5. **Run Davv_AI**:

   ```
   sudo python main.py
   ```