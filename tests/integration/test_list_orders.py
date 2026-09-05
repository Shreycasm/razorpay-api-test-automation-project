from typing import Any

import pytest

from razorpay.api.orders_api import OrdersApi
from razorpay.validators.schema_validator import SchemaValidator

from tests.constants import ERROR_SCHEMA, ORDER_LIST_SCHEMA


pytestmark = pytest.mark.integration


@pytest.mark.positive
def test_list_orders_success_with_no_query_params(
    orders_api: OrdersApi,
    schema_validator: SchemaValidator,
) -> None:

    response = orders_api.list_orders()

    assert response.http.status_code == 200
    assert response.data.count == 10
    assert len(response.data.items) == 10

    schema_validator.validate(
        instance=response.http.json(),
        schema_name=ORDER_LIST_SCHEMA,
    )


@pytest.mark.positive
@pytest.mark.parametrize(
    "authorized",
    [0, 1],
)
def test_list_orders_valid_authorized_param(
    orders_api: OrdersApi,
    schema_validator: SchemaValidator,
    authorized: int,
) -> None:

    response = orders_api.list_orders(
        authorized=authorized,
    )

    assert response.http.status_code == 200

    schema_validator.validate(
        instance=response.http.json(),
        schema_name=ORDER_LIST_SCHEMA,
    )


@pytest.mark.positive
@pytest.mark.parametrize(
    "count",
    [1, 10, 100],
)
def test_list_orders_valid_count_param(
    orders_api: OrdersApi,
    schema_validator: SchemaValidator,
    count: int,
) -> None:

    response = orders_api.list_orders(
        count=count,
    )

    assert response.http.status_code == 200
    assert len(response.data.items) <= count

    schema_validator.validate(
        instance=response.http.json(),
        schema_name=ORDER_LIST_SCHEMA,
    )


@pytest.mark.positive
@pytest.mark.parametrize(
    "skip",
    [1, 10, 100],
)
def test_list_orders_valid_skip_param(
    orders_api: OrdersApi,
    schema_validator: SchemaValidator,
    skip: int,
) -> None:

    response = orders_api.list_orders(
        skip=skip,
    )

    assert response.http.status_code == 200

    schema_validator.validate(
        instance=response.http.json(),
        schema_name=ORDER_LIST_SCHEMA,
    )


@pytest.mark.positive
def test_list_orders_valid_receipt_param(
    create_valid_order_dict: dict[str, Any],
    orders_api: OrdersApi,
    schema_validator: SchemaValidator,
) -> None:

    receipt = create_valid_order_dict["receipt"]

    response = orders_api.list_orders(
        receipt=receipt,
    )

    assert response.http.status_code == 200

    assert all(
        order.receipt == receipt
        for order in response.data.items
    )

    schema_validator.validate(
        instance=response.http.json(),
        schema_name=ORDER_LIST_SCHEMA,
    )


@pytest.mark.positive
def test_list_orders_valid_from_param(
    orders_api: OrdersApi,
    schema_validator: SchemaValidator,
) -> None:

    from_unix = 1788083097

    response = orders_api.list_orders(
        from_date=from_unix,
    )

    assert response.http.status_code == 200

    assert all(
        order.created_at >= from_unix
        for order in response.data.items
    )

    schema_validator.validate(
        instance=response.http.json(),
        schema_name=ORDER_LIST_SCHEMA,
    )


@pytest.mark.positive
def test_list_orders_valid_to_param(
    orders_api: OrdersApi,
    schema_validator: SchemaValidator,
) -> None:

    to_unix = 1788083097

    response = orders_api.list_orders(
        to_date=to_unix,
    )

    assert response.http.status_code == 200

    assert all(
        order.created_at <= to_unix
        for order in response.data.items
    )

    schema_validator.validate(
        instance=response.http.json(),
        schema_name=ORDER_LIST_SCHEMA,
    )


@pytest.mark.positive
def test_list_orders_with_all_valid_params(
    orders_api: OrdersApi,
    schema_validator: SchemaValidator,
) -> None:

    from_unix = 1784536311
    to_unix = 1788083097
    count = 1
    skip = 1
    authorized = 1
    receipt = "receipt"

    response = orders_api.list_orders(
        from_date=from_unix,
        to_date=to_unix,
        count=count,
        skip=skip,
        authorized=authorized,
        receipt=receipt,
    )

    assert response.http.status_code == 200

    schema_validator.validate(
        instance=response.http.json(),
        schema_name=ORDER_LIST_SCHEMA,
    )


@pytest.mark.positive
@pytest.mark.parametrize(
    "count",
    [1, 5, 15, 100],
)
def test_list_orders_respects_count(
    orders_api: OrdersApi,
    schema_validator: SchemaValidator,
    count: int,
) -> None:

    response = orders_api.list_orders(
        count=count,
    )

    assert response.http.status_code == 200
    assert len(response.data.items) <= count

    schema_validator.validate(
        instance=response.http.json(),
        schema_name=ORDER_LIST_SCHEMA,
    )


@pytest.mark.negative
@pytest.mark.parametrize(
    "invalid_count",
    [
        -1,
        0,
        101,
        "one-hundred",
        10.5,
        True,
    ],
)
def test_list_orders_invalid_count(
    orders_api: OrdersApi,
    schema_validator: SchemaValidator,
    invalid_count: Any,
) -> None:

    response = orders_api.list_orders_raw(
        count=invalid_count,
    )

    assert response.status_code == 400

    schema_validator.validate(
        instance=response.json(),
        schema_name=ERROR_SCHEMA,
    )


@pytest.mark.negative
@pytest.mark.parametrize(
    "invalid_skip",
    [
        "one-hundred",
        10.5,
        True,
    ],
)
def test_list_orders_invalid_skip(
    orders_api: OrdersApi,
    schema_validator: SchemaValidator,
    invalid_skip: Any,
) -> None:

    response = orders_api.list_orders_raw(
        skip=invalid_skip,
    )

    assert response.status_code == 400

    schema_validator.validate(
        instance=response.json(),
        schema_name=ERROR_SCHEMA,
    )


@pytest.mark.negative
def test_list_orders_negative_skip_sandbox_behavior(
    orders_api: OrdersApi,
    schema_validator: SchemaValidator,
) -> None:

    response = orders_api.list_orders_raw(
        skip=-1,
    )

    assert response.status_code == 200

    schema_validator.validate(
        instance=response.json(),
        schema_name=ORDER_LIST_SCHEMA,
    )


@pytest.mark.positive
def test_list_orders_reversed_date_range(
    orders_api: OrdersApi,
    schema_validator: SchemaValidator,
) -> None:

    from_unix = 1788083097
    to_unix = 1784536311

    response = orders_api.list_orders(
        from_date=from_unix,
        to_date=to_unix,
    )

    assert response.http.status_code == 200
    assert response.data.items == []

    schema_validator.validate(
        instance=response.http.json(),
        schema_name=ORDER_LIST_SCHEMA,
    )


@pytest.mark.negative
@pytest.mark.parametrize(
    "invalid_from",
    [
        "2026-01-01",
        "invalid",
        10.5,
        True,
    ],
)
def test_list_orders_invalid_from(
    orders_api: OrdersApi,
    schema_validator: SchemaValidator,
    invalid_from: Any,
) -> None:

    response = orders_api.list_orders_raw(
        from_date=invalid_from,
    )

    assert response.status_code == 400

    schema_validator.validate(
        instance=response.json(),
        schema_name=ERROR_SCHEMA,
    )


@pytest.mark.negative
@pytest.mark.parametrize(
    "invalid_to",
    [
        "2026-01-01",
        "invalid",
        10.5,
        True,
    ],
)
def test_list_orders_invalid_to(
    orders_api: OrdersApi,
    schema_validator: SchemaValidator,
    invalid_to: Any,
) -> None:

    response = orders_api.list_orders_raw(
        to_date=invalid_to,
    )

    assert response.status_code == 400

    schema_validator.validate(
        instance=response.json(),
        schema_name=ERROR_SCHEMA,
    )


@pytest.mark.negative
def test_list_order_with_invalid_param(
    orders_api: OrdersApi,
    schema_validator: SchemaValidator,
) -> None:

    response = orders_api.list_orders_raw(
        invalid_parameter=1,
    )

    assert response.status_code == 400

    schema_validator.validate(
        instance=response.json(),
        schema_name=ERROR_SCHEMA,
    )


@pytest.mark.negative
@pytest.mark.parametrize(
    "invalid_authorized",
    [
        -1,
        2,
        "true",
        1.5,
    ],
)
def test_list_orders_invalid_authorized(
    orders_api: OrdersApi,
    schema_validator: SchemaValidator,
    invalid_authorized: Any,
) -> None:

    response = orders_api.list_orders_raw(
        authorized=invalid_authorized,
    )

    assert response.status_code == 400

    schema_validator.validate(
        instance=response.json(),
        schema_name=ERROR_SCHEMA,
    )