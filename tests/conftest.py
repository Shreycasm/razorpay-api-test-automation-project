from typing import Any

import pytest
import structlog

from tests.test_data.order_request import valid_order, valid_update_order
from tests.test_data.order_response import valid_order_response, valid_list_order_response


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
