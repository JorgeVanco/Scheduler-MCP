from datetime import datetime
import dateutil


def getDateTimeFromISO8601String(s) -> datetime:
    """Convert an ISO 8601 string to a datetime object."""
    d = dateutil.parser.parse(s)
    return d


def parse_iso_date(s) -> str:
    """Parse an ISO 8601 date string and return it in a easily readable format."""
    return getDateTimeFromISO8601String(s).strftime("%Y-%m-%d %H:%M")
