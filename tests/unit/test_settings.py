from __future__ import annotations

from typing import Any

import allure
import pytest
from pydantic import ValidationError

from razorpay.config.settings import Settings

pytestmark = pytest.mark.unit


@pytest.fixture(autouse=True)
def allure_settings_labels() -> None:
    allure.dynamic.epic("Razorpay API")
    allure.dynamic.feature("Framework")
    allure.dynamic.story("Settings")


@pytest.mark.positive
def test_validate_settings_success() -> None:

    config_settings = Settings()

    assert isinstance(config_settings, Settings)
    assert str(config_settings.base_url) == "https://api.razorpay.com/"
    assert config_settings.request_timeout_seconds == 30
    assert config_settings.log_level == "INFO"
    assert config_settings.api_key.startswith("rzp_test_")


@pytest.mark.negative
def test_validate_settings_invalid_base_url(
    monkeypatch: pytest.MonkeyPatch,
) -> None:

    monkeypatch.setenv("BASE_URL", "invalid-url")

    with pytest.raises(ValidationError):
        Settings()


@pytest.mark.parametrize(
    "log_level",
    [
        "INFO",
        "debug",
        "wArning",
        "ErRoR",
        "CRITICAL",
    ],
)
@pytest.mark.positive
def test_validate_settings_valid_log_level(
    log_level: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:

    monkeypatch.setenv("LOG_LEVEL", log_level)

    assert Settings().log_level == log_level.upper()


@pytest.mark.parametrize(
    "log_level",
    [
        "verbose",
        "trace",
    ],
)
@pytest.mark.negative
def test_validate_settings_invalid_log_level(
    log_level: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:

    monkeypatch.setenv("LOG_LEVEL", log_level)

    with pytest.raises(ValidationError):
        Settings()


@pytest.mark.parametrize(
    ("timeout", "expected"),
    [
        ("30", 30),
        ("15", 15),
    ],
)
@pytest.mark.positive
def test_validate_settings_valid_timeout(
    timeout: str,
    expected: int,
    monkeypatch: pytest.MonkeyPatch,
) -> None:

    monkeypatch.setenv("REQUEST_TIMEOUT_SECONDS", timeout)

    assert Settings().request_timeout_seconds == expected


@pytest.mark.parametrize(
    "timeout",
    [
        "abc",
        "-1",
    ],
)
@pytest.mark.negative
def test_validate_settings_invalid_timeout(
    monkeypatch: pytest.MonkeyPatch,
    timeout: Any,
) -> None:

    monkeypatch.setenv("REQUEST_TIMEOUT_SECONDS", timeout)

    with pytest.raises(ValidationError):
        Settings()