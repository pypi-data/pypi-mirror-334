from typing import NotRequired, TypedDict
from uuid import UUID


class ConsumerModel(TypedDict):
    id: UUID
    first_name: str
    last_name: str
    phone_number: str
    email: NotRequired[str]
