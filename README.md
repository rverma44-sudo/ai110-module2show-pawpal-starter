# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Smarter Scheduling

PawPal+ includes a bunch of features that automate scheduling to make it intelligent rather than manual and laborous:

- **Sorted Schedules** — tasks are automatically sorted chronologically 
  by time so owners always see their day in order
- **Smart Filtering** — tasks can be filtered by completion status or 
  pet name to focus on what still needs to be done
- **Recurring Tasks** — daily and weekly tasks automatically reschedule 
  themselves after being marked complete, so nothing falls through 
  the cracks
- **Conflict Detection** — the scheduler warns owners when two tasks 
  are booked at the same time, for the same pet or across pets, 
  without crashing the app
- **Time-Constrained Planning** — the scheduler only includes tasks 
  that fit within the owner's available daily minutes, and explains 
  which tasks were excluded and why