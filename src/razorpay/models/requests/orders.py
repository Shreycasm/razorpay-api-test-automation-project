from typing import Any

from pydantic import BaseModel, ConfigDict

from razorpay.enums.currency import Currency
from razorpay.models.types import Amount, Notes, Receipt


class CreateOrderRequest(BaseModel):

    model_config = ConfigDict(
        extra="forbid"
    )

    amount: Amount
    currency: Currency
    receipt: Receipt | None = None
    notes: Notes | None = None

    def to_api_payload(self) -> dict[str, Any]:

        return self.model_dump(
            mode="json",
            exclude_none=True)


class UpdateOrderRequest(BaseModel):
    
    model_config = ConfigDict(
        extra="forbid"
    )

    notes: Notes

    def to_api_payload(self) -> dict[str, Any]:

        return self.model_dump(
            mode="json",
            exclude_none=True)
