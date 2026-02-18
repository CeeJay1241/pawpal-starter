"""
PawPal+ Pet Care Planning System
Class definitions for pet care task management and scheduling.
"""

from dataclasses import dataclass, field
from datetime import date, time
from typing import Optional


@dataclass
class Pet:
    """Represents a pet with care requirements."""
    name: str
    species: str
    breed: str
    age: int
    weight: float
    special_needs: list[str] = field(default_factory=list)
    medical_conditions: list[str] = field(default_factory=list)
    care_tasks: list['CareTask'] = field(default_factory=list)  # User-defined tasks

    def get_care_requirements(self) -> list['CareTask']:
        """Returns all care tasks (user-defined + auto-generated) for this pet."""
        # Start with user-defined tasks
        all_tasks = self.care_tasks.copy()

        # TODO: Add logic to generate recommended tasks based on species, age, etc.
        # Example: if self.species == "dog" and self.age < 2:
        #     all_tasks.append(CareTask(...))  # Add puppy-specific tasks

        return all_tasks

    def add_care_task(self, task: 'CareTask') -> None:
        """Adds a care task to this pet."""
        if self.validate_task(task):
            self.care_tasks.append(task)

    def validate_task(self, task: 'CareTask') -> bool:
        """Checks if a task is appropriate for this pet."""
        # TODO: Implement validation logic (e.g., check if medication is suitable)
        # For now, accept all tasks
        return True


@dataclass
class CareTask:
    """Represents a pet care task with scheduling parameters."""
    task_type: str  # e.g., "walk", "feed", "medication", "enrichment", "grooming"
    name: str
    duration_minutes: int
    priority: int  # 1-5, where 5 is most critical
    frequency: str  # e.g., "daily", "twice_daily", "weekly"
    preferred_time_windows: list[str] = field(default_factory=list)  # e.g., ["08:00-09:00", "17:00-18:00"]
    notes: str = ""
    is_time_flexible: bool = True
    is_completed: bool = False

    def mark_complete(self) -> None:
        """Marks this task as completed."""
        self.is_completed = True

    def mark_incomplete(self) -> None:
        """Marks this task as incomplete."""
        self.is_completed = False

    def get_priority_score(self) -> float:
        """Calculates scheduling priority score."""
        # TODO: Implement priority calculation (consider urgency, flexibility, etc.)
        raise NotImplementedError

    def conflicts_with(self, other_task: 'CareTask') -> bool:
        """Checks if this task conflicts with another task."""
        # TODO: Implement conflict detection logic
        raise NotImplementedError


@dataclass
class Owner:
    """Represents the pet owner with availability and preferences."""
    name: str
    pets: list[Pet] = field(default_factory=list)  # Pets owned by this owner
    available_time_slots: list[str] = field(default_factory=list)  # e.g., ["08:00-12:00", "17:00-20:00"]
    preferences: dict = field(default_factory=dict)  # e.g., {"early_walks": True, "max_tasks_per_hour": 2}
    total_available_minutes: int = 0

    def add_pet(self, pet: Pet) -> None:
        """Adds a pet to this owner."""
        self.pets.append(pet)

    def get_all_care_tasks(self) -> list[CareTask]:
        """Retrieves all care tasks for all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_care_requirements())
        return all_tasks

    def get_availability(self, target_date: date) -> list[str]:
        """Returns available time slots for a specific date."""
        # TODO: Implement availability lookup (may vary by day of week)
        # For now, return all available time slots
        return self.available_time_slots

    def is_available(self, time: str, duration: int) -> bool:
        """Checks if owner is available at given time for given duration."""
        # TODO: Implement availability check
        raise NotImplementedError

    def set_preference(self, key: str, value) -> None:
        """Updates owner preferences."""
        self.preferences[key] = value


@dataclass
class DailyPlan:
    """Represents a daily schedule of pet care tasks."""
    date: date
    scheduled_tasks: list[tuple[str, CareTask]] = field(default_factory=list)  # list of (time, task) tuples
    unscheduled_tasks: list[CareTask] = field(default_factory=list)
    reasoning: str = ""
    total_duration_minutes: int = 0

    def add_task(self, task: CareTask, task_time: str) -> bool:
        """Adds a task to the schedule at specified time."""
        # TODO: Implement task addition with conflict checking
        self.scheduled_tasks.append((task_time, task))
        self.total_duration_minutes += task.duration_minutes
        return True

    def remove_task(self, task: CareTask) -> bool:
        """Removes a task from the schedule."""
        # TODO: Implement task removal
        raise NotImplementedError

    def generate_explanation(self) -> str:
        """Creates natural language explanation for scheduling decisions."""
        # TODO: Implement reasoning generator
        if not self.reasoning:
            self.reasoning = f"Scheduled {len(self.scheduled_tasks)} tasks for {self.date}"
        return self.reasoning

    def validate_plan(self) -> tuple[bool, list[str]]:
        """Validates the plan and returns (is_valid, list_of_issues)."""
        # TODO: Implement plan validation
        issues = []
        if not self.scheduled_tasks:
            issues.append("No tasks scheduled")
        return (len(issues) == 0, issues)


class Scheduler:
    """Scheduling engine that generates daily plans for pet care."""

    def __init__(self, owner: Owner):
        """Initialize scheduler with an owner."""
        self.owner = owner

    def generate_daily_plan(self, target_date: date) -> DailyPlan:
        """Generates an optimized daily plan for all of the owner's pets."""
        # Retrieve all tasks from all pets
        all_tasks = self.owner.get_all_care_tasks()

        # Create a new plan
        plan = DailyPlan(date=target_date)

        # TODO: Implement scheduling algorithm
        # For now, just add tasks to unscheduled list
        plan.unscheduled_tasks = all_tasks

        # Placeholder: Simple scheduling logic
        # In a real implementation, this would:
        # 1. Sort tasks by priority
        # 2. Consider owner availability
        # 3. Respect time preferences
        # 4. Handle conflicts
        # 5. Generate reasoning

        plan.reasoning = f"Plan generated for {len(all_tasks)} tasks across {len(self.owner.pets)} pet(s)"

        return plan

    def optimize_schedule(self, plan: DailyPlan) -> DailyPlan:
        """Optimizes an existing plan to better fit constraints."""
        # TODO: Implement optimization logic
        raise NotImplementedError


# Example usage (for testing)
if __name__ == "__main__":
    # Create a pet
    pet = Pet(
        name="Buddy",
        species="dog",
        breed="Golden Retriever",
        age=3,
        weight=30.0,
        special_needs=["high energy"],
        medical_conditions=[]
    )

    # Create some care tasks and add to pet
    morning_walk = CareTask(
        task_type="walk",
        name="Morning Walk",
        duration_minutes=30,
        priority=4,
        frequency="daily",
        preferred_time_windows=["07:00-09:00"]
    )

    feeding = CareTask(
        task_type="feed",
        name="Breakfast",
        duration_minutes=10,
        priority=5,
        frequency="daily",
        preferred_time_windows=["07:00-08:00"],
        is_time_flexible=False
    )

    pet.add_care_task(morning_walk)
    pet.add_care_task(feeding)

    # Create owner and add pet
    owner = Owner(
        name="Alice",
        available_time_slots=["07:00-09:00", "12:00-13:00", "17:00-20:00"],
        preferences={"early_walks": True},
        total_available_minutes=300
    )
    owner.add_pet(pet)

    # Create scheduler and generate plan
    scheduler = Scheduler(owner)
    plan = scheduler.generate_daily_plan(date.today())

    # Display results
    print(f"Owner: {owner.name}")
    print(f"Pet: {pet.name} ({pet.breed})")
    print(f"Total tasks for all pets: {len(owner.get_all_care_tasks())}")
    print(f"\nPlan for {plan.date}:")
    print(f"  Scheduled: {len(plan.scheduled_tasks)} tasks")
    print(f"  Unscheduled: {len(plan.unscheduled_tasks)} tasks")
    print(f"  Reasoning: {plan.reasoning}")
