from __future__ import annotations
from dataclasses import dataclass, field, replace
from datetime import date, timedelta


@dataclass
class Task:
    name: str
    duration_minutes: int
    priority: int
    category: str
    is_completed: bool = False
    notes: str = ""
    time: str = "00:00"
    frequency: str = "once"
    due_date: date = field(default_factory=date.today)

    def mark_complete(self) -> None:
        """Marks this task as completed and advances due_date for recurring tasks."""
        self.is_completed = True
        if self.frequency == "daily":
            self.due_date = date.today() + timedelta(days=1)
        elif self.frequency == "weekly":
            self.due_date = date.today() + timedelta(weeks=1)

    def reset(self) -> None:
        """Clears the completed status so the task can be rescheduled."""
        self.is_completed = False

    def next_occurrence(self) -> str | None:
        """Returns the next due date as YYYY-MM-DD for recurring tasks, or None for one-time tasks."""
        if self.frequency == "once":
            return None
        return self.due_date.strftime("%Y-%m-%d")

    def is_higher_priority_than(self, other: Task) -> bool:
        """Returns True if this task has a higher priority than the given task."""
        return self.priority > other.priority


@dataclass
class Pet:
    name: str
    species: str
    breed: str
    age_years: int
    health_notes: list[str] = field(default_factory=list)
    _tasks: list[Task] = field(default_factory=list, repr=False)

    def add_task(self, task: Task) -> None:
        """Adds a task to this pet's task list."""
        self._tasks.append(task)

    def remove_task(self, task_name: str) -> bool:
        """Removes a task by name and returns whether the removal succeeded."""
        for i, task in enumerate(self._tasks):
            if task.name == task_name:
                self._tasks.pop(i)
                return True
        return False

    def get_tasks(self) -> list[Task]:
        """Returns a copy of all tasks assigned to this pet."""
        return list(self._tasks)

    def get_total_task_duration(self) -> int:
        """Returns the total minutes across all tasks assigned to this pet."""
        return sum(task.duration_minutes for task in self._tasks)


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
        """Adds a pet to this owner's list of pets."""
        self._pets.append(pet)

    def remove_pet(self, pet_name: str) -> bool:
        """Removes a pet by name and returns whether the removal succeeded."""
        for i, pet in enumerate(self._pets):
            if pet.name == pet_name:
                self._pets.pop(i)
                return True
        return False

    def get_pets(self) -> list[Pet]:
        """Returns a copy of all pets belonging to this owner."""
        return list(self._pets)

    def set_available_time(self, minutes: int) -> None:
        """Updates the owner's daily time budget in minutes."""
        self.available_minutes_per_day = minutes

    def get_all_tasks(self) -> list[Task]:
        """Returns every task across all of this owner's pets in a single list."""
        tasks: list[Task] = []
        for pet in self._pets:
            tasks.extend(pet.get_tasks())
        return tasks


class Scheduler:
    def __init__(self, owner: Owner) -> None:
        self.owner = owner
        self.pets: list[Pet] = []
        self.scheduled_tasks: list[Task] = []

    def generate_plan(self) -> list[Task]:
        """Selects tasks that fit within the owner's daily time budget, ordered by priority."""
        self.pets = self.owner.get_pets()
        candidates = sorted(
            (t for pet in self.pets for t in pet.get_tasks() if not t.is_completed),
            key=lambda t: t.priority,
            reverse=True,
        )
        plan: list[Task] = []
        time_used = 0
        for task in candidates:
            if time_used + task.duration_minutes <= self.owner.available_minutes_per_day:
                plan.append(task)
                time_used += task.duration_minutes
        self.scheduled_tasks = plan
        return self.scheduled_tasks

    def filter_by_priority(self, min_priority: int) -> list[Task]:
        """Returns all tasks across the owner's pets at or above the given priority level."""
        self.pets = self.owner.get_pets()
        return [
            task
            for pet in self.pets
            for task in pet.get_tasks()
            if task.priority >= min_priority
        ]

    def fits_within_time(self, tasks: list[Task]) -> bool:
        """Returns True if the combined duration of the given tasks fits within the owner's daily budget."""
        return (
            sum(t.duration_minutes for t in tasks)
            <= self.owner.available_minutes_per_day
        )

    def explain_plan(self) -> str:
        """Returns a human-readable summary of which tasks were scheduled and why others were skipped."""
        self.pets = self.owner.get_pets()
        all_tasks = [t for pet in self.pets for t in pet.get_tasks()]
        scheduled_names = {t.name for t in self.scheduled_tasks}

        skipped_no_time = sorted(
            [t for t in all_tasks if not t.is_completed and t.name not in scheduled_names],
            key=lambda t: t.priority,
            reverse=True,
        )
        skipped_done = [t for t in all_tasks if t.is_completed and t.name not in scheduled_names]

        lines = [
            f"Daily plan for {self.owner.name} "
            f"({self.owner.available_minutes_per_day} min available, "
            f"{self.get_total_scheduled_duration()} min scheduled):",
        ]

        if self.scheduled_tasks:
            lines.append("\nIncluded tasks (highest priority first):")
            for t in self.scheduled_tasks:
                lines.append(f"  + {t.name} [{t.category}] | {t.duration_minutes} min | priority {t.priority}")
        else:
            lines.append("\nNo tasks could be scheduled within the available time.")

        if skipped_no_time:
            lines.append("\nSkipped — insufficient time remaining:")
            for t in skipped_no_time:
                lines.append(f"  - {t.name} [{t.category}] | {t.duration_minutes} min | priority {t.priority}")

        if skipped_done:
            lines.append("\nSkipped — already completed:")
            for t in skipped_done:
                lines.append(f"  - {t.name} [{t.category}]")

        return "\n".join(lines)

    def get_total_scheduled_duration(self) -> int:
        """Returns the total minutes consumed by all currently scheduled tasks."""
        return sum(t.duration_minutes for t in self.scheduled_tasks)

    def sort_by_time(self) -> list[Task]:
        """Returns scheduled tasks sorted chronologically by their time attribute without modifying the original list."""
        if not self.scheduled_tasks:
            return []
        return sorted(
            self.scheduled_tasks,
            key=lambda t: tuple(int(part) for part in t.time.split(":")),
        )

    def filter_by_status(self, is_completed: bool) -> list[Task]:
        """Returns scheduled tasks that match the given completion state."""
        return [t for t in self.scheduled_tasks if t.is_completed == is_completed]

    def filter_by_pet(self, pet_name: str) -> list[Task]:
        """Returns scheduled tasks belonging to the pet with the given name, case-insensitively."""
        scheduled_ids = {id(t) for t in self.scheduled_tasks}
        for pet in self.pets:
            if pet.name.lower() == pet_name.lower():
                return [t for t in pet.get_tasks() if id(t) in scheduled_ids]
        return []

    def mark_task_complete(self, task_name: str) -> str | None:
        """Marks a scheduled task complete by name and queues the next occurrence if it is recurring."""
        target = next((t for t in self.scheduled_tasks if t.name == task_name), None)
        if target is None:
            return f"Warning: no scheduled task named '{task_name}' was found."
        target.mark_complete()
        if target.frequency != "once":
            new_occurrence = replace(target, is_completed=False)
            for pet in self.pets:
                if any(id(t) == id(target) for t in pet.get_tasks()):
                    pet.add_task(new_occurrence)
                    break
        return None

    def detect_conflicts(self) -> str | None:
        """Returns a warning string listing tasks that share the same scheduled time, or None if no conflicts exist."""
        time_groups: dict[str, list[str]] = {}
        for task in self.scheduled_tasks:
            time_groups.setdefault(task.time, []).append(task.name)
        conflicts = {t: names for t, names in time_groups.items() if len(names) > 1}
        if not conflicts:
            return None
        lines = ["Scheduling conflicts detected:"]
        for t in sorted(conflicts):
            lines.append(f"  {t} — {', '.join(conflicts[t])}")
        return "\n".join(lines)
