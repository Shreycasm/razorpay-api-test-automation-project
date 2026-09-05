from dataclasses import dataclass
from typing import TypeVar

from requests import Response

T = TypeVar("T")


@dataclass(slots=True)
class ApiResponse[T]:
    http: Response
    data: T
