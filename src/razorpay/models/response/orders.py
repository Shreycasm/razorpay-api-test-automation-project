from pydantic import BaseModel, ConfigDict


class OrderResponse(BaseModel):

    model_config = ConfigDict(
        extra="ignore"
    )

    id: str
    entity: str
    amount: int
    amount_paid: int | None
    amount_due: int | None
    currency: str
    receipt: str | None
    status: str
    offer_id: str | None
    created_at: int
    attempts: int
    notes: dict[str, str] | list[None]


class OrderListResponse(BaseModel):
    model_config = ConfigDict(
        extra="ignore"
    )
    
    entity: str
    count: int
    items: list[OrderResponse]
