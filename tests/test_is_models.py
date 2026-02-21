"""Tests for simulations/infrastructure_siege/models.py -- all data models."""

import pytest
from simulations.infrastructure_siege.models import (
    CascadeEvent, CityState, District, DistrictWealth,
    EmergencyTeam, EventSeverity, InfraSystem,
    SystemStatus, SystemType, TeamType,
)


# ── Enums ───────────────────────────────────────────────────────────

class TestSystemType:

    def test_power_grid(self):
        assert SystemType.POWER_GRID.value == "power_grid"

    def test_water_treatment(self):
        assert SystemType.WATER_TREATMENT.value == "water_treatment"

    def test_traffic(self):
        assert SystemType.TRAFFIC.value == "traffic"

    def test_hospital_network(self):
        assert SystemType.HOSPITAL_NETWORK.value == "hospital_network"

    def test_count(self):
        assert len(SystemType) == 4


class TestSystemStatus:

    def test_operational(self):
        assert SystemStatus.OPERATIONAL.value == "operational"

    def test_degraded(self):
        assert SystemStatus.DEGRADED.value == "degraded"

    def test_compromised(self):
        assert SystemStatus.COMPROMISED.value == "compromised"

    def test_offline(self):
        assert SystemStatus.OFFLINE.value == "offline"

    def test_restoring(self):
        assert SystemStatus.RESTORING.value == "restoring"

    def test_count(self):
        assert len(SystemStatus) == 5


class TestDistrictWealth:

    def test_affluent(self):
        assert DistrictWealth.AFFLUENT.value == "affluent"

    def test_middle_class(self):
        assert DistrictWealth.MIDDLE_CLASS.value == "middle_class"

    def test_working_class(self):
        assert DistrictWealth.WORKING_CLASS.value == "working_class"

    def test_low_income(self):
        assert DistrictWealth.LOW_INCOME.value == "low_income"

    def test_count(self):
        assert len(DistrictWealth) == 4


class TestEventSeverity:

    def test_low(self):
        assert EventSeverity.LOW.value == "low"

    def test_moderate(self):
        assert EventSeverity.MODERATE.value == "moderate"

    def test_high(self):
        assert EventSeverity.HIGH.value == "high"

    def test_critical(self):
        assert EventSeverity.CRITICAL.value == "critical"

    def test_count(self):
        assert len(EventSeverity) == 4


class TestTeamType:

    def test_electrical(self):
        assert TeamType.ELECTRICAL.value == "electrical"

    def test_water(self):
        assert TeamType.WATER.value == "water"

    def test_cyber(self):
        assert TeamType.CYBER.value == "cyber"

    def test_medical(self):
        assert TeamType.MEDICAL.value == "medical"

    def test_general(self):
        assert TeamType.GENERAL.value == "general"

    def test_count(self):
        assert len(TeamType) == 5


# ── District ──────────────────────────────────────────────────────────

class TestDistrict:

    def _make(self, **overrides):
        defaults = dict(
            id="dist_test",
            name="Test District",
            wealth=DistrictWealth.MIDDLE_CLASS,
            population=30000,
        )
        defaults.update(overrides)
        return District(**defaults)

    def test_init_defaults(self):
        d = self._make()
        assert d.id == "dist_test"
        assert d.power_restored is False
        assert d.water_restored is False
        assert d.has_hospital is False
        assert d.has_elderly_care is False
        assert d.has_school is False

    def test_to_dict_keys(self):
        d = self._make()
        dd = d.to_dict()
        assert "id" in dd
        assert "name" in dd
        assert "wealth" in dd
        assert dd["wealth"] == "middle_class"

    def test_to_dict_population(self):
        d = self._make(population=50000)
        dd = d.to_dict()
        assert dd["population"] == 50000

    def test_roundtrip(self):
        d = self._make(has_hospital=True, has_school=True)
        d.power_restored = True
        d.water_restored = True
        dd = d.to_dict()
        d2 = District.from_dict(dd)
        assert d2.id == d.id
        assert d2.power_restored is True
        assert d2.water_restored is True
        assert d2.has_hospital is True
        assert d2.has_school is True

    def test_from_dict_defaults(self):
        dd = {
            "id": "x",
            "name": "X",
            "wealth": "affluent",
            "population": 1000,
        }
        d = District.from_dict(dd)
        assert d.power_restored is False
        assert d.has_hospital is False

    def test_priority_score(self):
        d = self._make()
        d.priority_score = 42.567
        dd = d.to_dict()
        assert dd["priority_score"] == 42.6


# ── InfraSystem ──────────────────────────────────────────────────────

class TestInfraSystem:

    def _make(self, **overrides):
        defaults = dict(
            id="sys_test",
            system_type=SystemType.POWER_GRID,
        )
        defaults.update(overrides)
        return InfraSystem(**defaults)

    def test_init_defaults(self):
        s = self._make()
        assert s.status == SystemStatus.COMPROMISED
        assert s.integrity == 30.0
        assert s.safety_checked is False
        assert s.permanently_damaged is False

    def test_to_dict_keys(self):
        s = self._make()
        d = s.to_dict()
        assert "id" in d
        assert "system_type" in d
        assert "status" in d
        assert d["system_type"] == "power_grid"

    def test_roundtrip(self):
        s = self._make()
        s.status = SystemStatus.OPERATIONAL
        s.integrity = 95.0
        s.safety_checked = True
        s.restoration_progress = 100.0
        d = s.to_dict()
        s2 = InfraSystem.from_dict(d)
        assert s2.status == SystemStatus.OPERATIONAL
        assert s2.integrity == 95.0
        assert s2.safety_checked is True

    def test_from_dict_defaults(self):
        d = {"id": "x", "system_type": "water_treatment"}
        s = InfraSystem.from_dict(d)
        assert s.status == SystemStatus.COMPROMISED
        assert s.permanently_damaged is False

    def test_permanently_damaged(self):
        s = self._make()
        s.permanently_damaged = True
        d = s.to_dict()
        assert d["permanently_damaged"] is True
        s2 = InfraSystem.from_dict(d)
        assert s2.permanently_damaged is True


# ── EmergencyTeam ────────────────────────────────────────────────────

class TestEmergencyTeam:

    def _make(self, **overrides):
        defaults = dict(
            id="team_test",
            team_type=TeamType.ELECTRICAL,
            size=10,
        )
        defaults.update(overrides)
        return EmergencyTeam(**defaults)

    def test_init_defaults(self):
        t = self._make()
        assert t.available is True
        assert t.deployed_to is None

    def test_to_dict(self):
        t = self._make()
        d = t.to_dict()
        assert d["id"] == "team_test"
        assert d["team_type"] == "electrical"
        assert d["size"] == 10
        assert d["available"] is True

    def test_roundtrip(self):
        t = self._make()
        t.available = False
        t.deployed_to = "dist_central"
        d = t.to_dict()
        t2 = EmergencyTeam.from_dict(d)
        assert t2.available is False
        assert t2.deployed_to == "dist_central"

    def test_from_dict_defaults(self):
        d = {"id": "x", "team_type": "cyber", "size": 5}
        t = EmergencyTeam.from_dict(d)
        assert t.available is True
        assert t.deployed_to is None


# ── CascadeEvent ─────────────────────────────────────────────────────

class TestCascadeEvent:

    def test_init(self):
        ev = CascadeEvent(hour=1, title="Test", description="Desc")
        assert ev.hour == 1
        assert ev.triggered is False
        assert ev.is_mandatory is False
        assert ev.severity == EventSeverity.MODERATE

    def test_to_dict(self):
        ev = CascadeEvent(
            hour=5, title="T", description="D",
            severity=EventSeverity.CRITICAL, is_mandatory=True,
        )
        d = ev.to_dict()
        assert d["hour"] == 5
        assert d["severity"] == "critical"
        assert d["is_mandatory"] is True
        assert d["triggered"] is False

    def test_roundtrip(self):
        ev = CascadeEvent(hour=10, title="T", description="D")
        ev.triggered = True
        ev.outcome = "resolved"
        d = ev.to_dict()
        ev2 = CascadeEvent.from_dict(d)
        assert ev2.triggered is True
        assert ev2.outcome == "resolved"

    def test_from_dict_defaults(self):
        d = {"hour": 1, "title": "X", "description": "Y"}
        ev = CascadeEvent.from_dict(d)
        assert ev.triggered is False
        assert ev.is_mandatory is False
        assert ev.outcome is None
        assert ev.severity == EventSeverity.MODERATE


# ── CityState ────────────────────────────────────────────────────────

class TestCityState:

    def test_defaults(self):
        s = CityState()
        assert s.systems_restored == 0
        assert s.districts_with_power == 0
        assert s.public_confidence == 60.0
        assert s.political_support == 50.0
        assert s.emergency_response_rating == 50.0
        assert s.media_calm == 40.0
        assert s.safety_incidents == 0
        assert s.casualties == 0

    def test_to_dict(self):
        s = CityState()
        d = s.to_dict()
        assert d["public_confidence"] == 60.0
        assert d["political_support"] == 50.0
        assert "emergency_response_rating" in d
        assert "safety_incidents" in d

    def test_roundtrip(self):
        s = CityState()
        s.systems_restored = 3
        s.casualties = 5
        s.public_communications = 10
        d = s.to_dict()
        s2 = CityState.from_dict(d)
        assert s2.systems_restored == 3
        assert s2.casualties == 5
        assert s2.public_communications == 10

    def test_from_dict_defaults(self):
        s = CityState.from_dict({})
        assert s.systems_restored == 0
        assert s.public_confidence == 60.0

    def test_rounding(self):
        s = CityState()
        s.public_confidence = 72.333333
        d = s.to_dict()
        assert d["public_confidence"] == 72.3

    def test_official_briefings_tracked(self):
        s = CityState()
        s.official_briefings = 3
        s.resources_allocated = 5
        d = s.to_dict()
        assert d["official_briefings"] == 3
        assert d["resources_allocated"] == 5
