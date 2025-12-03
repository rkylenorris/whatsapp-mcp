import re
from datetime import datetime
from pathlib import Path
from models import Message
from typing import Callable

MESSAGE_PATTERN = re.compile(
    r"^(?P<date>[^-]+?) - (?:(?P<author>[^:]+?): )?(?P<text>.*)$"
)
DATE_FORMAT = "%m/%d/%y, %I:%M %p"


def import_chat_log(path: Path, filter_by: Callable | None = None) -> list[Message]:

    if not path.exists():
        raise FileNotFoundError(f"File {path.name} not found.")

    messages = []
    current_msg = None
    chat_name = path.stem.strip()

    with path.open(encoding="utf-8") as log:

        for line in log:

            line = line.rstrip("\n")
            msg_match = MESSAGE_PATTERN.match(line)

            if msg_match:

                if current_msg:
                    messages.append(current_msg)

                date_txt = msg_match.group('date').strip()
                timestamp = datetime.strptime(date_txt, DATE_FORMAT)
                author = msg_match.group('author')
                text = msg_match.group('text')

                current_msg = Message(
                    timestamp=timestamp,
                    author=author,
                    text=text,
                    chat_name=chat_name
                )
            else:

                if current_msg:
                    current_msg.text += f"\n{line}"

        if current_msg:
            messages.append(current_msg)

    if filter_by:
        filtered = list(filter(filter_by, messages))
        return list(sorted(filtered, key=lambda m: m.timestamp))

    return list(sorted(messages, key=lambda m: m.timestamp, reverse=True))
