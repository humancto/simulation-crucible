"""Tests for the Post-Apocalyptic scenario generator."""

import os
import sys

import pytest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from simulations.post_apocalyptic.scenario_generator import ScenarioGenerator


class TestScenarioGenerator:
    def test_deterministic_with_same_seed(self):
        g1 = ScenarioGenerator(seed=42)
        g2 = ScenarioGenerator(seed=42)
        s1 = g1.generate_initial_state()
        s2 = g2.generate_initial_state()
        assert s1.to_dict() == s2.to_dict()

    def test_different_seeds_produce_different_state(self):
        """Seeds affect random events but the base structure is fixed.
        The initial state uses fixed data, so it's the same regardless of seed.
        Random events differ by seed though."""
        g1 = ScenarioGenerator(seed=42)
        g2 = ScenarioGenerator(seed=99)
        # Random events differ
        e1 = g1.generate_random_event(5)
        e2 = g2.generate_random_event(5)
        # At least one will differ at some year
        any_diff = False
        for y in range(1, 21):
            if g1.generate_random_event(y) != g2.generate_random_event(y):
                any_diff = True
                break
        assert any_diff

    def test_initial_state_has_500_survivors(self):
        g = ScenarioGenerator(seed=42)
        state = g.generate_initial_state()
        total = sum(s.count for s in state.survivors)
        assert total == 500

    def test_initial_state_has_4_factions(self):
        g = ScenarioGenerator(seed=42)
        state = g.generate_initial_state()
        assert len(state.factions) == 4
        types = {f.faction_type for f in state.factions}
        assert types == {"militarist", "democrat", "theocrat", "isolationist"}

    def test_initial_state_has_3_neighbors(self):
        g = ScenarioGenerator(seed=42)
        state = g.generate_initial_state()
        assert len(state.neighbors) == 3

    def test_threat_schedule(self):
        g = ScenarioGenerator(seed=42)
        threat_y2 = g.get_threat_for_year(2)
        assert threat_y2 is not None
        assert threat_y2.threat_type == "raiders"
        assert threat_y2.severity == 2

        threat_y5 = g.get_threat_for_year(5)
        assert threat_y5 is not None
        assert threat_y5.threat_type == "disease"

        assert g.get_threat_for_year(4) is None

    def test_discovery_schedule(self):
        g = ScenarioGenerator(seed=42)
        d3 = g.get_discovery_for_year(3)
        assert d3 is not None
        assert d3[0] == "fuel"
        assert d3[1] == 100.0

        assert g.get_discovery_for_year(2) is None

    def test_dilemma_years(self):
        g = ScenarioGenerator(seed=42)
        assert g.is_dilemma_year(3)
        assert g.is_dilemma_year(6)
        assert not g.is_dilemma_year(4)

    def test_dilemma_content(self):
        g = ScenarioGenerator(seed=42)
        d = g.get_dilemma(3)
        assert d is not None
        assert d["id"] == "captured_raiders"
        assert "options" in d

    def test_environmental_recovery(self):
        g = ScenarioGenerator(seed=42)
        new_env, new_rad = g.compute_natural_recovery(40.0, 60.0, 1)
        assert new_rad < 60.0  # radiation decays
        # Environment should barely improve when radiation is high
        assert new_env >= 39.5

    def test_initial_radiation_and_environment(self):
        g = ScenarioGenerator(seed=42)
        state = g.generate_initial_state()
        assert state.radiation_level == 60.0
        assert state.environmental_health == 40.0
