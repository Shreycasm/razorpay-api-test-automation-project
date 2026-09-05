from typing import Any

import pytest
import allure

from razorpay.api.orders_api import OrdersApi
from razorpay.validators.schema_validator import SchemaValidator

from tests.constants import ERROR_SCHEMA, ORDER_SCHEMA


pytestmark = pytest.mark.integration


@pytest.fixture(autouse=True)
def allure_update_order_labels() -> None:
    allure.dynamic.epic("Razorpay API")
    allure.dynamic.feature("Orders API")
    allure.dynamic.story("Update Order")


@pytest.mark.positive
@allure.severity(allure.severity_level.CRITICAL)
def test_update_order_notes_success(
    create_valid_order_dict: dict[str, Any],
    update_valid_order_dict: dict[str, Any],
    orders_api: OrdersApi,
    schema_validator: SchemaValidator,
) -> None:
    create_response = orders_api.create_order(
        payload=create_valid_order_dict,
    )

    order_id = create_response.data.id

    response = orders_api.update_order(
        order_id=order_id,
        payload=update_valid_order_dict,
    )

    assert response.http.status_code == 200
    assert response.data.id == order_id
    assert response.data.notes == update_valid_order_dict["notes"]

    schema_validator.validate(
        instance=response.http.json(),
        schema_name=ORDER_SCHEMA,
    )


@pytest.mark.positive
def test_update_order_multiple_notes(
    create_valid_order_dict: dict[str, Any],
    orders_api: OrdersApi,
    schema_validator: SchemaValidator,
) -> None:
    create_response = orders_api.create_order(
        payload=create_valid_order_dict,
    )

    updated_notes = {
        "source": "automation",
        "framework": "pytest",
        "environment": "sandbox",
    }

    response = orders_api.update_order(
        order_id=create_response.data.id,
        payload={
            "notes": updated_notes,
        },
    )

    assert response.http.status_code == 200
    assert response.data.notes == updated_notes

    schema_validator.validate(
        instance=response.http.json(),
        schema_name=ORDER_SCHEMA,
    )


@pytest.mark.positive
def test_update_order_replaces_existing_notes(
    create_valid_order_dict: dict[str, Any],
    update_valid_order_dict: dict[str, Any],
    orders_api: OrdersApi,
    schema_validator: SchemaValidator,
) -> None:
    create_response = orders_api.create_order(
        payload=create_valid_order_dict,
    )

    order_id = create_response.data.id

    response = orders_api.update_order(
        order_id=order_id,
        payload=update_valid_order_dict,
    )

    assert response.http.status_code == 200
    assert response.data.notes == update_valid_order_dict["notes"]

    schema_validator.validate(
        instance=response.http.json(),
        schema_name=ORDER_SCHEMA,
    )


@pytest.mark.positive
def test_update_order_with_empty_notes(
    create_valid_order_dict: dict[str, Any],
    orders_api: OrdersApi,
    schema_validator: SchemaValidator,
) -> None:
    create_response = orders_api.create_order(
        payload=create_valid_order_dict,
    )

    response = orders_api.update_order(
        order_id=create_response.data.id,
        payload={
            "notes": {},
        },
    )

    assert response.http.status_code == 200
    assert response.data.notes == []

    schema_validator.validate(
        instance=response.http.json(),
        schema_name=ORDER_SCHEMA,
    )


@pytest.mark.positive
def test_update_order_notes_max_15_keys(
    create_valid_order_dict: dict[str, Any],
    orders_api: OrdersApi,
    schema_validator: SchemaValidator,
) -> None:
    create_response = orders_api.create_order(
        payload=create_valid_order_dict,
    )

    notes = {
        f"key_{index}": f"value_{index}"
        for index in range(15)
    }

    response = orders_api.update_order(
        order_id=create_response.data.id,
        payload={
            "notes": notes,
        },
    )

    assert response.http.status_code == 200
    assert len(response.data.notes) == 15

    schema_validator.validate(
        instance=response.http.json(),
        schema_name=ORDER_SCHEMA,
    )


@pytest.mark.xfail(
    reason=(
        "Sandbox accepts more than 15 notes but the Documentation "
        "says it should only accept 15"
    ),
    strict=True,
)
@pytest.mark.negative
def test_update_order_notes_more_than_15_keys(
    create_valid_order_dict: dict[str, Any],
    orders_api: OrdersApi,
    schema_validator: SchemaValidator,
) -> None:
    create_response = orders_api.create_order(
        payload=create_valid_order_dict,
    )

    notes = {
        f"key_{index}": f"value_{index}"
        for index in range(16)
    }

    response = orders_api.update_order_raw(
        order_id=create_response.data.id,
        payload={
            "notes": notes,
        },
    )

    assert response.status_code == 400

    schema_validator.validate(
        instance=response.json(),
        schema_name=ERROR_SCHEMA,
    )


@pytest.mark.positive
def test_update_order_notes_key_max_length(
    create_valid_order_dict: dict[str, Any],
    orders_api: OrdersApi,
    schema_validator: SchemaValidator,
) -> None:
    create_response = orders_api.create_order(
        payload=create_valid_order_dict,
    )

    notes = {
        "k" * 256: "value",
    }

    response = orders_api.update_order(
        order_id=create_response.data.id,
        payload={
            "notes": notes,
        },
    )

    assert response.http.status_code == 200

    schema_validator.validate(
        instance=response.http.json(),
        schema_name=ORDER_SCHEMA,
    )


@pytest.mark.xfail(
    reason=(
        "Sandbox accepts notes keys with more than 256 characters "
        "but the Documentation says it should only accept 256"
    ),
    strict=True,
)
@pytest.mark.negative
def test_update_order_notes_key_more_than_max_length(
    create_valid_order_dict: dict[str, Any],
    orders_api: OrdersApi,
    schema_validator: SchemaValidator,
) -> None:
    create_response = orders_api.create_order(
        payload=create_valid_order_dict,
    )

    notes = {
        "k" * 257: "value",
    }

    response = orders_api.update_order_raw(
        order_id=create_response.data.id,
        payload={
            "notes": notes,
        },
    )

    assert response.status_code == 400

    schema_validator.validate(
        instance=response.json(),
        schema_name=ERROR_SCHEMA,
    )


@pytest.mark.positive
def test_update_order_notes_value_max_length(
    create_valid_order_dict: dict[str, Any],
    orders_api: OrdersApi,
    schema_validator: SchemaValidator,
) -> None:
    create_response = orders_api.create_order(
        payload=create_valid_order_dict,
    )

    notes = {
        "key": "v" * 256,
    }

    response = orders_api.update_order(
        order_id=create_response.data.id,
        payload={
            "notes": notes,
        },
    )

    assert response.http.status_code == 200

    schema_validator.validate(
        instance=response.http.json(),
        schema_name=ORDER_SCHEMA,
    )


@pytest.mark.xfail(
    reason=(
        "Sandbox accepts notes values with more than 256 characters "
        "but the Documentation says it should only accept 256"
    ),
    strict=True,
)
@pytest.mark.negative
def test_update_order_notes_value_more_than_max_length(
    create_valid_order_dict: dict[str, Any],
    orders_api: OrdersApi,
    schema_validator: SchemaValidator,
) -> None:
    create_response = orders_api.create_order(
        payload=create_valid_order_dict,
    )

    notes = {
        "key": "v" * 257,
    }

    response = orders_api.update_order_raw(
        order_id=create_response.data.id,
        payload={
            "notes": notes,
        },
    )

    assert response.status_code == 400

    schema_validator.validate(
        instance=response.json(),
        schema_name=ERROR_SCHEMA,
    )


@pytest.mark.xfail(
    strict=True,
    reason=(
        "Razorpay documentation specifies HTTP 400 for a non-existent "
        "order ID, but the Sandbox currently returns HTTP 404."
    ),
)
@pytest.mark.parametrize(
    "invalid_order_id",
    [
        "test",
        "ord_test",
        "1234567890123456789012",
        "ord_1234567890123456789012",
        "",
    ],
)
@pytest.mark.negative
def test_update_order_invalid_order_id(
    orders_api: OrdersApi,
    schema_validator: SchemaValidator,
    invalid_order_id: str,
) -> None:
    response = orders_api.update_order_raw(
        order_id=invalid_order_id,
        payload={
            "notes": {
                "key": "value",
            },
        },
    )

    assert response.status_code == 400

    schema_validator.validate(
        instance=response.json(),
        schema_name=ERROR_SCHEMA,
    )


@pytest.mark.negative
def test_update_order_nonexistent_order_id(
    orders_api: OrdersApi,
    schema_validator: SchemaValidator,
) -> None:
    order_id = "order_TV000000000000"

    response = orders_api.update_order_raw(
        order_id=order_id,
        payload={
            "notes": {
                "key": "value",
            },
        },
    )

    assert response.status_code == 400

    schema_validator.validate(
        instance=response.json(),
        schema_name=ERROR_SCHEMA,
    )


@pytest.mark.parametrize(
    "field,value",
    [
        ("amount", 500),
        ("currency", "USD"),
        ("receipt", "updated_receipt"),
        ("status", "paid"),
    ],
)
@pytest.mark.negative
def test_update_order_immutable_field(
    create_valid_order_dict: dict[str, Any],
    orders_api: OrdersApi,
    schema_validator: SchemaValidator,
    field: str,
    value: Any,
) -> None:
    create_response = orders_api.create_order(
        payload=create_valid_order_dict,
    )

    response = orders_api.update_order_raw(
        order_id=create_response.data.id,
        payload={
            field: value,
        },
    )

    assert response.status_code == 400

    schema_validator.validate(
        instance=response.json(),
        schema_name=ERROR_SCHEMA,
    )


@pytest.mark.negative
def test_update_order_without_notes(
    create_valid_order_dict: dict[str, Any],
    orders_api: OrdersApi,
    schema_validator: SchemaValidator,
) -> None:
    create_response = orders_api.create_order(
        payload=create_valid_order_dict,
    )

    response = orders_api.update_order_raw(
        order_id=create_response.data.id,
        payload={},
    )

    assert response.status_code == 400

    schema_validator.validate(
        instance=response.json(),
        schema_name=ERROR_SCHEMA,
    )


@pytest.mark.positive
def test_update_order_notes_persist(
    create_valid_order_dict: dict[str, Any],
    update_valid_order_dict: dict[str, Any],
    orders_api: OrdersApi,
    schema_validator: SchemaValidator,
) -> None:
    create_response = orders_api.create_order(
        payload=create_valid_order_dict,
    )

    order_id = create_response.data.id

    update_response = orders_api.update_order(
        order_id=order_id,
        payload=update_valid_order_dict,
    )

    assert update_response.http.status_code == 200

    get_response = orders_api.get_order(
        order_id=order_id,
    )

    assert get_response.http.status_code == 200
    assert get_response.data.notes == update_valid_order_dict["notes"]

    schema_validator.validate(
        instance=get_response.http.json(),
        schema_name=ORDER_SCHEMA,
    )
