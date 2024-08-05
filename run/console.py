import cmd
import os
import time
import pyautogui

from src.find_requirements import FindRequirements
from src.run_process import RunProcess
from divide_to_simple import DivideToSimple


class AICommand(cmd.Cmd):
    """ AI command prompt to access models data """
    prompt = '(User): '

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.dataset_dir = os.path.join(self.current_dir, "dataset")
        self.api_key_file = os.path.join(self.current_dir, "dataset/API_KEY")
        self.get_started = True
        self.run_process = None
        self.find_requirement = None
        self.divide_to_simple= None
        self.configure_api_key()

    def configure_api_key(self):
        try:
            with open(self.api_key_file, 'r') as file:
                api_key = file.read().strip()
                if not api_key:
                    print("API key not found in the text file.")
                    self.prompt_api_key()
        except FileNotFoundError:
            print("API key file not found.")
            self.prompt_api_key()

    def prompt_api_key(self):
        api_key = input("Enter your API key: ").strip()
        with open(self.api_key_file, 'w') as file:
            file.write(api_key)

    def do_nothing(self, arg):
        """ Does nothing """
        pass

    def do_quit(self, arg):
        """ Close program and saves safely data """
        return True

    def do_EOF(self, arg):
        """ Close program and saves safely data, when
        user input is CTRL + D
        """
        print("")
        return True

    def do_clear(self, arg):
        """ Clears the screen """
        print("\033c")

    def take_screenshot(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_name = time.strftime("%y_%m_%d_%H%M%S")
        full_path = os.path.join(current_dir, "src/screenshot_image/" + f"{image_name}.png")
        try:
            # Capture the screenshot
            screenshot = pyautogui.screenshot()
            # Save the screenshot to the specified file path
            screenshot.save(full_path)
            print("Screenshot saved successfully!")
        except Exception as e:
            print(f"An error occurred: {e}")
        return full_path

    def replace_files(self):
        try:
            # Replace data.json
            with open(os.path.join(self.dataset_dir, "Run_process.json"), 'r') as src_file:
                data = src_file.read()
                with open(os.path.join(self.dataset_dir, "data.json"), 'w') as dest_file:
                    dest_file.write(data)

            # Replace datafix.json
            with open(os.path.join(self.dataset_dir, "FixError.json"), 'r') as src_file:
                data = src_file.read()
                with open(os.path.join(self.dataset_dir, "datafix.json"), 'w') as dest_file:
                    dest_file.write(data)
        
            with open(os.path.join(self.dataset_dir, "Find_Req.json"), 'r') as src_file:
                data = src_file.read()
                with open(os.path.join(self.dataset_dir, "data_find_req.json"), 'w') as dest_file:
                    dest_file.write(data)
            with open(os.path.join(self.dataset_dir, "Divide_to_sm.json"), 'r') as src_file:
                data = src_file.read()
                with open(os.path.join(self.dataset_dir, "Data_Divide_to_sm.json"), 'w') as dest_file:
                    dest_file.write(data)
            print("New dataset created.")
        except Exception as e:
            print(f"An error occurred while replacing files: {e}")

    def default(self, arg):
        """ Handle new ways of inputting data """
        if self.get_started:
            self.run_process = RunProcess()
            self.find_requirement = FindRequirements()
            self.divide_to_simple = DivideToSimple()
            self.get_started = False
        # Assuming "prompt" is the command to execute
        if arg.strip() == "#new":
            self.replace_files()
        else:
            result, input_msg = self.find_requirement.Run(arg)
            if result == "#screenshot":
                screenshot_path = self.take_screenshot()
                self.run_process.run(input_msg=input_msg, image_path=screenshot_path)
            elif result == "#simple":
                self.run_process.run(input_msg=input_msg)
            elif result == "#big":
                self.divide_to_simple.run(input_msg=input_msg)
            elif result == "#response":
                print(input_msg)
            else:
                print("Invalid command.")


if __name__ == '__main__':
    AICommand().cmdloop()
