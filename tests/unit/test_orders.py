from typing import Any
from unittest.mock import MagicMock

import pytest
from pydantic import ValidationError

from razorpay.api.orders_api import OrdersApi
from razorpay.models.requests.orders import (
    CreateOrderRequest,
    UpdateOrderRequest,
)
from razorpay.models.response.orders import (
    OrderListResponse,
    OrderResponse,
)


pytestmark = pytest.mark.unit


def mock_response(
    *,
    status_code: int,
    json_data: dict[str, Any],
) -> MagicMock:
    response = MagicMock()
    response.status_code = status_code
    response.ok = 200 <= status_code <= 299
    response.json.return_value = json_data
    response.text = str(json_data)

    return response


@pytest.mark.positive
def test_create_order_sends_correct_request(
    orders_api: OrdersApi,
    valid_order_response_dict: dict[str, Any],
    create_valid_order_dict: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    response = mock_response(
        status_code=200,
        json_data=valid_order_response_dict,
    )

    mock_post = MagicMock(return_value=response)

    monkeypatch.setattr(
        orders_api,
        "post",
        mock_post,
    )

    orders_api.create_order(create_valid_order_dict)

    expected_payload = CreateOrderRequest.model_validate(
        create_valid_order_dict
    ).to_api_payload()

    mock_post.assert_called_once_with(
        endpoint="/v1/orders",
        json=expected_payload,
        raise_for_error=True,
    )


@pytest.mark.negative
def test_create_order_rejects_invalid_payload(
    orders_api: OrdersApi,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    invalid_payload = {
        "amount": -100,
        "currency": "INR",
    }

    mock_post = MagicMock()

    monkeypatch.setattr(
        orders_api,
        "post",
        mock_post,
    )

    with pytest.raises(ValidationError):
        orders_api.create_order(invalid_payload)

    mock_post.assert_not_called()


@pytest.mark.negative
def test_create_order_rejects_invalid_response(
    orders_api: OrdersApi,
    create_valid_order_dict: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    response = mock_response(
        status_code=200,
        json_data={
            "id": "order_123",
        },
    )

    mock_post = MagicMock(return_value=response)

    monkeypatch.setattr(
        orders_api,
        "post",
        mock_post,
    )

    with pytest.raises(ValidationError):
        orders_api.create_order(create_valid_order_dict)


@pytest.mark.positive
def test_create_order_raw_returns_raw_response(
    orders_api: OrdersApi,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    response = mock_response(
        status_code=400,
        json_data={
            "error": {
                "code": "BAD_REQUEST_ERROR",
            }
        },
    )

    mock_post = MagicMock(return_value=response)

    monkeypatch.setattr(
        orders_api,
        "post",
        mock_post,
    )

    payload = {
        "amount": -100,
    }

    result = orders_api.create_order_raw(payload)

    assert result is response

    mock_post.assert_called_once_with(
        endpoint="/v1/orders",
        json=payload,
        raise_for_error=False,
    )


@pytest.mark.positive
def test_get_order_success(
    orders_api: OrdersApi,
    valid_order_response_dict: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    response = mock_response(
        status_code=200,
        json_data=valid_order_response_dict,
    )

    mock_get = MagicMock(return_value=response)

    monkeypatch.setattr(
        orders_api,
        "get",
        mock_get,
    )

    result = orders_api.get_order(
        "order_TI1JG5cveAZ3d1",
    )

    assert result.http is response
    assert isinstance(result.data, OrderResponse)
    assert result.data.id == "order_TI1JG5cveAZ3d1"

    mock_get.assert_called_once_with(
        endpoint="/v1/orders/order_TI1JG5cveAZ3d1",
        raise_for_error=True,
    )


@pytest.mark.negative
def test_get_order_rejects_invalid_response(
    orders_api: OrdersApi,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    response = mock_response(
        status_code=200,
        json_data={
            "id": "order_123",
        },
    )

    mock_get = MagicMock(return_value=response)

    monkeypatch.setattr(
        orders_api,
        "get",
        mock_get,
    )

    with pytest.raises(ValidationError):
        orders_api.get_order(
            "order_TI1JG5cveAZ3d1",
        )


@pytest.mark.positive
def test_get_order_raw_returns_raw_response(
    orders_api: OrdersApi,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    response = mock_response(
        status_code=404,
        json_data={
            "error": {
                "code": "NOT_FOUND",
            }
        },
    )

    mock_get = MagicMock(return_value=response)

    monkeypatch.setattr(
        orders_api,
        "get",
        mock_get,
    )

    result = orders_api.get_order_raw(
        "order_invalid",
    )

    assert result is response

    mock_get.assert_called_once_with(
        endpoint="/v1/orders/order_invalid",
        raise_for_error=False,
    )


@pytest.mark.positive
def test_list_orders_success(
    orders_api: OrdersApi,
    valid_list_order_response_dict: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    response = mock_response(
        status_code=200,
        json_data=valid_list_order_response_dict,
    )

    mock_get = MagicMock(return_value=response)

    monkeypatch.setattr(
        orders_api,
        "get",
        mock_get,
    )

    result = orders_api.list_orders(
        count=10,
        skip=20,
    )

    assert result.http is response
    assert isinstance(result.data, OrderListResponse)

    mock_get.assert_called_once_with(
        endpoint="/v1/orders",
        params={
            "count": 10,
            "skip": 20,
        },
        raise_for_error=True,
    )


@pytest.mark.negative
def test_list_orders_rejects_invalid_response(
    orders_api: OrdersApi,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    response = mock_response(
        status_code=200,
        json_data={
            "count": 10,
        },
    )

    mock_get = MagicMock(return_value=response)

    monkeypatch.setattr(
        orders_api,
        "get",
        mock_get,
    )

    with pytest.raises(ValidationError):
        orders_api.list_orders(
            count=10,
        )


@pytest.mark.positive
def test_list_orders_raw_returns_raw_response(
    orders_api: OrdersApi,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    response = mock_response(
        status_code=400,
        json_data={
            "error": {
                "code": "BAD_REQUEST_ERROR",
            }
        },
    )

    mock_get = MagicMock(return_value=response)

    monkeypatch.setattr(
        orders_api,
        "get",
        mock_get,
    )

    result = orders_api.list_orders_raw(
        count=10,
    )

    assert result is response

    mock_get.assert_called_once_with(
        endpoint="/v1/orders",
        params={
            "count": 10,
        },
        raise_for_error=False,
    )


@pytest.mark.positive
def test_update_order_success(
    orders_api: OrdersApi,
    valid_order_response_dict: dict[str, Any],
    update_valid_order_dict: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    response = mock_response(
        status_code=200,
        json_data=valid_order_response_dict,
    )

    mock_patch = MagicMock(return_value=response)

    monkeypatch.setattr(
        orders_api,
        "patch",
        mock_patch,
    )

    result = orders_api.update_order(
        "order_TI1JG5cveAZ3d1",
        update_valid_order_dict,
    )

    assert result.http is response
    assert isinstance(result.data, OrderResponse)

    expected_payload = UpdateOrderRequest.model_validate(
        update_valid_order_dict
    ).to_api_payload()

    mock_patch.assert_called_once_with(
        endpoint="/v1/orders/order_TI1JG5cveAZ3d1",
        json=expected_payload,
        raise_for_error=True,
    )


@pytest.mark.negative
def test_update_order_rejects_invalid_payload(
    orders_api: OrdersApi,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    invalid_payload = {
        "notes": "invalid" * 25,
    }

    mock_patch = MagicMock()

    monkeypatch.setattr(
        orders_api,
        "patch",
        mock_patch,
    )

    with pytest.raises(ValidationError):
        orders_api.update_order(
            "order_TI1JG5cveAZ3d1",
            invalid_payload,
        )

    mock_patch.assert_not_called()


@pytest.mark.negative
def test_update_order_rejects_invalid_response(
    orders_api: OrdersApi,
    update_valid_order_dict: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    response = mock_response(
        status_code=200,
        json_data={
            "id": "order_123",
        },
    )

    mock_patch = MagicMock(return_value=response)

    monkeypatch.setattr(
        orders_api,
        "patch",
        mock_patch,
    )

    with pytest.raises(ValidationError):
        orders_api.update_order(
            "order_TI1JG5cveAZ3d1",
            update_valid_order_dict,
        )


@pytest.mark.positive
def test_update_order_raw_returns_raw_response(
    orders_api: OrdersApi,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    response = mock_response(
        status_code=400,
        json_data={
            "error": {
                "code": "BAD_REQUEST_ERROR",
            }
        },
    )

    mock_patch = MagicMock(return_value=response)

    monkeypatch.setattr(
        orders_api,
        "patch",
        mock_patch,
    )

    payload = {
        "notes": {
            "test": "invalid",
        }
    }

    result = orders_api.update_order_raw(
        "order_invalid",
        payload,
    )

    assert result is response

    mock_patch.assert_called_once_with(
        endpoint="/v1/orders/order_invalid",
        json=payload,
        raise_for_error=False,
    )
