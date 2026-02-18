"""
PawPal+ Main Script
Demonstrates the pet care planning system.
"""

from datetime import date
from pawpal_system import Pet, CareTask, Owner, Scheduler


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

    # Add tasks for Buddy
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

    evening_walk = CareTask(
        task_type="walk",
        name="Evening Walk",
        duration_minutes=45,
        priority=4,
        frequency="daily",
        preferred_time_windows=["18:00-20:00"],
        notes="Longer walk to burn energy"
    )

    # Add tasks for Whiskers
    whiskers_breakfast = CareTask(
        task_type="feed",
        name="Whiskers' Breakfast",
        duration_minutes=5,
        priority=5,
        frequency="daily",
        preferred_time_windows=["07:00-08:00"],
        is_time_flexible=False
    )

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

    play_time = CareTask(
        task_type="enrichment",
        name="Interactive Play",
        duration_minutes=20,
        priority=3,
        frequency="daily",
        preferred_time_windows=["12:00-13:00", "19:00-20:00"],
        notes="Feather toy or laser pointer"
    )

    # Add tasks to pets
    buddy.add_care_task(morning_walk)
    buddy.add_care_task(buddy_breakfast)
    buddy.add_care_task(evening_walk)

    whiskers.add_care_task(whiskers_breakfast)
    whiskers.add_care_task(joint_medication)
    whiskers.add_care_task(play_time)

    # Add pets to owner
    owner.add_pet(buddy)
    owner.add_pet(whiskers)

    # Create scheduler and generate plan
    scheduler = Scheduler(owner)
    plan = scheduler.generate_daily_plan(date.today())

    # Print Today's Schedule
    print("=" * 60)
    print(f"TODAY'S SCHEDULE - {plan.date.strftime('%A, %B %d, %Y')}")
    print("=" * 60)
    print(f"\nOwner: {owner.name}")
    print(f"Pets: {', '.join([pet.name for pet in owner.pets])}")
    print(f"Available Time: {owner.total_available_minutes} minutes")
    print(f"  Time Slots: {', '.join(owner.available_time_slots)}")

    print("\n" + "-" * 60)
    print("TASKS TO COMPLETE")
    print("-" * 60)

    all_tasks = owner.get_all_care_tasks()

    # Group tasks by pet
    for pet in owner.pets:
        pet_tasks = pet.get_care_requirements()
        if pet_tasks:
            print(f"\n{pet.name} ({pet.species.title()}):")
            for task in pet_tasks:
                priority_stars = "⭐" * task.priority
                time_pref = task.preferred_time_windows[0] if task.preferred_time_windows else "Flexible"
                flexible = "✓" if task.is_time_flexible else "✗"

                print(f"  • {task.name}")
                print(f"    Type: {task.task_type.title()} | Duration: {task.duration_minutes}min | Priority: {priority_stars}")
                print(f"    Preferred Time: {time_pref} | Flexible: {flexible}")
                if task.notes:
                    print(f"    Notes: {task.notes}")

    print("\n" + "-" * 60)
    print("PLAN SUMMARY")
    print("-" * 60)
    print(f"Total Tasks: {len(all_tasks)}")
    print(f"Scheduled Tasks: {len(plan.scheduled_tasks)}")
    print(f"Unscheduled Tasks: {len(plan.unscheduled_tasks)}")
    print(f"Total Time Required: {sum(task.duration_minutes for task in all_tasks)} minutes")
    print(f"\nReasoning: {plan.reasoning}")

    if plan.scheduled_tasks:
        print("\n" + "-" * 60)
        print("SCHEDULED TASKS")
        print("-" * 60)
        for time, task in sorted(plan.scheduled_tasks):
            print(f"{time} - {task.name} ({task.duration_minutes}min)")

    if plan.unscheduled_tasks:
        print("\n" + "-" * 60)
        print("TASKS PENDING SCHEDULING")
        print("-" * 60)
        for task in sorted(plan.unscheduled_tasks, key=lambda t: t.priority, reverse=True):
            print(f"  • {task.name} (Priority: {task.priority})")

    print("\n" + "=" * 60)
    print("💡 TIP: Implement the scheduling algorithm to auto-schedule tasks!")
    print("=" * 60)


if __name__ == "__main__":
    main()
