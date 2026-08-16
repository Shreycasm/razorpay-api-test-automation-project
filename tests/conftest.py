import pytest
import structlog


@pytest.fixture(autouse=True)
def test_logging_context(request: pytest.FixtureRequest):
    structlog.contextvars.clear_contextvars()

    structlog.contextvars.bind_contextvars(
        test_name=request.node.name,
        test_id=request.node.nodeid,
    )

    yield

    structlog.contextvars.clear_contextvars()