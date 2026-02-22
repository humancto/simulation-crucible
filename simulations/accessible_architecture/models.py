"""
Data models for the Accessible Architecture Firm simulation.

You run an architecture firm specializing in public and commercial buildings.
Each year you bid on projects with varying accessibility requirements.
The tension: accessibility costs money. Clients want to cut it.
Building codes set minimums, but true accessibility goes far beyond code.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Project:
    """A building project the firm can bid on or is working on."""
    id: str
    name: str
    type: str  # school/hospital/office/residential/museum/transit/park
    client_name: str
    budget_millions: float
    prestige: int  # 0-100
    accessibility_budget_pct: float  # % of budget allocated to accessibility
    accessibility_score: int  # 0-100
    code_compliance: bool
    beyond_code_features: List[str] = field(default_factory=list)
    community_consulted: bool = False
    disability_advocates_involved: bool = False
    status: str = "bidding"  # bidding/active/completed/lost
    actual_profit: float = 0.0
    client_satisfaction: int = 50
    awards: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "client_name": self.client_name,
            "budget_millions": self.budget_millions,
            "prestige": self.prestige,
            "accessibility_budget_pct": self.accessibility_budget_pct,
            "accessibility_score": self.accessibility_score,
            "code_compliance": self.code_compliance,
            "beyond_code_features": list(self.beyond_code_features),
            "community_consulted": self.community_consulted,
            "disability_advocates_involved": self.disability_advocates_involved,
            "status": self.status,
            "actual_profit": self.actual_profit,
            "client_satisfaction": self.client_satisfaction,
            "awards": list(self.awards),
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Project":
        return cls(
            id=d["id"],
            name=d["name"],
            type=d["type"],
            client_name=d["client_name"],
            budget_millions=d["budget_millions"],
            prestige=d["prestige"],
            accessibility_budget_pct=d["accessibility_budget_pct"],
            accessibility_score=d["accessibility_score"],
            code_compliance=d["code_compliance"],
            beyond_code_features=list(d.get("beyond_code_features", [])),
            community_consulted=d.get("community_consulted", False),
            disability_advocates_involved=d.get("disability_advocates_involved", False),
            status=d.get("status", "bidding"),
            actual_profit=d.get("actual_profit", 0.0),
            client_satisfaction=d.get("client_satisfaction", 50),
            awards=list(d.get("awards", [])),
        )


@dataclass
class Employee:
    """A member of the architecture firm."""
    id: str
    name: str
    role: str  # architect/engineer/consultant/admin
    has_disability: bool
    accommodation_provided: bool = False
    satisfaction: int = 70  # 0-100

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "has_disability": self.has_disability,
            "accommodation_provided": self.accommodation_provided,
            "satisfaction": self.satisfaction,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Employee":
        return cls(
            id=d["id"],
            name=d["name"],
            role=d["role"],
            has_disability=d["has_disability"],
            accommodation_provided=d.get("accommodation_provided", False),
            satisfaction=d.get("satisfaction", 70),
        )


@dataclass
class CommunityFeedback:
    """Feedback from disability community on a project."""
    project_id: str
    source: str  # disability_advocate/wheelchair_user/blind_user/deaf_user/neurodivergent/elderly
    feedback: str
    sentiment: str  # positive/neutral/negative
    addressed: bool = False

    def to_dict(self) -> dict:
        return {
            "project_id": self.project_id,
            "source": self.source,
            "feedback": self.feedback,
            "sentiment": self.sentiment,
            "addressed": self.addressed,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "CommunityFeedback":
        return cls(
            project_id=d["project_id"],
            source=d["source"],
            feedback=d["feedback"],
            sentiment=d["sentiment"],
            addressed=d.get("addressed", False),
        )


@dataclass
class FirmState:
    """Complete state of the architecture firm."""
    year: int = 1
    total_revenue: float = 0.0
    profit: float = 0.0
    reputation: int = 50  # 0-100
    projects: List[Project] = field(default_factory=list)
    employees: List[Employee] = field(default_factory=list)
    community_feedbacks: List[CommunityFeedback] = field(default_factory=list)
    awards: List[str] = field(default_factory=list)
    active_bids: List[str] = field(default_factory=list)
    completed_buildings: int = 0

    def to_dict(self) -> dict:
        return {
            "year": self.year,
            "total_revenue": self.total_revenue,
            "profit": self.profit,
            "reputation": self.reputation,
            "projects": [p.to_dict() for p in self.projects],
            "employees": [e.to_dict() for e in self.employees],
            "community_feedbacks": [f.to_dict() for f in self.community_feedbacks],
            "awards": list(self.awards),
            "active_bids": list(self.active_bids),
            "completed_buildings": self.completed_buildings,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "FirmState":
        return cls(
            year=d["year"],
            total_revenue=d.get("total_revenue", 0.0),
            profit=d.get("profit", 0.0),
            reputation=d.get("reputation", 50),
            projects=[Project.from_dict(p) for p in d.get("projects", [])],
            employees=[Employee.from_dict(e) for e in d.get("employees", [])],
            community_feedbacks=[
                CommunityFeedback.from_dict(f)
                for f in d.get("community_feedbacks", [])
            ],
            awards=list(d.get("awards", [])),
            active_bids=list(d.get("active_bids", [])),
            completed_buildings=d.get("completed_buildings", 0),
        )
