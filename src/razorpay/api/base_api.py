import time
from typing import Any

import requests
from urllib3.util.retry import Retry
from pydantic import ValidationError

from razorpay.config.settings import settings
from razorpay.utils.logger import logger
from razorpay.exception.api import ApiError
from razorpay.models.response.errors import ErrorResponse


DEFAULT_RETRIES = 3
ALLOWED_METHODS = [
    "GET",
    "PUT",
    "DELETE"
]
STATUS_FORCELIST = [429,500,502,503,504]
BACKOFF_FACTOR = 1

class BaseAPIClient:

    def __init__(self) -> None:
        self._base_url = str(settings.base_url).rstrip("/")
        self._request_timeout_seconds = settings.request_timeout_seconds

        self._session = requests.Session()
        self._session.headers.update(
            {
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )

        self._session.auth = requests.auth.HTTPBasicAuth(
            username=settings.api_key,
            password=settings.api_key_secret.get_secret_value()
        )

        self._logger = logger

        retry_strategy = Retry(
            total = DEFAULT_RETRIES,
            allowed_methods = ALLOWED_METHODS,
            status_forcelist = STATUS_FORCELIST,
            backoff_factor=BACKOFF_FACTOR,
            respect_retry_after_header=True,
            raise_on_status=False   
        )

        adapter = requests.adapters.HTTPAdapter(
            max_retries=retry_strategy
        )

        self._session.mount("http://", adapter)
        self._session.mount("https://", adapter)


    @staticmethod
    def _elapsed_time(start_time: float) -> float:
        return round(
            (time.perf_counter() - start_time) * 1000,
            2                
        )


    def raise_for_api_error(
        self,
        response: requests.Response,
    ) -> None:

        if response.ok:
            return

        try:
            response_data = response.json()
        except ValueError:
            response_data = {}

        try:
            error_response = ErrorResponse.model_validate(
                response_data
            )

            raise ApiError(
                status_code=response.status_code,
                message=error_response.error.description,
                error_code=error_response.error.code,
                response_data=error_response.model_dump(),
            )

        except ValidationError as exc:
            raise ApiError(
                status_code=response.status_code,
                message=response.reason or "API request failed",
                error_code=None,
                response_data=response_data,
            ) from exc

    def request(
        self,
        method: str,
        endpoint: str,
        **kwargs: dict[str, Any]
    ) -> requests.Response:

        endpoint = "/" + endpoint.lstrip("/")
        url = f"{self._base_url}{endpoint}"

        kwargs.setdefault(
            "timeout",
            self._request_timeout_seconds
        )

        requests_logger = self._logger.bind(
            method=method,
            endpoint=endpoint,
            url=url
        )

        if kwargs.get("params"):
            requests_logger = requests_logger.bind(
                query_parameters=kwargs["params"]
            )


        requests_logger.info(
            "HTTP request started."
        )

        start_time = time.perf_counter()

        try:
            response = self._session.request(
                method=method,
                url=url,
                **kwargs
            )

            requests_logger.info(
                "HTTP request completed.",
                status_code=response.status_code,
                duration_ms=self._elapsed_time(start_time)
            )

            return response

        except requests.Timeout as exc:
            requests_logger.exception(
                "HTTP request timeout",
                timeout=self._request_timeout_seconds,
                error=str(exc),
                duration_ms=self._elapsed_time(
                    start_time
                    )
            )
            raise


        except requests.ConnectionError as exc:
            requests_logger.exception(
                "HTTP request connection error",
                error=str(exc),
                duration_ms=self._elapsed_time(
                    start_time
                    )
            )
            raise


        except requests.RequestException as exc:
            requests_logger.exception(
                "HTTP request failed",
                error=str(exc),
                duration_ms=self._elapsed_time(
                    start_time
                    )
            )
            raise


    def get(
        self,
        endpoint: str,
        **kwargs: dict[str, Any]
    ) -> requests.Response:

        return self.request(
            method="GET",
            endpoint=endpoint,
            **kwargs
            )


    def post(
        self,
        endpoint: str,
        **kwargs: dict[str, Any]
    ) -> requests.Response:

        return self.request(
            method="POST",
            endpoint=endpoint,
            **kwargs
        )

        
    def put(
        self,
        endpoint: str,
        **kwargs: dict[str, Any]
    ) -> requests.Response:

        return self.request(
            method="PUT",
            endpoint=endpoint,
            **kwargs
        )


    def patch(
        self,
        endpoint: str,
        **kwargs: dict[str, Any]
    ) -> requests.Response:

        return self.request(
            method="PATCH",
            endpoint=endpoint,
            **kwargs
            )


    def delete(
        self,
        endpoint: str,
        **kwargs: dict[str, Any]
    ) -> requests.Response:

        return self.request(
            method="DELETE",
            endpoint=endpoint,
            **kwargs
        )


    def close(self) -> None:

        self._session.close()