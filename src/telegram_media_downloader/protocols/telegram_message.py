from datetime import datetime
from typing import Any, Protocol


class TelegramMessage(Protocol):
    id: int
    date: datetime
    media: Any
    text: str | None 