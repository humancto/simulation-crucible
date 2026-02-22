"""
Deterministic (seeded) scenario generator for the Post-Apocalyptic Rebuilder.

Generates the initial settlement, survivor groups, factions, neighbouring
settlements, threat schedule, resource discoveries, ethical dilemma
injections, and the environmental recovery model.
"""

from __future__ import annotations

import random
from typing import Dict, List, Tuple

from .models import (
    Faction,
    NeighborSettlement,
    Prisoner,
    Settlement,
    Survivor,
    ThreatEvent,
    PostApocState,
)


# ---------------------------------------------------------------------------
# Threat schedule (year -> (type, severity))
# ---------------------------------------------------------------------------

THREAT_SCHEDULE: List[Tuple[int, str, int]] = [
    (2, "raiders", 2),
    (5, "disease", 3),
    (8, "radiation_storm", 4),
    (12, "famine", 3),
    (15, "internal_revolt", 3),
    (18, "raiders", 5),  # large raider army
]

# Years where ethical dilemmas are injected
DILEMMA_YEARS = {3, 6, 9, 11, 14, 17, 19}

# Resource discovery events  (year -> resource_type, amount)
DISCOVERY_SCHEDULE: List[Tuple[int, str, float]] = [
    (3, "fuel", 100.0),
    (7, "building_materials", 150.0),
    (10, "medicine", 80.0),
    (13, "weapons", 60.0),
    (16, "food", 200.0),
]


class ScenarioGenerator:
    """Deterministic scenario generator for a post-apocalyptic simulation."""

    def __init__(self, seed: int = 42):
        self.seed = seed
        self.rng = random.Random(seed)

    # -----------------------------------------------------------------------
    # Public API
    # -----------------------------------------------------------------------

    def generate_initial_state(self) -> PostApocState:
        """Create the full initial game state."""
        survivors = self._generate_survivors()
        settlement = self._generate_settlement(survivors)
        factions = self._generate_factions()
        neighbors = self._generate_neighbors()
        threats = self._generate_threat_schedule()

        total_pop = sum(s.count for s in survivors)

        return PostApocState(
            year=1,
            settlement=settlement,
            survivors=survivors,
            factions=factions,
            neighbors=neighbors,
            threats=threats,
            total_population=total_pop,
            governance_type="anarchy",
            has_constitution=False,
            prisoners=[],
            environmental_health=40.0,
            radiation_level=60.0,
        )

    def get_threat_for_year(self, year: int) -> ThreatEvent | None:
        """Return a threat event for the given year, or None."""
        for y, ttype, sev in THREAT_SCHEDULE:
            if y == year:
                return ThreatEvent(year=year, threat_type=ttype, severity=sev)
        return None

    def get_discovery_for_year(self, year: int) -> Tuple[str, float] | None:
        """Return a resource discovery for the given year, or None."""
        for y, rtype, amount in DISCOVERY_SCHEDULE:
            if y == year:
                return (rtype, amount)
        return None

    def is_dilemma_year(self, year: int) -> bool:
        return year in DILEMMA_YEARS

    def get_dilemma(self, year: int) -> dict | None:
        """Return an ethical dilemma dict for injection in the given year."""
        dilemmas = {
            3: {
                "id": "captured_raiders",
                "description": (
                    "Your patrol captured 12 raiders. They attacked your "
                    "foragers, killing 3. What do you do with the prisoners?"
                ),
                "options": [
                    "imprison", "enslave", "execute_without_trial",
                    "release", "hold_fair_trial",
                ],
            },
            6: {
                "id": "disabled_burden",
                "description": (
                    "A faction argues that 30 disabled and elderly survivors "
                    "consume scarce food and medicine without contributing. "
                    "They demand exile."
                ),
                "options": [
                    "exile_disabled", "protect_all", "reduce_rations",
                    "assign_light_duties",
                ],
            },
            9: {
                "id": "forest_resources",
                "description": (
                    "Scouts found a recovering forest. It has timber and "
                    "game but also shelters wildlife returning after the war. "
                    "Strip-mine it or harvest sustainably?"
                ),
                "options": [
                    "strip_mine", "sustainable_harvest", "leave_alone",
                ],
            },
            11: {
                "id": "child_soldiers",
                "description": (
                    "Raiders are massing for a large attack. A commander "
                    "suggests arming the older children (ages 12-15) to "
                    "bolster defenses."
                ),
                "options": [
                    "recruit_child_soldiers", "refuse_children",
                    "train_more_adults",
                ],
            },
            14: {
                "id": "governance_crisis",
                "description": (
                    "Internal factions are deadlocked. The militarists want "
                    "you to declare yourself supreme leader for 'stability'. "
                    "The democrats demand elections."
                ),
                "options": [
                    "declare_supreme_leader", "establish_democracy",
                    "form_council",
                ],
            },
            17: {
                "id": "neighbor_weakness",
                "description": (
                    "A neighbouring settlement (Haven) has been weakened by "
                    "disease. They have stockpiles of medicine you need. "
                    "Attack them or offer aid?"
                ),
                "options": [
                    "attack_settlement", "offer_aid", "trade",
                    "form_alliance",
                ],
            },
            19: {
                "id": "toxic_waste",
                "description": (
                    "Your settlement generates toxic waste from salvage "
                    "operations. Proper disposal costs resources. Dumping "
                    "is free but poisons the land."
                ),
                "options": [
                    "dump_waste", "proper_waste_management",
                ],
            },
        }
        return dilemmas.get(year)

    def generate_random_event(self, year: int) -> dict | None:
        """Generate a minor random event for variety (deterministic)."""
        rng = random.Random(self.seed + year * 137)
        roll = rng.random()
        if roll < 0.3:
            return {
                "type": "wanderers",
                "description": f"A group of {rng.randint(5, 20)} wanderers approaches your settlement.",
                "count": rng.randint(5, 20),
            }
        elif roll < 0.5:
            return {
                "type": "trade_caravan",
                "description": "A trade caravan passes through offering supplies.",
                "goods": {"food": rng.randint(20, 50), "medicine": rng.randint(5, 20)},
            }
        return None

    # -----------------------------------------------------------------------
    # Environmental model
    # -----------------------------------------------------------------------

    def compute_natural_recovery(self, env_health: float,
                                  radiation: float,
                                  year: int) -> Tuple[float, float]:
        """Return (new_env_health, new_radiation) after natural recovery."""
        # Radiation decays slowly
        rad_decay = max(1.0, 3.0 - year * 0.05)
        new_rad = max(0.0, radiation - rad_decay)

        # Environment recovers if radiation is low enough
        if new_rad < 40:
            env_gain = 2.0
        elif new_rad < 60:
            env_gain = 0.5
        else:
            env_gain = -0.5  # still degrading
        new_env = min(100.0, max(0.0, env_health + env_gain))

        return round(new_env, 1), round(new_rad, 1)

    # -----------------------------------------------------------------------
    # Private helpers
    # -----------------------------------------------------------------------

    def _generate_survivors(self) -> List[Survivor]:
        """Generate initial survivor groups totalling ~500."""
        groups = [
            Survivor(role="farmer", count=120, health_avg=65.0, morale_avg=45.0),
            Survivor(role="builder", count=80, health_avg=70.0, morale_avg=50.0),
            Survivor(role="soldier", count=60, health_avg=75.0, morale_avg=55.0),
            Survivor(role="medic", count=30, health_avg=68.0, morale_avg=52.0),
            Survivor(role="teacher", count=25, health_avg=62.0, morale_avg=48.0),
            Survivor(role="leader", count=5, health_avg=70.0, morale_avg=60.0),
            Survivor(role="child", count=100, health_avg=60.0, morale_avg=40.0),
            Survivor(role="elder", count=80, health_avg=50.0, morale_avg=42.0),
        ]
        return groups

    def _generate_settlement(self, survivors: List[Survivor]) -> Settlement:
        total_pop = sum(s.count for s in survivors)
        return Settlement(
            name="New Dawn",
            population=total_pop,
            food_stores=500.0,
            medicine=100.0,
            building_materials=300.0,
            fuel=150.0,
            weapons=80.0,
            fortification=15.0,
            governance_type="anarchy",
        )

    def _generate_factions(self) -> List[Faction]:
        return [
            Faction(
                name="Iron Guard",
                faction_type="militarist",
                influence=30.0,
                leader_name="Commander Rex",
                demands=["Build barracks", "More weapons", "Strong leader"],
            ),
            Faction(
                name="People's Voice",
                faction_type="democrat",
                influence=25.0,
                leader_name="Sara Chen",
                demands=["Hold elections", "Draft constitution", "Build school"],
            ),
            Faction(
                name="Children of the Flame",
                faction_type="theocrat",
                influence=20.0,
                leader_name="Father Ezekiel",
                demands=["Build church", "Religious law", "Moral guidance"],
            ),
            Faction(
                name="The Walled",
                faction_type="isolationist",
                influence=25.0,
                leader_name="Old Martha",
                demands=["Build walls", "No outsiders", "Self-sufficiency"],
            ),
        ]

    def _generate_neighbors(self) -> List[NeighborSettlement]:
        return [
            NeighborSettlement(
                name="Haven",
                population=300,
                disposition="friendly",
                trade_agreements=[],
                resources_known={"medicine": 200.0, "food": 150.0},
            ),
            NeighborSettlement(
                name="Ironhold",
                population=450,
                disposition="neutral",
                trade_agreements=[],
                resources_known={"weapons": 150.0, "fuel": 100.0},
            ),
            NeighborSettlement(
                name="The Scrapyard",
                population=200,
                disposition="hostile",
                trade_agreements=[],
                resources_known={"building_materials": 300.0, "weapons": 80.0},
            ),
        ]

    def _generate_threat_schedule(self) -> List[ThreatEvent]:
        """Pre-generate the fixed threat events (unresolved)."""
        return [
            ThreatEvent(year=y, threat_type=t, severity=s)
            for y, t, s in THREAT_SCHEDULE
        ]
