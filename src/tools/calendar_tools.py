from datetime import datetime
from typing import List, Dict, Any
import json
import pytz
import os

# Models
from src.models import CalendarModel, CalendarEvent, TaskListModel, TaskModel


# Google API client libraries
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

timezone = pytz.timezone("Europe/Madrid")
# Scopes for API access
SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/tasks",
]

creds = None

# Check for existing token
if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_info(
        json.loads(open("token.json").read()), SCOPES
    )

# If there are no valid credentials, authenticate
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)

    # Save credentials for next run
    with open("token.json", "w") as token:
        token.write(creds.to_json())

print("Authentication successful!")

# Build service clients
calendar_service = build("calendar", "v3", credentials=creds)
tasks_service = build("tasks", "v1", credentials=creds)


async def create_calendar_event(
    summary: str,
    start_time: str,
    end_time: str,
    calendar_id: str = os.getenv("CALENDAR_ID"),
) -> Dict[str, Any]:
    """Create a new calendar event.

    Args:
        summary (str): Summary of the event.
        start_time (str): Start time in ISO format.
        end_time (str): End time in ISO format.
        calendar_id (str): Calendar ID. Defaults to the environment variable CALENDAR_ID.
    """
    print(f"Creating new event '{summary}'...")

    # Create event body
    event_body = {
        "summary": summary,
        "start": {"dateTime": start_time, "timeZone": str(timezone)},
        "end": {"dateTime": end_time, "timeZone": str(timezone)},
    }

    # Insert new event
    created_event = (
        calendar_service.events()
        .insert(calendarId=calendar_id, body=event_body)
        .execute()
    )

    print(f"Event created: {created_event['htmlLink']}")
    return created_event


async def list_calendars() -> List[Dict[str, Any]]:
    """List all calendars."""
    calendars_result = calendar_service.calendarList().list().execute()
    calendars = [
        CalendarModel(id=calendar["id"], summary=calendar["summary"])
        for calendar in calendars_result.get("items", [])
    ]
    return calendars


async def get_calendar_events(id=None, date=None) -> List[CalendarEvent]:
    """Fetch calendar events for the specified date (today by default)."""
    if not date:
        date = datetime.now(timezone)
    if id is None:
        id = "primary"

    # Set time boundaries for the day
    start_time = date.replace(hour=0, minute=0, second=0).isoformat()
    end_time = date.replace(hour=23, minute=59, second=59).isoformat()

    events_result = (
        calendar_service.events()
        .list(
            calendarId=id,
            timeMin=start_time,
            timeMax=end_time,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )

    events = [
        CalendarEvent(
            id=event["id"],
            summary=event.get("summary", "No summary"),
            start=event["start"]["dateTime"],
            end=event["end"]["dateTime"],
        )
        for event in events_result.get("items", [])
    ]

    return events


async def list_tasks() -> List[Dict[str, Any]]:
    """List all task lists."""
    tasklists_result = tasks_service.tasklists().list().execute()
    tasklists = [
        TaskListModel(title=task_list["title"], id=task_list["id"])
        for task_list in tasklists_result.get("items", [])
    ]
    return tasklists


async def get_tasks(task_list_id="@default") -> List[Dict[str, Any]]:
    """Fetch tasks from a specific task list."""

    # Get incomplete tasks
    tasks_result = (
        tasks_service.tasks()
        .list(
            tasklist=task_list_id,
            showCompleted=False,
            showHidden=False,
            showDeleted=False,
        )
        .execute()
    )

    tasks = tasks_result.get("items", [])

    tasks = [
        TaskModel(
            id=task["id"],
            title=task["title"],
            notes=task.get("notes", ""),
            due_date=task.get("due", "No due date"),
        )
        for task in tasks
    ]

    return tasks
