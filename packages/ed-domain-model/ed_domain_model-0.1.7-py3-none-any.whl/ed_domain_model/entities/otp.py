from datetime import datetime
from enum import StrEnum
from typing import TypedDict
from uuid import UUID


class OtpVerificationAction(StrEnum):
    VERIFY_EMAIL = "VERIFY_EMAIL"
    VERIFY_PHONE_NUMBER = "VERIFY_PHONE_NUMBER"
    LOGIN = "LOGIN"


class Otp(TypedDict):
    id: UUID
    user_id: UUID
    value: str
    action: OtpVerificationAction
    create_datetime: datetime
    expiry_datetime: datetime
