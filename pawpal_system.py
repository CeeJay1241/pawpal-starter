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

    def get_care_requirements(self) -> list['CareTask']:
        """Returns recommended care tasks based on pet characteristics."""
        # TODO: Implement logic to generate care tasks based on species, age, etc.
        raise NotImplementedError

    def validate_task(self, task: 'CareTask') -> bool:
        """Checks if a task is appropriate for this pet."""
        # TODO: Implement validation logic
        raise NotImplementedError


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
    available_time_slots: list[str] = field(default_factory=list)  # e.g., ["08:00-12:00", "17:00-20:00"]
    preferences: dict = field(default_factory=dict)  # e.g., {"early_walks": True, "max_tasks_per_hour": 2}
    total_available_minutes: int = 0

    def get_availability(self, target_date: date) -> list[str]:
        """Returns available time slots for a specific date."""
        # TODO: Implement availability lookup (may vary by day of week)
        raise NotImplementedError

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
        raise NotImplementedError

    def remove_task(self, task: CareTask) -> bool:
        """Removes a task from the schedule."""
        # TODO: Implement task removal
        raise NotImplementedError

    def generate_plan(self, pet: Pet, owner: Owner, tasks: list[CareTask]) -> None:
        """Generates an optimized daily plan based on constraints."""
        # TODO: Implement main scheduling algorithm
        raise NotImplementedError

    def generate_explanation(self) -> str:
        """Creates natural language explanation for scheduling decisions."""
        # TODO: Implement reasoning generator
        raise NotImplementedError

    def validate_plan(self) -> tuple[bool, list[str]]:
        """Validates the plan and returns (is_valid, list_of_issues)."""
        # TODO: Implement plan validation
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

    # Create owner
    owner = Owner(
        name="Alice",
        available_time_slots=["07:00-09:00", "12:00-13:00", "17:00-20:00"],
        preferences={"early_walks": True},
        total_available_minutes=300
    )

    # Create some care tasks
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

    # Create a daily plan
    plan = DailyPlan(date=date.today())

    print(f"Created pet: {pet.name}, {pet.breed}")
    print(f"Owner: {owner.name}")
    print(f"Tasks created: {morning_walk.name}, {feeding.name}")
    print(f"Plan date: {plan.date}")
