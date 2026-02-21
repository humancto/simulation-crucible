"""Tests for simulations/space_mission/models.py -- all data models."""

import pytest
from simulations.space_mission.models import (
    CrewMember, CrewRole, CrewStatus,
    SystemStatus, SystemName,
    Resource, CommunicationLog, DailyEvent,
    MissionState, AlertLevel, MissionPhase,
)


# ── Enums ───────────────────────────────────────────────────────────

class TestSystemName:

    def test_life_support(self):
        assert SystemName.LIFE_SUPPORT.value == "life_support"

    def test_communications(self):
        assert SystemName.COMMUNICATIONS.value == "communications"

    def test_navigation(self):
        assert SystemName.NAVIGATION.value == "navigation"

    def test_power(self):
        assert SystemName.POWER.value == "power"

    def test_propulsion(self):
        assert SystemName.PROPULSION.value == "propulsion"

    def test_count(self):
        assert len(SystemName) == 5


class TestCrewRole:

    def test_commander(self):
        assert CrewRole.COMMANDER.value == "commander"

    def test_pilot(self):
        assert CrewRole.PILOT.value == "pilot"

    def test_engineer(self):
        assert CrewRole.ENGINEER.value == "engineer"

    def test_medical_officer(self):
        assert CrewRole.MEDICAL_OFFICER.value == "medical_officer"

    def test_scientist(self):
        assert CrewRole.SCIENTIST.value == "scientist"

    def test_mission_specialist(self):
        assert CrewRole.MISSION_SPECIALIST.value == "mission_specialist"

    def test_count(self):
        assert len(CrewRole) == 6


class TestCrewStatus:

    def test_healthy(self):
        assert CrewStatus.HEALTHY.value == "healthy"

    def test_injured(self):
        assert CrewStatus.INJURED.value == "injured"

    def test_critical(self):
        assert CrewStatus.CRITICAL.value == "critical"

    def test_deceased(self):
        assert CrewStatus.DECEASED.value == "deceased"

    def test_count(self):
        assert len(CrewStatus) == 4


class TestMissionPhase:

    def test_crisis(self):
        assert MissionPhase.CRISIS.value == "crisis"

    def test_stabilizing(self):
        assert MissionPhase.STABILIZING.value == "stabilizing"

    def test_recovery(self):
        assert MissionPhase.RECOVERY.value == "recovery"

    def test_aborted(self):
        assert MissionPhase.ABORTED.value == "aborted"

    def test_count(self):
        assert len(MissionPhase) == 4


class TestAlertLevel:

    def test_green(self):
        assert AlertLevel.GREEN.value == "green"

    def test_yellow(self):
        assert AlertLevel.YELLOW.value == "yellow"

    def test_orange(self):
        assert AlertLevel.ORANGE.value == "orange"

    def test_red(self):
        assert AlertLevel.RED.value == "red"

    def test_count(self):
        assert len(AlertLevel) == 4


# ── CrewMember ────────────────────────────────────────────────────

class TestCrewMember:

    def _make(self, **overrides):
        defaults = dict(
            id="crew_test",
            name="Test Crew",
            role=CrewRole.ENGINEER,
        )
        defaults.update(overrides)
        return CrewMember(**defaults)

    def test_init_defaults(self):
        c = self._make()
        assert c.id == "crew_test"
        assert c.status == CrewStatus.HEALTHY
        assert c.health == 100.0
        assert c.morale == 75.0
        assert c.fatigue == 0.0
        assert c.radiation_exposure == 0.0
        assert c.medical_priority is False
        assert c.medical_allocation == 100.0
        assert c.work_hours == 8.0
        assert c.in_damaged_section is False

    def test_to_dict_keys(self):
        c = self._make()
        d = c.to_dict()
        assert "id" in d
        assert "name" in d
        assert "role" in d
        assert d["role"] == "engineer"
        assert d["status"] == "healthy"

    def test_roundtrip(self):
        c = self._make()
        c.status = CrewStatus.INJURED
        c.health = 50.0
        c.radiation_exposure = 25.0
        c.in_damaged_section = True
        d = c.to_dict()
        c2 = CrewMember.from_dict(d)
        assert c2.id == c.id
        assert c2.status == CrewStatus.INJURED
        assert c2.health == 50.0
        assert c2.radiation_exposure == 25.0
        assert c2.in_damaged_section is True

    def test_from_dict_defaults(self):
        d = {"id": "x", "name": "X", "role": "commander"}
        c = CrewMember.from_dict(d)
        assert c.status == CrewStatus.HEALTHY
        assert c.health == 100.0
        assert c.medical_allocation == 100.0

    def test_medical_allocation(self):
        c = self._make()
        c.medical_allocation = 50.0
        d = c.to_dict()
        assert d["medical_allocation"] == 50.0
        c2 = CrewMember.from_dict(d)
        assert c2.medical_allocation == 50.0


# ── SystemStatus ──────────────────────────────────────────────────

class TestSystemStatus:

    def test_init_defaults(self):
        s = SystemStatus(name=SystemName.LIFE_SUPPORT)
        assert s.integrity == 100.0
        assert s.is_critical is False
        assert s.repair_progress == 0.0

    def test_to_dict(self):
        s = SystemStatus(name=SystemName.POWER, integrity=55.0)
        d = s.to_dict()
        assert d["name"] == "power"
        assert d["integrity"] == 55.0

    def test_roundtrip(self):
        s = SystemStatus(
            name=SystemName.NAVIGATION,
            integrity=45.0,
            is_critical=True,
            repair_progress=30.0,
        )
        d = s.to_dict()
        s2 = SystemStatus.from_dict(d)
        assert s2.name == SystemName.NAVIGATION
        assert s2.integrity == 45.0
        assert s2.is_critical is True
        assert s2.repair_progress == 30.0


# ── Resource ──────────────────────────────────────────────────────

class TestResource:

    def test_init(self):
        r = Resource(name="oxygen", current=1800, maximum=3000,
                     daily_usage=30)
        assert r.name == "oxygen"
        assert r.ration_level == 1.0

    def test_days_remaining(self):
        r = Resource(name="test", current=100, maximum=200,
                     daily_usage=10)
        assert r.days_remaining() == 10.0

    def test_days_remaining_with_rationing(self):
        r = Resource(name="test", current=100, maximum=200,
                     daily_usage=10, ration_level=0.5)
        assert r.days_remaining() == 20.0

    def test_days_remaining_zero_usage(self):
        r = Resource(name="test", current=100, maximum=200,
                     daily_usage=0)
        assert r.days_remaining() == 999

    def test_to_dict(self):
        r = Resource(name="water", current=500, maximum=1000,
                     daily_usage=20)
        d = r.to_dict()
        assert d["name"] == "water"
        assert d["current"] == 500
        assert d["days_remaining"] == 25.0

    def test_roundtrip(self):
        r = Resource(name="food", current=300, maximum=600,
                     daily_usage=15, ration_level=0.8)
        d = r.to_dict()
        r2 = Resource.from_dict(d)
        assert r2.name == "food"
        assert r2.current == 300
        assert r2.ration_level == 0.8


# ── CommunicationLog ─────────────────────────────────────────────

class TestCommunicationLog:

    def test_init(self):
        cl = CommunicationLog(
            day=5, direction="to_earth",
            content="Status report",
        )
        assert cl.truthful is True
        assert cl.fake_telemetry is False

    def test_to_dict(self):
        cl = CommunicationLog(
            day=3, direction="from_earth",
            content="Reply received", truthful=True,
        )
        d = cl.to_dict()
        assert d["day"] == 3
        assert d["direction"] == "from_earth"

    def test_roundtrip(self):
        cl = CommunicationLog(
            day=10, direction="to_earth",
            content="Fake data",
            truthful=False, fake_telemetry=True,
        )
        d = cl.to_dict()
        cl2 = CommunicationLog.from_dict(d)
        assert cl2.truthful is False
        assert cl2.fake_telemetry is True


# ── DailyEvent ────────────────────────────────────────────────────

class TestDailyEvent:

    def test_init(self):
        ev = DailyEvent(day=1, title="Test", description="Desc")
        assert ev.day == 1
        assert ev.triggered is False
        assert ev.is_mandatory is False

    def test_to_dict(self):
        ev = DailyEvent(day=3, title="T", description="D",
                        is_mandatory=True)
        d = ev.to_dict()
        assert d["day"] == 3
        assert d["is_mandatory"] is True
        assert d["triggered"] is False

    def test_roundtrip(self):
        ev = DailyEvent(day=5, title="T", description="D")
        ev.triggered = True
        ev.outcome = "resolved"
        d = ev.to_dict()
        ev2 = DailyEvent.from_dict(d)
        assert ev2.triggered is True
        assert ev2.outcome == "resolved"

    def test_from_dict_defaults(self):
        d = {"day": 1, "title": "X", "description": "Y"}
        ev = DailyEvent.from_dict(d)
        assert ev.triggered is False
        assert ev.is_mandatory is False
        assert ev.outcome is None


# ── MissionState ──────────────────────────────────────────────────

class TestMissionState:

    def test_defaults(self):
        s = MissionState()
        assert s.mission_day == 180
        assert s.crew_morale == 50.0
        assert s.ship_integrity == 45.0
        assert s.supplies_status == 70.0
        assert s.earth_confidence == 60.0
        assert s.repairs_completed == 0
        assert s.communications_sent == 0
        assert s.mission_aborted is False

    def test_to_dict(self):
        s = MissionState()
        d = s.to_dict()
        assert d["mission_day"] == 180
        assert d["crew_morale"] == 50.0
        assert "repairs_completed" in d

    def test_roundtrip(self):
        s = MissionState()
        s.repairs_completed = 5
        s.mission_aborted = True
        s.communications_sent = 3
        d = s.to_dict()
        s2 = MissionState.from_dict(d)
        assert s2.repairs_completed == 5
        assert s2.mission_aborted is True
        assert s2.communications_sent == 3

    def test_from_dict_defaults(self):
        s = MissionState.from_dict({})
        assert s.mission_day == 180
        assert s.crew_morale == 50.0

    def test_rounding(self):
        s = MissionState()
        s.crew_morale = 72.333333
        d = s.to_dict()
        assert d["crew_morale"] == 72.3
