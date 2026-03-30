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
        """Marks this task as completed."""
        self.is_completed = True

    def reset(self) -> None:
        """Clears the completed status so the task can be rescheduled."""
        self.is_completed = False

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
        return list(self._pets)

    def set_available_time(self, minutes: int) -> None:
        self.available_minutes_per_day = minutes

    def get_all_tasks(self) -> list[Task]:
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
        self.pets = self.owner.get_pets()
        return [
            task
            for pet in self.pets
            for task in pet.get_tasks()
            if task.priority >= min_priority
        ]

    def fits_within_time(self, tasks: list[Task]) -> bool:
        return (
            sum(t.duration_minutes for t in tasks)
            <= self.owner.available_minutes_per_day
        )

    def explain_plan(self) -> str:
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
        return sum(t.duration_minutes for t in self.scheduled_tasks)
