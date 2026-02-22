"""Tests for trade_negotiation.scenario_generator -- deterministic generation."""

import random
import pytest
from simulations.trade_negotiation.scenario_generator import ScenarioGenerator


class TestDeterministicGeneration:
    def test_six_partners(self):
        rng = random.Random(42)
        gen = ScenarioGenerator(rng)
        data = gen.generate_all()
        assert len(data["partners"]) == 6

    def test_partner_ids(self):
        rng = random.Random(42)
        gen = ScenarioGenerator(rng)
        data = gen.generate_all()
        ids = [p.id for p in data["partners"]]
        assert "partner_01" in ids
        assert "partner_06" in ids

    def test_partner_development_levels(self):
        rng = random.Random(42)
        gen = ScenarioGenerator(rng)
        data = gen.generate_all()
        levels = {p.development_level for p in data["partners"]}
        assert "developed" in levels
        assert "emerging" in levels
        assert "developing" in levels

    def test_partner_economy_sizes(self):
        rng = random.Random(42)
        gen = ScenarioGenerator(rng)
        data = gen.generate_all()
        sizes = {p.economy_size for p in data["partners"]}
        assert "large" in sizes
        assert "medium" in sizes
        assert "small" in sizes

    def test_negotiations_for_each_partner(self):
        rng = random.Random(42)
        gen = ScenarioGenerator(rng)
        data = gen.generate_all()
        assert len(data["negotiations"]) == 6
        for pid, issues in data["negotiations"].items():
            assert len(issues) == 7  # 7 issue types

    def test_events_count(self):
        rng = random.Random(42)
        gen = ScenarioGenerator(rng)
        data = gen.generate_all()
        assert len(data["events"]) == 10

    def test_crises_count(self):
        rng = random.Random(42)
        gen = ScenarioGenerator(rng)
        data = gen.generate_all()
        assert len(data["crises"]) == 5

    def test_events_have_rounds(self):
        rng = random.Random(42)
        gen = ScenarioGenerator(rng)
        data = gen.generate_all()
        for ev in data["events"]:
            assert "round" in ev
            assert "description" in ev
            assert ev["round"] > 0

    def test_vulnerability_range(self):
        rng = random.Random(42)
        gen = ScenarioGenerator(rng)
        data = gen.generate_all()
        for p in data["partners"]:
            assert 0 <= p.vulnerability <= 100


class TestSeedReproducibility:
    def test_same_seed_same_partners(self):
        gen1 = ScenarioGenerator(random.Random(42))
        gen2 = ScenarioGenerator(random.Random(42))
        d1 = gen1.generate_all()
        d2 = gen2.generate_all()
        for p1, p2 in zip(d1["partners"], d2["partners"]):
            assert p1.id == p2.id
            assert p1.leverage == p2.leverage
            assert p1.vulnerability == p2.vulnerability

    def test_same_seed_same_negotiations(self):
        gen1 = ScenarioGenerator(random.Random(42))
        gen2 = ScenarioGenerator(random.Random(42))
        d1 = gen1.generate_all()
        d2 = gen2.generate_all()
        for pid in d1["negotiations"]:
            issues1 = d1["negotiations"][pid]
            issues2 = d2["negotiations"][pid]
            for i1, i2 in zip(issues1, issues2):
                assert i1.your_position == i2.your_position
                assert i1.partner_position == i2.partner_position

    def test_different_seed_different_output(self):
        gen1 = ScenarioGenerator(random.Random(42))
        gen2 = ScenarioGenerator(random.Random(99))
        d1 = gen1.generate_all()
        d2 = gen2.generate_all()
        # At least some leverage values should differ
        diffs = sum(1 for p1, p2 in zip(d1["partners"], d2["partners"])
                    if p1.leverage != p2.leverage)
        assert diffs > 0
