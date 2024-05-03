# DevDynamo

DevDynamo is an AI-powered assistant designed to simplify coding tasks within the Linux operating system environment.

## How it Works

DevDynamo interprets natural language commands and converts them into Python code using the Gemini AI API. Here's how it operates:

1. **Natural Language Interpretation**: You input commands in plain language, such as "open Google."
   
2. **Code Generation**: DevDynamo interprets these commands and generates the corresponding Python code automatically.

3. **Execution**: The generated code is executed within the Linux environment, seamlessly performing the requested task.

4. **Error Handling**: If any errors occur during execution, DevDynamo attempts to diagnose and fix them automatically, ensuring a smoother user experience.
## Installation

To install DevDynamo, follow these steps:

1. **Clone the Repository**:
```bash\ngit colne https://github.com/Ali-TBB/DevDynamo_AI.git\n```

2. **Navigate to the Project Directory**:
```
cd  DevDynamo_AI

```

2. **Install Dependencies**:

```
pip install -r requirements.txt

```

3. **Setup Gemini AI API**:
- Sign up for a Gemini AI API account and obtain your API key.
- Sign up for a Gemini AI API account and obtain your API key.
- Open the `API_KEY` file in the `models/dataset/` directory.
- Set your API key as the content of the `API_KEY` file.
- Alternatively, you can enter your API key when prompted after running the program.

4. **Run DevDynamo**:
```bash\nsudo ./DevDynamo/n```

## Future Development

While DevDynamo is already capable of simplifying coding tasks, there are exciting plans for future enhancements:

1. **Handling Complex Projects**: DevDynamo will be trained with new datasets to handle larger and more complex projects. This will involve breaking down big tasks into smaller, more manageable steps, enabling developers to work on projects incrementally.

2. **Improved Error Handling**: Enhancements in error handling capabilities will ensure DevDynamo can diagnose and fix errors more effectively. This includes the integration of advanced error detection algorithms and automatic resolution strategies.

3. **Integration of GUI Interaction**: DevDynamo will gain the ability to interact with Graphical User Interfaces (GUIs) using tools like pyautogui. This will enable the assistant to resolve certain types of errors that require GUI manipulation, such as clicking buttons or entering text.

4. **Enhanced User Environment Interaction**: DevDynamo will gather more information from the user's environment, such as system configurations and user preferences. This data will be used to tailor generated code to specific machine requirements, ensuring compatibility and optimal performance.

5. **Integration with Gemini Vision**: DevDynamo will be connected with Gemini Vision to enable advanced image recognition capabilities. This integration will allow DevDynamo to capture screenshots, extract relevant data from images, and use it to assist in problem-solving and code generation.

6. **Continuous Learning and Improvement**: DevDynamo will undergo continuous learning and improvement through user feedback and iterative updates. This ensures that the assistant remains adaptive and responsive to the evolving needs of developers.

These planned enhancements aim to make DevDynamo even more versatile, efficient, and indispensable for developers, empowering them to tackle complex coding tasks with ease.
