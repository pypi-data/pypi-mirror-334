from typing import TypedDict
from uuid import UUID


class Car(TypedDict):
    id: UUID
    make: str
    model: str
    year: int
    registration_number: str
    license_plate_number: str
    color: str
    seats: int
