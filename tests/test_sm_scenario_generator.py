"""Tests for simulations/space_mission/scenario_generator.py."""

import random
import pytest
from simulations.space_mission.scenario_generator import ScenarioGenerator
from simulations.space_mission.models import (
    CrewMember, CrewRole, CrewStatus,
    SystemStatus, SystemName,
    Resource, DailyEvent, MissionState,
)


@pytest.fixture
def gen():
    return ScenarioGenerator(random.Random(42))


# ── generate_crew ──────────────────────────────────────────────────

class TestGenerateCrew:

    def test_returns_list(self, gen):
        crew = gen.generate_crew()
        assert isinstance(crew, list)

    def test_crew_count(self, gen):
        assert len(gen.generate_crew()) == 6

    def test_all_crew_members(self, gen):
        for c in gen.generate_crew():
            assert isinstance(c, CrewMember)

    def test_unique_ids(self, gen):
        ids = [c.id for c in gen.generate_crew()]
        assert len(ids) == len(set(ids))

    def test_has_commander(self, gen):
        roles = {c.role for c in gen.generate_crew()}
        assert CrewRole.COMMANDER in roles

    def test_has_pilot(self, gen):
        roles = {c.role for c in gen.generate_crew()}
        assert CrewRole.PILOT in roles

    def test_has_engineer(self, gen):
        roles = {c.role for c in gen.generate_crew()}
        assert CrewRole.ENGINEER in roles

    def test_has_medical_officer(self, gen):
        roles = {c.role for c in gen.generate_crew()}
        assert CrewRole.MEDICAL_OFFICER in roles

    def test_has_scientist(self, gen):
        roles = {c.role for c in gen.generate_crew()}
        assert CrewRole.SCIENTIST in roles

    def test_has_mission_specialist(self, gen):
        roles = {c.role for c in gen.generate_crew()}
        assert CrewRole.MISSION_SPECIALIST in roles

    def test_commander_exists(self, gen):
        ids = {c.id for c in gen.generate_crew()}
        assert "crew_commander" in ids

    def test_medical_exists(self, gen):
        ids = {c.id for c in gen.generate_crew()}
        assert "crew_medical" in ids

    def test_specialist_exists(self, gen):
        ids = {c.id for c in gen.generate_crew()}
        assert "crew_specialist" in ids

    def test_medical_has_priority(self, gen):
        crew = gen.generate_crew()
        med = [c for c in crew if c.id == "crew_medical"]
        assert len(med) == 1
        assert med[0].medical_priority is True

    def test_two_in_damaged_section(self, gen):
        crew = gen.generate_crew()
        in_damaged = [c for c in crew if c.in_damaged_section]
        assert len(in_damaged) == 2

    def test_all_healthy_initially(self, gen):
        for c in gen.generate_crew():
            assert c.status == CrewStatus.HEALTHY

    def test_deterministic(self):
        g1 = ScenarioGenerator(random.Random(99))
        g2 = ScenarioGenerator(random.Random(99))
        c1 = g1.generate_crew()
        c2 = g2.generate_crew()
        assert len(c1) == len(c2)
        for a, b in zip(c1, c2):
            assert a.id == b.id


# ── generate_systems ──────────────────────────────────────────────

class TestGenerateSystems:

    def test_returns_list(self, gen):
        systems = gen.generate_systems()
        assert isinstance(systems, list)

    def test_system_count(self, gen):
        assert len(gen.generate_systems()) == 5

    def test_all_system_status(self, gen):
        for s in gen.generate_systems():
            assert isinstance(s, SystemStatus)

    def test_has_life_support(self, gen):
        names = {s.name for s in gen.generate_systems()}
        assert SystemName.LIFE_SUPPORT in names

    def test_has_communications(self, gen):
        names = {s.name for s in gen.generate_systems()}
        assert SystemName.COMMUNICATIONS in names

    def test_has_navigation(self, gen):
        names = {s.name for s in gen.generate_systems()}
        assert SystemName.NAVIGATION in names

    def test_has_power(self, gen):
        names = {s.name for s in gen.generate_systems()}
        assert SystemName.POWER in names

    def test_has_propulsion(self, gen):
        names = {s.name for s in gen.generate_systems()}
        assert SystemName.PROPULSION in names

    def test_life_support_damaged(self, gen):
        systems = gen.generate_systems()
        ls = [s for s in systems if s.name == SystemName.LIFE_SUPPORT]
        assert len(ls) == 1
        assert ls[0].integrity < 50

    def test_critical_systems_exist(self, gen):
        systems = gen.generate_systems()
        critical = [s for s in systems if s.is_critical]
        assert len(critical) >= 2

    def test_all_below_100(self, gen):
        for s in gen.generate_systems():
            assert s.integrity < 100


# ── generate_resources ────────────────────────────────────────────

class TestGenerateResources:

    def test_returns_list(self, gen):
        resources = gen.generate_resources()
        assert isinstance(resources, list)

    def test_resource_count(self, gen):
        assert len(gen.generate_resources()) == 5

    def test_all_resources(self, gen):
        for r in gen.generate_resources():
            assert isinstance(r, Resource)

    def test_has_oxygen(self, gen):
        names = {r.name for r in gen.generate_resources()}
        assert "oxygen" in names

    def test_has_water(self, gen):
        names = {r.name for r in gen.generate_resources()}
        assert "water" in names

    def test_has_food(self, gen):
        names = {r.name for r in gen.generate_resources()}
        assert "food" in names

    def test_has_medical_supplies(self, gen):
        names = {r.name for r in gen.generate_resources()}
        assert "medical_supplies" in names

    def test_has_power_cells(self, gen):
        names = {r.name for r in gen.generate_resources()}
        assert "power_cells" in names

    def test_current_below_max(self, gen):
        for r in gen.generate_resources():
            assert r.current <= r.maximum

    def test_default_ration_level(self, gen):
        for r in gen.generate_resources():
            assert r.ration_level == 1.0

    def test_positive_daily_usage(self, gen):
        for r in gen.generate_resources():
            assert r.daily_usage > 0


# ── generate_events ───────────────────────────────────────────────

class TestGenerateEvents:

    def test_returns_list(self, gen):
        events = gen.generate_events()
        assert isinstance(events, list)

    def test_event_count(self, gen):
        assert len(gen.generate_events()) >= 15

    def test_all_daily_events(self, gen):
        for ev in gen.generate_events():
            assert isinstance(ev, DailyEvent)

    def test_has_mandatory_events(self, gen):
        mandatory = [ev for ev in gen.generate_events() if ev.is_mandatory]
        assert len(mandatory) >= 10

    def test_first_day_event(self, gen):
        events = gen.generate_events()
        day1 = [ev for ev in events if ev.day == 1]
        assert len(day1) >= 1

    def test_last_day_event(self, gen):
        events = gen.generate_events()
        day30 = [ev for ev in events if ev.day == 30]
        assert len(day30) >= 1

    def test_radiation_event(self, gen):
        events = gen.generate_events()
        radiation = [ev for ev in events
                     if "radiation" in ev.title.lower()
                     or "solar" in ev.title.lower()]
        assert len(radiation) >= 1

    def test_medical_event(self, gen):
        events = gen.generate_events()
        medical = [ev for ev in events
                   if "medical" in ev.title.lower()
                   or "patel" in ev.description.lower()]
        assert len(medical) >= 1

    def test_navigation_event(self, gen):
        events = gen.generate_events()
        nav = [ev for ev in events
               if "navigation" in ev.title.lower()]
        assert len(nav) >= 1

    def test_crew_confrontation_event(self, gen):
        events = gen.generate_events()
        conf = [ev for ev in events
                if "confrontation" in ev.title.lower()
                or "morale" in ev.description.lower()]
        assert len(conf) >= 1

    def test_events_not_triggered(self, gen):
        for ev in gen.generate_events():
            assert ev.triggered is False


# ── generate_mission_state ────────────────────────────────────────

class TestGenerateMissionState:

    def test_returns_mission_state(self, gen):
        s = gen.generate_mission_state()
        assert isinstance(s, MissionState)

    def test_initial_values(self, gen):
        s = gen.generate_mission_state()
        assert s.mission_day == 180
        assert s.crew_morale == 50.0
        assert s.mission_aborted is False
