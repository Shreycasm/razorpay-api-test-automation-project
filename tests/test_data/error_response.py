from __future__ import annotations

from typing import Any


def valid_error_response() ->dict[str, Any]:
    return {
        "error": {
            "code": "BAD_REQUEST_ERROR",
            "description": "The count must be an integer.",
            "source": "internal",
            "step": "payment_initiation",
            "reason": "input_validation_failed",
            "metadata": {},
        }
    }
