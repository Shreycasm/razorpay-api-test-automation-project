from typing import Any

import requests

from razorpay.api.base_api import BaseAPIClient
from razorpay.models.requests.orders import (
    CreateOrderRequest,
    UpdateOrderRequest,
)
from razorpay.models.response.api_response import ApiResponse
from razorpay.models.response.orders import (
    OrderListResponse,
    OrderResponse,
)


class OrdersApi(BaseAPIClient):

    _ENDPOINT = "/v1/orders"

    def create_order(
        self,
        payload: dict[str, Any],
    ) -> ApiResponse[OrderResponse]:

        payload = CreateOrderRequest.model_validate(payload)

        response = self.post(
            endpoint=self._ENDPOINT,
            json=payload.to_api_payload(),
            raise_for_error=True,
        )

        return ApiResponse(
            http=response,
            data=OrderResponse.model_validate(response.json()),
        )

    def create_order_raw(
        self,
        payload: dict[str, Any],
    ) -> requests.Response:

        return self.post(
            endpoint=self._ENDPOINT,
            json=payload,
            raise_for_error=False,
        )

    def get_order(
        self,
        order_id: str,
    ) -> ApiResponse[OrderResponse]:

        response = self.get(
            endpoint=f"{self._ENDPOINT}/{order_id}",
            raise_for_error=True,
        )

        return ApiResponse(
            http=response,
            data=OrderResponse.model_validate(response.json()), 
        )

    def get_order_raw(
        self, 
        order_id: str,
    ) -> requests.Response:

        return self.get(
            endpoint=f"{self._ENDPOINT}/{order_id}",
            raise_for_error=False,
        )

    def list_orders(
        self,
        *,
        count: int | None = None,
        skip: int | None = None,
        authorized: int | None = None,
        from_date: int | None = None,
        to_date: int | None = None,
        receipt: str | None = None,
    ) -> ApiResponse[OrderListResponse]:

        query_params: dict[str, Any] = {}

        if from_date is not None:
            query_params["from"] = from_date

        if to_date is not None:
            query_params["to"] = to_date

        if receipt is not None:
            query_params["receipt"] = receipt

        if authorized is not None:
            query_params["authorized"] = authorized

        if count is not None:
            query_params["count"] = count

        if skip is not None:
            query_params["skip"] = skip

        response = self.get(
            endpoint=self._ENDPOINT,
            params=query_params,
            raise_for_error=True,
        )

        return ApiResponse(
            http=response,
            data=OrderListResponse.model_validate(response.json()),
        )

    def list_orders_raw(
        self,
        **query_params: Any,
    ) -> requests.Response:

        return self.get(
            endpoint=self._ENDPOINT,
            params=query_params,
            raise_for_error=False,
        )

    def update_order(
        self,
        order_id: str,
        payload: dict[str, Any],
    ) -> ApiResponse[OrderResponse]:

        payload = UpdateOrderRequest.model_validate(payload)
        response = self.patch(
            endpoint=f"{self._ENDPOINT}/{order_id}",
            json=payload.to_api_payload(),
            raise_for_error=True,
        )

        return ApiResponse(
            http=response,
            data=OrderResponse.model_validate(response.json()),
        )

    def update_order_raw(
        self,
        order_id: str,
        payload: dict[str, Any],
    ) -> requests.Response:

        return self.patch(
            endpoint=f"{self._ENDPOINT}/{order_id}",
            json=payload,
            raise_for_error=False,
        )
