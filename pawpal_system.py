from __future__ import annotations
import json
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

    @property
    def priority_label(self) -> str:
        """Returns a human-readable priority label with color-coded emoji."""
        return {5: "🔴 Critical", 4: "🟠 High", 3: "🟡 Medium", 2: "🟢 Low", 1: "⚪ Minimal"}.get(
            self.priority, f"P{self.priority}"
        )

    @property
    def category_emoji(self) -> str:
        """Returns an emoji matching the task's category."""
        return {
            "exercise": "🏃",
            "nutrition": "🍖",
            "health": "💊",
            "hygiene": "🛁",
            "enrichment": "🧸",
            "grooming": "✂️",
            "other": "📋",
        }.get(self.category, "📋")

    @property
    def display_name(self) -> str:
        """Returns the category emoji followed by the task name."""
        return f"{self.category_emoji} {self.name}"

    @property
    def status_label(self) -> str:
        """Returns a human-readable completion status label with emoji."""
        return "✅ Done" if self.is_completed else "⏳ Pending"

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

    def to_dict(self) -> dict:
        """Converts the Owner and all nested Pets and Tasks into a JSON-serializable dict."""
        def task_to_dict(t: Task) -> dict:
            return {
                "name": t.name,
                "duration_minutes": t.duration_minutes,
                "priority": t.priority,
                "category": t.category,
                "is_completed": t.is_completed,
                "notes": t.notes,
                "time": t.time,
                "frequency": t.frequency,
                "due_date": t.due_date.strftime("%Y-%m-%d"),
            }

        def pet_to_dict(p: Pet) -> dict:
            return {
                "name": p.name,
                "species": p.species,
                "breed": p.breed,
                "age_years": p.age_years,
                "health_notes": p.health_notes,
                "tasks": [task_to_dict(t) for t in p.get_tasks()],
            }

        return {
            "name": self.name,
            "email": self.email,
            "available_minutes_per_day": self.available_minutes_per_day,
            "preferences": self.preferences,
            "pets": [pet_to_dict(p) for p in self._pets],
        }

    @classmethod
    def from_dict(cls, data: dict) -> Owner:
        """Reconstructs a fully populated Owner from a plain dictionary."""
        owner = cls(
            name=data["name"],
            email=data["email"],
            available_minutes_per_day=data["available_minutes_per_day"],
            preferences=data.get("preferences", []),
        )
        for pet_data in data.get("pets", []):
            pet = Pet(
                name=pet_data["name"],
                species=pet_data["species"],
                breed=pet_data["breed"],
                age_years=pet_data["age_years"],
                health_notes=pet_data.get("health_notes", []),
            )
            for task_data in pet_data.get("tasks", []):
                task = Task(
                    name=task_data["name"],
                    duration_minutes=task_data["duration_minutes"],
                    priority=task_data["priority"],
                    category=task_data["category"],
                    is_completed=task_data.get("is_completed", False),
                    notes=task_data.get("notes", ""),
                    time=task_data.get("time", "00:00"),
                    frequency=task_data.get("frequency", "once"),
                    due_date=date.fromisoformat(task_data["due_date"]),
                )
                pet.add_task(task)
            owner.add_pet(pet)
        return owner

    def save_to_json(self, filepath: str = "data.json") -> None:
        """Writes the owner data to a JSON file. Prints a warning if the write fails."""
        try:
            with open(filepath, "w") as f:
                json.dump(self.to_dict(), f, indent=2)
        except Exception as e:
            print(f"Warning: could not save data to {filepath}: {e}")

    @classmethod
    def load_from_json(cls, filepath: str = "data.json") -> Owner:
        """Loads an Owner from a JSON file. Returns a default Owner if the file is missing or invalid."""
        try:
            with open(filepath, "r") as f:
                data = json.load(f)
            return cls.from_dict(data)
        except Exception:
            return cls(name="Jordan", email="", available_minutes_per_day=60)


class Scheduler:
    def __init__(self, owner: Owner) -> None:
        self.owner = owner
        self.pets: list[Pet] = []
        self.scheduled_tasks: list[Task] = []
        self.weighted_plan: list[Task] = []

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
        self.scheduled_tasks = self.sort_by_priority_then_time()
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

    def sort_by_priority_then_time(self) -> list[Task]:
        """Returns scheduled tasks sorted by priority descending then time ascending without mutating scheduled_tasks."""
        if not self.scheduled_tasks:
            return []
        return sorted(
            self.scheduled_tasks,
            key=lambda t: (-t.priority, tuple(int(p) for p in t.time.split(":"))),
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

    def score_task(self, task: Task) -> float:
        """Compute a composite [0.0, 1.0] score for a task using priority, duration, recurrence, and due-date factors."""
        pool = [t for pet in self.owner.get_pets() for t in pet.get_tasks() if not t.is_completed]
        if not pool:
            return 0.0

        max_priority = max(t.priority for t in pool)
        max_duration = max(t.duration_minutes for t in pool)

        # Priority (40%) — higher raw priority scores higher
        priority_score = task.priority / max_priority if max_priority > 0 else 0.0

        # Duration efficiency (30%) — shorter tasks score higher to maximise task count
        duration_score = 1.0 - (task.duration_minutes / max_duration) if max_duration > 0 else 0.0

        # Recurrence urgency (20%) — missing a recurring task has ongoing consequences
        recurrence_score = {"daily": 1.0, "weekly": 0.5, "once": 0.0}.get(task.frequency, 0.0)

        # Due-date proximity (10%) — overdue/due-today scores 1.0; future tasks decay over 30 days
        days_until = (task.due_date - date.today()).days
        proximity_score = 1.0 if days_until <= 0 else max(0.0, 1.0 - days_until / 30)

        return (
            0.40 * priority_score
            + 0.30 * duration_score
            + 0.20 * recurrence_score
            + 0.10 * proximity_score
        )

    def generate_weighted_plan(self) -> list[Task]:
        """Select tasks within the owner's daily budget ordered by composite score descending; stores result in weighted_plan."""
        self.pets = self.owner.get_pets()
        candidates = sorted(
            (t for pet in self.pets for t in pet.get_tasks() if not t.is_completed),
            key=self.score_task,
            reverse=True,
        )
        plan: list[Task] = []
        time_used = 0
        for task in candidates:
            if time_used + task.duration_minutes <= self.owner.available_minutes_per_day:
                plan.append(task)
                time_used += task.duration_minutes
        self.weighted_plan = plan
        return self.weighted_plan

    def explain_weighted_plan(self) -> str:
        """Return a human-readable breakdown of each weighted-plan task's composite score and dominant scoring factor."""
        if not self.weighted_plan:
            return "No weighted plan generated. Call generate_weighted_plan() first."

        pool = [t for pet in self.owner.get_pets() for t in pet.get_tasks() if not t.is_completed]
        max_priority = max((t.priority for t in pool), default=1)
        max_duration = max((t.duration_minutes for t in pool), default=1)
        recurrence_map = {"daily": 1.0, "weekly": 0.5, "once": 0.0}
        today = date.today()

        total_min = sum(t.duration_minutes for t in self.weighted_plan)
        lines = [
            f"Weighted plan for {self.owner.name} "
            f"({total_min} / {self.owner.available_minutes_per_day} min used):",
            "",
        ]

        for task in self.weighted_plan:
            p = 0.40 * (task.priority / max_priority)
            d = 0.30 * (1.0 - task.duration_minutes / max_duration)
            r = 0.20 * recurrence_map.get(task.frequency, 0.0)
            days_until = (task.due_date - today).days
            q = 0.10 * (1.0 if days_until <= 0 else max(0.0, 1.0 - days_until / 30))
            composite = p + d + r + q

            dominant = max(
                [("priority (40%)", p), ("duration efficiency (30%)", d),
                 ("recurrence urgency (20%)", r), ("due-date proximity (10%)", q)],
                key=lambda x: x[1],
            )[0]

            lines.append(
                f"  {task.name:<24} | score {composite:.3f} | top factor: {dominant}"
            )

        return "\n".join(lines)
