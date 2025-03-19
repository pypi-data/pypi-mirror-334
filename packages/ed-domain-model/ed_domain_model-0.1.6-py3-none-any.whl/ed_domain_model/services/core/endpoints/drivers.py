from ed_domain_model.services.common.endpoint import (BaseEndpoint,
                                                      EndpointDescription)
from ed_domain_model.services.common.http_methods import HttpMethod
from ed_domain_model.services.core.dtos.create_driver_dto import \
    CreateDriverDto
from ed_domain_model.services.core.dtos.delivery_job_dto import DeliveryJobDto
from ed_domain_model.services.core.dtos.driver_dto import DriverDto


class DriversEndpoint(BaseEndpoint):
    def __init__(self, base_url: str):
        self._base_url = base_url
        self._descriptions: list[EndpointDescription] = [
            {
                'name': 'create_driver',
                'method': HttpMethod.POST,
                'path': f"{self._base_url}/drivers",
                'request_model': CreateDriverDto,
                'response_model': DriverDto
            },
            {
                'name': 'get_driver_delivery_jobs',
                'method': HttpMethod.GET,
                'path': f"{self._base_url}/drivers/{{driver_id}}/delivery-jobs",
                'path_params': {'driver_id': str},
                'response_model': list[DeliveryJobDto]
            },
            {
                'name': 'upload_driver_profile',
                'method': HttpMethod.POST,
                'path': f"{self._base_url}/drivers/{{driver_id}}/upload",
                'path_params': {'driver_id': str},
                'response_model': DriverDto
            },
            {
                'name': 'get_driver',
                'method': HttpMethod.GET,
                'path': f"{self._base_url}/drivers/{{driver_id}}",
                'path_params': {'driver_id': str},
                'response_model': DriverDto
            }
        ]

    @property
    def descriptions(self) -> list[EndpointDescription]:
        return self._descriptions
