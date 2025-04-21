from datetime import datetime, timedelta
import pytz


async def get_current_time() -> str:
    """Get the current time in ISO format."""

    # Get the current time in local timezone
    local_now = datetime.now(pytz.timezone("Europe/Madrid"))

    return local_now.isoformat()


async def get_date_in_iso_format(date_str: str) -> str:
    """Get the time from a date string in ISO format
    From (YYYY-MM-DD HH:MM) to (YYYY-MM-DDTHH:MM:SS).

    Example:
    Input: "2023-10-01 12:30"
    Output: "2023-10-01T12:30:00"
    """
    # Parse the date string
    date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M")

    # Convert to ISO format
    iso_time = date_obj.isoformat()

    return iso_time


from pydantic import BaseModel, Field


class SumToDateInput(BaseModel):
    date_str: str = Field(
        description="The date to which weeks, days, hours, and minutes will be added. Should be a string"
    )
    weeks: int = Field(description="Number of weeks to add")
    days: int = Field(description="Number of days to add")
    hours: int = Field(description="Number of hours to add")
    minutes: int = Field(description="Number of minutes to add")


async def sum_to_date(
    date_str: str, weeks: int, days: int, hours: int, minutes: int
) -> str:
    """Add weeks, days, hours, and minutes to a date string in ISO format.

    Returns: The resulting date in ISO format.
    """
    date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
    return (
        date_obj + timedelta(weeks=weeks, days=days, hours=hours, minutes=minutes)
    ).isoformat()
