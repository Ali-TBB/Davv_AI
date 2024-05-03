import cmd
import shlex
import os
from BaseModel import configure_api_key
from Run_pross import Run_pross

class AICommand(cmd.Cmd):
    """ AI command prompt to access models data """
    prompt = '(User): '

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
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

    def default(self, arg):
        """ handle new ways of inputting data """
        # Assuming "prompt" is the command to execute
        op = Run_pross(arg, "command.py")
        op.Start()
        op.Run()

if __name__ == '__main__':
    AICommand().cmdloop()
