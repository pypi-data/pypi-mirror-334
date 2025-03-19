from ed_domain_model.services.auth.dtos import (CreateUserDto,
                                                CreateUserVerifyDto,
                                                LoginUserDto,
                                                LoginUserVerifyDto,
                                                UnverifiedUserDto, UserDto,
                                                VerifyTokenDto)
from ed_domain_model.services.common.endpoint import (BaseEndpoint,
                                                      EndpointDescription)
from ed_domain_model.services.common.http_methods import HttpMethod


class AuthEndpoint(BaseEndpoint):
    def __init__(self, base_url: str):
        self._base_url = base_url
        self._descriptions: list[EndpointDescription] = [
            {
                'name': 'create_get_otp',
                'method': HttpMethod.POST,
                'path': f"{self._base_url}/auth/create/get-otp",
                'request_model': CreateUserDto,
                'response_model': UnverifiedUserDto
            },
            {
                'name': 'create_verify_otp',
                'method': HttpMethod.POST,
                'path': f"{self._base_url}/auth/create/verify-otp",
                'request_model': CreateUserVerifyDto,
                'response_model': UserDto
            },
            {
                'name': 'login_get_otp',
                'method': HttpMethod.POST,
                'path': f"{self._base_url}/auth/login/get-otp",
                'request_model': LoginUserDto,
                'response_model': UnverifiedUserDto
            },
            {
                'name': 'login_verify_otp',
                'method': HttpMethod.POST,
                'path': f"{self._base_url}/auth/login/verify-otp",
                'request_model': LoginUserVerifyDto,
                'response_model': UserDto
            },
            {
                'name': 'verify_token',
                'method': HttpMethod.POST,
                'path': f"{self._base_url}/auth/token/verify",
                'request_model': VerifyTokenDto,
                'response_model': UserDto
            }
        ]

    @property
    def descriptions(self) -> list[EndpointDescription]:
        return self._descriptions

