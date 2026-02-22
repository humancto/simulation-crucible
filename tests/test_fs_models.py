"""Tests for simulations/film_studio/models.py -- all data models."""

import pytest
from simulations.film_studio.models import (
    FilmProject, Director, CrewStatus, StudioState,
)


# ── FilmProject Tests ─────────────────────────────────────────────────────


class TestFilmProject:

    def test_create_project(self):
        p = FilmProject(
            id="f1", title="Test Film", genre="drama",
            director_name="Jane Doe", director_diversity=True,
            cast_diversity_score=80, budget_millions=50.0,
            projected_box_office=120.0, artistic_merit=85,
            representation_score=90, is_sequel=False, is_original=True,
            cultural_sensitivity=75, labor_practices="fair",
            status="pitched",
        )
        assert p.id == "f1"
        assert p.title == "Test Film"
        assert p.director_diversity is True
        assert p.is_original is True
        assert p.status == "pitched"
        assert p.actual_box_office == 0.0

    def test_project_to_dict(self):
        p = FilmProject(
            id="f2", title="Action Movie", genre="action",
            director_name="John Smith", director_diversity=False,
            cast_diversity_score=30, budget_millions=200.0,
            projected_box_office=600.0, artistic_merit=40,
            representation_score=20, is_sequel=True, is_original=False,
            cultural_sensitivity=50, labor_practices="standard",
            status="greenlit", actual_box_office=550.0, awards_potential=15,
        )
        d = p.to_dict()
        assert d["id"] == "f2"
        assert d["budget_millions"] == 200.0
        assert d["actual_box_office"] == 550.0
        assert d["is_sequel"] is True

    def test_project_from_dict(self):
        d = {
            "id": "f3", "title": "Indie Gem", "genre": "indie",
            "director_name": "Ava Chen", "director_diversity": True,
            "cast_diversity_score": 90, "budget_millions": 15.0,
            "projected_box_office": 30.0, "artistic_merit": 92,
            "representation_score": 95, "is_sequel": False,
            "is_original": True, "cultural_sensitivity": 88,
            "labor_practices": "fair", "status": "released",
            "actual_box_office": 45.0, "awards_potential": 85,
        }
        p = FilmProject.from_dict(d)
        assert p.title == "Indie Gem"
        assert p.actual_box_office == 45.0
        assert p.awards_potential == 85

    def test_project_roundtrip(self):
        p = FilmProject(
            id="rt", title="Roundtrip", genre="horror",
            director_name="Test Dir", director_diversity=True,
            cast_diversity_score=77, budget_millions=33.3,
            projected_box_office=88.8, artistic_merit=65,
            representation_score=82, is_sequel=False, is_original=True,
            cultural_sensitivity=70, labor_practices="exploitative",
            status="in_production", actual_box_office=0.0, awards_potential=55,
        )
        d = p.to_dict()
        restored = FilmProject.from_dict(d)
        assert restored.id == p.id
        assert restored.title == p.title
        assert restored.genre == p.genre
        assert restored.director_name == p.director_name
        assert restored.director_diversity == p.director_diversity
        assert restored.cast_diversity_score == p.cast_diversity_score
        assert restored.budget_millions == p.budget_millions
        assert restored.projected_box_office == p.projected_box_office
        assert restored.artistic_merit == p.artistic_merit
        assert restored.representation_score == p.representation_score
        assert restored.is_sequel == p.is_sequel
        assert restored.is_original == p.is_original
        assert restored.cultural_sensitivity == p.cultural_sensitivity
        assert restored.labor_practices == p.labor_practices
        assert restored.status == p.status
        assert restored.actual_box_office == p.actual_box_office
        assert restored.awards_potential == p.awards_potential


# ── Director Tests ────────────────────────────────────────────────────────


class TestDirector:

    def test_create_director(self):
        d = Director(
            name="Test Director", reputation=75,
            is_underrepresented=True, demands_creative_control=True,
            previous_films=5, specialty="drama",
        )
        assert d.name == "Test Director"
        assert d.reputation == 75
        assert d.is_underrepresented is True

    def test_director_to_dict(self):
        d = Director("Jane", 80, False, True, 10, "comedy")
        result = d.to_dict()
        assert result["name"] == "Jane"
        assert result["reputation"] == 80
        assert result["specialty"] == "comedy"

    def test_director_roundtrip(self):
        d = Director("Roundtrip", 42, True, False, 3, "documentary")
        data = d.to_dict()
        restored = Director.from_dict(data)
        assert restored.name == d.name
        assert restored.reputation == d.reputation
        assert restored.is_underrepresented == d.is_underrepresented
        assert restored.demands_creative_control == d.demands_creative_control
        assert restored.previous_films == d.previous_films
        assert restored.specialty == d.specialty


# ── CrewStatus Tests ──────────────────────────────────────────────────────


class TestCrewStatus:

    def test_create_crew(self):
        c = CrewStatus("vfx", 100, 85000, 10.0, 70)
        assert c.department == "vfx"
        assert c.headcount == 100
        assert c.replaced_by_ai_count == 0
        assert c.harassment_reports == []

    def test_crew_to_dict(self):
        c = CrewStatus("animation", 80, 75000, 8.0, 72,
                        replaced_by_ai_count=5,
                        harassment_reports=["hr_001"])
        d = c.to_dict()
        assert d["department"] == "animation"
        assert d["replaced_by_ai_count"] == 5
        assert d["harassment_reports"] == ["hr_001"]

    def test_crew_roundtrip(self):
        c = CrewStatus("production", 200, 65000, 12.0, 68,
                        replaced_by_ai_count=10,
                        harassment_reports=["hr_001", "hr_002"])
        d = c.to_dict()
        restored = CrewStatus.from_dict(d)
        assert restored.department == c.department
        assert restored.headcount == c.headcount
        assert restored.avg_pay == c.avg_pay
        assert restored.overtime_hours == c.overtime_hours
        assert restored.morale == c.morale
        assert restored.replaced_by_ai_count == c.replaced_by_ai_count
        assert restored.harassment_reports == c.harassment_reports


# ── StudioState Tests ─────────────────────────────────────────────────────


class TestStudioState:

    def test_create_state(self):
        s = StudioState()
        assert s.year == 1
        assert s.total_budget == 500.0
        assert s.profit == 0.0
        assert s.reputation == 50.0
        assert s.awards_count == 0

    def test_state_to_dict(self):
        s = StudioState(year=3, total_budget=400.0, profit=50.0,
                         reputation=65.0, awards_count=2,
                         box_office_total=300.0, audience_satisfaction=60.0)
        d = s.to_dict()
        assert d["year"] == 3
        assert d["total_budget"] == 400.0
        assert d["awards_count"] == 2

    def test_state_roundtrip(self):
        s = StudioState(
            year=5, total_budget=350.0, profit=120.0,
            reputation=72.5,
            released_films=[{"id": "f1", "title": "Test"}],
            active_projects=[{"id": "f2", "title": "Active"}],
            pitched_projects=[{"id": "f3", "title": "Pitched"}],
            crew={"vfx": {"department": "vfx", "headcount": 100,
                          "avg_pay": 85000, "overtime_hours": 10,
                          "morale": 70, "replaced_by_ai_count": 0,
                          "harassment_reports": []}},
            awards_count=3,
            box_office_total=500.0,
            audience_satisfaction=65.5,
        )
        d = s.to_dict()
        restored = StudioState.from_dict(d)
        assert restored.year == s.year
        assert restored.total_budget == s.total_budget
        assert restored.profit == s.profit
        assert restored.reputation == s.reputation
        assert restored.awards_count == s.awards_count
        assert restored.box_office_total == s.box_office_total
        assert restored.audience_satisfaction == s.audience_satisfaction
        assert len(restored.released_films) == 1
        assert len(restored.active_projects) == 1
        assert len(restored.pitched_projects) == 1
        assert "vfx" in restored.crew
