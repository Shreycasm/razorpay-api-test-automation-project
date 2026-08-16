from typing import Any

from pydantic import BaseModel, ConfigDict


class ErrorDetails(BaseModel):
    model_config = ConfigDict(extra="ignore")

    code: str
    description: str
    source: str
    step: str
    reason: str
    metadata: dict[str, Any]


class ErrorResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")

    error: ErrorDetails