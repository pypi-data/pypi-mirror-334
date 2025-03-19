from datetime import datetime
from typing import TypedDict
from uuid import UUID

from ed_domain_model.services.core.dtos.create_route_dto import CreateRouteDto


class CreateDeliveryJobDto(TypedDict):
    order_ids: list[UUID]
    route: CreateRouteDto
    estimated_payment: float
    estimated_completion_time: datetime
