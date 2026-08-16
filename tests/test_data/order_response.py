from typing import Any


def valid_order_response() -> dict[str, Any]:

    return {
        "id": "order_TI1JG5cveAZ3d1",
        "entity": "order",
        "amount": 100,
        "amount_paid": 0,
        "amount_due": 100,
        "currency": "INR",
        "receipt": "receipt_e35b487a862b470dbcd369d0b49841ab",
        "offer_id": None,
        "status": "created",
        "attempts": 0,
        "notes": {
            "source": "automation",
            "framework": "pytest"
        },
        "created_at": 1785044647
    }



def valid_list_order_response() -> dict[str, Any]:

    return {
        "entity" : "collection",
        "count" : 1,
        "items" : [valid_order_response()]
    }
