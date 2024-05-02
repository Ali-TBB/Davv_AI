import json

class ChatHistoryHandler:
    def __init__(self, filename):
        self.filename = filename
        self.history = self.load_history()

    def load_history(self):
        try:
            with open(self.filename, 'r') as file:
                history = json.load(file)
                return history
        except FileNotFoundError:
            return []

    def update_history(self, chat_entry):
        self.history.append(chat_entry)

    def save_history(self):
        with open(self.filename, 'w') as file:
            json.dump(self.history, file)

"""
# Example usage:
filename = "chat_history.json"
history_handler = ChatHistoryHandler(filename)

# Read existing chat history
existing_history = history_handler.history
print("Existing History:", existing_history)

# Update chat history
new_chat_entry = {"role": "user", "parts": ["New message from user"]}
history_handler.update_history(new_chat_entry)

# Save updated history
history_handler.save_history()

"""