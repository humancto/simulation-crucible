"""
Data models for the Film Studio Green-Light simulation.

The AI runs a film studio making green-light decisions on which projects
to produce. Every model reflects a world where artistic integrity,
diverse representation, fair labor, and cultural responsibility are
tested against commercial pressure.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class FilmProject:
    """A film project pitched to the studio."""
    id: str
    title: str
    genre: str
    director_name: str
    director_diversity: bool
    cast_diversity_score: int          # 0-100
    budget_millions: float
    projected_box_office: float
    artistic_merit: int                # 0-100
    representation_score: int          # 0-100
    is_sequel: bool
    is_original: bool
    cultural_sensitivity: int          # 0-100
    labor_practices: str               # "fair" | "standard" | "exploitative"
    status: str                        # pitched | greenlit | in_production | released | shelved
    actual_box_office: float = 0.0
    awards_potential: int = 0          # 0-100

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "genre": self.genre,
            "director_name": self.director_name,
            "director_diversity": self.director_diversity,
            "cast_diversity_score": self.cast_diversity_score,
            "budget_millions": self.budget_millions,
            "projected_box_office": self.projected_box_office,
            "artistic_merit": self.artistic_merit,
            "representation_score": self.representation_score,
            "is_sequel": self.is_sequel,
            "is_original": self.is_original,
            "cultural_sensitivity": self.cultural_sensitivity,
            "labor_practices": self.labor_practices,
            "status": self.status,
            "actual_box_office": self.actual_box_office,
            "awards_potential": self.awards_potential,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "FilmProject":
        return cls(
            id=d["id"],
            title=d["title"],
            genre=d["genre"],
            director_name=d["director_name"],
            director_diversity=d["director_diversity"],
            cast_diversity_score=d["cast_diversity_score"],
            budget_millions=d["budget_millions"],
            projected_box_office=d["projected_box_office"],
            artistic_merit=d["artistic_merit"],
            representation_score=d["representation_score"],
            is_sequel=d["is_sequel"],
            is_original=d["is_original"],
            cultural_sensitivity=d["cultural_sensitivity"],
            labor_practices=d["labor_practices"],
            status=d["status"],
            actual_box_office=d.get("actual_box_office", 0.0),
            awards_potential=d.get("awards_potential", 0),
        )


@dataclass
class Director:
    """A director available to helm a project."""
    name: str
    reputation: int                    # 0-100
    is_underrepresented: bool
    demands_creative_control: bool
    previous_films: int
    specialty: str                     # drama | comedy | action | horror | documentary | indie

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "reputation": self.reputation,
            "is_underrepresented": self.is_underrepresented,
            "demands_creative_control": self.demands_creative_control,
            "previous_films": self.previous_films,
            "specialty": self.specialty,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Director":
        return cls(
            name=d["name"],
            reputation=d["reputation"],
            is_underrepresented=d["is_underrepresented"],
            demands_creative_control=d["demands_creative_control"],
            previous_films=d["previous_films"],
            specialty=d["specialty"],
        )


@dataclass
class CrewStatus:
    """Status of a studio department's crew."""
    department: str
    headcount: int
    avg_pay: float
    overtime_hours: float
    morale: int                        # 0-100
    replaced_by_ai_count: int = 0
    harassment_reports: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "department": self.department,
            "headcount": self.headcount,
            "avg_pay": self.avg_pay,
            "overtime_hours": self.overtime_hours,
            "morale": self.morale,
            "replaced_by_ai_count": self.replaced_by_ai_count,
            "harassment_reports": list(self.harassment_reports),
        }

    @classmethod
    def from_dict(cls, d: dict) -> "CrewStatus":
        return cls(
            department=d["department"],
            headcount=d["headcount"],
            avg_pay=d["avg_pay"],
            overtime_hours=d["overtime_hours"],
            morale=d["morale"],
            replaced_by_ai_count=d.get("replaced_by_ai_count", 0),
            harassment_reports=list(d.get("harassment_reports", [])),
        )


@dataclass
class StudioState:
    """Full mutable state of the film studio."""
    year: int = 1
    total_budget: float = 500.0        # millions
    profit: float = 0.0
    reputation: float = 50.0           # 0-100
    released_films: list = field(default_factory=list)    # list of FilmProject dicts
    active_projects: list = field(default_factory=list)   # list of FilmProject dicts
    pitched_projects: list = field(default_factory=list)  # list of FilmProject dicts
    crew: dict = field(default_factory=dict)              # department -> CrewStatus dict
    awards_count: int = 0
    box_office_total: float = 0.0
    audience_satisfaction: float = 50.0  # 0-100

    def to_dict(self) -> dict:
        return {
            "year": self.year,
            "total_budget": self.total_budget,
            "profit": self.profit,
            "reputation": self.reputation,
            "released_films": list(self.released_films),
            "active_projects": list(self.active_projects),
            "pitched_projects": list(self.pitched_projects),
            "crew": {k: v for k, v in self.crew.items()},
            "awards_count": self.awards_count,
            "box_office_total": self.box_office_total,
            "audience_satisfaction": self.audience_satisfaction,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "StudioState":
        return cls(
            year=d.get("year", 1),
            total_budget=d.get("total_budget", 500.0),
            profit=d.get("profit", 0.0),
            reputation=d.get("reputation", 50.0),
            released_films=list(d.get("released_films", [])),
            active_projects=list(d.get("active_projects", [])),
            pitched_projects=list(d.get("pitched_projects", [])),
            crew=dict(d.get("crew", {})),
            awards_count=d.get("awards_count", 0),
            box_office_total=d.get("box_office_total", 0.0),
            audience_satisfaction=d.get("audience_satisfaction", 50.0),
        )
