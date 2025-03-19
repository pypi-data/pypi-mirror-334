from datetime import datetime
from enum import StrEnum
from typing import TypedDict
from uuid import UUID


class NotificationType(StrEnum):
    SMS = "SMS"
    EMAIL = "EMAIL"
    IN_APP = "IN_APP"


class Notification(TypedDict):
    id: UUID
    user_id: UUID
    notification_type: NotificationType
    message: str
    read_status: bool

    created_datetime: datetime
