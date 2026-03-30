from pawpal_system import Pet, Task


def test_task_completion():
    # Verifies that mark_complete() sets is_completed to True and reset() reverses it
    task = Task(name="Morning Walk", duration_minutes=30, priority=5, category="exercise")

    task.mark_complete()
    assert task.is_completed is True, "mark_complete() should set is_completed to True"

    task.reset()
    assert task.is_completed is False, "reset() should set is_completed back to False"


def test_task_addition():
    # Verifies that add_task() appends tasks to a Pet and get_tasks() reflects the correct count
    pet = Pet(name="Max", species="Dog", breed="Labrador Retriever", age_years=3)

    pet.add_task(Task(name="Feeding", duration_minutes=10, priority=5, category="nutrition"))
    assert len(pet.get_tasks()) == 1, "Pet should have exactly 1 task after the first add_task() call"

    pet.add_task(Task(name="Enrichment Play", duration_minutes=20, priority=4, category="enrichment"))
    assert len(pet.get_tasks()) == 2, "Pet should have exactly 2 tasks after the second add_task() call"
