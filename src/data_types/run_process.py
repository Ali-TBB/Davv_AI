import typing_extensions as typing


class RunProcessDataType(typing.TypedDict):
    action: str
    language: str
    code: str
    response: str