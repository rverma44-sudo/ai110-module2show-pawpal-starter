from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler

DIVIDER = "=" * 60
SECTION  = "-" * 60


def _scheduler_for_pet(owner: Owner, pet: Pet) -> Scheduler:
    """Return a Scheduler scoped to a single pet, sharing the owner's time budget."""
    scoped_owner = Owner(
        name=owner.name,
        email=owner.email,
        available_minutes_per_day=owner.available_minutes_per_day,
        preferences=list(owner.preferences),
    )
    scoped_owner.add_pet(pet)
    return Scheduler(scoped_owner)


def print_pet_schedule(owner: Owner, pet: Pet) -> None:
    scheduler = _scheduler_for_pet(owner, pet)
    scheduler.generate_plan()

    all_tasks   = pet.get_tasks()
    scheduled   = scheduler.scheduled_tasks
    scheduled_names = {t.name for t in scheduled}
    excluded    = [t for t in all_tasks if not t.is_completed and t.name not in scheduled_names]
    total_min   = scheduler.get_total_scheduled_duration()
    budget      = owner.available_minutes_per_day

    print(SECTION)
    print(f"  {pet.name}  |  {pet.species}  |  {pet.breed}  |  {pet.age_years} yr old")
    if pet.health_notes:
        print(f"  Health notes: {', '.join(pet.health_notes)}")
    print(SECTION)

    if scheduled:
        print("  Scheduled Tasks:")
        for i, task in enumerate(scheduled, start=1):
            print(
                f"    {i}. {task.name:<22}"
                f" | {task.duration_minutes:>3} min"
                f" | priority {task.priority}"
                f" | {task.category}"
            )
    else:
        print("  No tasks could fit within today's time budget.")

    print()
    print(f"  Time used : {total_min} / {budget} min")
    print(f"  Remaining : {budget - total_min} min")

    if excluded:
        print()
        print(f"  !! WARNING: {len(excluded)} task(s) excluded due to time limit:")
        for task in sorted(excluded, key=lambda t: t.priority, reverse=True):
            print(f"       - {task.name} ({task.duration_minutes} min, priority {task.priority})")

    print()
    print("  Scheduler Explanation:")
    print("  " + "-" * 56)
    for line in scheduler.explain_plan().splitlines():
        print(f"  {line}")
    print()


def main() -> None:
    # --- Owner -----------------------------------------------------------
    owner = Owner(
        name="Alex Rivera",
        email="alex@example.com",
        available_minutes_per_day=120,
        preferences=["morning routines first", "avoid late grooming"],
    )

    # --- Pet 1: Max the dog ----------------------------------------------
    max_dog = Pet(
        name="Max",
        species="Dog",
        breed="Labrador Retriever",
        age_years=3,
        health_notes=["on joint supplement"],
    )
    max_dog.add_task(Task("Morning Walk",    duration_minutes=30, priority=5, category="exercise",    time="07:00"))
    max_dog.add_task(Task("Feeding",         duration_minutes=10, priority=5, category="nutrition",   time="17:30"))
    max_dog.add_task(Task("Enrichment Play", duration_minutes=20, priority=4, category="enrichment",  time="12:00"))
    max_dog.add_task(Task("Full Grooming",   duration_minutes=45, priority=3, category="grooming",    time="09:30"))

    # --- Pet 2: Luna the cat ---------------------------------------------
    luna_cat = Pet(
        name="Luna",
        species="Cat",
        breed="Domestic Shorthair",
        age_years=5,
        health_notes=["daily thyroid medication"],
    )
    luna_cat.add_task(Task("Feeding",       duration_minutes=10, priority=5, category="nutrition",   time="08:00"))
    luna_cat.add_task(Task("Medication",    duration_minutes=5,  priority=5, category="health",      time="08:05"))
    luna_cat.add_task(Task("Litter Box",    duration_minutes=5,  priority=4, category="hygiene",     time="10:00"))
    luna_cat.add_task(Task("Playtime",      duration_minutes=15, priority=3, category="enrichment",  time="15:00"))
    luna_cat.add_task(Task("Claw Trim",     duration_minutes=60, priority=2, category="grooming",    time="16:00"))

    owner.add_pet(max_dog)
    owner.add_pet(luna_cat)

    # --- Header ----------------------------------------------------------
    print()
    print(DIVIDER)
    print("  PawPal+  |  Today's Schedule")
    print(DIVIDER)
    print(f"  Owner  : {owner.name}  ({owner.email})")
    print(f"  Budget : {owner.available_minutes_per_day} minutes / day")
    print(DIVIDER)
    print()

    # --- Per-pet schedules -----------------------------------------------
    for pet in owner.get_pets():
        print_pet_schedule(owner, pet)

    print(DIVIDER)
    print("  End of schedule.")
    print(DIVIDER)
    print()

    # --- Sorting & filtering demo -----------------------------------------
    print(DIVIDER)
    print("  Sorting & Filtering Demo  (Max's schedule)")
    print(DIVIDER)
    print()

    max_scheduler = _scheduler_for_pet(owner, max_dog)
    max_scheduler.generate_plan()

    print("  Raw scheduled order (by priority, as generated):")
    for t in max_scheduler.scheduled_tasks:
        print(f"    {t.time}  {t.name}")

    print()
    print("  Chronological order (sort_by_time):")
    for t in max_scheduler.sort_by_time():
        print(f"    {t.time}  {t.name}")

    # Mark one task complete to make status filtering interesting
    morning_walk = next(t for t in max_scheduler.scheduled_tasks if t.name == "Morning Walk")
    morning_walk.mark_complete()

    print()
    print("  [ Marked 'Morning Walk' as complete ]")
    print()
    print("  filter_by_status(True)  — completed tasks:")
    done = max_scheduler.filter_by_status(True)
    if done:
        for t in done:
            print(f"    [x]  {t.name}")
    else:
        print("    (none)")

    print()
    print("  filter_by_status(False)  — pending tasks:")
    pending = max_scheduler.filter_by_status(False)
    if pending:
        for t in pending:
            print(f"    [ ]  {t.name}")
    else:
        print("    (none)")

    # Build a combined multi-pet scheduler to demonstrate filter_by_pet
    combined_scheduler = Scheduler(owner)
    combined_scheduler.generate_plan()

    print()
    print(SECTION)
    print("  filter_by_pet demo  (combined owner scheduler — both pets)")
    print(SECTION)
    for pet_name in ["Max", "Luna"]:
        tasks = combined_scheduler.filter_by_pet(pet_name)
        print(f"\n  Tasks scheduled for '{pet_name}':")
        if tasks:
            for t in tasks:
                print(f"    {t.time}  {t.name:<22} | {t.duration_minutes} min | priority {t.priority}")
        else:
            print("    (none scheduled)")

    print()
    print(DIVIDER)
    print("  End of demo.")
    print(DIVIDER)
    print()

    # --- Recurring tasks demo --------------------------------------------
    print(DIVIDER)
    print("  Recurring Tasks Demo")
    print(DIVIDER)
    print()

    recur_owner = Owner("Sam Lee", "sam@example.com", 120)
    recur_pet = Pet(name="Biscuit", species="Dog", breed="Beagle", age_years=4)

    daily_walk = Task(
        "Evening Walk", duration_minutes=30, priority=4, category="exercise",
        time="18:00", frequency="daily", due_date=date(2026, 3, 29),
    )
    weekly_checkup = Task(
        "Vet Checkup", duration_minutes=60, priority=5, category="health",
        time="10:00", frequency="weekly", due_date=date(2026, 3, 29),
    )
    one_time_bath = Task(
        "Bath", duration_minutes=20, priority=3, category="grooming",
        time="11:00", frequency="once", due_date=date(2026, 3, 29),
    )

    recur_pet.add_task(daily_walk)
    recur_pet.add_task(weekly_checkup)
    recur_pet.add_task(one_time_bath)
    recur_owner.add_pet(recur_pet)

    recur_scheduler = Scheduler(recur_owner)
    recur_scheduler.generate_plan()

    def print_task_list(label: str, tasks: list) -> None:
        print(f"  {label}")
        for t in tasks:
            status = "[x]" if t.is_completed else "[ ]"
            print(f"    {status}  {t.name:<22} | {t.frequency:<8} | due {t.due_date}")
        print()

    print_task_list("BEFORE mark_task_complete:", recur_pet.get_tasks())

    recur_scheduler.mark_task_complete("Evening Walk")
    recur_scheduler.mark_task_complete("Vet Checkup")
    recur_scheduler.mark_task_complete("Bath")

    print_task_list("AFTER  mark_task_complete:", recur_pet.get_tasks())

    print("  Next occurrences:")
    for task in [daily_walk, weekly_checkup, one_time_bath]:
        nxt = task.next_occurrence()
        print(f"    {task.name:<22} → {nxt if nxt else '(one-time, no next occurrence)'}")

    print()

    # --- Conflict detection demo -----------------------------------------
    print(DIVIDER)
    print("  Conflict Detection Demo")
    print(DIVIDER)
    print()

    conflict_owner = Owner("Conflict Demo", "", 180)
    conflict_pet = Pet(name="Rocky", species="Dog", breed="Bulldog", age_years=2)

    conflict_pet.add_task(Task("Morning Walk",   duration_minutes=30, priority=5, category="exercise",   time="07:00"))
    conflict_pet.add_task(Task("Feeding",        duration_minutes=10, priority=5, category="nutrition",  time="07:00"))  # conflict
    conflict_pet.add_task(Task("Medication",     duration_minutes=5,  priority=4, category="health",     time="08:00"))
    conflict_pet.add_task(Task("Enrichment",     duration_minutes=20, priority=3, category="enrichment", time="08:00"))  # conflict
    conflict_pet.add_task(Task("Evening Walk",   duration_minutes=30, priority=4, category="exercise",   time="17:00"))

    conflict_owner.add_pet(conflict_pet)
    conflict_scheduler = Scheduler(conflict_owner)
    conflict_scheduler.generate_plan()

    print("  Scheduled tasks:")
    for t in conflict_scheduler.scheduled_tasks:
        print(f"    {t.time}  {t.name}")

    print()
    result = conflict_scheduler.detect_conflicts()
    if result:
        print(f"  {result.replace(chr(10), chr(10) + '  ')}")
    else:
        print("  No conflicts found.")

    print()

    # --- Part 4: detect_conflicts() review (flagged for human review) ----
    print(DIVIDER)
    print("  Part 4 — detect_conflicts() design review")
    print(DIVIDER)
    print("""
  CURRENT implementation (explicit dict + setdefault):
  ┌─────────────────────────────────────────────────────┐
  │  time_groups: dict[str, list[str]] = {}             │
  │  for task in self.scheduled_tasks:                  │
  │      time_groups.setdefault(task.time,[]).append(…) │
  │  conflicts = {t: n for t, n in time_groups.items()  │
  │               if len(n) > 1}                        │
  │  if not conflicts: return None                      │
  │  lines = ["Scheduling conflicts detected:"]         │
  │  for t in sorted(conflicts):                        │
  │      lines.append(f"  {t} — {…}")                  │
  │  return "\\n".join(lines)                           │
  └─────────────────────────────────────────────────────┘
  Trade-off: verbose, zero extra imports, easy to step
  through line by line.

  SIMPLIFIED candidate (defaultdict + single-expression return):
  ┌─────────────────────────────────────────────────────┐
  │  from collections import defaultdict                │
  │  groups: dict[str,list[str]] = defaultdict(list)    │
  │  for task in self.scheduled_tasks:                  │
  │      groups[task.time].append(task.name)            │
  │  conflicts = {t: n for t, n in groups.items()       │
  │               if len(n) > 1}                        │
  │  if not conflicts: return None                      │
  │  return "Scheduling conflicts detected:\\n" +       │
  │      "\\n".join(f"  {t} — {', '.join(n)}"          │
  │                 for t, n in sorted(conflicts.items()))│
  └─────────────────────────────────────────────────────┘
  Trade-off: terser return expression, but requires an
  extra import and the single-line return is harder to
  read at a glance. Flagged for human review — do not
  apply automatically.
""")
    print(DIVIDER)
    print("  End of all demos.")
    print(DIVIDER)
    print()


if __name__ == "__main__":
    main()
