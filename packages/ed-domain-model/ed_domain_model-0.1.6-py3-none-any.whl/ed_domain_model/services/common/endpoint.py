from abc import ABCMeta, abstractmethod
from typing import Any, NotRequired, TypedDict

from ed_domain_model.services.common.http_methods import HttpMethod


class EndpointDescription(TypedDict):
    name: str
    path: str
    method: HttpMethod
    headers: NotRequired[type]
    query_params: NotRequired[type]
    path_params: NotRequired[dict[str, type]]
    request_model: NotRequired[type]
    response_model: NotRequired[type]


class EndpointCallParams(TypedDict):
    headers: NotRequired[dict]
    query_params: NotRequired[dict]
    path_params: NotRequired[dict]
    request: NotRequired[Any]


class BaseEndpoint(metaclass=ABCMeta):
    @property
    @abstractmethod
    def descriptions(self) -> list[EndpointDescription]: ...
       
    def get_description(self, name: str) -> EndpointDescription:
        for description in self.descriptions:
            if description['name'] == name:
                return description

        raise ValueError(f"Endpoint description not found for {name}")

