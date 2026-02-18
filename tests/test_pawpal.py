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

        # Assert: Plan should be created
        assert plan is not None
        assert plan.date == date.today()
        assert len(plan.unscheduled_tasks) == 1  # Task should be in unscheduled (no algorithm yet)


# Run tests with pytest
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
