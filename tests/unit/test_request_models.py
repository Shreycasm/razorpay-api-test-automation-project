from __future__ import annotations

from typing import Any
from copy import deepcopy

import pytest
from pydantic import ValidationError

from razorpay.enums.currency import Currency
from razorpay.models.requests.orders import CreateOrderRequest, UpdateOrderRequest


def build_request(
    valid_request: dict[str, Any],
    **changes: Any,
) -> dict[str, Any]:
    request = deepcopy(valid_request)
    request.update(changes)

    return request


def test_validate_create_order_request_success(
    create_valid_order_dict: dict[str, Any],
) -> None:

    request = CreateOrderRequest(**create_valid_order_dict)

    assert request.amount == 100
    assert request.currency == Currency.INR
    assert request.receipt.startswith("receipt_")
    assert request.notes.get("source") == create_valid_order_dict["notes"]["source"]
    assert request.notes.get("framework") == create_valid_order_dict["notes"]["framework"]


def test_create_order_request_to_api_payload_excludes_none(
    create_valid_order_dict: dict[str, Any],
) -> None:
    request_data = deepcopy(create_valid_order_dict)
    request_data["receipt"] = None
    request_data["notes"] = None

    request = CreateOrderRequest(**request_data)

    payload = request.to_api_payload()

    assert payload == {
        "amount": 100,
        "currency": Currency.INR.value,
    }


@pytest.mark.parametrize(
    "field",
    [
        "amount",
        "currency",
    ],
)
def test_validate_create_order_request_missing_required_field(
    create_valid_order_dict: dict[str, Any],
    field: str,
) -> None:
    request = deepcopy(create_valid_order_dict)
    request.pop(field)

    with pytest.raises(ValidationError) as exc:
        CreateOrderRequest(**request)

    error = exc.value.errors()[0]

    assert error["loc"] == (field,)
    assert error["type"] == "missing"



@pytest.mark.parametrize(
    "amount",
    [
        -1,
        0,
        99,
    ],
)
def test_validate_create_order_request_invalid_amount(
    create_valid_order_dict: dict[str, Any],
    amount: int,
) -> None:
    request = build_request(
        create_valid_order_dict,
        amount=amount,
    )

    with pytest.raises(ValidationError) as exc:
        CreateOrderRequest(**request)

    assert any(
        error["loc"] == ("amount",)
        and error["type"] == "greater_than_equal"
        for error in exc.value.errors()
    )


@pytest.mark.parametrize(
    "currency",
    [
        123,
        "USDT",
        None,
    ],
)
def test_validate_create_order_request_invalid_currency(
    create_valid_order_dict: dict[str, Any],
    currency: Any,
) -> None:
    request = build_request(
        create_valid_order_dict,
        currency=currency,
    )

    with pytest.raises(ValidationError) as exc:
        CreateOrderRequest(**request)

    error = exc.value.errors()[0]

    assert error["loc"] == ("currency",)


def test_validate_create_order_request_receipt_too_long(
    create_valid_order_dict: dict[str, Any],
) -> None:
    request = build_request(
        create_valid_order_dict,
        receipt="S" * 41,
    )

    with pytest.raises(ValidationError) as exc:
        CreateOrderRequest(**request)

    error = exc.value.errors()[0]

    assert error["loc"] == ("receipt",)
    assert error["type"] == "string_too_long"


def test_validate_create_order_request_notes_more_than_15(
    create_valid_order_dict: dict[str, Any],
) -> None:
    request = build_request(
        create_valid_order_dict,
        notes={
            f"key_{i}": f"value_{i}"
            for i in range(16)
        },
    )

    with pytest.raises(ValidationError) as exc:
        CreateOrderRequest(**request)

    error = exc.value.errors()[0]

    assert error["loc"] == ("notes",)
    assert error["type"] == "too_long"


def test_validate_create_order_request_notes_key_too_long(
    create_valid_order_dict: dict[str, Any],
) -> None:
    request = build_request(
        create_valid_order_dict,
        notes={
            "S" * 257: "value",
        },
    )

    with pytest.raises(ValidationError) as exc:
        CreateOrderRequest(**request)

    error = exc.value.errors()[0]

    assert error["loc"][0] == "notes"
    assert error["loc"][-1] == "[key]"
    assert error["type"] == "string_too_long"


def test_validate_create_order_request_notes_value_too_long(
    create_valid_order_dict: dict[str, Any],
) -> None:
    request = build_request(
        create_valid_order_dict,
        notes={
            "key": "V" * 257,
        },
    )

    with pytest.raises(ValidationError) as exc:
        CreateOrderRequest(**request)

    error = exc.value.errors()[0]

    assert error["loc"] == ("notes", "key")
    assert error["type"] == "too_long"


def test_validate_create_order_request_extra_field(
    create_valid_order_dict: dict[str, Any],
) -> None:
    request = build_request(
        create_valid_order_dict,
        extra_field="unexpected",
    )

    with pytest.raises(ValidationError) as exc:
        CreateOrderRequest(**request)

    error = exc.value.errors()[0]

    assert error["loc"] == ("extra_field",)
    assert error["type"] == "extra_forbidden"


def test_validate_update_order_request_success(
    update_valid_order_dict: dict[str, Any],
) -> None:
    request = UpdateOrderRequest(**update_valid_order_dict)

    assert isinstance(request, UpdateOrderRequest)
    assert request.notes["source"] == update_valid_order_dict["notes"]["source"]
    assert request.notes["framework"] == update_valid_order_dict["notes"]["framework"]


def test_update_order_request_to_api_payload(
    update_valid_order_dict: dict[str, Any],
) -> None:
    request = UpdateOrderRequest(**update_valid_order_dict)

    payload = request.to_api_payload()

    assert payload == {
        "notes": {
            "source": update_valid_order_dict["notes"]["source"],
            "framework": update_valid_order_dict["notes"]["framework"]
        },
    }


def test_validate_update_order_request_missing_notes(
    update_valid_order_dict: dict[str, Any],
) -> None:
    request = deepcopy(update_valid_order_dict)
    request.pop("notes")

    with pytest.raises(ValidationError) as exc:
        UpdateOrderRequest(**request)

    error = exc.value.errors()[0]

    assert error["loc"] == ("notes",)
    assert error["type"] == "missing"


def test_validate_update_order_request_notes_more_than_15(
    update_valid_order_dict: dict[str, Any],
) -> None:
    request = build_request(
        update_valid_order_dict,
        notes={
            f"key_{i}": f"value_{i}"
            for i in range(16)
        },
    )

    with pytest.raises(ValidationError) as exc:
        UpdateOrderRequest(**request)

    error = exc.value.errors()[0]

    assert error["loc"] == ("notes",)
    assert error["type"] == "too_long"


def test_validate_update_order_request_notes_key_too_long(
    update_valid_order_dict: dict[str, Any],
) -> None:
    request = build_request(
        update_valid_order_dict,
        notes={
            "S" * 257: "value",
        },
    )

    with pytest.raises(ValidationError) as exc:
        UpdateOrderRequest(**request)

    error = exc.value.errors()[0]

    assert error["loc"][0] == "notes"
    assert error["loc"][-1] == "[key]"
    assert error["type"] == "string_too_long"


def test_validate_update_order_request_notes_value_too_long(
    update_valid_order_dict: dict[str, Any],
) -> None:
    request = build_request(
        update_valid_order_dict,
        notes={
            "key": "V" * 257,
        },
    )

    with pytest.raises(ValidationError) as exc:
        UpdateOrderRequest(**request)

    error = exc.value.errors()[0]

    assert error["loc"] == ("notes", "key")
    assert error["type"] == "too_long"


def test_validate_update_order_request_extra_field(
    update_valid_order_dict: dict[str, Any],
) -> None:
    request = build_request(
        update_valid_order_dict,
        extra_field="unexpected",
    )

    with pytest.raises(ValidationError) as exc:
        UpdateOrderRequest(**request)

    error = exc.value.errors()[0]

    assert error["loc"] == ("extra_field",)
    assert error["type"] == "extra_forbidden"
