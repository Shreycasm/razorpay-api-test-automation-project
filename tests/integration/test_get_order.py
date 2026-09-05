from copy import deepcopy
from typing import Any

import allure
import pytest

from razorpay.api.orders_api import OrdersApi
from razorpay.validators.schema_validator import SchemaValidator
from tests.constants import ERROR_SCHEMA, ORDER_SCHEMA

pytestmark = pytest.mark.integration


@pytest.fixture(autouse=True)
def allure_get_order_labels() -> None:
    allure.dynamic.epic("Razorpay API")
    allure.dynamic.feature("Orders API")
    allure.dynamic.story("Get Order")


@pytest.mark.positive
@allure.severity(allure.severity_level.CRITICAL)
def test_get_order_by_order_id_success(
    create_valid_order_dict: dict[str, Any],
    orders_api: OrdersApi,
    schema_validator: SchemaValidator,
) -> None:

    payload = deepcopy(create_valid_order_dict)

    post_response = orders_api.create_order(
        payload=payload,
    )

    get_response = orders_api.get_order(
        order_id=post_response.data.id,
    )

    assert get_response.http.status_code == 200
    assert get_response.data.id == post_response.data.id

    schema_validator.validate(
        get_response.http.json(),
        ORDER_SCHEMA,
    )


@pytest.mark.negative
@pytest.mark.parametrize(
    "invalid_order_id",
    [
        "ord_test",
        "order_TVz59mXM4yfQc",
        "1234567890123456789012",
        None,
        True,
    ],
)
def test_get_order_invalid_order_id(
    orders_api: OrdersApi,
    schema_validator: SchemaValidator,
    invalid_order_id: Any,
) -> None:

    response = orders_api.get_order_raw(
        order_id=invalid_order_id,
    )

    assert response.status_code == 400

    schema_validator.validate(
        response.json(),
        ERROR_SCHEMA,
    )