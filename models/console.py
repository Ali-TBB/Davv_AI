import cmd
import shlex
import os
from BaseModel import configure_api_key
from Run_process import Run_process

class AICommand(cmd.Cmd):
    """ AI command prompt to access models data """
    prompt = '(User): '

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.dataset_dir = os.path.join(self.current_dir, "dataset")
        self.api_key_file = os.path.join(self.current_dir, "dataset/API_KEY")
        self.configure_api_key()

    def configure_api_key(self):
        try:
            with open(self.api_key_file, 'r') as file:
                api_key = file.read().strip()
                if api_key:
                    configure_api_key(api_key)
                else:
                    print("API key not found in the text file.")
                    self.prompt_api_key()
        except FileNotFoundError:
            print("API key file not found.")
            self.prompt_api_key()

    def prompt_api_key(self):
        api_key = input("Enter your API key: ").strip()
        with open(self.api_key_file, 'w') as file:
            file.write(api_key)
        configure_api_key(api_key)

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

    def emptyline(self):
        """ Overrides the empty line method """
        pass

    def do_clear(self, arg):
        """ Clears the screen """
        print("\033c")

    def do_SHOW(self, arg):
        tokens = shlex.split(arg)
        if len(tokens) == 0:
            print("** missing the flag**")
            return
        if tokens[0] not in {"-H", "-R"}:
            print("** flag doesn't exist **")
            return
        else:
            if tokens[0] == "-R":
                removeHistory()
            if tokens[0] == "-H":
                printHistory()

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

            print("New dataset created.")
        except Exception as e:
            print(f"An error occurred while replacing files: {e}")

    def default(self, arg):
        """ handle new ways of inputting data """
        # Assuming "prompt" is the command to execute
        if arg.strip() == "#new":
            self.replace_files()
        else:
            # Assuming "prompt" is the command to execute
            op = Run_process(arg, "command.py")
            op.Start()
            op.Run()

if __name__ == '__main__':
    AICommand().cmdloop()
