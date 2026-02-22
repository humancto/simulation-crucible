"""Tests for simulations/territory_control/scenario_generator.py."""

import random
import pytest
from simulations.territory_control.scenario_generator import ScenarioGenerator


class TestScenarioGeneration:

    def test_generates_5_nations(self):
        gen = ScenarioGenerator(random.Random(42))
        data = gen.generate_all()
        assert len(data["nations"]) == 5

    def test_generates_25_territories(self):
        gen = ScenarioGenerator(random.Random(42))
        data = gen.generate_all()
        assert len(data["territories"]) == 25

    def test_generates_initial_treaties(self):
        gen = ScenarioGenerator(random.Random(42))
        data = gen.generate_all()
        assert len(data["treaties"]) >= 3

    def test_generates_crisis_events(self):
        gen = ScenarioGenerator(random.Random(42))
        data = gen.generate_all()
        assert len(data["crisis_events"]) > 0

    def test_generates_ai_behaviors(self):
        gen = ScenarioGenerator(random.Random(42))
        data = gen.generate_all()
        assert "nation_iron" in data["ai_behaviors"]
        assert "nation_trade" in data["ai_behaviors"]

    def test_generates_resource_market(self):
        gen = ScenarioGenerator(random.Random(42))
        data = gen.generate_all()
        assert "food" in data["resource_market"]
        assert "oil" in data["resource_market"]


class TestDeterminism:

    def test_same_seed_same_nations(self):
        gen1 = ScenarioGenerator(random.Random(42))
        gen2 = ScenarioGenerator(random.Random(42))
        n1 = gen1.generate_nations()
        n2 = gen2.generate_nations()
        assert [n.id for n in n1] == [n.id for n in n2]

    def test_same_seed_same_territories(self):
        gen1 = ScenarioGenerator(random.Random(42))
        gen2 = ScenarioGenerator(random.Random(42))
        t1 = gen1.generate_territories()
        t2 = gen2.generate_territories()
        assert [t.id for t in t1] == [t.id for t in t2]
        assert [t.civilian_morale for t in t1] == [t.civilian_morale for t in t2]


class TestNationProperties:

    def test_player_nation_exists(self):
        gen = ScenarioGenerator(random.Random(42))
        nations = gen.generate_nations()
        ids = [n.id for n in nations]
        assert "nation_player" in ids

    def test_iron_dominion_is_expansionist(self):
        gen = ScenarioGenerator(random.Random(42))
        nations = gen.generate_nations()
        iron = [n for n in nations if n.id == "nation_iron"][0]
        assert iron.behavior == "expansionist"

    def test_merchant_league_is_diplomatic(self):
        gen = ScenarioGenerator(random.Random(42))
        nations = gen.generate_nations()
        trade = [n for n in nations if n.id == "nation_trade"][0]
        assert trade.behavior == "diplomatic"


class TestTerritoryProperties:

    def test_each_territory_has_resources(self):
        gen = ScenarioGenerator(random.Random(42))
        territories = gen.generate_territories()
        for t in territories:
            assert len(t.resources) > 0

    def test_each_territory_has_population(self):
        gen = ScenarioGenerator(random.Random(42))
        territories = gen.generate_territories()
        for t in territories:
            assert t.population > 0

    def test_territories_assigned_to_nations(self):
        gen = ScenarioGenerator(random.Random(42))
        data = gen.generate_all()
        for n in data["nations"]:
            assert len(n.territories) > 0

    def test_5_territories_per_nation(self):
        gen = ScenarioGenerator(random.Random(42))
        data = gen.generate_all()
        for n in data["nations"]:
            assert len(n.territories) == 5


class TestCrisisEvents:

    def test_crisis_at_round_3(self):
        gen = ScenarioGenerator(random.Random(42))
        crises = gen.generate_crisis_events()
        assert 3 in crises
        assert crises[3]["type"] == "border_skirmish"

    def test_crisis_at_round_6(self):
        gen = ScenarioGenerator(random.Random(42))
        crises = gen.generate_crisis_events()
        assert 6 in crises
        assert crises[6]["type"] == "refugee_crisis"

    def test_all_crises_have_description(self):
        gen = ScenarioGenerator(random.Random(42))
        crises = gen.generate_crisis_events()
        for r, c in crises.items():
            assert "description" in c
            assert len(c["description"]) > 0
