from typing import TypedDict
from uuid import UUID

from ed_domain_model.entities.location import Location


class BusinessModel(TypedDict):
    id: UUID
    business_name: str
    owner_first_name: str
    owner_last_name: str
    phone_number: str
    email: str
    location: Location
