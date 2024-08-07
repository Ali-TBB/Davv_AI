import typing_extensions as typing


class StepDataType(typing.TypedDict):
    action: str
    file_name: str
    code: str
    
class DivideToSimpleDataType(typing.TypedDict):
    steps: list[StepDataType]
