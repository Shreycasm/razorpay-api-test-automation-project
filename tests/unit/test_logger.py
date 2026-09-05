import json

import allure
import pytest

from razorpay.utils.logger import LOG_FILE, LOG_DIR, logger


pytestmark = pytest.mark.unit


@pytest.fixture(autouse=True)
def allure_logger_labels() -> None:
    allure.dynamic.epic("Razorpay API")
    allure.dynamic.feature("Framework")
    allure.dynamic.story("Logger")


@pytest.mark.positive
def test_log_directory_exists() -> None:
    assert LOG_DIR.exists()
    assert LOG_DIR.is_dir()


@pytest.mark.positive
def test_log_file_exists() -> None:
    assert LOG_FILE.exists()
    assert LOG_FILE.is_file()


@pytest.mark.positive
def test_logger_name() -> None:
    assert logger.name == "razorpay"


@pytest.mark.positive
def test_logger_writes_info_to_file() -> None:
    test_message = "logger info test"

    logger.info(test_message)

    log_content = LOG_FILE.read_text(encoding="utf-8")

    assert test_message in log_content


@pytest.mark.positive
def test_logger_writes_error_to_file() -> None:
    test_message = "logger error test"

    logger.error(test_message)

    log_content = LOG_FILE.read_text(encoding="utf-8")

    assert test_message in log_content


@pytest.mark.positive
def test_logger_writes_json_to_file() -> None:
    test_message = "logger json test"

    logger.info(
        test_message,
        method="POST",
        endpoint="/v1/orders",
        status_code=201,
    )

    log_lines = LOG_FILE.read_text(encoding="utf-8").splitlines()

    log_entry = json.loads(log_lines[-1])

    assert log_entry["event"] == test_message
    assert log_entry["method"] == "POST"
    assert log_entry["endpoint"] == "/v1/orders"
    assert log_entry["status_code"] == 201


@pytest.mark.positive
def test_logger_records_exception() -> None:
    test_message = "exception logging test"

    try:
        1 / 0
    except ZeroDivisionError:
        logger.exception(test_message)

    log_content = LOG_FILE.read_text(encoding="utf-8")

    assert test_message in log_content
    assert "ZeroDivisionError" in log_content
