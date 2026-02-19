# PawPal+ Project Reflection

## 1. System Design
## Core actions:
- Add a a pet
- Schedule a walk
- Groom pet

**a. Initial design**

- Briefly describe your initial UML design.
My initial UML had four classes: Pet, Owner, CareTask, and DailyPlan. 
- What classes did you include, and what responsibilities did you assign to each?
Pet stored basic info like name, species, and age. Owner held the pet reference and availability. CareTask tracked what needed to be done and when. DailyPlan was meant to hold the final schedule.

**b. Design changes**

- Did your design change during implementation?
Yes
- If yes, describe at least one change and why you made it.
The biggest addition was a dedicated Scheduler class — originally I had DailyPlan doing the scheduling itself, but as the logic grew (two passes, conflict detection, sorting), it made more sense to separate the algorithm from the data. I also added ConflictReport as its own class once I realized conflict results needed to carry structured info (pet name, overlap type) rather than just a string.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
The scheduler considers: owner availability windows (hard constraint — tasks only fit within declared slots), task priority (higher priority tasks are placed first), task type (medication gets a bonus score), and whether a task is fixed-time (gets scheduled into a specific window rather than wherever fits). For recurring tasks, it also checks whether a task is due today before including it.
- How did you decide which constraints mattered most?
I prioritized availability as the hardest constraint because there's no point scheduling something the owner can't actually do. Priority score came second — the whole point of the app is making sure important care doesn't get dropped.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
The scheduler uses a forward-only slot cursor for simplicity and speed, but sacrifices schedule density: time gaps left before fixed-window tasks are permanently wasted rather than filled by flexible lower-priority tasks.

- Why is that tradeoff reasonable for this scenario?
The greedy cursor is reasonable here because pet care tasks are few, biologically spaced, and have a fallback pass — so wasted gaps rarely cause a task to go unscheduled.
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
I used AI throughout — mostly for implementation help (translating logic descriptions into working Python), debugging why the UI wasn't showing schedule output, and drafting tests. 
- What kinds of prompts or questions were most helpful?
The most useful prompts were specific and tied to the actual code: "why does the scheduler return nothing" rather than "how do schedulers work." Asking AI to compare the running code against a UML diagram was also unexpectedly useful.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
When AI suggested the initial test suite, one test was asserting len(plan.unscheduled_tasks) == 1 — which was a leftover from before the algorithm was implemented. It was technically passing, but for the wrong reason.
- How did you evaluate or verify what the AI suggested?
 caught it by reading the test carefully and running the app manually to confirm tasks were actually being scheduled. That moment made me realize AI can produce tests that pass without actually verifying the right thing.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
I tested three main areas: sorting correctness (does sort_by_time handle midnight tasks and missing start minutes?), recurrence logic (does next_due_date advance correctly for daily vs weekly tasks?), and conflict detection (does the scheduler flag overlaps but not adjacent tasks?).
- Why were these tests important?
These mattered because they're the behaviors most likely to break silently — a sorting bug won't crash anything, it'll just show tasks in the wrong order, and you might not notice.

**b. Confidence**

- How confident are you that your scheduler works correctly?
I'd say 4/5. The core scheduling path is well-tested. What I'm less confident about is the two-pass fallback — I only tested it end-to-end with a single task.
- What edge cases would you test next if you had more time?
Edge cases like a fully packed slot forcing Pass 2, or a twice_daily task when there's only one available window, aren't directly tested yet.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
I'm most satisfied with the conflict detection system. It's clean — it doesn't raise exceptions, it returns structured ConflictReport objects, and it correctly distinguishes same-pet vs cross-pet overlaps. It also connects naturally to the UI through st.warning.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
The twice_daily expansion is a bit fragile — it assumes exactly two time windows and breaks down silently if there's only one. I'd redesign that to be more explicit about what happens when windows are missing.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
The biggest lesson was that AI is much more useful when you already understand the problem. Early in the project when I was still fuzzy on the design, AI suggestions felt random. Once I had a clear mental model, I could give precise prompts and actually evaluate whether the output was correct. AI didn't replace understanding — it accelerated it.