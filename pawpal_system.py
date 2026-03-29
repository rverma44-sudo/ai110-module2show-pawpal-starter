from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class Task:
    name: str
    duration_minutes: int
    priority: int
    category: str
    is_completed: bool = False
    notes: str = ""

    def mark_complete(self) -> None:
        # Mark this task as done
        pass

    def reset(self) -> None:
        # Clear completion status so the task can be rescheduled
        pass

    def is_higher_priority_than(self, other: Task) -> bool:
        # Return True if this task's priority is greater than other's
        pass


@dataclass
class Pet:
    name: str
    species: str
    breed: str
    age_years: int
    health_notes: list[str] = field(default_factory=list)
    _tasks: list[Task] = field(default_factory=list, repr=False)

    def add_task(self, task: Task) -> None:
        # Append task to the pet's task list
        pass

    def remove_task(self, task_name: str) -> bool:
        # Remove the first task matching task_name; return True if found
        pass

    def get_tasks(self) -> list[Task]:
        # Return a copy of the pet's task list
        pass

    def get_total_task_duration(self) -> int:
        # Sum duration_minutes across all tasks
        pass


class Owner:
    def __init__(
        self,
        name: str,
        email: str,
        available_minutes_per_day: int,
        preferences: list[str] | None = None,
    ) -> None:
        self.name = name
        self.email = email
        self.available_minutes_per_day = available_minutes_per_day
        self.preferences: list[str] = preferences or []
        self._pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        # Add a Pet instance to the owner's pet list
        pass

    def remove_pet(self, pet_name: str) -> bool:
        # Remove the first pet matching pet_name; return True if found
        pass

    def get_pets(self) -> list[Pet]:
        # Return a copy of the owner's pet list
        pass

    def set_available_time(self, minutes: int) -> None:
        # Update the daily available time budget
        pass


class Scheduler:
    def __init__(self, owner: Owner, pet: Pet) -> None:
        self.owner = owner
        self.pet = pet
        self.scheduled_tasks: list[Task] = []

    def generate_plan(self) -> list[Task]:
        # Select and order tasks that fit within the owner's available time
        pass

    def filter_by_priority(self, min_priority: int) -> list[Task]:
        # Return tasks with priority >= min_priority
        pass

    def fits_within_time(self, tasks: list[Task]) -> bool:
        # Return True if the total duration of tasks <= owner's available minutes
        pass

    def explain_plan(self) -> str:
        # Return a human-readable explanation of why each task was included or skipped
        pass

    def get_total_scheduled_duration(self) -> int:
        # Sum duration_minutes for all tasks in scheduled_tasks
        pass
