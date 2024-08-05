import sys


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


if __name__ == "__main__":
    target = arg(1, "console")
    if target == "console":
        from run import console

        console.AICommand().cmdloop()
    else:
        print("Invalid target")
        sys.exit(1)
