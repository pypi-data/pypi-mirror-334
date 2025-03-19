from typing import TypedDict
from uuid import UUID

from ed_domain_model.services.core.dtos.create_car_dto import CreateCarDto
from ed_domain_model.services.core.dtos.create_location_dto import \
    CreateLocationDto


class CreateDriverDto(TypedDict):
    user_id: UUID
    first_name: str
    last_name: str
    profile_image: str
    phone_number: str
    email: str
    location: CreateLocationDto
    car: CreateCarDto
