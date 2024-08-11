import typing_extensions as typing


class RunProcessDataType(typing.TypedDict):
    """
    Represents the data type for running a process.

    Attributes:
        action (str): The action to be performed.
        language (str): The programming language of the code.
        code (str): The code to be executed.
        response (str): The response from the process.
    """

    action: str
    language: str
    code: str
    response: str