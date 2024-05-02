import cmd
import shlex
from Run_pross import Run_pross

class AICommand(cmd.Cmd):
    """ AI command prompt to access models data """
    prompt = '(User): '

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
                removeHistory()  # Assuming this is defined elsewhere
            if tokens[0] == "-H":
                printHistory()  # Assuming this is defined elsewhere

    def default(self, arg):
        """ handle new ways of inputting data """
        # Assuming "prompt" is the command to execute
        op = Run_pross(arg, "command.py")
        op.Start()
        op.Run()

if __name__ == '__main__':
    AICommand().cmdloop()
