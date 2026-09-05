from __future__ import annotations

from copy import deepcopy
from typing import Any

import pytest
from pydantic import ValidationError

from razorpay.models.response.errors import ErrorResponse
from tests.test_data.error_response import valid_error_response


pytestmark = pytest.mark.unit


@pytest.fixture(scope="module")
def error_response_fixture() -> dict[str, Any]:
    return valid_error_response()


@pytest.mark.positive
def test_validate_error_response_success(
    error_response_fixture: dict[str, Any],
) -> None:
    response = ErrorResponse.model_validate(
        error_response_fixture
    )

    assert isinstance(response, ErrorResponse)
    assert response.error.code == error_response_fixture["error"]["code"]
    assert response.error.description == error_response_fixture["error"]["description"]
    assert response.error.source == error_response_fixture["error"]["source"]
    assert response.error.step == error_response_fixture["error"]["step"]
    assert response.error.reason == error_response_fixture["error"]["reason"]
    assert response.error.metadata == error_response_fixture["error"]["metadata"]


@pytest.mark.parametrize(
    "field",
    [
        "code",
        "description",
        "source",
        "step",
        "reason",
        "metadata",
    ],
)
@pytest.mark.negative
def test_validate_error_response_missing_field(
    error_response_fixture: dict[str, Any],
    field: str,
) -> None:
    payload = deepcopy(error_response_fixture)
    payload["error"].pop(field)

    with pytest.raises(ValidationError) as exc_info:
        ErrorResponse.model_validate(payload)

    error = exc_info.value.errors()[0]

    assert error["loc"] == ("error", field)
    assert error["type"] == "missing"


@pytest.mark.negative
def test_validate_error_response_missing_error() -> None:
    payload: dict[str, Any] = {}

    with pytest.raises(ValidationError) as exc_info:
        ErrorResponse.model_validate(payload)

    error = exc_info.value.errors()[0]

    assert error["loc"] == ("error",)
    assert error["type"] == "missing"


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("code", 123),
        ("description", 123),
        ("source", 123),
        ("step", 123),
        ("reason", 123),
        ("metadata", "invalid"),
    ],
)
@pytest.mark.negative
def test_validate_error_response_invalid_field_type(
    error_response_fixture: dict[str, Any],
    field: str,
    value: Any,
) -> None:
    payload = deepcopy(error_response_fixture)
    payload["error"][field] = value

    with pytest.raises(ValidationError) as exc_info:
        ErrorResponse.model_validate(payload)

    error = exc_info.value.errors()[0]

    assert error["loc"] == ("error", field)


@pytest.mark.positive
def test_validate_error_response_ignores_extra_fields(
    error_response_fixture: dict[str, Any],
) -> None:
    payload = deepcopy(error_response_fixture)

    payload["unexpected_root"] = "ignored"
    payload["error"]["unexpected"] = "ignored"

    response = ErrorResponse.model_validate(payload)

    assert not hasattr(response, "unexpected_root")
    assert not hasattr(response.error, "unexpected")


@pytest.mark.positive
def test_validate_error_response_with_metadata(
    error_response_fixture: dict[str, Any],
) -> None:
    payload = deepcopy(error_response_fixture)

    payload["error"]["metadata"] = {
        "field": "count",
        "value": 10,
        "expected_type": "integer",
    }

    response = ErrorResponse.model_validate(payload)

    assert response.error.metadata == payload["error"]["metadata"]


@pytest.mark.parametrize(
    "payload",
    [
        None,
        [],
        "invalid",
        123,
    ],
)
@pytest.mark.negative
def test_validate_error_response_invalid_root_input(
    payload: Any,
) -> None:
    with pytest.raises(ValidationError):
        ErrorResponse.model_validate(payload)
