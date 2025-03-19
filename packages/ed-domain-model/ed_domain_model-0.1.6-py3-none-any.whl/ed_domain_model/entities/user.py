from datetime import datetime
from typing import NotRequired, TypedDict
from uuid import UUID


class User(TypedDict):
    id: UUID
    first_name: str
    last_name: str
    email: NotRequired[str]
    phone_number: NotRequired[str]
    password: str
    create_datetime: datetime
    update_datetime: datetime
    verified: bool
