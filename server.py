from mcp.server.fastmcp import FastMCP
from chat_parser import import_chat_log
from pathlib import Path
from datetime import datetime

mcp = FastMCP("whatsapp-helper", json_response=True)


@mcp.tool()
def ping(name: str = "world") -> str:
    """Simple sanity check tool."""
    return f"Hello, {name}! MCP is alive."


@mcp.tool()
def get_recent(
    chat_name: str = "Family",
    limit: int = 50
) -> dict:
    chat_path = Path(f"chats/{chat_name}.txt")
    msgs = import_chat_log(chat_path)[:limit]

    return {
        "chat_name": chat_name,
        "count": len(msgs),
        "messages": [
            {
                "timestamp": m.timestamp.isoformat(),
                "author": m.author,
                "text": m.text
            } for m in msgs
        ]
    }


@mcp.tool()
def get_from_date(
    date_string: str,  # format: %m/%d/%y
    date_format: str = '%m/%d/%y',
    chat_name: str = "Family"
) -> dict:
    chat_path = Path(f"chats/{chat_name}.txt")
    start_date = datetime.strptime(date_string, date_format)
    msgs = import_chat_log(
        chat_path, lambda m: m.timestamp >= start_date)

    return {
        "chat_name": chat_name,
        "count": len(msgs),
        "start_date": start_date.isoformat(),
        "messages": [
            {
                "timestamp": m.timestamp.isoformat(),
                "author": m.author,
                "text": m.text
            } for m in msgs
        ]
    }


if __name__ == "__main__":
    # For quick dev/testing use HTTP; later you can do stdio if needed.
    mcp.run()
