"""Tests for the Accessible Architecture scenario generator."""

import os
import sys

import pytest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from simulations.accessible_architecture.scenario_generator import ScenarioGenerator


class TestScenarioGenerator:
    def test_deterministic(self):
        g1 = ScenarioGenerator(seed=42)
        g2 = ScenarioGenerator(seed=42)
        state1 = g1.generate_initial_state()
        state2 = g2.generate_initial_state()
        assert state1.year == state2.year
        assert len(state1.employees) == len(state2.employees)
        assert len(state1.projects) == len(state2.projects)
        for p1, p2 in zip(state1.projects, state2.projects):
            assert p1.id == p2.id
            assert p1.name == p2.name
            assert p1.budget_millions == p2.budget_millions

    def test_initial_state_has_employees(self):
        g = ScenarioGenerator(seed=42)
        state = g.generate_initial_state()
        assert len(state.employees) >= 6
        assert len(state.employees) <= 8

    def test_initial_state_has_projects(self):
        g = ScenarioGenerator(seed=42)
        state = g.generate_initial_state()
        assert len(state.projects) >= 3
        assert len(state.projects) <= 5

    def test_year_projects_range(self):
        g = ScenarioGenerator(seed=42)
        projects = g.generate_year_projects(5)
        assert len(projects) >= 3
        assert len(projects) <= 5

    def test_project_ids_contain_year(self):
        g = ScenarioGenerator(seed=42)
        projects = g.generate_year_projects(7)
        for p in projects:
            assert "y7" in p.id

    def test_community_feedback_generated(self):
        g = ScenarioGenerator(seed=42)
        feedbacks = g.generate_community_feedback("test_project", 1)
        assert len(feedbacks) >= 1
        assert len(feedbacks) <= 3
        for fb in feedbacks:
            assert fb.project_id == "test_project"
            assert fb.source in [
                "disability_advocate", "wheelchair_user", "blind_user",
                "deaf_user", "neurodivergent", "elderly",
            ]

    def test_scandal_event_structure(self):
        g = ScenarioGenerator(seed=99)  # seed that generates scandal
        # Try multiple seeds to find one that generates a scandal
        found = False
        for seed in range(100):
            g = ScenarioGenerator(seed=seed)
            event = g.generate_scandal_event(5)
            if event:
                found = True
                assert "title" in event
                assert "description" in event
                break
        assert found, "No scandal generated across 100 seeds"

    def test_award_opportunity(self):
        found = False
        for seed in range(100):
            g = ScenarioGenerator(seed=seed)
            award = g.generate_award_opportunity(5)
            if award:
                found = True
                assert "award_name" in award
                assert "requires_accessibility_score" in award
                break
        assert found, "No award generated across 100 seeds"

    def test_applicant_generation(self):
        found_disabled = False
        found_non_disabled = False
        for seed in range(100):
            g = ScenarioGenerator(seed=seed)
            app = g.generate_applicant(3)
            if app:
                assert "name" in app
                assert "role" in app
                assert "has_disability" in app
                if app["has_disability"]:
                    found_disabled = True
                else:
                    found_non_disabled = True
        assert found_disabled, "No disabled applicant generated"
        assert found_non_disabled, "No non-disabled applicant generated"

    def test_different_seeds_different_results(self):
        g1 = ScenarioGenerator(seed=1)
        g2 = ScenarioGenerator(seed=999)
        state1 = g1.generate_initial_state()
        state2 = g2.generate_initial_state()
        # At minimum employees or project names should differ
        names1 = [e.name for e in state1.employees]
        names2 = [e.name for e in state2.employees]
        # Very unlikely to be identical with different seeds
        assert names1 != names2 or len(state1.projects) != len(state2.projects)
