import json
import os


class ChatHistoryHandler:
    """
    A class that handles the chat history.

    Attributes:
        filename (str): The name of the file to store the chat history.
        full_path (str): The full path of the file to store the chat history.
        history (list): The list of chat entries representing the chat history.

    Methods:
        get_full_path(): Returns the full path of the chat history file.
        load_history(): Loads the chat history from the file.
        update_history(chat_entry): Appends a new chat entry to the chat history.
        save_history(): Saves the chat history to the file.
    """

    def __init__(self, filename):
        self.filename = filename
        self.full_path = self.get_full_path()
        self.history = self.load_history()

    def get_full_path(self):
        """
        Returns the full path of the chat history file.

        Returns:
            str: The full path of the chat history file.
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(current_dir, self.filename)

    def load_history(self):
        """
        Loads the chat history from the file.

        Returns:
            list: The list of chat entries representing the chat history.
        """
        try:
            with open(self.full_path, 'r') as file:
                history = json.load(file)
                return history
        except FileNotFoundError:
            return []

    def update_history(self, chat_entry):
        """
        Appends a new chat entry to the chat history.

        Args:
            chat_entry (str): The chat entry to be added to the chat history.
        """
        self.history.append(chat_entry)

    def save_history(self):
        """
        Saves the chat history to the file.
        """
        with open(self.full_path, 'w') as file:
            json.dump(self.history, file, indent=4)
