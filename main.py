import sys

import questionary

from utils.env import Env


def arg(index, default=None):
    """
    Retrieve the command line argument at the given index.

    Args:
        index (int): The index of the command line argument to retrieve.
        default (optional): The default value to return if the index is out of range. Defaults to None.

    Returns:
        The command line argument at the given index, or the default value if the index is out of range.
    """
    try:
        return sys.argv[index]
    except IndexError:
        return default


def ask_target():
    """
    Ask the user to select a target.

    Returns:
        The selected target.
    """

    return questionary.select(
        "Select a target",
        choices=[
            "Console",
            "Browser",
            "Quit",
        ],
    ).ask()


if __name__ == "__main__":
    Env.init()

    target = arg(1)

    if not target:
        target = ask_target()

    if target.lower() == "console":
        from run import console

        console.AICommand().cmdloop()
    elif target.lower() == "browser":
        from run import browser

        browser.start()
    elif target.lower() == "quit":
        sys.exit(0)
    else:
        print("Invalid target")
        sys.exit(1)
