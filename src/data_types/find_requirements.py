import typing_extensions as typing


class FindRequirementsDataType(typing.TypedDict):
    """
    Represents the data type for finding requirements.

    Attributes:
        action (str): The action to be performed.
        response (str): The response to the action.
    """

    action: str
    response: str
