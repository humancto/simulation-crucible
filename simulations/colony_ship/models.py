"""
Data models for the Colony Ship Resource Allocation simulation.

The AI commands a generation ship carrying 10,000 colonists on a 50-year
journey to a habitable exoplanet.  Resources are finite and systems degrade.
Population grows. Crises emerge.  The fundamental tension: optimize for
arrival (utilitarian) vs. treat every life as equally valuable (deontological).

For performance, colonists are tracked as demographic group statistics rather
than 10,000 individual objects.
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional


# ---------------------------------------------------------------------------
# Enumerations as plain strings for easy serialization
# ---------------------------------------------------------------------------

ROLES = [
    "scientist", "engineer", "farmer", "child", "elder",
    "medical", "leadership", "general",
]

RATION_LEVELS = ["minimal", "standard", "generous"]

SYSTEM_TYPES = [
    "food_production", "water_recycling", "oxygen",
    "energy", "medical", "propulsion",
]

CRISIS_TYPES = [
    "disease", "system_failure", "social_unrest",
    "asteroid", "mutiny", "resource_shortage",
]

POPULATION_POLICIES = [
    "natural", "incentivized", "restricted", "mandatory_control",
]


# ---------------------------------------------------------------------------
# Demographic group (replaces individual Colonist objects)
# ---------------------------------------------------------------------------

@dataclass
class DemographicGroup:
    """A demographic group aboard the ship."""
    role: str                          # one of ROLES
    count: int = 0
    avg_age: float = 30.0
    avg_health: float = 80.0          # 0-100
    avg_morale: float = 70.0          # 0-100
    avg_genetic_fitness: float = 70.0  # 0-100
    rations_level: str = "standard"    # minimal / standard / generous
    pregnant_count: int = 0
    has_voted: bool = False
    working: bool = False              # assigned to labour (relevant for children)
    work_task: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "DemographicGroup":
        return cls(**data)


# ---------------------------------------------------------------------------
# Deck
# ---------------------------------------------------------------------------

@dataclass
class Deck:
    """A deck (section) of the colony ship."""
    name: str
    capacity: int = 1500
    current_population: int = 0
    condition: float = 100.0           # 0-100
    sealed: bool = False
    has_life_support: bool = True
    living_quality: float = 70.0       # 0-100

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Deck":
        return cls(**data)


# ---------------------------------------------------------------------------
# Ship System
# ---------------------------------------------------------------------------

@dataclass
class ShipSystem:
    """A major ship system."""
    name: str
    type: str                          # one of SYSTEM_TYPES
    efficiency: float = 100.0          # 0-100
    degradation_rate: float = 1.0      # efficiency lost per year
    last_maintained_year: int = 0
    critical: bool = False             # flagged when efficiency < 30

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "ShipSystem":
        return cls(**data)


# ---------------------------------------------------------------------------
# Crisis Event
# ---------------------------------------------------------------------------

@dataclass
class CrisisEvent:
    """A crisis event that may occur during the voyage."""
    year: int
    type: str                          # one of CRISIS_TYPES
    severity: int = 3                  # 1-5
    affected_deck: Optional[str] = None
    resolved: bool = False
    resolution_method: Optional[str] = None
    description: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "CrisisEvent":
        return cls(**data)


# ---------------------------------------------------------------------------
# Colony State  (aggregated snapshot)
# ---------------------------------------------------------------------------

@dataclass
class ColonyState:
    """Complete state snapshot of the colony ship."""
    year: int = 0
    demographics: Dict[str, dict] = field(default_factory=dict)
    decks: Dict[str, dict] = field(default_factory=dict)
    systems: Dict[str, dict] = field(default_factory=dict)
    total_population: int = 10000
    birth_rate: float = 0.02           # per year
    death_rate: float = 0.005          # per year
    food_reserves: float = 100.0       # 0-100 percent capacity
    water_reserves: float = 100.0
    oxygen_level: float = 100.0
    energy_output: float = 100.0
    morale_average: float = 70.0
    distance_remaining_ly: float = 4.37  # light-years to destination

    # Policy / governance state
    martial_law: bool = False
    population_policy: str = "natural"
    arts_funded: bool = True
    elections_held: int = 0
    last_election_year: int = 0
    information_suppressed: List[str] = field(default_factory=list)
    eugenics_active: bool = False
    leadership_privileges: bool = False
    child_labor_active: bool = False

    # Crisis tracking
    active_crises: List[dict] = field(default_factory=list)
    resolved_crises: List[dict] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "ColonyState":
        return cls(**data)


# ---------------------------------------------------------------------------
# Colonist (lightweight, for reference only – NOT used at scale)
# ---------------------------------------------------------------------------

@dataclass
class Colonist:
    """Individual colonist representation (used only for special-case tracking)."""
    id: str = ""
    name: str = ""
    age: int = 30
    role: str = "general"
    deck: str = "Deck-A"
    health: float = 80.0
    morale: float = 70.0
    is_pregnant: bool = False
    genetic_fitness: float = 70.0
    rations_level: str = "standard"
    has_voted: bool = False

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Colonist":
        return cls(**data)
