from __future__ import annotations

from typing import Any
from uuid import uuid4

from razorpay.enums.currency import Currency


DEFAULT_AMOUNT=100
DEFAULT_CURRENCY=Currency.INR

def generate_receipt() -> str:
    return f"receipt_{uuid4().hex}"


def generate_notes() -> str:
    return {
        "source": f"automation_{uuid4().hex}",
        "framework": f"pytest_{uuid4().hex}"
    }


def valid_order(
    *,
    amount=DEFAULT_AMOUNT,
    currency=DEFAULT_CURRENCY,
    receipt:str | None = None,
    notes:dict[str, Any] | None = None
) -> dict[str, Any]:

    return {
        "amount": amount,
        "currency": currency.value,
        "receipt": receipt or generate_receipt(),
        "notes": notes if notes is not None else generate_notes()
    }


def valid_update_order(
    notes: dict[str, Any] | None = None
) -> dict[str, Any]:

    return {
        "notes": notes if notes is not None else generate_notes()
    }
