"""
PawPal+ Main Script
Demonstrates the pet care planning system.
"""

from datetime import date
from pawpal_system import Pet, CareTask, Owner, Scheduler, DailyPlan


def main():
    # Create owner
    owner = Owner(
        name="Sarah Johnson",
        available_time_slots=["06:00-09:00", "12:00-13:00", "17:00-21:00"],
        preferences={"early_walks": True, "max_tasks_per_hour": 2},
        total_available_minutes=420
    )

    # Create first pet: Buddy (dog)
    buddy = Pet(
        name="Buddy",
        species="dog",
        breed="Golden Retriever",
        age=3,
        weight=30.0,
        special_needs=["high energy", "loves water"],
        medical_conditions=[]
    )

    # Create second pet: Whiskers (cat)
    whiskers = Pet(
        name="Whiskers",
        species="cat",
        breed="Siamese",
        age=5,
        weight=4.5,
        special_needs=[],
        medical_conditions=["senior joint care"]
    )

    # Add tasks OUT OF ORDER to demonstrate sort_by_time -------------------

    # Buddy: add evening tasks first, then morning tasks
    evening_walk = CareTask(
        task_type="walk",
        name="Evening Walk",
        duration_minutes=45,
        priority=4,
        frequency="daily",
        preferred_time_windows=["18:00-20:00"],
        notes="Longer walk to burn energy"
    )

    buddy_dinner = CareTask(
        task_type="feed",
        name="Buddy's Dinner",
        duration_minutes=10,
        priority=5,
        frequency="daily",
        preferred_time_windows=["17:30-18:30"],
        is_time_flexible=False
    )

    morning_walk = CareTask(
        task_type="walk",
        name="Morning Walk",
        duration_minutes=30,
        priority=4,
        frequency="daily",
        preferred_time_windows=["06:30-08:00"],
        notes="Buddy loves the park in the morning"
    )

    buddy_breakfast = CareTask(
        task_type="feed",
        name="Buddy's Breakfast",
        duration_minutes=10,
        priority=5,
        frequency="daily",
        preferred_time_windows=["07:00-08:00"],
        is_time_flexible=False
    )

    # Whiskers: add medication first, then feeding, then play
    joint_medication = CareTask(
        task_type="medication",
        name="Joint Supplement",
        duration_minutes=5,
        priority=5,
        frequency="daily",
        preferred_time_windows=["08:00-09:00"],
        notes="Give with food",
        is_time_flexible=False
    )

    whiskers_breakfast = CareTask(
        task_type="feed",
        name="Whiskers' Breakfast",
        duration_minutes=5,
        priority=5,
        frequency="daily",
        preferred_time_windows=["07:00-08:00"],
        is_time_flexible=False
    )

    play_time = CareTask(
        task_type="enrichment",
        name="Interactive Play",
        duration_minutes=20,
        priority=3,
        frequency="daily",
        preferred_time_windows=["12:00-13:00", "19:00-20:00"],
        notes="Feather toy or laser pointer"
    )

    # Register tasks in the out-of-order sequence
    buddy.add_care_task(evening_walk)      # evening before morning
    buddy.add_care_task(buddy_dinner)
    buddy.add_care_task(morning_walk)
    buddy.add_care_task(buddy_breakfast)

    whiskers.add_care_task(joint_medication)   # medication before breakfast
    whiskers.add_care_task(whiskers_breakfast)
    whiskers.add_care_task(play_time)

    owner.add_pet(buddy)
    owner.add_pet(whiskers)

    # Generate plan
    scheduler = Scheduler(owner)
    plan = scheduler.generate_daily_plan(date.today())

    # ------------------------------------------------------------------
    # 1. Full schedule sorted by time (Scheduler.sort_by_time)
    # ------------------------------------------------------------------
    print("=" * 60)
    print(f"TODAY'S SCHEDULE - {plan.date.strftime('%A, %B %d, %Y')}")
    print("=" * 60)
    print(f"Owner: {owner.name}  |  Pets: {', '.join(p.name for p in owner.pets)}")
    print(f"Reasoning: {plan.reasoning}")

    print("\n" + "-" * 60)
    print("ALL TASKS  (sorted by time via Scheduler.sort_by_time)")
    print("-" * 60)
    for time_str, task in Scheduler.sort_by_time(plan.scheduled_tasks):
        status = "[done]" if task.is_completed else "[todo]"
        print(f"  {time_str}  {status}  {task.name:<30} ({task.duration_minutes}min, {task.pet_name})")

    # ------------------------------------------------------------------
    # 2. Filter by pet  (DailyPlan.filter_tasks)
    # ------------------------------------------------------------------
    print("\n" + "-" * 60)
    print("BUDDY'S TASKS ONLY  (filter_tasks pet_name='Buddy')")
    print("-" * 60)
    for time_str, task in plan.filter_tasks(pet_name="Buddy"):
        print(f"  {time_str}  {task.name} ({task.duration_minutes}min)")

    print("\n" + "-" * 60)
    print("WHISKERS' TASKS ONLY  (filter_tasks pet_name='Whiskers')")
    print("-" * 60)
    for time_str, task in plan.filter_tasks(pet_name="Whiskers"):
        print(f"  {time_str}  {task.name} ({task.duration_minutes}min)")

    # ------------------------------------------------------------------
    # 3. Mark some tasks complete, then filter by status
    # ------------------------------------------------------------------
    # Simulate completing the first two tasks of the day
    sorted_all = Scheduler.sort_by_time(plan.scheduled_tasks)
    for _, task in sorted_all[:2]:
        task.mark_complete()

    print("\n" + "-" * 60)
    print("PENDING TASKS  (filter_tasks completed=False)")
    print("-" * 60)
    pending = plan.filter_tasks(completed=False)
    if pending:
        for time_str, task in pending:
            print(f"  {time_str}  {task.name} ({task.pet_name})")
    else:
        print("  All done!")

    print("\n" + "-" * 60)
    print("COMPLETED TASKS  (filter_tasks completed=True)")
    print("-" * 60)
    for time_str, task in plan.filter_tasks(completed=True):
        print(f"  {time_str}  {task.name} ({task.pet_name})")

    # ------------------------------------------------------------------
    # 4. Combined filter: Buddy's pending tasks
    # ------------------------------------------------------------------
    print("\n" + "-" * 60)
    print("BUDDY'S PENDING TASKS  (filter_tasks pet_name='Buddy', completed=False)")
    print("-" * 60)
    for time_str, task in plan.filter_tasks(pet_name="Buddy", completed=False):
        print(f"  {time_str}  {task.name}")

    # ------------------------------------------------------------------
    # 5. Unscheduled tasks
    # ------------------------------------------------------------------
    if plan.unscheduled_tasks:
        print("\n" + "-" * 60)
        print("COULD NOT SCHEDULE")
        print("-" * 60)
        for task in sorted(plan.unscheduled_tasks, key=lambda t: t.priority, reverse=True):
            print(f"  {task.name} (priority {task.priority}, {task.pet_name})")

    # ------------------------------------------------------------------
    # 6. Conflict detection demo
    # The scheduler prevents conflicts during normal planning, so we inject
    # overlapping tasks directly into a fresh DailyPlan to demonstrate
    # that detect_conflicts catches both same-pet and cross-pet clashes.
    # ------------------------------------------------------------------
    print("\n" + "-" * 60)
    print("CONFLICT DETECTION DEMO  (scheduler.detect_conflicts)")
    print("-" * 60)

    conflict_plan = DailyPlan(date=date.today())

    # Same-pet conflict: two Buddy tasks both starting at 07:00
    buddy_feed = CareTask(
        task_type="feed", name="Buddy's Breakfast",
        duration_minutes=10, priority=5, frequency="daily",
        pet_name="Buddy", scheduled_start_minute=420,   # 07:00
    )
    buddy_walk = CareTask(
        task_type="walk", name="Morning Walk",
        duration_minutes=30, priority=4, frequency="daily",
        pet_name="Buddy", scheduled_start_minute=420,   # 07:00 — overlaps!
    )
    # Cross-pet conflict: Whiskers task overlaps Buddy's walk (07:05)
    whiskers_feed = CareTask(
        task_type="feed", name="Whiskers' Breakfast",
        duration_minutes=15, priority=5, frequency="daily",
        pet_name="Whiskers", scheduled_start_minute=425,  # 07:05 — overlaps walk
    )

    # Inject directly, bypassing add_task's conflict guard, to simulate a
    # broken plan and prove detect_conflicts catches it
    conflict_plan.scheduled_tasks = [
        ("07:00", buddy_feed),
        ("07:00", buddy_walk),
        ("07:05", whiskers_feed),
    ]

    conflicts = scheduler.detect_conflicts(conflict_plan)
    if conflicts:
        for report in conflicts:
            print(f"  {report}")
    else:
        print("  No conflicts detected.")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
