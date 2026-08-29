from dataclasses import dataclass
from typing import Generic, TypeVar

from requests import Response

T = TypeVar("T")


@dataclass(slots=True)
class ApiResponse(Generic[T]):
    http: Response
    data: T
