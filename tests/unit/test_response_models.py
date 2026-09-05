from __future__ import annotations

from copy import deepcopy
from typing import Any

import allure
import pytest
from pydantic import ValidationError

from razorpay.models.response.orders import (
    OrderListResponse,
    OrderResponse,
)


pytestmark = pytest.mark.unit


@pytest.fixture(autouse=True)
def allure_response_models_labels() -> None:
    allure.dynamic.epic("Razorpay API")
    allure.dynamic.feature("Framework")
    allure.dynamic.story("Response Models")


@pytest.mark.positive
def test_validate_order_response_success(
    valid_order_response_dict: dict[str, Any],
) -> None:
    response = OrderResponse.model_validate(
        valid_order_response_dict
    )

    assert isinstance(response, OrderResponse)


@pytest.mark.parametrize(
    "field",
    [
        "id",
        "entity",
        "amount",
        "amount_paid",
        "amount_due",
        "currency",
        "receipt",
        "status",
        "offer_id",
        "created_at",
        "attempts",
        "notes",
    ],
)
@pytest.mark.negative
def test_validate_order_response_missing_field(
    valid_order_response_dict: dict[str, Any],
    field: str,
) -> None:
    response = deepcopy(valid_order_response_dict)
    response.pop(field)

    with pytest.raises(ValidationError) as exc:
        OrderResponse.model_validate(response)

    error = exc.value.errors()[0]

    assert error["loc"] == (field,)
    assert error["type"] == "missing"


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("id", 123),
        ("entity", 123),
        ("amount", "#100"),
        ("amount_paid", "zero"),
        ("amount_due", "onehundred"),
        ("currency", 123),
        ("receipt", 123),
        ("status", 123),
        ("offer_id", 123),
        ("created_at", "/1785044647"),
        ("attempts", "/0/"),
        ("notes", 123),
    ],
)
@pytest.mark.negative
def test_validate_order_response_invalid_field_type(
    valid_order_response_dict: dict[str, Any],
    field: str,
    value: Any,
) -> None:
    response = deepcopy(valid_order_response_dict)
    response[field] = value

    with pytest.raises(ValidationError) as exc:
        OrderResponse.model_validate(response)

    error = exc.value.errors()[0]

    assert error["loc"][0] == field


@pytest.mark.parametrize(
    "field",
    [
        "amount_paid",
        "amount_due",
        "receipt",
        "offer_id",
    ],
)
@pytest.mark.positive
def test_validate_order_response_nullable_field(
    valid_order_response_dict: dict[str, Any],
    field: str,
) -> None:
    response = deepcopy(valid_order_response_dict)
    response[field] = None

    order = OrderResponse.model_validate(response)

    assert getattr(order, field) is None


@pytest.mark.positive
def test_validate_order_response_empty_notes(
    valid_order_response_dict: dict[str, Any],
) -> None:
    response = deepcopy(valid_order_response_dict)
    response["notes"] = []

    order = OrderResponse.model_validate(response)

    assert order.notes == []


@pytest.mark.positive
def test_validate_order_response_notes_dict(
    valid_order_response_dict: dict[str, Any],
) -> None:
    response = deepcopy(valid_order_response_dict)

    response["notes"] = {
        "source": "automation",
        "framework": "pytest",
    }

    order = OrderResponse.model_validate(response)

    assert order.notes == response["notes"]


@pytest.mark.positive
def test_validate_order_response_ignores_extra_field(
    valid_order_response_dict: dict[str, Any],
) -> None:
    response = deepcopy(valid_order_response_dict)
    response["unexpected"] = "value"

    order = OrderResponse.model_validate(response)

    assert not hasattr(order, "unexpected")


@pytest.mark.positive
def test_validate_order_list_response_success(
    valid_list_order_response_dict: dict[str, Any],
) -> None:
    response = OrderListResponse.model_validate(
        valid_list_order_response_dict
    )

    assert isinstance(response, OrderListResponse)
    assert len(response.items) == 1
    assert isinstance(response.items[0], OrderResponse)


@pytest.mark.parametrize(
    "field",
    [
        "entity",
        "count",
        "items",
    ],
)
@pytest.mark.negative
def test_validate_order_list_response_missing_field(
    valid_list_order_response_dict: dict[str, Any],
    field: str,
) -> None:
    response = deepcopy(valid_list_order_response_dict)
    response.pop(field)

    with pytest.raises(ValidationError) as exc:
        OrderListResponse.model_validate(response)

    error = exc.value.errors()[0]

    assert error["loc"] == (field,)
    assert error["type"] == "missing"


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("entity", 123),
        ("count", "#1"),
        ("items", "invalid"),
    ],
)
@pytest.mark.negative
def test_validate_order_list_response_invalid_field_type(
    valid_list_order_response_dict: dict[str, Any],
    field: str,
    value: Any,
) -> None:
    response = deepcopy(valid_list_order_response_dict)
    response[field] = value

    with pytest.raises(ValidationError) as exc:
        OrderListResponse.model_validate(response)

    error = exc.value.errors()[0]

    assert error["loc"][0] == field


@pytest.mark.positive
def test_validate_order_list_response_empty_items(
    valid_list_order_response_dict: dict[str, Any],
) -> None:
    response = deepcopy(valid_list_order_response_dict)
    response["items"] = []

    order_list = OrderListResponse.model_validate(response)

    assert order_list.items == []


@pytest.mark.negative
def test_validate_order_list_response_invalid_nested_order(
    valid_list_order_response_dict: dict[str, Any],
) -> None:
    response = deepcopy(valid_list_order_response_dict)

    response["items"][0]["amount"] = "invalid"

    with pytest.raises(ValidationError) as exc:
        OrderListResponse.model_validate(response)

    error = exc.value.errors()[0]

    assert error["loc"][0] == "items"


@pytest.mark.positive
def test_validate_order_list_response_ignores_extra_field(
    valid_list_order_response_dict: dict[str, Any],
) -> None:
    response = deepcopy(valid_list_order_response_dict)
    response["unexpected"] = "value"

    order_list = OrderListResponse.model_validate(response)

    assert not hasattr(order_list, "unexpected")


@pytest.mark.positive
def test_validate_order_list_response_nested_extra_field(
    valid_list_order_response_dict: dict[str, Any],
) -> None:
    response = deepcopy(valid_list_order_response_dict)

    response["items"][0]["unexpected"] = "value"

    order_list = OrderListResponse.model_validate(response)

    assert not hasattr(order_list.items[0], "unexpected")
