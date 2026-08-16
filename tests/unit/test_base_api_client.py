from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest
import requests
from requests.auth import HTTPBasicAuth

from razorpay.api.base_api import BaseAPIClient
from razorpay.config.settings import settings
from razorpay.exception.api import ApiError 


@pytest.fixture
def base_api_client() -> BaseAPIClient:
    client = BaseAPIClient()

    yield client

    client.close()


@pytest.fixture
def mock_response() -> MagicMock:
    response = MagicMock()
    response.status_code = 200
    response.ok = True
    return response


def test_session_uses_basic_auth() -> None:

    base_api_client = BaseAPIClient()

    auth = base_api_client._session.auth

    assert isinstance(auth, HTTPBasicAuth)
    assert auth.username == settings.api_key
    assert auth.password == settings.api_key_secret.get_secret_value()

    base_api_client.close()


def test_session_has_default_headers() -> None:

    base_api_client = BaseAPIClient()

    headers = base_api_client._session.headers

    assert headers.get("Content-Type") == "application/json"
    assert headers.get("Accept") == "application/json"

    base_api_client.close()


def test_retry_configuration() -> None:
    base_api_client = BaseAPIClient()

    adapter = base_api_client._session.get_adapter("https://")

    retry = adapter.max_retries

    assert retry.total == 3

    assert retry.backoff_factor == 1

    assert retry.status_forcelist == [
        429,
        500,
        502,
        503,
        504,
    ]

    assert retry.allowed_methods == [
        "GET",
        "PUT",
        "DELETE",
    ]

    assert retry.raise_on_status is False


def test_retry_respects_retry_after_header() -> None:
    base_api_client = BaseAPIClient()

    adapter = base_api_client._session.get_adapter("https://")

    retry = adapter.max_retries

    assert retry.respect_retry_after_header is True


@pytest.mark.parametrize(
    "method",
    [
        "POST",
        "PATCH",
    ],
)
def test_non_idempotent_methods_are_not_retried(
    base_api_client: BaseAPIClient,
    method: str,
) -> None:

    adapter = base_api_client._session.get_adapter("https://")
    retry = adapter.max_retries

    assert method not in retry.allowed_methods


def test_request_builds_url_and_uses_default_timeout( 
    mock_response: MagicMock
    ) -> None:
    base_api_client = BaseAPIClient()

    base_api_client._session.request = MagicMock(
        return_value=mock_response
    )

    result = base_api_client.request(
        method="GET",
        endpoint="/v1/orders",
    )

    assert result is mock_response

    base_api_client._session.request.assert_called_once_with(
        method="GET",
        url=f"{base_api_client._base_url}/v1/orders",
        timeout=base_api_client._request_timeout_seconds,
    )



def test_request_normalizes_endpoint(
    mock_response: MagicMock,
    ) -> None:
    base_api_client = BaseAPIClient()

    base_api_client._session.request = MagicMock(
        return_value=mock_response
    )

    base_api_client.request(
        method="GET",
        endpoint="v1/orders",
    )

    base_api_client._session.request.assert_called_once_with(
        method="GET",
        url=f"{base_api_client._base_url}/v1/orders",
        timeout=base_api_client._request_timeout_seconds,
    )


def test_request_preserves_custom_timeout(
    mock_response: MagicMock,
    ) -> None:
    base_api_client = BaseAPIClient()

    base_api_client._session.request = MagicMock(
        return_value=mock_response
    )

    base_api_client.request(
        method="GET",
        endpoint="/v1/orders",
        timeout=30,
    )

    base_api_client._session.request.assert_called_once_with(
        method="GET",
        url=f"{base_api_client._base_url}/v1/orders",
        timeout=30,
    )


def test_request_passes_query_params(
    mock_response: MagicMock,
    ) -> None:
    base_api_client = BaseAPIClient()

    base_api_client._session.request = MagicMock(
        return_value=mock_response
    )

    base_api_client._session.request = MagicMock(
        return_value=mock_response
    )

    params = {
        "count": 10,
        "skip": 5,
    }

    base_api_client.request(
        method="GET",
        endpoint="/v1/orders",
        params=params,
    )

    base_api_client._session.request.assert_called_once_with(
        method="GET",
        url=f"{base_api_client._base_url}/v1/orders",
        timeout=base_api_client._request_timeout_seconds,
        params=params,
    )


def test_request_reraises_timeout() -> None:
    base_api_client = BaseAPIClient()

    base_api_client._session.request = MagicMock(
        side_effect=requests.Timeout("Request timed out")
    )

    with pytest.raises(requests.Timeout):
        base_api_client.request(
            method="GET",
            endpoint="/v1/orders",
        )


def test_request_reraises_connection_error() -> None:
    base_api_client = BaseAPIClient()

    base_api_client._session.request = MagicMock(
        side_effect=requests.ConnectionError(
            "Connection failed"
        )
    )

    with pytest.raises(requests.ConnectionError):
        base_api_client.request(
            method="GET",
            endpoint="/v1/orders",
        )


def test_request_reraises_generic_request_error() -> None:
    base_api_client = BaseAPIClient()

    base_api_client._session.request = MagicMock(
        side_effect=requests.RequestException(
            "Request failed"
        )
    )

    with pytest.raises(requests.RequestException):
        base_api_client.request(
            method="GET",
            endpoint="/v1/orders",
        )


def test_raise_for_api_error_returns_for_successful_response() -> None:
    base_api_client = BaseAPIClient()

    response = MagicMock()
    response.ok = True

    result = base_api_client.raise_for_api_error(response)

    assert result is None

    base_api_client.close()


def test_raise_for_api_error_raises_api_error(
    error_response_fixture: dict[str, Any],
) -> None:
    base_api_client = BaseAPIClient()

    response = MagicMock()
    response.ok = False
    response.status_code = 400
    response.json.return_value = error_response_fixture

    with pytest.raises(ApiError) as exc:
        base_api_client.raise_for_api_error(response)

    error = exc.value

    assert error.status_code == 400
    assert error.error_code == error_response_fixture["error"]["code"]
    assert error.message == error_response_fixture["error"]["description"]
    assert error.response_data == error_response_fixture

    base_api_client.close()


def test_raise_for_api_error_handles_invalid_error_response(
    base_api_client: BaseAPIClient,
) -> None:

    response = MagicMock()
    response.ok = False
    response.status_code = 500
    response.reason = "Internal Server Error"
    response.json.return_value = {
        "unexpected": "response"
    }

    with pytest.raises(ApiError) as exc_info:
        base_api_client.raise_for_api_error(response)

    error = exc_info.value

    assert error.status_code == 500
    assert error.message == "Internal Server Error"
    assert error.error_code is None
    assert error.response_data == {
        "unexpected": "response"
    }


def test_raise_for_api_error_handles_non_json_response(
    base_api_client: BaseAPIClient,
) -> None:

    response = MagicMock()
    response.ok = False
    response.status_code = 502
    response.reason = "Bad Gateway"
    response.json.side_effect = ValueError(
        "Invalid JSON"
    )

    with pytest.raises(ApiError) as exc_info:
        base_api_client.raise_for_api_error(response)

    error = exc_info.value

    assert error.status_code == 502
    assert error.message == "Bad Gateway"
    assert error.error_code is None
    assert error.response_data == {}


def test_raise_for_api_error_uses_default_message(
    base_api_client: BaseAPIClient,
) -> None:

    response = MagicMock()
    response.ok = False
    response.status_code = 500
    response.reason = ""
    response.json.return_value = {
        "unexpected": "response"
    }

    with pytest.raises(ApiError) as exc_info:
        base_api_client.raise_for_api_error(response)

    error = exc_info.value

    assert error.status_code == 500
    assert error.message == "API request failed"
    assert error.error_code is None
    assert error.response_data == {
        "unexpected": "response"
    }