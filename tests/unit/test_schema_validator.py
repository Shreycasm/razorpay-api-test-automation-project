from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

import allure
import pytest
from jsonschema import ValidationError

from razorpay.validators.schema_validator import SchemaValidator
from tests.constants import (
    ERROR_SCHEMA,
    ORDER_LIST_SCHEMA,
    ORDER_SCHEMA,
)


pytestmark = pytest.mark.unit


@pytest.fixture(autouse=True)
def allure_schema_validator_labels() -> None:
    allure.dynamic.epic("Razorpay API")
    allure.dynamic.feature("Framework")
    allure.dynamic.story("Schema Validator")


@pytest.mark.positive
def test_validate_order_schema_success(
    schema_validator: SchemaValidator,
    valid_order_response_dict: dict[str, Any],
) -> None:
    schema_validator.validate(
        valid_order_response_dict,
        ORDER_SCHEMA,
    )


@pytest.mark.parametrize(
    "field_name",
    [
        "id",
        "entity",
        "amount",
        "amount_paid",
        "amount_due",
        "currency",
        "receipt",
        "status",
        "attempts",
        "notes",
        "created_at",
        "offer_id",
    ],
)
@pytest.mark.negative
def test_validate_order_schema_missing_required_field(
    schema_validator: SchemaValidator,
    valid_order_response_dict: dict[str, Any],
    field_name: str,
) -> None:
    response = deepcopy(valid_order_response_dict)
    response.pop(field_name)

    with pytest.raises(ValidationError):
        schema_validator.validate(
            response,
            ORDER_SCHEMA,
        )


@pytest.mark.negative
def test_validate_order_schema_invalid_order_id(
    schema_validator: SchemaValidator,
    valid_order_response_dict: dict[str, Any],
) -> None:
    response = deepcopy(valid_order_response_dict)
    response["id"] = "collection_asbckajcabccja"

    with pytest.raises(ValidationError):
        schema_validator.validate(
            response,
            ORDER_SCHEMA,
        )


@pytest.mark.parametrize(
    "status",
    [
        "invalid",
        "CREATED",
        "PAID",
        "FAILED",
        "CONVERTED",
    ],
)
@pytest.mark.negative
def test_validate_order_schema_invalid_status(
    schema_validator: SchemaValidator,
    valid_order_response_dict: dict[str, Any],
    status: str,
) -> None:
    response = deepcopy(valid_order_response_dict)
    response["status"] = status

    with pytest.raises(ValidationError):
        schema_validator.validate(
            response,
            ORDER_SCHEMA,
        )


@pytest.mark.parametrize(
    "entity",
    [
        "ORDER",
        "payments",
        "collection",
    ],
)
@pytest.mark.negative
def test_validate_order_schema_invalid_order_entity(
    schema_validator: SchemaValidator,
    valid_order_response_dict: dict[str, Any],
    entity: str,
) -> None:
    response = deepcopy(valid_order_response_dict)
    response["entity"] = entity

    with pytest.raises(ValidationError):
        schema_validator.validate(
            response,
            ORDER_SCHEMA,
        )


@pytest.mark.negative
def test_validate_order_schema_invalid_created_at(
    schema_validator: SchemaValidator,
    valid_order_response_dict: dict[str, Any],
) -> None:
    response = deepcopy(valid_order_response_dict)
    response["created_at"] = "invalid"

    with pytest.raises(ValidationError):
        schema_validator.validate(
            response,
            ORDER_SCHEMA,
        )


@pytest.mark.negative
def test_validate_order_schema_additional_property(
    schema_validator: SchemaValidator,
    valid_order_response_dict: dict[str, Any],
) -> None:
    response = deepcopy(valid_order_response_dict)
    response["unexpected"] = "value"

    with pytest.raises(ValidationError):
        schema_validator.validate(
            response,
            ORDER_SCHEMA,
        )


@pytest.mark.positive
def test_validate_order_list_schema_success(
    schema_validator: SchemaValidator,
    valid_list_order_response_dict: dict[str, Any],
) -> None:
    schema_validator.validate(
        valid_list_order_response_dict,
        ORDER_LIST_SCHEMA,
    )


@pytest.mark.negative
def test_validate_order_list_schema_more_than_max_items(
    schema_validator: SchemaValidator,
    valid_list_order_response_dict: dict[str, Any],
) -> None:
    response = deepcopy(valid_list_order_response_dict)
    response["items"] *= 101
    response["count"] = len(response["items"])

    with pytest.raises(ValidationError):
        schema_validator.validate(
            response,
            ORDER_LIST_SCHEMA,
        )


@pytest.mark.parametrize(
    "entity",
    [
        "orders",
        "payments",
        "Collection",
    ],
)
@pytest.mark.negative
def test_validate_order_list_schema_invalid_entity(
    schema_validator: SchemaValidator,
    valid_list_order_response_dict: dict[str, Any],
    entity: str,
) -> None:
    response = deepcopy(valid_list_order_response_dict)
    response["entity"] = entity

    with pytest.raises(ValidationError):
        schema_validator.validate(
            response,
            ORDER_LIST_SCHEMA,
        )


@pytest.mark.negative
def test_validate_order_list_schema_additional_property(
    schema_validator: SchemaValidator,
    valid_list_order_response_dict: dict[str, Any],
) -> None:
    response = deepcopy(valid_list_order_response_dict)
    response["unexpected"] = "value"

    with pytest.raises(ValidationError):
        schema_validator.validate(
            response,
            ORDER_LIST_SCHEMA,
        )


@pytest.mark.negative
def test_validate_order_list_schema_missing_required_field(
    schema_validator: SchemaValidator,
    valid_list_order_response_dict: dict[str, Any],
) -> None:
    response = deepcopy(valid_list_order_response_dict)
    response.pop("items")

    with pytest.raises(ValidationError):
        schema_validator.validate(
            response,
            ORDER_LIST_SCHEMA,
        )


@pytest.mark.negative
def test_validate_order_list_schema_invalid_count(
    schema_validator: SchemaValidator,
    valid_list_order_response_dict: dict[str, Any],
) -> None:
    response = deepcopy(valid_list_order_response_dict)
    response["count"] = -1

    with pytest.raises(ValidationError):
        schema_validator.validate(
            response,
            ORDER_LIST_SCHEMA,
        )


@pytest.mark.positive
def test_validate_error_schema_success(
    schema_validator: SchemaValidator,
    error_response_fixture: dict[str, Any],
) -> None:
    schema_validator.validate(
        error_response_fixture,
        ERROR_SCHEMA,
    )


@pytest.mark.parametrize(
    "subfield_name",
    [
        "code",
        "description",
        "step",
        "metadata",
        "source",
        "reason",
    ],
)
@pytest.mark.negative
def test_validate_error_schema_missing_required_field(
    schema_validator: SchemaValidator,
    error_response_fixture: dict[str, Any],
    subfield_name: str,
) -> None:
    response = deepcopy(error_response_fixture)
    response["error"].pop(subfield_name)

    with pytest.raises(ValidationError):
        schema_validator.validate(
            response,
            ERROR_SCHEMA,
        )


@pytest.mark.negative
def test_validate_error_schema_missing_error_field(
    schema_validator: SchemaValidator,
    error_response_fixture: dict[str, Any],
) -> None:
    response = deepcopy(error_response_fixture)
    response.pop("error")

    with pytest.raises(ValidationError):
        schema_validator.validate(
            response,
            ERROR_SCHEMA,
        )


@pytest.mark.negative
def test_validate_error_schema_additional_property(
    schema_validator: SchemaValidator,
    error_response_fixture: dict[str, Any],
) -> None:
    response = deepcopy(error_response_fixture)
    response["unexpected"] = "value"

    with pytest.raises(ValidationError):
        schema_validator.validate(
            response,
            ERROR_SCHEMA,
        )


@pytest.mark.negative
def test_validate_error_schema_additional_nested_property(
    schema_validator: SchemaValidator,
    error_response_fixture: dict[str, Any],
) -> None:
    response = deepcopy(error_response_fixture)
    response["error"]["unexpected"] = "value"

    with pytest.raises(ValidationError):
        schema_validator.validate(
            response,
            ERROR_SCHEMA,
        )


@pytest.mark.negative
def test_validate_error_schema_invalid_field_type(
    schema_validator: SchemaValidator,
    error_response_fixture: dict[str, Any],
) -> None:
    response = deepcopy(error_response_fixture)
    response["error"]["code"] = 123

    with pytest.raises(ValidationError):
        schema_validator.validate(
            response,
            ERROR_SCHEMA,
        )


@pytest.mark.negative
def test_validate_unknown_schema(
    schema_validator: SchemaValidator,
) -> None:
    with pytest.raises(FileNotFoundError):
        schema_validator.validate(
            {},
            Path("unknown.json"),
        )
