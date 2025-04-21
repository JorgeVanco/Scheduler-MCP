from pydantic import BaseModel, Field, model_validator
from src.utils import parse_iso_date
from typing import Any


class CalendarModel(BaseModel):
    id: str = Field(..., description="ID of the calendar")
    summary: str = Field(..., description="Name of the calendar")

    def __str__(self) -> str:
        return f"Calendar: {self.summary}"

    def __repr__(self) -> str:
        return self.__str__()


class CalendarEvent(BaseModel):
    id: str = Field(..., description="ID of the event")
    summary: str = Field(..., description="Summary of the event")
    start: str = Field(..., description="Start time of the event")
    end: str = Field(..., description="End time of the event")

    def __str__(self) -> str:
        return f"**{parse_iso_date(self.start)} - {parse_iso_date(self.end)}**: {self.summary}"

    def __repr__(self) -> str:
        return self.__str__()


class TaskListModel(BaseModel):
    id: str = Field(..., description="ID of the task list")
    title: str = Field(..., description="Title of the task list")

    def __str__(self) -> str:
        return f"Task List: {self.title}"

    def __repr__(self) -> str:
        return self.__str__()


class TaskModel(BaseModel):
    id: str = Field(..., description="ID of the task")
    title: str = Field(..., description="Title of the task")
    notes: str = Field("", description="Notes for the task")
    due_date: str = Field("No due date", description="Due date of the task")

    def __str__(self) -> str:
        return (
            f"Task: {self.title}"
            + (f", Notes: {self.notes}" if self.notes != "" else "")
            + (
                f", Due: {parse_iso_date(self.due_date)}"
                if self.due_date != "No due date"
                else ""
            )
        )

    def __repr__(self) -> str:
        return self.__str__()


class CalendarEventList(BaseModel):
    events: list[dict[str, list[CalendarEvent]]] = Field(
        [], description="List of calendar events"
    )

    @model_validator(mode="before")
    @classmethod
    def filter_events(cls, data) -> Any:
        raw_events = data.get("events", [])
        data["events"] = [
            events for events in raw_events if len(list(events.values())[0]) > 0
        ]
        return data

    def __str__(self) -> str:
        calendar_str = [
            "Calendar: {calendar}\n{calendar_values}".format(
                calendar=list(calendar.keys())[0],
                calendar_values="\n".join([str(c) for c in list(calendar.values())[0]]),
            )
            for calendar in self.events
        ]
        return ("\n\n" + "#" * 20 + "\n\n").join(calendar_str)

    def __repr__(self) -> str:
        return self.__str__()


class TasksList(BaseModel):
    tasks: list[dict[str, list[TaskModel]]] = Field([], description="List of tasks")

    @model_validator(mode="before")
    @classmethod
    def filter_tasks(cls, data) -> Any:
        raw_tasks = data.get("tasks", [])
        data["tasks"] = [
            tasks for tasks in raw_tasks if len(list(tasks.values())[0]) > 0
        ]
        return data

    def __str__(self) -> str:
        task_str = [
            "Task List: {task_list}\n{task_values}".format(
                task_list=list(task_list.keys())[0],
                task_values="\n".join(
                    [" - " + str(t) for t in list(task_list.values())[0]]
                ),
            )
            for task_list in self.tasks
        ]
        return ("\n\n" + "#" * 20 + "\n\n").join(task_str)

    def __repr__(self) -> str:
        return self.__str__()
