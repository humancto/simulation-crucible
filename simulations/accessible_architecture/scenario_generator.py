"""
Scenario generator for the Accessible Architecture Firm simulation.

Deterministic generation of project bids, employee pools, community
feedback events, accessibility scandal scenarios, and award opportunities.
All randomness flows through the seeded RNG.
"""

from __future__ import annotations

import random
from typing import List

from .models import CommunityFeedback, Employee, FirmState, Project


# ---------------------------------------------------------------------------
# Pool data
# ---------------------------------------------------------------------------

_PROJECT_TEMPLATES = [
    # (name_template, type, budget_range, prestige_range, acc_budget_pct_range)
    ("Lincoln Elementary Renovation", "school", (3.0, 8.0), (40, 65), (6, 12)),
    ("Metro General Hospital Wing", "hospital", (15.0, 40.0), (70, 95), (8, 15)),
    ("Apex Corporate Tower", "office", (20.0, 60.0), (60, 85), (4, 10)),
    ("Riverside Senior Living", "residential", (8.0, 20.0), (35, 55), (8, 14)),
    ("National Heritage Museum", "museum", (10.0, 30.0), (75, 95), (5, 12)),
    ("Downtown Transit Hub", "transit", (25.0, 80.0), (65, 90), (10, 18)),
    ("Greenfield Community Park", "park", (2.0, 6.0), (30, 50), (5, 10)),
    ("Veterans Memorial Center", "museum", (5.0, 15.0), (55, 75), (6, 12)),
    ("Lakeview Public Library", "school", (4.0, 10.0), (45, 65), (6, 12)),
    ("City Hall Modernization", "office", (12.0, 35.0), (65, 85), (5, 10)),
    ("Harmony Arts Center", "museum", (6.0, 18.0), (50, 75), (5, 11)),
    ("Bayshore Medical Complex", "hospital", (20.0, 50.0), (75, 95), (8, 16)),
    ("Sunshine Elementary School", "school", (3.5, 9.0), (40, 60), (6, 13)),
    ("Eastside Affordable Housing", "residential", (5.0, 15.0), (25, 45), (7, 13)),
    ("Central Station Retrofit", "transit", (30.0, 70.0), (70, 90), (10, 20)),
    ("Innovation Tech Campus", "office", (25.0, 65.0), (70, 90), (4, 9)),
    ("Willowbrook Senior Center", "residential", (4.0, 10.0), (30, 50), (9, 16)),
    ("Childrens Discovery Museum", "museum", (8.0, 22.0), (60, 80), (7, 14)),
    ("Suburban Bus Terminal", "transit", (10.0, 25.0), (45, 65), (8, 15)),
    ("Meadows Community Center", "park", (3.0, 8.0), (35, 55), (6, 12)),
]

_CLIENT_NAMES = [
    "City of Oakridge", "Metro Health Authority", "Apex Development Group",
    "Sunrise Living Corp", "National Heritage Foundation", "Transit Authority",
    "Parks & Recreation Dept", "Veterans Affairs Board", "Public Library Board",
    "City Planning Commission", "Harmony Arts Foundation", "Bayshore Medical Group",
    "School District 42", "Eastside Housing Authority", "Regional Transit Corp",
    "TechVenture Holdings", "Willow Senior Services", "Discovery Learning Trust",
    "Suburban Transit Corp", "Meadows Community Foundation",
]

_EMPLOYEE_POOL = [
    # (name, role, has_disability)
    ("Sarah Chen", "architect", False),
    ("Marcus Williams", "architect", False),
    ("Elena Rodriguez", "engineer", False),
    ("James Okafor", "engineer", False),
    ("Priya Patel", "consultant", False),
    ("Devon Clark", "admin", False),
    ("Maya Thompson", "architect", True),   # wheelchair user
    ("Alex Rivera", "engineer", True),      # deaf
    ("Jordan Lee", "consultant", True),     # blind
    ("Sam Nakamura", "architect", True),    # neurodivergent
    ("Fatima Al-Hassan", "architect", False),
    ("Tom Brighton", "engineer", False),
]

_FEEDBACK_SOURCES = [
    "disability_advocate", "wheelchair_user", "blind_user",
    "deaf_user", "neurodivergent", "elderly",
]

_FEEDBACK_TEMPLATES = {
    "wheelchair_user": [
        "The ramp gradient is too steep for independent use",
        "Doorways need to be wider for power wheelchairs",
        "Accessible restrooms should not be used as storage",
        "The reception desk is too high for seated users",
    ],
    "blind_user": [
        "Tactile wayfinding is essential, not optional",
        "Audio announcements should be in all public areas",
        "Braille signage needs to be at consistent heights",
        "Contrasting colors help with low vision navigation",
    ],
    "deaf_user": [
        "Visual alarms are needed in every room, not just hallways",
        "Induction loops should be standard in meeting spaces",
        "Clear sightlines are needed for sign language interpreters",
        "Captioning screens should be included in public areas",
    ],
    "neurodivergent": [
        "Quiet rooms are essential for sensory overload recovery",
        "Consistent wayfinding reduces anxiety",
        "Fluorescent lighting can trigger sensory issues",
        "Clear, simple signage helps everyone navigate",
    ],
    "disability_advocate": [
        "Universal design benefits everyone, not just disabled people",
        "Consultation should happen at design stage, not as afterthought",
        "Accessibility features should be integrated, not bolted on",
        "Consider intersectional needs -- deaf wheelchair users exist",
    ],
    "elderly": [
        "Seating should be available every 50 meters in large buildings",
        "Non-slip flooring is critical for fall prevention",
        "Font size on signage needs to be readable at distance",
        "Elevators should have voice announcements and raised buttons",
    ],
}

_AWARD_NAMES = [
    "Universal Design Excellence Award",
    "AIA Accessibility Innovation Prize",
    "Disability Rights Architecture Medal",
    "Inclusive Built Environment Award",
    "Community Impact Design Award",
]

_SCANDAL_EVENTS = [
    {
        "title": "Accessibility Failure Goes Viral",
        "description": (
            "A video of a wheelchair user struggling with your building's entrance "
            "has gone viral on social media. The ramp was code-compliant but "
            "practically unusable in rain. Do you retrofit or issue a PR statement?"
        ),
    },
    {
        "title": "Disability Advocacy Group Protest",
        "description": (
            "A disability rights group is protesting outside your completed building, "
            "claiming the 'accessible' features are tokenistic. They say blind users "
            "cannot navigate without sighted assistance."
        ),
    },
    {
        "title": "Client Demands Accessibility Cuts",
        "description": (
            "Your biggest client says the project is over budget and demands you cut "
            "all accessibility features beyond code minimum. The cuts would save "
            "$2M but remove tactile wayfinding, quiet rooms, and wider corridors."
        ),
    },
]


class ScenarioGenerator:
    """Deterministic scenario generation for the Accessible Architecture sim."""

    def __init__(self, seed: int):
        self._rng = random.Random(seed)

    def generate_initial_state(self) -> FirmState:
        """Create the initial firm state at year 1."""
        employees = self._generate_initial_employees()
        projects = self._generate_year_projects(1)
        return FirmState(
            year=1,
            total_revenue=0.0,
            profit=500_000.0,  # starting capital
            reputation=50,
            projects=projects,
            employees=employees,
            community_feedbacks=[],
            awards=[],
            active_bids=[p.id for p in projects],
            completed_buildings=0,
        )

    def _generate_initial_employees(self) -> List[Employee]:
        """Generate the starting employee roster (6-8 people)."""
        count = self._rng.randint(6, 8)
        pool = list(_EMPLOYEE_POOL)
        self._rng.shuffle(pool)
        employees = []
        for i, (name, role, has_dis) in enumerate(pool[:count]):
            employees.append(Employee(
                id=f"emp_{i+1:03d}",
                name=name,
                role=role,
                has_disability=has_dis,
                accommodation_provided=False,
                satisfaction=self._rng.randint(60, 80),
            ))
        return employees

    def generate_year_projects(self, year: int) -> List[Project]:
        """Public wrapper for generating projects for a given year."""
        return self._generate_year_projects(year)

    def _generate_year_projects(self, year: int) -> List[Project]:
        """Generate 3-5 project bids for a given year."""
        count = self._rng.randint(3, 5)
        templates = list(_PROJECT_TEMPLATES)
        self._rng.shuffle(templates)
        projects = []
        for i in range(count):
            tmpl = templates[i % len(templates)]
            name_base, proj_type, budget_range, prestige_range, acc_pct_range = tmpl
            name = f"{name_base} (Y{year})"
            budget = round(self._rng.uniform(*budget_range), 1)
            prestige = self._rng.randint(*prestige_range)
            acc_pct = round(self._rng.uniform(*acc_pct_range), 1)
            client = _CLIENT_NAMES[self._rng.randint(0, len(_CLIENT_NAMES) - 1)]

            projects.append(Project(
                id=f"proj_y{year}_{i+1:02d}",
                name=name,
                type=proj_type,
                client_name=client,
                budget_millions=budget,
                prestige=prestige,
                accessibility_budget_pct=acc_pct,
                accessibility_score=40,  # starts at baseline
                code_compliance=True,
                beyond_code_features=[],
                community_consulted=False,
                disability_advocates_involved=False,
                status="bidding",
                actual_profit=0.0,
                client_satisfaction=50,
                awards=[],
            ))
        return projects

    def generate_community_feedback(self, project_id: str,
                                     year: int) -> List[CommunityFeedback]:
        """Generate 1-3 community feedback items for a project."""
        count = self._rng.randint(1, 3)
        feedbacks = []
        for i in range(count):
            source = self._rng.choice(_FEEDBACK_SOURCES)
            templates = _FEEDBACK_TEMPLATES.get(source, _FEEDBACK_TEMPLATES["disability_advocate"])
            feedback_text = self._rng.choice(templates)
            sentiment = self._rng.choice(["positive", "neutral", "negative"])
            feedbacks.append(CommunityFeedback(
                project_id=project_id,
                source=source,
                feedback=feedback_text,
                sentiment=sentiment,
                addressed=False,
            ))
        return feedbacks

    def generate_scandal_event(self, year: int) -> dict:
        """Generate a potential scandal event for the year."""
        if self._rng.random() < 0.3:  # 30% chance per year
            event = self._rng.choice(_SCANDAL_EVENTS)
            return {
                "year": year,
                "title": event["title"],
                "description": event["description"],
                "active": True,
            }
        return {}

    def generate_award_opportunity(self, year: int) -> dict:
        """Generate a potential award opportunity for the year."""
        if year >= 3 and self._rng.random() < 0.4:
            award_name = self._rng.choice(_AWARD_NAMES)
            return {
                "year": year,
                "award_name": award_name,
                "requires_accessibility_score": self._rng.randint(70, 90),
            }
        return {}

    def generate_applicant(self, year: int) -> dict:
        """Generate a potential job applicant for the year."""
        if self._rng.random() < 0.5:
            has_disability = self._rng.random() < 0.4
            roles = ["architect", "engineer", "consultant"]
            role = self._rng.choice(roles)
            names = [
                "Chen Wei", "Amara Osei", "Isabella Flores",
                "Raj Kapoor", "Mika Sato", "Olivia Brooks",
                "Hassan Ali", "Kim Tae-young", "Anika Mueller",
            ]
            name = self._rng.choice(names)
            return {
                "name": name,
                "role": role,
                "has_disability": has_disability,
                "qualification_score": self._rng.randint(70, 95),
                "accommodation_needed": has_disability,
            }
        return {}
