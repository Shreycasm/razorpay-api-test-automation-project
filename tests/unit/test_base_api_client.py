from unittest.mock import MagicMock

import pytest
import requests
from requests.auth import HTTPBasicAuth

from razorpay.api.base_api import BaseAPIClient
from razorpay.config.settings import settings


@pytest.fixture
def mock_response() -> MagicMock:
    response = MagicMock()
    response.status_code = 200
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

