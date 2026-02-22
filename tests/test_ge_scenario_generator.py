"""Tests for simulations/geoengineering/scenario_generator.py."""

import random
import pytest
from simulations.geoengineering.scenario_generator import ScenarioGenerator


class TestDeterministicGeneration:

    def test_same_seed_same_technologies(self):
        gen1 = ScenarioGenerator(random.Random(42))
        gen2 = ScenarioGenerator(random.Random(42))
        t1 = gen1.generate_technologies()
        t2 = gen2.generate_technologies()
        assert list(t1.keys()) == list(t2.keys())

    def test_same_seed_same_regions(self):
        gen1 = ScenarioGenerator(random.Random(42))
        gen2 = ScenarioGenerator(random.Random(42))
        r1 = gen1.generate_regions()
        r2 = gen2.generate_regions()
        assert list(r1.keys()) == list(r2.keys())

    def test_different_seed_same_structure(self):
        gen1 = ScenarioGenerator(random.Random(42))
        gen2 = ScenarioGenerator(random.Random(99))
        t1 = gen1.generate_technologies()
        t2 = gen2.generate_technologies()
        # Same structure regardless of seed
        assert len(t1) == len(t2) == 6


class TestTechnologies:

    def test_six_technologies(self):
        gen = ScenarioGenerator(random.Random(42))
        techs = gen.generate_technologies()
        assert len(techs) == 6

    def test_tech_types(self):
        gen = ScenarioGenerator(random.Random(42))
        techs = gen.generate_technologies()
        types = {t.tech_type for t in techs.values()}
        assert "aerosol" in types
        assert "cloud" in types
        assert "ocean" in types
        assert "space" in types
        assert "capture" in types

    def test_all_start_not_deployed(self):
        gen = ScenarioGenerator(random.Random(42))
        techs = gen.generate_technologies()
        for t in techs.values():
            assert t.deployment_ready is False
            assert t.regions_deployed == []


class TestRegions:

    def test_eight_regions(self):
        gen = ScenarioGenerator(random.Random(42))
        regions = gen.generate_regions()
        assert len(regions) == 8

    def test_region_names(self):
        gen = ScenarioGenerator(random.Random(42))
        regions = gen.generate_regions()
        expected = {
            "North America", "Europe", "China", "India",
            "Africa", "South America", "Small Island States",
            "Southeast Asia",
        }
        assert set(regions.keys()) == expected

    def test_vulnerability_varies(self):
        gen = ScenarioGenerator(random.Random(42))
        regions = gen.generate_regions()
        vulns = [r.climate_vulnerability for r in regions.values()]
        assert max(vulns) > 80
        assert min(vulns) < 30


class TestResearchProjects:

    def test_project_count(self):
        gen = ScenarioGenerator(random.Random(42))
        projects = gen.generate_research_projects()
        assert len(projects) == 6

    def test_projects_have_phases(self):
        gen = ScenarioGenerator(random.Random(42))
        projects = gen.generate_research_projects()
        for p in projects:
            assert p.phase in (1, 2, 3)


class TestCorporatePartners:

    def test_partner_count(self):
        gen = ScenarioGenerator(random.Random(42))
        partners = gen.generate_corporate_partners()
        assert len(partners) == 5

    def test_oversight_levels(self):
        gen = ScenarioGenerator(random.Random(42))
        partners = gen.generate_corporate_partners()
        levels = {p.oversight_level for p in partners}
        assert "minimal" in levels
        assert "moderate" in levels


class TestEvents:

    def test_events_generated(self):
        gen = ScenarioGenerator(random.Random(42))
        events = gen.generate_events()
        assert len(events) >= 10

    def test_events_span_years(self):
        gen = ScenarioGenerator(random.Random(42))
        events = gen.generate_events()
        years = [e["year"] for e in events]
        assert min(years) <= 3
        assert max(years) == 30


class TestGeoState:

    def test_initial_state(self):
        gen = ScenarioGenerator(random.Random(42))
        state = gen.generate_geo_state()
        assert state.year == 1
        assert state.budget == 50.0
        assert state.global_temperature_rise == 1.5
