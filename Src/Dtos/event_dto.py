from dataclasses import dataclass
from typing import Any


@dataclass
class event_dto:
    event_type: str
    payload: Any