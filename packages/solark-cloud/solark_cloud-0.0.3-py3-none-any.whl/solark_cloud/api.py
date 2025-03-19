"""Implementation of Sol-Ark Cloud API."""

import time
import typing

import requests

from .schemas import (
    FlowRequest,
    FlowResponse,
    GenericResponse,
    LoginRequest,
    LoginResponse,
    PlantsRequest,
    PlantsResponse,
    RequestT,
    ResponseT,
)


class SolArkCloudException(Exception):
    """Base exception for Sol-Ark Cloud API client."""

    def __init__(self, msg: str, code: int, **_: typing.Any):
        super().__init__(msg)
        self.msg = msg
        self.code = code

    def __repr__(self):
        return f"{self.__class__.__name__} {self.code}: {self.msg}"


class NotLoggedInError(SolArkCloudException):
    """Raised when a request is made before logging in."""

    def __init__(self):
        super().__init__("Must call login() first to get credentials", 1001)


class TokenExpiredError(SolArkCloudException):
    """Raised when the access token has expired."""

    def __init__(self):
        super().__init__("Access token has expired", 1002)


class AuthenticationError(SolArkCloudException):
    """Raised when authentication fails."""


class UnknownError(Exception):
    """Raised when an unknown error occurs."""


class SolArkCloud:
    """Sol-Ark Cloud API client."""

    def __init__(self, base_url: str = "https://api.solarkcloud.com"):
        self.base_url = base_url
        self.access_token = None
        self.refresh_token = None
        self.expires_at = None

    def _handle_request(
        self,
        endpoint: str,
        request: RequestT,
        responseType: ResponseT,
        params: dict = None,
    ) -> ResponseT:
        if self.access_token is None:
            raise NotLoggedInError()
        if time.time() >= self.expires_at:
            raise TokenExpiredError()

        # Add auth headers.
        headers = {
            "Authorization": f"Bearer {self.access_token}",
        }

        # Make the request and return it. This will raise any errors.
        return self._handle_response(
            requests.get(
                f"{self.base_url}/api/v1/{endpoint}",
                json=request.data,
                headers=headers,
                params=params,
            ),
            responseType,
        )

    def _handle_response(
        self, response: requests.Response, responseType: ResponseT
    ) -> ResponseT:

        # TODO: Should we propogate these or return our own error that abstracts?
        response.raise_for_status()

        # Start with a generic response which works for error conditions, but if it's
        # successful then go ahead and return the specific response type.
        generic = GenericResponse(response.json())
        if generic["success"]:
            return responseType(response.json())

        # If it's not successful, then we need to raise an error. These are discovered
        # by trial and error.
        if generic["code"] == 102:
            raise AuthenticationError(**generic.data)

        # We don't know what the error is, so we'll just raise a generic error. This means
        # we have never encountered this in development, unfortunately.
        raise UnknownError(**generic.data)

    def login(self, username: str, password: str) -> LoginResponse:
        """Login to Sol-Ark Cloud API."""
        payload = LoginRequest(
            {
                "username": username,
                "password": password,
            }
        ).data
        response = self._handle_response(
            requests.post(f"{self.base_url}/oauth/token", json=payload), LoginResponse
        )
        self.access_token = response["data"]["access_token"]
        self.refresh_token = response["data"]["refresh_token"]
        self.expires_at = time.time() + response["data"]["expires_in"]
        return response

    def plants(self) -> PlantsResponse:
        """Get list of all available plants."""
        return self._handle_request(
            "plants",
            PlantsRequest(),
            PlantsResponse,
            params={
                # TODO: Handle pagination properly.
                "page": 1,
                "limit": 100,
                "name": "",
                "status": "",
                "type": -1,
                "sortCol": "createAt",
                "order": 2,
            },
        )

    def flow(self, plant_id: int) -> FlowResponse:
        """Get flow data for a plant."""
        return self._handle_request(
            f"plant/energy/{plant_id}/flow", FlowRequest(), FlowResponse
        )
