"""
Unit tests for PawPal+ pet care planning system.
"""

import sys
from pathlib import Path

# Add parent directory to path so we can import pawpal_system
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from datetime import date
from pawpal_system import Pet, CareTask, Owner, DailyPlan, Scheduler


class TestCareTask:
    """Tests for CareTask class."""

    def test_task_completion(self):
        """Verify that calling mark_complete() changes the task's status."""
        # Arrange: Create a task
        task = CareTask(
            task_type="walk",
            name="Morning Walk",
            duration_minutes=30,
            priority=4,
            frequency="daily"
        )

        # Assert: Task should start as incomplete
        assert task.is_completed is False

        # Act: Mark the task as complete
        task.mark_complete()

        # Assert: Task should now be completed
        assert task.is_completed is True

    def test_task_mark_incomplete(self):
        """Verify that a completed task can be marked incomplete."""
        # Arrange: Create and complete a task
        task = CareTask(
            task_type="feed",
            name="Breakfast",
            duration_minutes=10,
            priority=5,
            frequency="daily"
        )
        task.mark_complete()

        # Assert: Task should be completed
        assert task.is_completed is True

        # Act: Mark task as incomplete
        task.mark_incomplete()

        # Assert: Task should now be incomplete
        assert task.is_completed is False


class TestPet:
    """Tests for Pet class."""

    def test_task_addition(self):
        """Verify that adding a task to a Pet increases that pet's task count."""
        # Arrange: Create a pet
        pet = Pet(
            name="Buddy",
            species="dog",
            breed="Golden Retriever",
            age=3,
            weight=30.0
        )

        # Assert: Pet should start with no tasks
        initial_task_count = len(pet.care_tasks)
        assert initial_task_count == 0

        # Act: Add a task to the pet
        task1 = CareTask(
            task_type="walk",
            name="Morning Walk",
            duration_minutes=30,
            priority=4,
            frequency="daily"
        )
        pet.add_care_task(task1)

        # Assert: Task count should increase by 1
        assert len(pet.care_tasks) == initial_task_count + 1

        # Act: Add another task
        task2 = CareTask(
            task_type="feed",
            name="Breakfast",
            duration_minutes=10,
            priority=5,
            frequency="daily"
        )
        pet.add_care_task(task2)

        # Assert: Task count should now be 2
        assert len(pet.care_tasks) == 2

    def test_get_care_requirements(self):
        """Verify that get_care_requirements returns all tasks."""
        # Arrange: Create a pet and add tasks
        pet = Pet(
            name="Whiskers",
            species="cat",
            breed="Siamese",
            age=5,
            weight=4.5
        )

        task1 = CareTask(
            task_type="feed",
            name="Breakfast",
            duration_minutes=5,
            priority=5,
            frequency="daily"
        )

        task2 = CareTask(
            task_type="grooming",
            name="Brush Fur",
            duration_minutes=15,
            priority=3,
            frequency="weekly"
        )

        pet.add_care_task(task1)
        pet.add_care_task(task2)

        # Act: Get care requirements
        requirements = pet.get_care_requirements()

        # Assert: Should return all tasks
        assert len(requirements) == 2
        assert task1 in requirements
        assert task2 in requirements


class TestOwner:
    """Tests for Owner class."""

    def test_add_pet(self):
        """Verify that adding a pet to an owner increases pet count."""
        # Arrange: Create owner and pet
        owner = Owner(name="Alice")
        pet = Pet(
            name="Max",
            species="dog",
            breed="Labrador",
            age=2,
            weight=25.0
        )

        # Assert: Owner should start with no pets
        assert len(owner.pets) == 0

        # Act: Add pet to owner
        owner.add_pet(pet)

        # Assert: Owner should now have 1 pet
        assert len(owner.pets) == 1
        assert owner.pets[0] == pet

    def test_get_all_care_tasks(self):
        """Verify that owner can retrieve tasks from all pets."""
        # Arrange: Create owner with two pets
        owner = Owner(name="Bob")

        pet1 = Pet(name="Buddy", species="dog", breed="Beagle", age=3, weight=20.0)
        pet2 = Pet(name="Mittens", species="cat", breed="Tabby", age=4, weight=5.0)

        task1 = CareTask(
            task_type="walk",
            name="Walk Buddy",
            duration_minutes=30,
            priority=4,
            frequency="daily"
        )

        task2 = CareTask(
            task_type="feed",
            name="Feed Mittens",
            duration_minutes=5,
            priority=5,
            frequency="daily"
        )

        pet1.add_care_task(task1)
        pet2.add_care_task(task2)

        owner.add_pet(pet1)
        owner.add_pet(pet2)

        # Act: Get all tasks
        all_tasks = owner.get_all_care_tasks()

        # Assert: Should return tasks from both pets
        assert len(all_tasks) == 2
        assert task1 in all_tasks
        assert task2 in all_tasks


class TestScheduler:
    """Tests for Scheduler class."""

    def test_generate_daily_plan(self):
        """Verify that scheduler can generate a plan."""
        # Arrange: Create owner with pet and tasks
        owner = Owner(
            name="Charlie",
            available_time_slots=["07:00-09:00", "17:00-20:00"]
        )

        pet = Pet(name="Rex", species="dog", breed="German Shepherd", age=5, weight=35.0)

        task = CareTask(
            task_type="walk",
            name="Evening Walk",
            duration_minutes=45,
            priority=4,
            frequency="daily"
        )

        pet.add_care_task(task)
        owner.add_pet(pet)

        scheduler = Scheduler(owner)

        # Act: Generate plan
        plan = scheduler.generate_daily_plan(date.today())

        # Assert: Plan should be created with the task scheduled
        assert plan is not None
        assert plan.date == date.today()
        assert len(plan.scheduled_tasks) == 1
        assert len(plan.unscheduled_tasks) == 0


class TestSorting:
    """Tests for Scheduler.sort_by_time()."""

    def test_sort_by_time_returns_chronological_order(self):
        """Verify sort_by_time returns tasks ordered earliest to latest by scheduled_start_minute."""
        # Arrange: three tasks provided out of chronological order
        task_evening = CareTask(
            task_type="walk", name="Evening Walk",
            duration_minutes=30, priority=3, frequency="daily",
            scheduled_start_minute=1020,  # 17:00
        )
        task_lunch = CareTask(
            task_type="feed", name="Lunch",
            duration_minutes=10, priority=5, frequency="daily",
            scheduled_start_minute=720,  # 12:00
        )
        task_morning = CareTask(
            task_type="walk", name="Morning Walk",
            duration_minutes=30, priority=4, frequency="daily",
            scheduled_start_minute=420,  # 07:00
        )
        unsorted = [("17:00", task_evening), ("12:00", task_lunch), ("07:00", task_morning)]

        # Act
        result = Scheduler.sort_by_time(unsorted)

        # Assert: tasks are in chronological order
        names = [task.name for _, task in result]
        assert names == ["Morning Walk", "Lunch", "Evening Walk"]

    def test_sort_by_time_falls_back_to_time_string(self):
        """Verify sort_by_time parses the time string when scheduled_start_minute is None."""
        # Arrange: tasks without scheduled_start_minute set
        task_early = CareTask(
            task_type="feed", name="Breakfast",
            duration_minutes=10, priority=5, frequency="daily",
            scheduled_start_minute=None,
        )
        task_late = CareTask(
            task_type="walk", name="Evening Walk",
            duration_minutes=30, priority=3, frequency="daily",
            scheduled_start_minute=None,
        )
        unsorted = [("18:00", task_late), ("07:30", task_early)]

        # Act
        result = Scheduler.sort_by_time(unsorted)

        # Assert: earlier time string comes first
        assert result[0][1].name == "Breakfast"
        assert result[1][1].name == "Evening Walk"

    def test_sort_by_time_midnight_task_sorts_first(self):
        """Verify a task at 00:00 (minute 0) sorts before all daytime tasks."""
        # Arrange
        midnight_task = CareTask(
            task_type="medication", name="Midnight Meds",
            duration_minutes=5, priority=5, frequency="daily",
            scheduled_start_minute=0,  # 00:00
        )
        morning_task = CareTask(
            task_type="feed", name="Breakfast",
            duration_minutes=10, priority=5, frequency="daily",
            scheduled_start_minute=480,  # 08:00
        )
        unsorted = [("08:00", morning_task), ("00:00", midnight_task)]

        # Act
        result = Scheduler.sort_by_time(unsorted)

        # Assert: midnight task is first
        assert result[0][1].name == "Midnight Meds"
        assert result[1][1].name == "Breakfast"


class TestRecurrence:
    """Tests for recurring task logic: mark_complete, next_due_date, create_next_occurrence."""

    def test_daily_task_sets_next_due_date_to_tomorrow(self):
        """mark_complete on a daily task sets next_due_date to on_date + 1 day."""
        # Arrange
        task = CareTask(
            task_type="walk", name="Morning Walk",
            duration_minutes=30, priority=4, frequency="daily",
        )
        today = date(2026, 2, 18)

        # Act
        task.mark_complete(on_date=today)

        # Assert
        assert task.is_completed is True
        assert task.next_due_date == date(2026, 2, 19)

    def test_weekly_task_sets_next_due_date_to_next_week(self):
        """mark_complete on a weekly task sets next_due_date to on_date + 7 days."""
        # Arrange
        task = CareTask(
            task_type="grooming", name="Brush Coat",
            duration_minutes=20, priority=3, frequency="weekly",
        )
        today = date(2026, 2, 18)

        # Act
        task.mark_complete(on_date=today)

        # Assert
        assert task.next_due_date == date(2026, 2, 25)

    def test_create_next_occurrence_resets_all_fields(self):
        """create_next_occurrence returns a fresh copy with completion state cleared."""
        # Arrange: complete a task so it has next_due_date
        task = CareTask(
            task_type="walk", name="Morning Walk",
            duration_minutes=30, priority=4, frequency="daily",
            scheduled_start_minute=420,
        )
        task.mark_complete(on_date=date(2026, 2, 18))

        # Act
        next_task = Scheduler.create_next_occurrence(task)

        # Assert: copy is reset and ready for scheduling
        assert next_task is not None
        assert next_task.is_completed is False
        assert next_task.scheduled_start_minute is None
        assert next_task.next_due_date is None
        # Original task must be unchanged (create_next_occurrence uses replace())
        assert task.is_completed is True
        assert task.next_due_date == date(2026, 2, 19)

    def test_create_next_occurrence_returns_none_if_never_completed(self):
        """create_next_occurrence returns None when the task has no next_due_date."""
        # Arrange: task was never marked complete
        task = CareTask(
            task_type="walk", name="Morning Walk",
            duration_minutes=30, priority=4, frequency="daily",
        )

        # Act
        result = Scheduler.create_next_occurrence(task)

        # Assert
        assert result is None

    def test_completed_task_excluded_when_not_yet_due(self):
        """Scheduler skips a task whose next_due_date is strictly after the target date."""
        # Arrange: complete the task today so next_due_date = tomorrow
        task = CareTask(
            task_type="feed", name="Breakfast",
            duration_minutes=10, priority=5, frequency="daily",
        )
        today = date(2026, 2, 18)
        task.mark_complete(on_date=today)  # next_due_date = 2026-02-19

        pet = Pet(name="Buddy", species="dog", breed="Beagle", age=3, weight=20.0)
        pet.add_care_task(task)
        owner = Owner(name="Alice", available_time_slots=["07:00-09:00"])
        owner.add_pet(pet)
        scheduler = Scheduler(owner)

        # Act: schedule for today — task is already done for today
        plan = scheduler.generate_daily_plan(today)

        # Assert: task appears in neither list (filtered out entirely)
        all_names = (
            [t.name for _, t in plan.scheduled_tasks]
            + [t.name for t in plan.unscheduled_tasks]
        )
        assert "Breakfast" not in all_names

    def test_completed_task_included_when_due_today(self):
        """Scheduler includes a task whose next_due_date equals the target date."""
        # Arrange: complete the task yesterday so next_due_date = today
        task = CareTask(
            task_type="feed", name="Breakfast",
            duration_minutes=10, priority=5, frequency="daily",
        )
        yesterday = date(2026, 2, 17)
        task.mark_complete(on_date=yesterday)  # next_due_date = 2026-02-18

        pet = Pet(name="Buddy", species="dog", breed="Beagle", age=3, weight=20.0)
        pet.add_care_task(task)
        owner = Owner(name="Alice", available_time_slots=["07:00-09:00"])
        owner.add_pet(pet)
        scheduler = Scheduler(owner)

        # Act: schedule for today — filter is next_due_date > today, so today == today passes
        plan = scheduler.generate_daily_plan(date(2026, 2, 18))

        # Assert: task is scheduled (it fits in the 07:00-09:00 slot)
        scheduled_names = [t.name for _, t in plan.scheduled_tasks]
        assert "Breakfast" in scheduled_names


class TestConflictDetection:
    """Tests for conflict detection via DailyPlan.add_task and Scheduler.detect_conflicts."""

    def test_detect_conflicts_flags_overlapping_tasks(self):
        """detect_conflicts returns a ConflictReport when two tasks overlap in time."""
        # Arrange: task_b starts before task_a finishes
        task_a = CareTask(
            task_type="walk", name="Morning Walk",
            duration_minutes=30, priority=4, frequency="daily",
            pet_name="Buddy", scheduled_start_minute=420,  # 07:00–07:30
        )
        task_b = CareTask(
            task_type="feed", name="Breakfast",
            duration_minutes=20, priority=5, frequency="daily",
            pet_name="Buddy", scheduled_start_minute=430,  # 07:10–07:30 — overlaps
        )
        plan = DailyPlan(date=date(2026, 2, 18))
        plan.scheduled_tasks = [("07:00", task_a), ("07:10", task_b)]
        scheduler = Scheduler(Owner(name="Alice"))

        # Act
        reports = scheduler.detect_conflicts(plan)

        # Assert: one conflict reported between the two tasks
        assert len(reports) == 1
        assert reports[0].task_a is task_a
        assert reports[0].task_b is task_b

    def test_detect_conflicts_no_report_for_adjacent_tasks(self):
        """Tasks that touch (A ends exactly when B starts) do not count as a conflict."""
        # Arrange: task_b starts at the exact minute task_a ends
        task_a = CareTask(
            task_type="walk", name="Morning Walk",
            duration_minutes=30, priority=4, frequency="daily",
            pet_name="Buddy", scheduled_start_minute=420,  # 07:00–07:30
        )
        task_b = CareTask(
            task_type="feed", name="Breakfast",
            duration_minutes=10, priority=5, frequency="daily",
            pet_name="Buddy", scheduled_start_minute=450,  # 07:30–07:40 — touching, not overlapping
        )
        plan = DailyPlan(date=date(2026, 2, 18))
        plan.scheduled_tasks = [("07:00", task_a), ("07:30", task_b)]
        scheduler = Scheduler(Owner(name="Alice"))

        # Act
        reports = scheduler.detect_conflicts(plan)

        # Assert: no conflict
        assert len(reports) == 0

    def test_detect_conflicts_classifies_same_pet_overlap(self):
        """ConflictReport.same_pet is True when both tasks belong to the same pet."""
        # Arrange
        task_a = CareTask(
            task_type="walk", name="Walk",
            duration_minutes=30, priority=4, frequency="daily",
            pet_name="Buddy", scheduled_start_minute=420,
        )
        task_b = CareTask(
            task_type="feed", name="Feed",
            duration_minutes=30, priority=5, frequency="daily",
            pet_name="Buddy", scheduled_start_minute=430,  # overlaps
        )
        plan = DailyPlan(date=date(2026, 2, 18))
        plan.scheduled_tasks = [("07:00", task_a), ("07:10", task_b)]

        # Act
        reports = Scheduler(Owner(name="Alice")).detect_conflicts(plan)

        # Assert
        assert len(reports) == 1
        assert reports[0].same_pet is True

    def test_detect_conflicts_classifies_cross_pet_overlap(self):
        """ConflictReport.same_pet is False when tasks belong to different pets."""
        # Arrange
        task_a = CareTask(
            task_type="walk", name="Walk Buddy",
            duration_minutes=30, priority=4, frequency="daily",
            pet_name="Buddy", scheduled_start_minute=420,
        )
        task_b = CareTask(
            task_type="feed", name="Feed Mittens",
            duration_minutes=30, priority=5, frequency="daily",
            pet_name="Mittens", scheduled_start_minute=430,  # overlaps
        )
        plan = DailyPlan(date=date(2026, 2, 18))
        plan.scheduled_tasks = [("07:00", task_a), ("07:10", task_b)]

        # Act
        reports = Scheduler(Owner(name="Alice")).detect_conflicts(plan)

        # Assert
        assert len(reports) == 1
        assert reports[0].same_pet is False

    def test_add_task_rejects_overlapping_time_slot(self):
        """DailyPlan.add_task returns False and leaves the plan unchanged when tasks overlap."""
        # Arrange
        plan = DailyPlan(date=date(2026, 2, 18))
        task_a = CareTask(
            task_type="walk", name="Morning Walk",
            duration_minutes=30, priority=4, frequency="daily",
        )
        task_b = CareTask(
            task_type="feed", name="Breakfast",
            duration_minutes=20, priority=5, frequency="daily",
        )
        plan.add_task(task_a, "07:00")  # 07:00–07:30

        # Act: add a task that overlaps (07:15–07:35)
        result = plan.add_task(task_b, "07:15")

        # Assert: rejected, plan unchanged, task_b left clean
        assert result is False
        assert len(plan.scheduled_tasks) == 1
        assert task_b.scheduled_start_minute is None

    def test_detect_conflicts_empty_plan_returns_no_reports(self):
        """detect_conflicts on an empty plan returns an empty list without error."""
        # Arrange
        plan = DailyPlan(date=date(2026, 2, 18))
        scheduler = Scheduler(Owner(name="Alice"))

        # Act
        reports = scheduler.detect_conflicts(plan)

        # Assert
        assert reports == []


# Run tests with pytest
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
