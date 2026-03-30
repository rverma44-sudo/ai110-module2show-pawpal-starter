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
        available_minutes_per_day=90,
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
    max_dog.add_task(Task("Morning Walk",    duration_minutes=30, priority=5, category="exercise"))
    max_dog.add_task(Task("Feeding",         duration_minutes=10, priority=5, category="nutrition"))
    max_dog.add_task(Task("Enrichment Play", duration_minutes=20, priority=4, category="enrichment"))
    max_dog.add_task(Task("Full Grooming",   duration_minutes=45, priority=3, category="grooming"))

    # --- Pet 2: Luna the cat ---------------------------------------------
    luna_cat = Pet(
        name="Luna",
        species="Cat",
        breed="Domestic Shorthair",
        age_years=5,
        health_notes=["daily thyroid medication"],
    )
    luna_cat.add_task(Task("Feeding",       duration_minutes=10, priority=5, category="nutrition"))
    luna_cat.add_task(Task("Medication",    duration_minutes=5,  priority=5, category="health"))
    luna_cat.add_task(Task("Litter Box",    duration_minutes=5,  priority=4, category="hygiene"))
    luna_cat.add_task(Task("Playtime",      duration_minutes=15, priority=3, category="enrichment"))
    luna_cat.add_task(Task("Claw Trim",     duration_minutes=60, priority=2, category="grooming"))

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


if __name__ == "__main__":
    main()
