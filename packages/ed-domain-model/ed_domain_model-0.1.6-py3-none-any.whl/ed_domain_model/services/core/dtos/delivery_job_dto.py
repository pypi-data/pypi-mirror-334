from datetime import datetime
from typing import NotRequired, TypedDict
from uuid import UUID

from ed_domain_model.entities.delivery_job import DeliveryJobStatus
from ed_domain_model.services.core.dtos.driver_payment_dto import \
    DriverPaymentDto
from ed_domain_model.services.core.dtos.route_dto import RouteDto


class DeliveryJobDto(TypedDict):
    id: UUID
    orders: list[UUID]
    route: RouteDto
    driver_payment: NotRequired[DriverPaymentDto]
    status: DeliveryJobStatus
    estimated_payment: float
    estimated_completion_time: datetime
