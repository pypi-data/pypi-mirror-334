from datetime import datetime
from enum import StrEnum
from typing import NotRequired, TypedDict
from uuid import UUID


class DeliveryJobStatus(StrEnum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"


class DeliveryJob(TypedDict):
    id: UUID
    order_ids: list[UUID]
    route_id: UUID
    driver_id: NotRequired[UUID]
    driver_payment_id: NotRequired[UUID]
    status: DeliveryJobStatus
    estimated_payment: float
    estimated_completion_time: datetime
