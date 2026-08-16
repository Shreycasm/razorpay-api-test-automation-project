from __future__ import annotations

from typing import Any

import pytest
from pydantic import ValidationError

from razorpay.models.requests.orders import CreateOrderRequest, UpdateOrderRequest

@pytest.fixture(scope="function")
def create_valid_order_model(
    create_valid_order_dict: dict[str, Any]
) -> CreateOrderRequest:

    return CreateOrderRequest(**create_valid_order_dict)


@pytest.fixture(scope="function")
def update_valid_order_model(
    update_valid_order_dict: dict[str, Any]
) -> UpdateOrderRequest:

    return UpdateOrderRequest(**update_valid_order_dict)


def build_request(
    create_valid_order_model: CreateOrderRequest,
    **changes: Any
) -> dict[str, Any]:

    request = create_valid_order_model.model_dump(mode="json")
    request.update(changes)

    return request



def build_update_request(
    update_valid_order_model: UpdateOrderRequest,
    **changes: Any
) -> dict[str, Any]:

    request = update_valid_order_model.model_dump(mode="json")
    request.update(changes)

    return request


def test_validate_create_order_request_succsess(
    create_valid_order_model: CreateOrderRequest
) -> None:

    assert isinstance(create_valid_order_model, CreateOrderRequest)


def test_validate_create_order_request_serialization(
    create_valid_order_model: CreateOrderRequest
) -> None:

    request = create_valid_order_model.model_dump(mode="json")

    assert request["amount"] == 100
    assert request["currency"] == "INR"
    assert request["notes"]["source"] == create_valid_order_model.notes["source"]
    assert request["notes"]["framework"] == create_valid_order_model.notes["framework"]
    assert request["receipt"].startswith("receipt_")



@pytest.mark.parametrize(
    "amount",
    [
        -1,
        99,
        0
    ]
)
def test_validate_cretae_order_request_invalid_amount(
    create_valid_order_model: CreateOrderRequest,
    amount: int
) -> None:

    request = build_request(
        create_valid_order_model=create_valid_order_model,
        amount=amount
    )

    with pytest.raises(ValidationError) as exc:
        CreateOrderRequest(**request)

    errors = exc.value.errors()
    assert any(
        error["loc"] == ("amount",)
        and error["type"] == "greater_than_equal"
        for error in errors
    )


@pytest.mark.parametrize(
    "currency",
    [123,"USDT", None],
)
def test_validate_create_order_invalid_currency(
    create_valid_order_model: CreateOrderRequest,
    currency: str,
) -> None:
    request = build_request(
        create_valid_order_model,
        currency=currency,
    )

    with pytest.raises(ValidationError) as exc:
        CreateOrderRequest(**request)

    error = exc.value.errors()[0]

    assert error["loc"] == ("currency",)
    assert error["type"] == "enum"


def test_validate_create_order_invalid_receipt_length(
    create_valid_order_model: CreateOrderRequest,
) -> None:
    request = build_request(
        create_valid_order_model,
        receipt="S" * 41,
    )

    with pytest.raises(ValidationError) as exc:
        CreateOrderRequest(**request)

    error = exc.value.errors()[0]

    assert error["loc"] == ("receipt",)
    assert error["type"] == "string_too_long"


def test_validate_create_order_notes_more_than_15(
    create_valid_order_model: CreateOrderRequest,
) -> None:
    request = build_request(
        create_valid_order_model,
        notes={f"key_{i}": f"value_{i}" for i in range(16)},
    )

    with pytest.raises(ValidationError) as exc:
        CreateOrderRequest(**request)

    error = exc.value.errors()[0]

    assert error["loc"] == ("notes",)
    assert error["type"] == "too_long"


def test_validate_create_order_notes_key_too_long(
    create_valid_order_model: CreateOrderRequest,
) -> None:
    request = build_request(
        create_valid_order_model,
        notes={"S" * 257: "value"},
    )

    with pytest.raises(ValidationError) as exc:
        CreateOrderRequest(**request)

    error = exc.value.errors()[0]

    assert error["loc"][0] == "notes"
    assert error["loc"][-1] == "[key]"
    assert error["type"] == "string_too_long"


def test_validate_create_order_notes_value_too_long(
    create_valid_order_model: CreateOrderRequest,
) -> None:
    request = build_request(
        create_valid_order_model,
        notes={"key": "V" * 257},
    )

    with pytest.raises(ValidationError) as exc:
        CreateOrderRequest(**request)

    error = exc.value.errors()[0]

    assert error["loc"] == ("notes", "key")
    assert error["type"] == "too_long"


def test_validate_create_order_extra_field(
    create_valid_order_model: CreateOrderRequest,
) -> None:
    request = build_request(
        create_valid_order_model,
        extra_field="unexpected",
    )

    with pytest.raises(ValidationError) as exc:
        CreateOrderRequest(**request)

    error = exc.value.errors()[0]

    assert error["type"] == "extra_forbidden"


def test_validate_update_order_succsess(
    update_valid_order_model: UpdateOrderRequest
) -> None:

    assert isinstance(update_valid_order_model, UpdateOrderRequest)


def test_validate_update_order_serialization(
    update_valid_order_model: UpdateOrderRequest
) -> None:

    request = update_valid_order_model.model_dump(mode="json")

    assert request["notes"] == update_valid_order_model.notes


def test_validate_update_order_invalid_notes_more_than_15(
    update_valid_order_model: UpdateOrderRequest,
) -> None:
    request = build_update_request(
        update_valid_order_model,
        notes={f"key_{i}": f"value_{i}" for i in range(16)},
    )

    with pytest.raises(ValidationError) as exc:
        UpdateOrderRequest(**request)

    error = exc.value.errors()[0]

    assert error["loc"] == ("notes",)
    assert error["type"] == "too_long"


def test_validate_update_order_notes_key_too_long(
    update_valid_order_model: UpdateOrderRequest
) -> None:
    request = build_update_request(
        update_valid_order_model,
        notes={"S" * 257: "value"},
    )

    with pytest.raises(ValidationError) as exc:
        UpdateOrderRequest(**request)

    error = exc.value.errors()[0]

    assert error["loc"][0] == "notes"
    assert error["loc"][-1] == "[key]"
    assert error["type"] == "string_too_long"


def test_validate_update_order_notes_value_too_long(
    update_valid_order_model: UpdateOrderRequest,
) -> None:
    request = build_update_request(
        update_valid_order_model,
        notes={"key": "V" * 257},
    )

    with pytest.raises(ValidationError) as exc:
        UpdateOrderRequest(**request)

    error = exc.value.errors()[0]

    assert error["loc"] == ("notes", "key")
    assert error["type"] == "too_long"


def test_validate_update_order_extra_field(
    update_valid_order_model: UpdateOrderRequest,
) -> None:
    request = build_update_request(
        update_valid_order_model,
        extra_field="unexpected",
    )

    with pytest.raises(ValidationError) as exc:
        UpdateOrderRequest(**request)

    error = exc.value.errors()[0]

    assert error["type"] == "extra_forbidden"
