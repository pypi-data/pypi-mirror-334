from typing import NotRequired, TypedDict


class ConsumerDto(TypedDict):
    first_name: str
    last_name: str
    phone_number: str
    email: NotRequired[str]
