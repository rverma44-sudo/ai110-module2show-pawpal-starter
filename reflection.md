# PawPal+ Project Reflection

## 1. System Design
**Action 1 — Register a pet:** The owner opens the app and adds a new pet by entering the pet's name, species, breed, age, and any health notes. The pet is then stored under the owner's profile and available for task assignment.

**Action 2 — Schedule daily tasks:** For each pet, the owner adds care tasks (walks, feeding, medication, grooming, etc.) with a duration, priority level, and category. The scheduler automatically generates a prioritized daily plan that fits within the owner's available time budget.

**Action 3 — Review and prioritize today's plan:** The owner views today's schedule sorted chronologically, checks off completed tasks, and reads the conflict warnings or explanation text to understand why certain tasks were included or excluded.
**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
My UML design has 4 classes:
Task: Assigns tasks and priority levels which are associated with name, duration, category, things like that. Task also manages its own state by marking tasks complete or resetting them
Pet - This class owns the list of tasks and manages them as well as calculating total task duration
Owner: This class manages the collection of pets and tracks how many minutes per day is available
Scheduler: This class is the brain, it generates a filtered, time-constrained daily plan and explains its reasoning based on the tasks and time delegated.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
Yes it did, my design had the flaw in the Scheduler class. The class only allowed for one pet to be held. That was an issue because it broke the core ownership model in the UML. If there are multiple pets, the schedule can't incorporate those which would make it useless.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?
The two biggest constraints that I chose mattered most were time and priority. Available minutes per day on the owner is the most important constraint as it is the hard cap on how much time can even be delegated for tasks. Right after time is priority because the tasks that have higher priority need to be done next given the timeframe. I didn't consider preference to be as important because from an objective standpoint going based on preference all the time won't ensure important tasks will be completed.
**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
The biggest tradeoff my scheduler makes is overlapping time. It only flags exact time matches not time windows such as a 10 min task at 9 am and a 20 min task at 9:05 because the schedule is for a pet owner with a loose daily routine, not an excruciatingly strict minute to minute schedule.
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?
I used AI throughout the creation of the program. First I used it to assist me in creating the UML diagram, then creating code for phase 2, then solving streamlit architectual problems in phase 3, then implementing and sorting tasks algorithmically in phase 4, then generating tests in phase 5 and finally, comparing the old uml with the current in phase 6.
I learned the best prompts were those that provided constraints to the model because it gave it more specific direction that it needed to follow. Open-ended prompts had more erros. 

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?
I didn't accept AI's suggestion about overlapping time windows because my tasks are structured by a single time string rather than a task window, so using a task window would require restructuring the entire task data model when that level of fine precision was not necessary. 
I verified this by running 2 tests at the same time with main.py and confirming the warning was correctly printed.
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?
I tested 5 main things: time-constrained plan generation, due_date advancement for daily and weekly recurrence, conflict detection, chronological sorting without list mutation, and recurring task creation after completion. 
These tests were important because they ensured common errors would not occur and the program would function as expected. I also tested edge cases so the program wouldn't crash.

**b. Confidence**

- How confident are you that your scheduler works correctly?
5/5 Given the only concern is the overlapping times, which I personally don't believe is a largely problematic concern, the tasks are easily updated into the scheduler and ranked based on time and priority
- What edge cases would you test next if you had more time?
I would test whether the UI displays conflict warnings after task and chore submissions.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
In general I'm really satisfied with the creation of the app. Prior to this course my understanding was a few prompts into ai and a program like this could be created but now I know that significantly more goes into it and there needs to be a human level of understanding to enhance it. 

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
With more time and another iteration I would probably just refine the time overlapping with tasks in order to create a minute by minute calendar, assign tasks based potentiall on what time of day they need to be done, things like that.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
I learned AI output scales heavily with how well a prompt is. Broad prompts are generic and not very effective whereas specific prompts allow for specified results and outputs. I needed to know not just what to create, but what constraints are needed to avoid what not to create.

## Prompt Comparison

**Models compared:** Google Gemini vs Anthropic Claude Sonnet

---

### Gemini's Approach

Gemini correctly identified `dataclasses.replace()` as the right tool 
and produced a clean, readable solution. It used a standard `for` loop 
with an early `break` to locate the target task, mutated it in place, 
then appended a fresh recurring instance. The explanation focused on 
practical benefits — avoiding boilerplate, memory safety, and clear 
intent — making it accessible and easy to follow. The solution would 
work correctly in the existing PawPal+ codebase with minimal changes.

**Patterns used:** `dataclasses.replace()`, `for` loop with `break`, 
`timedelta(days=7)`, `None` return type (implicit)

---

### Claude's Approach

Claude produced a more advanced solution that introduced several 
additional Python patterns. It used `next()` with a generator 
expression instead of a `for` loop, wrapped in `try/except 
StopIteration` for a clean `ValueError` on a missing task name. 
It introduced a `StrEnum` for `Frequency` to make comparisons 
identity-safe while keeping values serializable as plain strings. 
It preferred `timedelta(weeks=1)` over `timedelta(days=7)` for 
clearer intent, and made the return type explicit as `Task | None` 
so callers know a new task is only produced for weekly recurrences.

**Patterns used:** `dataclasses.replace()`, `next()` with generator, 
`try/except StopIteration`, `StrEnum`, `timedelta(weeks=1)`, 
explicit `Task | None` return type

---

### Which Was More Pythonic and Why

Claude's solution is more Pythonic by conventional Python standards. 
The use of `next()` with a generator expression is more idiomatic 
than a `for` loop with a `break` for finding a single item. The 
explicit `Task | None` return type makes the method's branching 
behavior visible in the signature without reading the body. 
`timedelta(weeks=1)` over `timedelta(days=7)` is a small but 
meaningful signal-of-intent improvement. The `StrEnum` addition 
goes furthest in terms of robustness, though it would require 
updating the existing Task dataclass and serialization logic in 
PawPal+, making it a larger change than the task strictly required.

Gemini's solution is more immediately portable into the existing 
codebase — it makes no assumptions about the Frequency type and 
introduces no new dependencies or enum infrastructure.

**Decision:** Claude's `next()` pattern and `timedelta(weeks=1)` 
preference were adopted. The `StrEnum` was not adopted because 
PawPal+ already stores frequency as a plain string and changing 
the type would break the existing JSON serialization and pytest 
suite without adding enough value to justify the refactor.

---

### What This Comparison Revealed

Both models independently converged on `dataclasses.replace()` as 
the correct tool, which confirms it is the genuinely idiomatic 
choice for this pattern in Python. The meaningful difference was 
not correctness but scope — Gemini solved exactly the stated 
problem while Claude proposed a more complete design that assumed 
a greenfield context. This revealed an important principle: a more 
Pythonic solution is not always the right solution. Evaluating AI 
output requires weighing technical elegance against the cost of 
integrating that solution into an existing system with existing 
constraints.