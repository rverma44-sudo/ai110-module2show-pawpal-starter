<!-- Reflects the final PawPal+ implementation — generated 2026-03-29 -->

# PawPal+ UML Class Diagram (Final)

## Part 1 — Changes from uml_draft.md to final implementation

### Task class
| What changed | Draft | Final |
|---|---|---|
| New attribute | — | `+str time` (default `"00:00"`) |
| New attribute | — | `+str frequency` (default `"once"`) |
| New attribute | — | `+date due_date` (default `date.today()`) |
| New method | — | `+next_occurrence() str?` — returns next due date string for recurring tasks, or None for one-time tasks |

### Owner class
| What changed | Draft | Final |
|---|---|---|
| New method | — | `+get_all_tasks() list~Task~` — flattens every task across all pets into one list |

### Pet class
No changes to public interface.

### Scheduler class
| What changed | Draft | Final |
|---|---|---|
| Attribute renamed + type changed | `+Pet pet` (singular, one Pet) | `+list~Pet~ pets` (plural list, populated at runtime by `generate_plan()`) |
| Constructor signature | implicitly accepted Pet | accepts only `Owner`; pets resolved at runtime via `owner.get_pets()` |
| New method | — | `+sort_by_time() list~Task~` |
| New method | — | `+filter_by_status(is_completed: bool) list~Task~` |
| New method | — | `+filter_by_pet(pet_name: str) list~Task~` |
| New method | — | `+mark_task_complete(task_name: str) str?` |
| New method | — | `+detect_conflicts() str?` |

### Relationships
| What changed | Draft | Final |
|---|---|---|
| Scheduler → Pet cardinality | `"1" --> "1" Pet : schedules for` | `"1" --> "0..*" Pet : resolves at runtime` (pets populated by `generate_plan()`, not the constructor) |

---

## Part 2 — Updated Mermaid diagram

```mermaid
classDiagram
    class Owner {
        +str name
        +str email
        +int available_minutes_per_day
        +list~str~ preferences
        +add_pet(pet: Pet) None
        +remove_pet(pet_name: str) bool
        +get_pets() list~Pet~
        +set_available_time(minutes: int) None
        +get_all_tasks() list~Task~
    }

    class Pet {
        +str name
        +str species
        +str breed
        +int age_years
        +list~str~ health_notes
        +add_task(task: Task) None
        +remove_task(task_name: str) bool
        +get_tasks() list~Task~
        +get_total_task_duration() int
    }

    class Task {
        +str name
        +int duration_minutes
        +int priority
        +str category
        +bool is_completed
        +str notes
        +str time
        +str frequency
        +date due_date
        +mark_complete() None
        +reset() None
        +next_occurrence() str?
        +is_higher_priority_than(other: Task) bool
    }

    class Scheduler {
        +Owner owner
        +list~Pet~ pets
        +list~Task~ scheduled_tasks
        +generate_plan() list~Task~
        +filter_by_priority(min_priority: int) list~Task~
        +fits_within_time(tasks: list~Task~) bool
        +explain_plan() str
        +get_total_scheduled_duration() int
        +sort_by_time() list~Task~
        +filter_by_status(is_completed: bool) list~Task~
        +filter_by_pet(pet_name: str) list~Task~
        +mark_task_complete(task_name: str) str?
        +detect_conflicts() str?
    }

    Owner "1" *-- "1..*" Pet : owns
    Pet "1" *-- "0..*" Task : has
    Scheduler "1" --> "1" Owner : uses
    Scheduler "1" --> "0..*" Pet : resolves at runtime
    Scheduler ..> Task : selects and orders
```
