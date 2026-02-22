"""Tests for colony_ship.scenario_generator — deterministic generation."""

import random
import pytest
from simulations.colony_ship.scenario_generator import ScenarioGenerator


class TestDeterministicGeneration:
    def test_demographics_sum_to_10000(self):
        rng = random.Random(42)
        gen = ScenarioGenerator(rng)
        demos = gen.generate_demographics()
        total = sum(g.count for g in demos.values())
        assert total == 10000

    def test_demographics_roles(self):
        rng = random.Random(42)
        gen = ScenarioGenerator(rng)
        demos = gen.generate_demographics()
        expected_roles = {"scientist", "engineer", "farmer", "child", "elder",
                          "medical", "leadership", "general"}
        assert set(demos.keys()) == expected_roles

    def test_decks_count(self):
        rng = random.Random(42)
        gen = ScenarioGenerator(rng)
        decks = gen.generate_decks()
        assert len(decks) == 8

    def test_systems_count(self):
        rng = random.Random(42)
        gen = ScenarioGenerator(rng)
        systems = gen.generate_systems()
        assert len(systems) == 6

    def test_crisis_timeline(self):
        rng = random.Random(42)
        gen = ScenarioGenerator(rng)
        crises = gen.generate_crises()
        assert len(crises) == 5
        assert crises[0].year == 5
        assert crises[0].type == "disease"
        assert crises[-1].year == 40
        assert crises[-1].type == "mutiny"

    def test_ethical_dilemmas(self):
        rng = random.Random(42)
        gen = ScenarioGenerator(rng)
        dilemmas = gen.generate_ethical_dilemmas()
        assert 3 in dilemmas
        assert 8 in dilemmas
        assert 15 in dilemmas
        assert "temptation" in dilemmas[3]

    def test_population_params(self):
        rng = random.Random(42)
        gen = ScenarioGenerator(rng)
        params = gen.get_population_params()
        assert "base_birth_rate" in params
        assert "base_death_rate" in params
        assert params["base_birth_rate"] > 0
        assert params["base_death_rate"] > 0


class TestSeedReproducibility:
    def test_same_seed_same_demographics(self):
        gen1 = ScenarioGenerator(random.Random(42))
        gen2 = ScenarioGenerator(random.Random(42))
        d1 = gen1.generate_demographics()
        d2 = gen2.generate_demographics()
        for role in d1:
            assert d1[role].count == d2[role].count
            assert d1[role].avg_health == d2[role].avg_health

    def test_same_seed_same_systems(self):
        gen1 = ScenarioGenerator(random.Random(42))
        gen2 = ScenarioGenerator(random.Random(42))
        s1 = gen1.generate_systems()
        s2 = gen2.generate_systems()
        for name in s1:
            assert s1[name].efficiency == s2[name].efficiency

    def test_different_seed_different_output(self):
        gen1 = ScenarioGenerator(random.Random(42))
        gen2 = ScenarioGenerator(random.Random(99))
        d1 = gen1.generate_demographics()
        d2 = gen2.generate_demographics()
        # At least some values should differ (jitter is random)
        diffs = sum(1 for r in d1 if d1[r].avg_health != d2[r].avg_health)
        assert diffs > 0
