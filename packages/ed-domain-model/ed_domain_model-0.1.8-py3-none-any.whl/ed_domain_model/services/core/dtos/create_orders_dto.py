from datetime import datetime
from typing import TypedDict

from ed_domain_model.entities.order import Parcel
from ed_domain_model.services.core.dtos.create_consumer_dto import \
    CreateConsumerDto


class CreateOrderDto(TypedDict):
    consumer: CreateConsumerDto
    latest_time_of_delivery: datetime
    parcel: Parcel


class CreateOrdersDto(TypedDict):
    orders: list[CreateOrderDto]
