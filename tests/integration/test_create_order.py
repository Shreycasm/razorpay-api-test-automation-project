from copy import deepcopy
from typing import Any

import pytest

from razorpay.api.orders_api import OrdersApi
from razorpay.enums.currency import Currency
from razorpay.validators.schema_validator import SchemaValidator

from tests.constants import ERROR_SCHEMA, ORDER_SCHEMA


pytestmark = pytest.mark.integration


@pytest.mark.positive
def test_create_order_success(
    orders_api: OrdersApi,
    create_valid_order_dict: dict[str, Any],
    schema_validator: SchemaValidator,
) -> None:

    response = orders_api.create_order(create_valid_order_dict)

    assert response.http.status_code == 200
    assert response.data.amount == create_valid_order_dict.get("amount")
    assert response.data.currency == create_valid_order_dict.get("currency")
    assert response.data.notes == create_valid_order_dict["notes"]
    assert response.data.receipt == create_valid_order_dict["receipt"]
    assert response.data.status == "created"

    schema_validator.validate(
        response.http.json(),
        ORDER_SCHEMA,
    )


@pytest.mark.positive
def test_create_order_success_without_optionals_fields(
    orders_api: OrdersApi,
    create_valid_order_dict: dict[str, Any],
    schema_validator: SchemaValidator,
) -> None:

    payload = deepcopy(create_valid_order_dict)
    payload.pop("notes")
    payload.pop("receipt")

    response = orders_api.create_order(payload)

    assert response.http.status_code == 200
    assert response.data.status == "created"
    assert response.data.notes == []
    assert response.data.receipt is None

    schema_validator.validate(
        response.http.json(),
        ORDER_SCHEMA,
    )


@pytest.mark.positive
def test_create_order_with_maximum_notes(
    orders_api: OrdersApi,
    create_valid_order_dict: dict[str, Any],
    schema_validator: SchemaValidator,
) -> None:

    payload = deepcopy(create_valid_order_dict)
    payload["notes"] = {
        f"key_{i}": f"value_{i}"
        for i in range(15)
    }

    response = orders_api.create_order(payload)

    assert response.http.status_code == 200
    assert response.data.notes == payload["notes"]

    schema_validator.validate(
        response.http.json(),
        ORDER_SCHEMA,
    )


@pytest.mark.positive
def test_create_order_with_maximum_notes_keys_length(
    orders_api: OrdersApi,
    create_valid_order_dict: dict[str, Any],
    schema_validator: SchemaValidator,
) -> None:

    payload = deepcopy(create_valid_order_dict)
    payload["notes"] = {"K" * 256: "value"}

    response = orders_api.create_order(payload)

    assert response.http.status_code == 200
    assert response.data.notes == payload["notes"]

    schema_validator.validate(
        response.http.json(),
        ORDER_SCHEMA,
    )


@pytest.mark.positive
def test_create_order_with_maximum_notes_values_length(
    orders_api: OrdersApi,
    create_valid_order_dict: dict[str, Any],
    schema_validator: SchemaValidator,
) -> None:

    payload = deepcopy(create_valid_order_dict)
    payload["notes"] = {"keys": "V" * 256}

    response = orders_api.create_order(payload)

    assert response.http.status_code == 200
    assert response.data.notes == payload["notes"]

    schema_validator.validate(
        response.http.json(),
        ORDER_SCHEMA,
    )


@pytest.mark.positive
def test_create_order_with_maximum_receipt_length(
    orders_api: OrdersApi,
    create_valid_order_dict: dict[str, Any],
    schema_validator: SchemaValidator,
) -> None:

    payload = deepcopy(create_valid_order_dict)
    payload["receipt"] = "R" * 40

    response = orders_api.create_order(payload)

    assert response.http.status_code == 200
    assert response.data.receipt == payload["receipt"]

    schema_validator.validate(
        response.http.json(),
        ORDER_SCHEMA,
    )


@pytest.mark.positive
@pytest.mark.parametrize(
    "currency",
    [
        Currency.INR,
        Currency.USD,
        Currency.AED,
        Currency.EUR,
    ],
)
def test_create_order_with_different_currencies(
    orders_api: OrdersApi,
    create_valid_order_dict: dict[str, Any],
    schema_validator: SchemaValidator,
    currency: Currency,
) -> None:

    payload = deepcopy(create_valid_order_dict)
    payload["currency"] = currency.value

    response = orders_api.create_order(payload)

    assert response.http.status_code == 200
    assert response.data.currency == currency.value

    schema_validator.validate(
        response.http.json(),
        ORDER_SCHEMA,
    )


@pytest.mark.positive
def test_create_order_amount_breakdown(
    orders_api: OrdersApi,
    create_valid_order_dict: dict[str, Any],
    schema_validator: SchemaValidator,
) -> None:

    response = orders_api.create_order(create_valid_order_dict)

    assert response.http.status_code == 200
    assert (
        response.data.amount_due + response.data.amount_paid
        == response.data.amount
    )

    schema_validator.validate(
        response.http.json(),
        ORDER_SCHEMA,
    )


@pytest.mark.positive
def test_create_order_unique_order_id(
    orders_api: OrdersApi,
    create_valid_order_dict: dict[str, Any],
    schema_validator: SchemaValidator,
) -> None:

    payload = create_valid_order_dict

    response_1 = orders_api.create_order(payload)
    response_2 = orders_api.create_order(payload)

    assert response_1.http.status_code == 200
    assert response_2.http.status_code == 200
    assert response_1.data.id != response_2.data.id

    schema_validator.validate(
        response_1.http.json(),
        ORDER_SCHEMA,
    )

    schema_validator.validate(
        response_2.http.json(),
        ORDER_SCHEMA,
    )


@pytest.mark.negative
def test_create_order_missing_amount(
    orders_api: OrdersApi,
    schema_validator: SchemaValidator,
    create_valid_order_dict: dict[str, Any],
) -> None:

    payload = deepcopy(create_valid_order_dict)
    payload.pop("amount")

    response = orders_api.create_order_raw(payload)

    assert response.status_code == 400

    schema_validator.validate(
        response.json(),
        ERROR_SCHEMA,
    )


@pytest.mark.negative
def test_create_order_missing_currency(
    orders_api: OrdersApi,
    schema_validator: SchemaValidator,
    create_valid_order_dict: dict[str, Any],
) -> None:

    payload = deepcopy(create_valid_order_dict)
    payload.pop("currency")

    response = orders_api.create_order_raw(payload)

    assert response.status_code == 400

    schema_validator.validate(
        response.json(),
        ERROR_SCHEMA,
    )


@pytest.mark.negative
@pytest.mark.parametrize(
    "invalid_amount",
    [
        0,
        -1,
        10.5,
        "one-hundred",
        99,
        None,
        True,
    ],
)
def test_create_order_invalid_amount(
    orders_api: OrdersApi,
    create_valid_order_dict: dict[str, Any],
    schema_validator: SchemaValidator,
    invalid_amount: Any,
) -> None:

    payload = deepcopy(create_valid_order_dict)
    payload["amount"] = invalid_amount

    response = orders_api.create_order_raw(payload)

    assert response.status_code == 400

    schema_validator.validate(
        response.json(),
        ERROR_SCHEMA,
    )


@pytest.mark.negative
@pytest.mark.parametrize(
    "invalid_currency",
    [
        123,
        "USDT",
        None,
        "inr",
        "Inr",
        "",
    ],
)
def test_create_order_invalid_currency(
    orders_api: OrdersApi,
    create_valid_order_dict: dict[str, Any],
    schema_validator: SchemaValidator,
    invalid_currency: Any,
) -> None:

    payload = deepcopy(create_valid_order_dict)
    payload["currency"] = invalid_currency

    response = orders_api.create_order_raw(payload)

    assert response.status_code == 400

    schema_validator.validate(
        response.json(),
        ERROR_SCHEMA,
    )


@pytest.mark.negative
@pytest.mark.xfail(
    reason=(
        "Sandbox accepts more than 40 characters for receipt, "
        "but the documentation says it should be 40."
    ),
    strict=True,
)
def test_create_order_receipt_more_than_40(
    orders_api: OrdersApi,
    create_valid_order_dict: dict[str, Any],
    schema_validator: SchemaValidator,
) -> None:

    payload = deepcopy(create_valid_order_dict)
    payload["receipt"] = "R" * 41

    response = orders_api.create_order_raw(payload)

    assert response.status_code == 400

    schema_validator.validate(
        response.json(),
        ERROR_SCHEMA,
    )


@pytest.mark.negative
@pytest.mark.parametrize(
    "invalid_receipt",
    [
        pytest.param(
            "😀",
            id="emoji",
        ),
        pytest.param(
            "中文",
            id="chinese",
            marks=pytest.mark.xfail(
                reason=(
                    "Sandbox accepts non-ASCII Chinese characters "
                    "for receipt although the documentation says "
                    "receipt should contain ASCII characters."
                ),
                strict=True,
            ),
        ),
        pytest.param(
            "العربية",
            id="arabic",
            marks=pytest.mark.xfail(
                reason=(
                    "Sandbox accepts non-ASCII Arabic characters "
                    "for receipt although the documentation says "
                    "receipt should contain ASCII characters."
                ),
                strict=True,
            ),
        ),
        pytest.param(
            "€, ¥",
            id="currency_symbols",
            marks=pytest.mark.xfail(
                reason=(
                    "Sandbox accepts non-ASCII/special characters "
                    "for receipt although the documentation says "
                    "receipt should contain ASCII characters."
                ),
                strict=True,
            ),
        ),
    ],
)
def test_create_order_invalid_receipt(
    orders_api: OrdersApi,
    create_valid_order_dict: dict[str, Any],
    schema_validator: SchemaValidator,
    invalid_receipt: str,
) -> None:

    payload = deepcopy(create_valid_order_dict)
    payload["receipt"] = invalid_receipt

    response = orders_api.create_order_raw(payload)

    assert response.status_code == 400

    schema_validator.validate(
        response.json(),
        ERROR_SCHEMA,
    )


@pytest.mark.negative
@pytest.mark.xfail(
    reason=(
        "Sandbox accepts more than 15 notes, "
        "but the documentation says it should only accept 15."
    ),
    strict=True,
)
def test_create_order_notes_more_than_15(
    orders_api: OrdersApi,
    create_valid_order_dict: dict[str, Any],
    schema_validator: SchemaValidator,
) -> None:

    payload = deepcopy(create_valid_order_dict)
    payload["notes"] = {
        f"key_{i + 1}": f"value_{i + 1}"
        for i in range(17)
    }

    response = orders_api.create_order_raw(payload)

    assert response.status_code == 400

    schema_validator.validate(
        response.json(),
        ERROR_SCHEMA,
    )


@pytest.mark.negative
@pytest.mark.xfail(
    reason=(
        "Sandbox accepts notes keys with more than 256 characters, "
        "but the documentation says it should only accept 256."
    ),
    strict=True,
)
def test_create_order_notes_keys_more_than_256(
    orders_api: OrdersApi,
    create_valid_order_dict: dict[str, Any],
    schema_validator: SchemaValidator,
) -> None:

    payload = deepcopy(create_valid_order_dict)
    payload["notes"] = {"K" * 257: "Value"}

    response = orders_api.create_order_raw(payload)

    assert response.status_code == 400

    schema_validator.validate(
        response.json(),
        ERROR_SCHEMA,
    )


@pytest.mark.negative
@pytest.mark.xfail(
    reason=(
        "Sandbox accepts notes values with more than 256 characters, "
        "but the documentation says it should only accept 256."
    ),
    strict=True,
)
def test_create_order_notes_values_more_than_256(
    orders_api: OrdersApi,
    create_valid_order_dict: dict[str, Any],
    schema_validator: SchemaValidator,
) -> None:

    payload = deepcopy(create_valid_order_dict)
    payload["notes"] = {"keys": "V" * 257}

    response = orders_api.create_order_raw(payload)

    assert response.status_code == 400

    schema_validator.validate(
        response.json(),
        ERROR_SCHEMA,
    )


@pytest.mark.negative
def test_create_order_unexpected_fields(
    orders_api: OrdersApi,
    create_valid_order_dict: dict[str, Any],
    schema_validator: SchemaValidator,
) -> None:

    payload = deepcopy(create_valid_order_dict)
    payload["unexpected"] = "value"

    response = orders_api.create_order_raw(payload)

    assert response.status_code == 400

    schema_validator.validate(
        response.json(),
        ERROR_SCHEMA,
    )
