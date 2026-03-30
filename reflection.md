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

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
