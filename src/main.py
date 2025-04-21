import httpx
from mcp.server.fastmcp import FastMCP

from src.tools import (
    create_calendar_event,
    list_calendars,
    get_calendar_events,
    list_tasks,
    get_tasks,
    get_current_time,
    get_date_in_iso_format,
    sum_to_date,
)


# Initialize FastMCP server
mcp: FastMCP = FastMCP("scheduler")
all_tools: list = [
    create_calendar_event,
    list_calendars,
    get_calendar_events,
    list_tasks,
    get_tasks,
    get_current_time,
    get_date_in_iso_format,
    sum_to_date,
]

for tool in all_tools:
    mcp.add_tool(tool)


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport="stdio")
