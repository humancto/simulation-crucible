"""Tests for the Accessible Architecture data models."""

import os
import sys

import pytest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from simulations.accessible_architecture.models import (
    CommunityFeedback,
    Employee,
    FirmState,
    Project,
)


class TestProject:
    def test_to_dict_roundtrip(self):
        p = Project(
            id="p1", name="Test School", type="school",
            client_name="City of Test", budget_millions=5.0,
            prestige=60, accessibility_budget_pct=10.0,
            accessibility_score=75, code_compliance=True,
            beyond_code_features=["tactile_wayfinding", "quiet_rooms"],
            community_consulted=True,
            disability_advocates_involved=True,
            status="active", actual_profit=0.6,
            client_satisfaction=80,
            awards=["Best Design"],
        )
        d = p.to_dict()
        p2 = Project.from_dict(d)
        assert p2.id == "p1"
        assert p2.name == "Test School"
        assert p2.type == "school"
        assert p2.budget_millions == 5.0
        assert p2.prestige == 60
        assert p2.accessibility_score == 75
        assert p2.beyond_code_features == ["tactile_wayfinding", "quiet_rooms"]
        assert p2.community_consulted is True
        assert p2.disability_advocates_involved is True
        assert p2.status == "active"
        assert p2.actual_profit == 0.6
        assert p2.client_satisfaction == 80
        assert p2.awards == ["Best Design"]

    def test_defaults(self):
        p = Project(
            id="p2", name="Test", type="office",
            client_name="Corp", budget_millions=10.0,
            prestige=50, accessibility_budget_pct=5.0,
            accessibility_score=40, code_compliance=True,
        )
        assert p.beyond_code_features == []
        assert p.community_consulted is False
        assert p.status == "bidding"
        assert p.actual_profit == 0.0


class TestEmployee:
    def test_to_dict_roundtrip(self):
        e = Employee(
            id="e1", name="Maya", role="architect",
            has_disability=True, accommodation_provided=True,
            satisfaction=85,
        )
        d = e.to_dict()
        e2 = Employee.from_dict(d)
        assert e2.id == "e1"
        assert e2.name == "Maya"
        assert e2.has_disability is True
        assert e2.accommodation_provided is True
        assert e2.satisfaction == 85


class TestCommunityFeedback:
    def test_to_dict_roundtrip(self):
        f = CommunityFeedback(
            project_id="p1", source="wheelchair_user",
            feedback="Ramp too steep", sentiment="negative",
            addressed=False,
        )
        d = f.to_dict()
        f2 = CommunityFeedback.from_dict(d)
        assert f2.project_id == "p1"
        assert f2.source == "wheelchair_user"
        assert f2.feedback == "Ramp too steep"
        assert f2.sentiment == "negative"
        assert f2.addressed is False


class TestFirmState:
    def test_to_dict_roundtrip(self):
        proj = Project(
            id="p1", name="Test", type="school",
            client_name="City", budget_millions=5.0,
            prestige=60, accessibility_budget_pct=10.0,
            accessibility_score=50, code_compliance=True,
        )
        emp = Employee(
            id="e1", name="Sarah", role="architect",
            has_disability=False,
        )
        fb = CommunityFeedback(
            project_id="p1", source="elderly",
            feedback="Needs seating", sentiment="neutral",
        )
        state = FirmState(
            year=3,
            total_revenue=5_000_000.0,
            profit=1_000_000.0,
            reputation=65,
            projects=[proj],
            employees=[emp],
            community_feedbacks=[fb],
            awards=["Design Award"],
            active_bids=["p1"],
            completed_buildings=2,
        )
        d = state.to_dict()
        state2 = FirmState.from_dict(d)
        assert state2.year == 3
        assert state2.total_revenue == 5_000_000.0
        assert state2.profit == 1_000_000.0
        assert state2.reputation == 65
        assert len(state2.projects) == 1
        assert state2.projects[0].id == "p1"
        assert len(state2.employees) == 1
        assert state2.employees[0].name == "Sarah"
        assert len(state2.community_feedbacks) == 1
        assert state2.awards == ["Design Award"]
        assert state2.active_bids == ["p1"]
        assert state2.completed_buildings == 2

    def test_empty_state(self):
        state = FirmState()
        d = state.to_dict()
        state2 = FirmState.from_dict(d)
        assert state2.year == 1
        assert state2.projects == []
        assert state2.employees == []
