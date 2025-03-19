from datetime import datetime
from typing import TypedDict
from uuid import UUID

from ed_domain_model.entities.route import WayPointAction


class WayPointDto(TypedDict):
    location_id: UUID
    action: WayPointAction
    eta: datetime
    sequence: int


class RouteDto(TypedDict):
    waypoints: list[WayPointDto]
    estimated_distance_in_kms: float
    estimated_time_in_minutes: int
