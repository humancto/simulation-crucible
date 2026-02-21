"""Tests for simulations/infrastructure_siege/scenario_generator.py."""

import random
import pytest
from simulations.infrastructure_siege.scenario_generator import ScenarioGenerator
from simulations.infrastructure_siege.models import (
    CascadeEvent, CityState, District, DistrictWealth,
    EmergencyTeam, EventSeverity, InfraSystem,
    SystemStatus, SystemType, TeamType,
)


@pytest.fixture
def gen():
    return ScenarioGenerator(random.Random(42))


# ── generate_districts ────────────────────────────────────────────────

class TestGenerateDistricts:

    def test_returns_list(self, gen):
        districts = gen.generate_districts()
        assert isinstance(districts, list)

    def test_district_count(self, gen):
        assert len(gen.generate_districts()) == 8

    def test_all_districts(self, gen):
        for d in gen.generate_districts():
            assert isinstance(d, District)

    def test_unique_ids(self, gen):
        ids = [d.id for d in gen.generate_districts()]
        assert len(ids) == len(set(ids))

    def test_has_affluent(self, gen):
        wealths = {d.wealth for d in gen.generate_districts()}
        assert DistrictWealth.AFFLUENT in wealths

    def test_has_middle_class(self, gen):
        wealths = {d.wealth for d in gen.generate_districts()}
        assert DistrictWealth.MIDDLE_CLASS in wealths

    def test_has_working_class(self, gen):
        wealths = {d.wealth for d in gen.generate_districts()}
        assert DistrictWealth.WORKING_CLASS in wealths

    def test_has_low_income(self, gen):
        wealths = {d.wealth for d in gen.generate_districts()}
        assert DistrictWealth.LOW_INCOME in wealths

    def test_has_hospitals(self, gen):
        hospitals = [d for d in gen.generate_districts() if d.has_hospital]
        assert len(hospitals) >= 2

    def test_has_elderly_care(self, gen):
        elderly = [d for d in gen.generate_districts() if d.has_elderly_care]
        assert len(elderly) >= 3

    def test_has_schools(self, gen):
        schools = [d for d in gen.generate_districts() if d.has_school]
        assert len(schools) >= 6

    def test_population_varies(self, gen):
        pops = {d.population for d in gen.generate_districts()}
        assert len(pops) > 3

    def test_no_services_initially(self, gen):
        for d in gen.generate_districts():
            assert d.power_restored is False
            assert d.water_restored is False

    def test_oakwood_is_affluent(self, gen):
        districts = gen.generate_districts()
        oakwood = [d for d in districts if d.id == "dist_oakwood"]
        assert len(oakwood) == 1
        assert oakwood[0].wealth == DistrictWealth.AFFLUENT

    def test_southgate_is_low_income(self, gen):
        districts = gen.generate_districts()
        sg = [d for d in districts if d.id == "dist_southgate"]
        assert len(sg) == 1
        assert sg[0].wealth == DistrictWealth.LOW_INCOME

    def test_southgate_has_hospital(self, gen):
        districts = gen.generate_districts()
        sg = [d for d in districts if d.id == "dist_southgate"]
        assert sg[0].has_hospital is True

    def test_deterministic(self):
        g1 = ScenarioGenerator(random.Random(99))
        g2 = ScenarioGenerator(random.Random(99))
        d1 = g1.generate_districts()
        d2 = g2.generate_districts()
        assert len(d1) == len(d2)
        for a, b in zip(d1, d2):
            assert a.id == b.id


# ── generate_systems ──────────────────────────────────────────────────

class TestGenerateSystems:

    def test_returns_list(self, gen):
        systems = gen.generate_systems()
        assert isinstance(systems, list)

    def test_system_count(self, gen):
        assert len(gen.generate_systems()) == 4

    def test_all_infra_systems(self, gen):
        for s in gen.generate_systems():
            assert isinstance(s, InfraSystem)

    def test_unique_ids(self, gen):
        ids = [s.id for s in gen.generate_systems()]
        assert len(ids) == len(set(ids))

    def test_has_power_grid(self, gen):
        types = {s.system_type for s in gen.generate_systems()}
        assert SystemType.POWER_GRID in types

    def test_has_water_treatment(self, gen):
        types = {s.system_type for s in gen.generate_systems()}
        assert SystemType.WATER_TREATMENT in types

    def test_has_traffic(self, gen):
        types = {s.system_type for s in gen.generate_systems()}
        assert SystemType.TRAFFIC in types

    def test_has_hospital_network(self, gen):
        types = {s.system_type for s in gen.generate_systems()}
        assert SystemType.HOSPITAL_NETWORK in types

    def test_all_compromised(self, gen):
        for s in gen.generate_systems():
            assert s.status == SystemStatus.COMPROMISED

    def test_integrity_below_50(self, gen):
        for s in gen.generate_systems():
            assert s.integrity < 50.0

    def test_not_safety_checked(self, gen):
        for s in gen.generate_systems():
            assert s.safety_checked is False

    def test_not_permanently_damaged(self, gen):
        for s in gen.generate_systems():
            assert s.permanently_damaged is False


# ── generate_teams ────────────────────────────────────────────────────

class TestGenerateTeams:

    def test_returns_list(self, gen):
        teams = gen.generate_teams()
        assert isinstance(teams, list)

    def test_team_count(self, gen):
        assert len(gen.generate_teams()) == 6

    def test_all_emergency_teams(self, gen):
        for t in gen.generate_teams():
            assert isinstance(t, EmergencyTeam)

    def test_unique_ids(self, gen):
        ids = [t.id for t in gen.generate_teams()]
        assert len(ids) == len(set(ids))

    def test_has_electrical(self, gen):
        types = {t.team_type for t in gen.generate_teams()}
        assert TeamType.ELECTRICAL in types

    def test_has_water(self, gen):
        types = {t.team_type for t in gen.generate_teams()}
        assert TeamType.WATER in types

    def test_has_cyber(self, gen):
        types = {t.team_type for t in gen.generate_teams()}
        assert TeamType.CYBER in types

    def test_has_medical(self, gen):
        types = {t.team_type for t in gen.generate_teams()}
        assert TeamType.MEDICAL in types

    def test_has_general(self, gen):
        types = {t.team_type for t in gen.generate_teams()}
        assert TeamType.GENERAL in types

    def test_all_available(self, gen):
        for t in gen.generate_teams():
            assert t.available is True

    def test_not_deployed(self, gen):
        for t in gen.generate_teams():
            assert t.deployed_to is None


# ── generate_events ───────────────────────────────────────────────────

class TestGenerateEvents:

    def test_returns_list(self, gen):
        events = gen.generate_events()
        assert isinstance(events, list)

    def test_event_count(self, gen):
        assert len(gen.generate_events()) >= 15

    def test_all_cascade_events(self, gen):
        for ev in gen.generate_events():
            assert isinstance(ev, CascadeEvent)

    def test_has_mandatory_events(self, gen):
        mandatory = [ev for ev in gen.generate_events() if ev.is_mandatory]
        assert len(mandatory) >= 10

    def test_first_hour_event(self, gen):
        events = gen.generate_events()
        hour1 = [ev for ev in events if ev.hour == 1]
        assert len(hour1) >= 1

    def test_last_hour_event(self, gen):
        events = gen.generate_events()
        hour72 = [ev for ev in events if ev.hour == 72]
        assert len(hour72) >= 1

    def test_cyberattack_event(self, gen):
        events = gen.generate_events()
        cyber = [ev for ev in events if "cyberattack" in ev.title.lower()]
        assert len(cyber) >= 1

    def test_hospital_event(self, gen):
        events = gen.generate_events()
        hosp = [ev for ev in events if "hospital" in ev.title.lower()]
        assert len(hosp) >= 1

    def test_water_event(self, gen):
        events = gen.generate_events()
        water = [ev for ev in events
                 if "water" in ev.title.lower()
                 or "contamination" in ev.title.lower()]
        assert len(water) >= 1

    def test_events_not_triggered(self, gen):
        for ev in gen.generate_events():
            assert ev.triggered is False

    def test_has_critical_events(self, gen):
        critical = [ev for ev in gen.generate_events()
                    if ev.severity == EventSeverity.CRITICAL]
        assert len(critical) >= 3


# ── generate_city_state ───────────────────────────────────────────────

class TestGenerateCityState:

    def test_returns_city_state(self, gen):
        s = gen.generate_city_state()
        assert isinstance(s, CityState)

    def test_initial_values(self, gen):
        s = gen.generate_city_state()
        assert s.systems_restored == 0
        assert s.public_confidence == 60.0
        assert s.casualties == 0
