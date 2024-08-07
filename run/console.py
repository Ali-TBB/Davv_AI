import os

import cmd
import questionary

from utils.env import Env
from src.ai_conversation import AIConversation


class AICommand(cmd.Cmd):
    """AI command prompt to access models data"""

    prompt = "(User): "

    conversation: AIConversation

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.dataset_dir = os.path.join(self.current_dir, "../src/dataset")
        self.hello()

    def hello(self):
        print("Hello, welcome to the AI command prompt.")
        self.configure_api_key()
        self.home()

    def configure_api_key(self):
        if not Env.has("API_KEY"):
            print("API key file not found.")
            self.prompt_api_key()

    def prompt_api_key(self):
        api_key = questionary.text("Enter your API key:").ask()
        if api_key:
            Env.set("API_KEY", api_key)
            print("API key set successfully.")
        else:
            print("API key is required.")
            self.prompt_api_key()

    def home(self):
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
        """Does nothing"""
        pass

    def do_quit(self, arg):
        """Close program and saves safely data"""
        print("Exiting the program, bye")
        exit()

    def do_EOF(self, arg):
        """Close program and saves safely data, when
        user input is CTRL + D
        """
        print("")
        return True

    def do_clear(self, arg):
        """Clears the screen"""
        print("\033c")

    def create_conversation(self):
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
            print("There is no conversations created yet")
            self.home()

    def default(self, arg):
        """Handle new ways of inputting data"""
        # Assuming "prompt" is the command to execute
        if arg.strip() == "#home":
            self.home()
        elif arg.strip() == "#new":
            self.create_conversation()
        else:
            print(self.conversation.handle_message(arg).content)


if __name__ == "__main__":
    AICommand().cmdloop()
