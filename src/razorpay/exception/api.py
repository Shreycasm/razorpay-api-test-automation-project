from typing import Any


class ApiError(Exception):

    def __init__(
        self,
        status_code: int,
        message: str,
        *,
        error_code: str | None = None,
        response_data: dict[str, Any] | None = None,
    ) -> None:
        self.status_code = status_code
        self.message = message
        self.error_code = error_code
        self.response_data = response_data

        super().__init__(message)