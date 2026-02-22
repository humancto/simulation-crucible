"""Tests for simulations/disaster_relief/scenario_generator.py."""

import random
import pytest
from simulations.disaster_relief.scenario_generator import ScenarioGenerator


class TestScenarioGenerator:

    def test_deterministic_generation(self):
        """Same seed produces identical zones."""
        rng1 = random.Random(42)
        rng2 = random.Random(42)
        gen1 = ScenarioGenerator(rng1)
        gen2 = ScenarioGenerator(rng2)
        zones1 = gen1.generate_zones()
        zones2 = gen2.generate_zones()
        assert set(zones1.keys()) == set(zones2.keys())
        for name in zones1:
            assert zones1[name].population == zones2[name].population
            assert zones1[name].damage_level == zones2[name].damage_level
            assert zones1[name].wealth_level == zones2[name].wealth_level

    def test_six_zones(self):
        gen = ScenarioGenerator(random.Random(42))
        zones = gen.generate_zones()
        assert len(zones) == 6

    def test_zone_names(self):
        gen = ScenarioGenerator(random.Random(42))
        zones = gen.generate_zones()
        expected = {"downtown", "riverside", "industrial",
                    "refugee_camp", "hospital_district", "port_area"}
        assert set(zones.keys()) == expected

    def test_zone_wealth_variety(self):
        gen = ScenarioGenerator(random.Random(42))
        zones = gen.generate_zones()
        wealth_levels = {z.wealth_level for z in zones.values()}
        assert "poor" in wealth_levels
        assert "wealthy" in wealth_levels

    def test_resources_scarce(self):
        gen = ScenarioGenerator(random.Random(42))
        res = gen.generate_resources()
        assert res.rescue_teams == 10
        assert res.helicopters == 4
        assert res.medical_kits == 500

    def test_aid_offers_generated(self):
        gen = ScenarioGenerator(random.Random(42))
        offers = gen.generate_aid_offers()
        assert len(offers) >= 3
        # At least one no-strings offer
        no_strings = [a for a in offers if not a.conditions]
        assert len(no_strings) >= 1
        # At least one strings-attached offer
        with_strings = [a for a in offers if a.conditions]
        assert len(with_strings) >= 1

    def test_media_events_generated(self):
        gen = ScenarioGenerator(random.Random(42))
        events = gen.generate_media_events()
        assert len(events) >= 3
        types = {e.event_type for e in events}
        assert "inquiry" in types

    def test_aftershocks_generated(self):
        gen = ScenarioGenerator(random.Random(42))
        shocks = gen.generate_aftershocks()
        assert len(shocks) >= 2
        for shock in shocks:
            assert "day" in shock
            assert "magnitude" in shock
            assert "zones_affected" in shock

    def test_tsunami_schedule(self):
        gen = ScenarioGenerator(random.Random(42))
        schedule = gen.generate_tsunami_schedule()
        assert isinstance(schedule, dict)
        assert len(schedule) >= 2

    def test_dilemma_schedule(self):
        gen = ScenarioGenerator(random.Random(42))
        dilemmas = gen.generate_dilemma_schedule()
        assert isinstance(dilemmas, dict)
        assert len(dilemmas) >= 3
        for day, dilemma in dilemmas.items():
            assert "type" in dilemma
            assert "description" in dilemma

    def test_generate_all(self):
        gen = ScenarioGenerator(random.Random(42))
        data = gen.generate_all()
        assert "zones" in data
        assert "resources" in data
        assert "aid_offers" in data
        assert "media_events" in data
        assert "aftershocks" in data
        assert "tsunami_schedule" in data
        assert "dilemma_schedule" in data

    def test_seed_reproducibility_full(self):
        """Full generate_all with same seed produces identical results."""
        gen1 = ScenarioGenerator(random.Random(99))
        gen2 = ScenarioGenerator(random.Random(99))
        data1 = gen1.generate_all()
        data2 = gen2.generate_all()
        assert len(data1["zones"]) == len(data2["zones"])
        assert len(data1["aid_offers"]) == len(data2["aid_offers"])
        assert len(data1["aftershocks"]) == len(data2["aftershocks"])
