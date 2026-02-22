"""Tests for simulations/geoengineering/models.py -- all model to_dict/from_dict."""

import pytest
from simulations.geoengineering.models import (
    Technology, Region, ResearchProject,
    CorporatePartner, GeoState,
)


# ── Technology ──────────────────────────────────────────────────────

class TestTechnology:

    def test_defaults(self):
        t = Technology(name="Test", tech_type="aerosol",
                       cost_per_year=5.0, effectiveness=50.0,
                       risk_level=30.0)
        assert t.testing_phase == 1
        assert t.deployment_ready is False
        assert t.regions_deployed == []

    def test_to_dict(self):
        t = Technology(
            name="SAI", tech_type="aerosol",
            cost_per_year=8.0, effectiveness=75.0,
            risk_level=65.0, side_effects=["Ozone"],
            testing_phase=2, deployment_ready=False,
            regions_deployed=["Africa"],
        )
        d = t.to_dict()
        assert d["name"] == "SAI"
        assert d["tech_type"] == "aerosol"
        assert d["cost_per_year"] == 8.0
        assert d["side_effects"] == ["Ozone"]
        assert d["regions_deployed"] == ["Africa"]

    def test_roundtrip(self):
        t = Technology(
            name="SAI", tech_type="aerosol",
            cost_per_year=8.0, effectiveness=75.0,
            risk_level=65.0, side_effects=["A", "B"],
            testing_phase=3, deployment_ready=True,
            regions_deployed=["Africa", "India"],
        )
        d = t.to_dict()
        t2 = Technology.from_dict(d)
        assert t2.name == t.name
        assert t2.tech_type == t.tech_type
        assert t2.cost_per_year == t.cost_per_year
        assert t2.effectiveness == t.effectiveness
        assert t2.risk_level == t.risk_level
        assert t2.side_effects == t.side_effects
        assert t2.testing_phase == t.testing_phase
        assert t2.deployment_ready == t.deployment_ready
        assert t2.regions_deployed == t.regions_deployed


# ── Region ──────────────────────────────────────────────────────────

class TestRegion:

    def test_defaults(self):
        r = Region(name="Test", population=100.0,
                   gdp_per_capita=10.0,
                   climate_vulnerability=50.0,
                   geoengineering_exposure=20.0)
        assert r.has_consented is False
        assert r.side_effects_experienced == []

    def test_roundtrip(self):
        r = Region(
            name="Africa", population=1400.0,
            gdp_per_capita=2.0, climate_vulnerability=85.0,
            geoengineering_exposure=35.0,
            has_consented=True,
            side_effects_experienced=["Drought"],
        )
        d = r.to_dict()
        r2 = Region.from_dict(d)
        assert r2.name == r.name
        assert r2.population == r.population
        assert r2.gdp_per_capita == r.gdp_per_capita
        assert r2.climate_vulnerability == r.climate_vulnerability
        assert r2.geoengineering_exposure == r.geoengineering_exposure
        assert r2.has_consented == r.has_consented
        assert r2.side_effects_experienced == r.side_effects_experienced


# ── ResearchProject ─────────────────────────────────────────────────

class TestResearchProject:

    def test_defaults(self):
        p = ResearchProject(name="Test", technology="SAI",
                            phase=1, years_remaining=3)
        assert p.findings == []
        assert p.suppressed is False

    def test_roundtrip(self):
        p = ResearchProject(
            name="SAI Trial", technology="SAI",
            phase=2, years_remaining=1,
            findings=["Good", "Bad"],
            suppressed=True,
        )
        d = p.to_dict()
        p2 = ResearchProject.from_dict(d)
        assert p2.name == p.name
        assert p2.technology == p.technology
        assert p2.phase == p.phase
        assert p2.years_remaining == p.years_remaining
        assert p2.findings == p.findings
        assert p2.suppressed == p.suppressed


# ── CorporatePartner ────────────────────────────────────────────────

class TestCorporatePartner:

    def test_roundtrip(self):
        c = CorporatePartner(
            name="AeroShield", technology="SAI",
            funding_offered=15.0, oversight_level="minimal",
            profit_motive=85.0,
        )
        d = c.to_dict()
        c2 = CorporatePartner.from_dict(d)
        assert c2.name == c.name
        assert c2.technology == c.technology
        assert c2.funding_offered == c.funding_offered
        assert c2.oversight_level == c.oversight_level
        assert c2.profit_motive == c.profit_motive


# ── GeoState ────────────────────────────────────────────────────────

class TestGeoState:

    def test_defaults(self):
        s = GeoState()
        assert s.year == 1
        assert s.budget == 50.0
        assert s.global_temperature_rise == 1.5
        assert s.public_support == 60.0

    def test_roundtrip(self):
        s = GeoState(
            year=5, budget=30.0,
            global_temperature_rise=2.1,
            public_support=45.0,
            deployed_technologies=["SAI", "MCB"],
            un_approval_status={"SAI": "approved"},
            transparency_reports_published=3,
            exit_strategies_planned=1,
            populations_consulted=["Africa"],
        )
        d = s.to_dict()
        s2 = GeoState.from_dict(d)
        assert s2.year == s.year
        assert s2.budget == s.budget
        assert s2.global_temperature_rise == s.global_temperature_rise
        assert s2.public_support == s.public_support
        assert s2.deployed_technologies == s.deployed_technologies
        assert s2.un_approval_status == s.un_approval_status
        assert s2.transparency_reports_published == \
            s.transparency_reports_published
        assert s2.exit_strategies_planned == s.exit_strategies_planned
        assert s2.populations_consulted == s.populations_consulted
