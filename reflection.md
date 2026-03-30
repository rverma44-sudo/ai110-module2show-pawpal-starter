# PawPal+ Project Reflection

## 1. System Design
Add a pet, look at schedule for today, prioritize committments.
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
