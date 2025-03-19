from datetime import datetime
from enum import StrEnum
from typing import NotRequired, TypedDict
from uuid import UUID


class DriverPaymentStatus(StrEnum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class PaymentMethod(StrEnum):
    BANK_TRANSFER = "BANK_TRANSFER"
    TELEBIRR = "TELEBIRR"


class Detail(TypedDict):
    payment_method: PaymentMethod

    # Bank transfer
    account_name: NotRequired[str]
    account_number: NotRequired[str]

    # Telebirr transfer
    phone_number: NotRequired[str]


class DriverPayment(TypedDict):
    id: UUID
    amount: float
    status: DriverPaymentStatus
    date: datetime
    detail: Detail
