from dataclasses import dataclass
from datetime import datetime


@dataclass
class Message:
    timestamp: datetime
    author: str | None
    text: str
    chat_name: str

    def __post_init__(self):
        if self.author is None:
            self.author = "System"
