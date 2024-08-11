import os

import cmd
import questionary

from utils.env import Env
from src.ai_conversation import AIConversation


class AICommand(cmd.Cmd):
    """
    AICommand class represents the command prompt interface for the AI application.
    """

    prompt = "(User): "

    conversation: AIConversation

    def __init__(self, *args, **kwargs):
        """
        Initializes the Console class.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Attributes:
            current_dir (str): The current directory of the console script.
            dataset_dir (str): The directory path of the dataset.

        Returns:
            None
        """

        super().__init__(*args, **kwargs)
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.dataset_dir = os.path.join(self.current_dir, "../src/dataset")
        self.hello()

    def hello(self):
        """
        Prints a welcome message and performs necessary setup tasks.
        """

        print("Hello, welcome to the DavvAI command prompt.")
        self.home()

    def home(self):
        """
        Displays a menu of options and performs the selected action.

        Returns:
            None
        """

        actions = {
            "Create a new conversation": self.create_conversation,
            "Open an existing conversation": self.open_conversation,
            # "Help": lambda: self.do_help(""),
            "Quit": lambda: self.do_quit(""),
        }
        action = questionary.select(
            "What would you like to do?",
            choices=actions.keys(),
        ).ask()
        actions[action]()

    def do_nothing(self, arg):
        """
        This method does nothing.

        Parameters:
        arg (any): The argument passed to the method.

        Returns:
        None
        """

        pass

    def do_quit(self, arg):
        """
        Quit the program.

        This method prints a message indicating that the program is exiting and then terminates the program.

        Args:
            arg: Any additional arguments passed to the command.

        Returns:
            None
        """

        print("Exiting the program, bye")
        exit()

    def do_EOF(self, arg):
        """
        Handle the end-of-file command.

        Args:
            arg: The argument passed to the command.

        Returns:
            True to exit the console loop.

        """

        print("")
        return True

    def do_clear(self, arg):
        """
        Clears the console screen.
        """

        print("\033c")

    def create_conversation(self):
        """
        Creates a new conversation.

        Prompts the user to enter a conversation name. If a name is provided, it clears the console,
        creates a new AIConversation instance with the given name, initializes it, and prints a success message.
        If no name is provided, it displays an error message and recursively calls itself to prompt for a valid name.
        """

        name = questionary.text("Enter the conversation name: ").ask()
        if name:
            self.do_clear("")
            self.conversation = AIConversation.new(name)
            self.conversation.init()
            print(f"Conversation {name} created successfully.")
        else:
            print("Conversation name is required.")
            self.create_conversation()

    def open_conversation(self):
        """
        Opens a conversation for the user to interact with.

        This method clears the console, retrieves a list of available conversations,
        prompts the user to select a conversation, and initializes the selected conversation.

        If no conversations are available, it prints a message and returns to the home screen.
        If the user cancels the selection, it returns to the home screen without initializing any conversation.
        """

        self.do_clear("")
        conversations = AIConversation.all()

        if conversations:
            name = questionary.select(
                "Select the conversation:",
                choices=[conversation.name for conversation in conversations]
                + ["Cancel"],
            ).ask()

            self.do_clear("")

            if name == "Cancel":
                self.home()
                return

            self.conversation = AIConversation.findWhere("`name` = ?", (name,))
            self.conversation.init()
        else:
            print("There are no conversations created yet")
            self.home()

    def default(self, arg):
        """
        Executes the default command based on the provided argument.

        Args:
            arg (str): The command argument.

        Returns:
            None
        """

        if arg.strip() == "#home":
            self.home()
        elif arg.strip() == "#new":
            self.create_conversation()
        else:
            message, answer = self.conversation.handle_message(arg)
            print(answer.content)


if __name__ == "__main__":
    AICommand().cmdloop()
