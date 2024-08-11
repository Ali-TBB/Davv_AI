import typing_extensions as typing


class StepDataType(typing.TypedDict):
    """
    Represents a step data type.

    Attributes:
        action (str): The action performed.
        file_name (str): The name of the file.
        code (str): The code snippet.
        language (str): The programming language used.
    """

    action: str
    file_name: str
    code: str
    language: str
    
class DivideToSimpleDataType(typing.TypedDict):
    """
    Represents a data type for dividing a complex number into its simple components.

    Attributes:
        steps (list[StepDataType]): The list of steps involved in the division process.
    """

    steps: list[StepDataType]
