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

## Smarter Scheduling

The scheduling engine in `pawpal_system.py` goes beyond a simple task list. Key features added:

**Two-pass greedy algorithm** — Tasks are sorted by priority score and placed into the owner's availability slots. Pass 1 respects each task's preferred time window; Pass 2 relaxes that constraint for any task that didn't fit, so high-priority tasks are never silently dropped.

**Priority scoring** — `CareTask.get_priority_score()` weights base priority (×10), fixed-time tasks (+20), and medication tasks (+15) so critical care always schedules first.

**Recurring task expansion** — `frequency="twice_daily"` tasks are split into AM/PM instances using the two preferred windows. `frequency="weekly"` tasks are skipped on non-matching weekdays via `scheduled_weekday`. Completed tasks set `next_due_date` automatically and reappear on the correct day.

**Conflict detection** — `Scheduler.detect_conflicts()` scans a plan pairwise and returns `ConflictReport` warnings that classify each overlap as same-pet or cross-pet, without raising exceptions.

**Filtering and sorting** — `DailyPlan.filter_tasks(pet_name=, completed=)` filters the schedule by pet, status, or both. `Scheduler.sort_by_time()` orders any task list chronologically using `scheduled_start_minute`.

**Auto-generated tasks** — `Pet.get_care_requirements()` automatically adds a training session for dogs under 2 and a weekly weight check for cats over 10, and forces feeding tasks to be time-inflexible for pets with medical conditions.

## Getting started

### Setup

```bash
python -m venv .venv
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
