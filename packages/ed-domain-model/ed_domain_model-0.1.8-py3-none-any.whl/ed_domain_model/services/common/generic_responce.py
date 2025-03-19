from typing import TypedDict


class GenericResponse(TypedDict):
    success: bool
    message: str
    data: type
    errors: list[str]
