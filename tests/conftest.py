from pathlib import Path
from typing import Any

import pytest
import structlog

from razorpay.validators.schema_validator import SchemaValidator
from tests.test_data.order_request import valid_order, valid_update_order
from tests.test_data.order_response import valid_order_response, valid_list_order_response
from tests.test_data.error_response import  valid_error_response


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = PROJECT_ROOT / "schemas"


@pytest.fixture(autouse=True)
def test_logging_context(request: pytest.FixtureRequest):
    structlog.contextvars.clear_contextvars()

    structlog.contextvars.bind_contextvars(
        test_name=request.node.name,
        test_id=request.node.nodeid,
    )

    yield

    structlog.contextvars.clear_contextvars()


@pytest.fixture(scope="session")
def schema_validator() -> SchemaValidator:
    return SchemaValidator(SCHEMA_DIR)


@pytest.fixture(scope="session")
def create_valid_order_dict() -> dict[str, Any]:

    return valid_order()


@pytest.fixture(scope="session")
def update_valid_order_dict() -> dict[str, Any]:

    return valid_update_order()


@pytest.fixture(scope="session")
def valid_order_response_dict() -> dict[str, Any]:

    return valid_order_response()


@pytest.fixture(scope="session")
def valid_list_order_response_dict() -> dict[str, Any]:

    return valid_list_order_response()


@pytest.fixture(scope="session")
def error_response_fixture() -> dict[str, Any]:
    return valid_error_response()
