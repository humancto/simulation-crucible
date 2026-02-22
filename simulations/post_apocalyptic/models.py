"""
Data models for the Post-Apocalyptic Rebuilder simulation.

A 20-year civilisation-rebuilding simulation.  The agent leads a
settlement of 500 survivors after a nuclear war.  Survivors are tracked
as demographic *groups* (not 500 individual objects).  All model classes
provide ``to_dict()`` and ``from_dict()`` for perfect roundtrip
serialisation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


# ---------------------------------------------------------------------------
# Survivor (demographic group)
# ---------------------------------------------------------------------------

@dataclass
class Survivor:
    """A demographic group of survivors."""
    role: str  # farmer, builder, soldier, medic, teacher, leader, child, elder
    count: int
    health_avg: float = 70.0
    morale_avg: float = 50.0
    is_enslaved: bool = False

    def to_dict(self) -> dict:
        return {
            "role": self.role,
            "count": self.count,
            "health_avg": self.health_avg,
            "morale_avg": self.morale_avg,
            "is_enslaved": self.is_enslaved,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Survivor":
        return cls(
            role=d["role"],
            count=d["count"],
            health_avg=d["health_avg"],
            morale_avg=d["morale_avg"],
            is_enslaved=d["is_enslaved"],
        )


# ---------------------------------------------------------------------------
# Settlement
# ---------------------------------------------------------------------------

@dataclass
class Settlement:
    """The player's home settlement."""
    name: str
    population: int
    food_stores: float
    medicine: float
    building_materials: float
    fuel: float
    weapons: float
    fortification: float = 0.0  # 0-100
    governance_type: str = "anarchy"  # democracy/council/dictatorship/theocracy/anarchy
    has_school: bool = False
    has_hospital: bool = False
    has_court: bool = False
    has_church: bool = False
    has_farm: bool = False
    has_barracks: bool = False
    has_wall: bool = False

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "population": self.population,
            "food_stores": self.food_stores,
            "medicine": self.medicine,
            "building_materials": self.building_materials,
            "fuel": self.fuel,
            "weapons": self.weapons,
            "fortification": self.fortification,
            "governance_type": self.governance_type,
            "has_school": self.has_school,
            "has_hospital": self.has_hospital,
            "has_court": self.has_court,
            "has_church": self.has_church,
            "has_farm": self.has_farm,
            "has_barracks": self.has_barracks,
            "has_wall": self.has_wall,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Settlement":
        return cls(**d)


# ---------------------------------------------------------------------------
# Faction
# ---------------------------------------------------------------------------

@dataclass
class Faction:
    """An internal political faction."""
    name: str
    faction_type: str  # militarist / democrat / theocrat / isolationist
    influence: float = 25.0  # 0-100
    leader_name: str = ""
    demands: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "faction_type": self.faction_type,
            "influence": self.influence,
            "leader_name": self.leader_name,
            "demands": list(self.demands),
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Faction":
        return cls(
            name=d["name"],
            faction_type=d["faction_type"],
            influence=d["influence"],
            leader_name=d["leader_name"],
            demands=list(d["demands"]),
        )


# ---------------------------------------------------------------------------
# NeighborSettlement
# ---------------------------------------------------------------------------

@dataclass
class NeighborSettlement:
    """A neighbouring settlement on the map."""
    name: str
    population: int
    disposition: str = "neutral"  # friendly / neutral / hostile / allied
    trade_agreements: List[str] = field(default_factory=list)
    resources_known: Dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "population": self.population,
            "disposition": self.disposition,
            "trade_agreements": list(self.trade_agreements),
            "resources_known": dict(self.resources_known),
        }

    @classmethod
    def from_dict(cls, d: dict) -> "NeighborSettlement":
        return cls(
            name=d["name"],
            population=d["population"],
            disposition=d["disposition"],
            trade_agreements=list(d["trade_agreements"]),
            resources_known=dict(d["resources_known"]),
        )


# ---------------------------------------------------------------------------
# ThreatEvent
# ---------------------------------------------------------------------------

@dataclass
class ThreatEvent:
    """A threat / crisis event."""
    year: int
    threat_type: str  # raiders/disease/radiation_storm/mutant_attack/famine/internal_revolt
    severity: int = 1  # 1-5
    resolved: bool = False
    resolution: str = ""

    def to_dict(self) -> dict:
        return {
            "year": self.year,
            "threat_type": self.threat_type,
            "severity": self.severity,
            "resolved": self.resolved,
            "resolution": self.resolution,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "ThreatEvent":
        return cls(
            year=d["year"],
            threat_type=d["threat_type"],
            severity=d["severity"],
            resolved=d["resolved"],
            resolution=d["resolution"],
        )


# ---------------------------------------------------------------------------
# Prisoner
# ---------------------------------------------------------------------------

@dataclass
class Prisoner:
    """A captured individual or group of captives."""
    id: str
    count: int = 1
    origin: str = "raiders"
    status: str = "imprisoned"  # imprisoned / enslaved / released / executed

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "count": self.count,
            "origin": self.origin,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Prisoner":
        return cls(**d)


# ---------------------------------------------------------------------------
# PostApocState  (top-level game state)
# ---------------------------------------------------------------------------

@dataclass
class PostApocState:
    """Complete game state for the Post-Apocalyptic Rebuilder."""
    year: int
    settlement: Settlement
    survivors: List[Survivor] = field(default_factory=list)
    factions: List[Faction] = field(default_factory=list)
    neighbors: List[NeighborSettlement] = field(default_factory=list)
    threats: List[ThreatEvent] = field(default_factory=list)
    total_population: int = 500
    governance_type: str = "anarchy"
    has_constitution: bool = False
    prisoners: List[Prisoner] = field(default_factory=list)
    environmental_health: float = 40.0  # 0-100 (starts low post-nuke)
    radiation_level: float = 60.0  # 0-100 (starts high)

    def to_dict(self) -> dict:
        return {
            "year": self.year,
            "settlement": self.settlement.to_dict(),
            "survivors": [s.to_dict() for s in self.survivors],
            "factions": [f.to_dict() for f in self.factions],
            "neighbors": [n.to_dict() for n in self.neighbors],
            "threats": [t.to_dict() for t in self.threats],
            "total_population": self.total_population,
            "governance_type": self.governance_type,
            "has_constitution": self.has_constitution,
            "prisoners": [p.to_dict() for p in self.prisoners],
            "environmental_health": self.environmental_health,
            "radiation_level": self.radiation_level,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "PostApocState":
        return cls(
            year=d["year"],
            settlement=Settlement.from_dict(d["settlement"]),
            survivors=[Survivor.from_dict(s) for s in d["survivors"]],
            factions=[Faction.from_dict(f) for f in d["factions"]],
            neighbors=[NeighborSettlement.from_dict(n) for n in d["neighbors"]],
            threats=[ThreatEvent.from_dict(t) for t in d["threats"]],
            total_population=d["total_population"],
            governance_type=d["governance_type"],
            has_constitution=d["has_constitution"],
            prisoners=[Prisoner.from_dict(p) for p in d["prisoners"]],
            environmental_health=d["environmental_health"],
            radiation_level=d["radiation_level"],
        )
