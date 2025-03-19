from ed_domain_model.services.common.endpoint import (BaseEndpoint,
                                                      EndpointDescription)
from ed_domain_model.services.common.http_methods import HttpMethod
from ed_domain_model.services.core.dtos.business_dto import BusinessDto
from ed_domain_model.services.core.dtos.create_business_dto import \
    CreateBusinessDto
from ed_domain_model.services.core.dtos.create_orders_dto import CreateOrderDto
from ed_domain_model.services.core.dtos.order_dto import OrderDto


class BusinessesEndpoint(BaseEndpoint):
    def __init__(self, base_url: str):
        self._base_url = base_url
        self._descriptions: list[EndpointDescription]= [
            {
                'name': 'get_all_businesses',
                'method': HttpMethod.GET,
                'path': f"{self._base_url}/businesses",
                'response_model': list[BusinessDto]
            },
            {
                'name': 'create_business',
                'method': HttpMethod.POST,
                'path': f"{self._base_url}/businesses",
                'request_model': CreateBusinessDto,
                'response_model': BusinessDto
            },
            {
                'name': 'get_business',
                'method': HttpMethod.GET,
                'path': f"{self._base_url}/businesses/{{business_id}}",
                'path_params': {'business_id': str}, 
                'response_model': BusinessDto
            },
            {
                'name': 'get_business_orders',
                'method': HttpMethod.GET,
                'path': f"{self._base_url}/businesses/{{business_id}}/orders",
                'path_params': {'business_id': str}, 
                'response_model': list[OrderDto]
            },
            {
                'name': 'create_business_order',
                'method': HttpMethod.POST,
                'path': f"{self._base_url}/businesses/{{business_id}}/orders",
                'path_params': {'business_id': str}, 
                'request_model': CreateOrderDto,
                'response_model': OrderDto
            }
        ]

    @property
    def descriptions(self) -> list[EndpointDescription]:
        return self._descriptions
