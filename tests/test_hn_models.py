"""Tests for simulations/hostage_negotiator/models.py -- all data models."""

import pytest
from simulations.hostage_negotiator.models import (
    CrisisPhase, HostageCondition, CommunicationTone, ConcessionType,
    ResolutionType, Hostage, Suspect, SwatCommander, MediaPresence,
    HourlyEvent, NegotiationState,
)


# ── Enums ───────────────────────────────────────────────────────────

class TestCrisisPhase:

    def test_initial_contact(self):
        assert CrisisPhase.INITIAL_CONTACT.value == "initial_contact"

    def test_rapport_building(self):
        assert CrisisPhase.RAPPORT_BUILDING.value == "rapport_building"

    def test_escalation(self):
        assert CrisisPhase.ESCALATION.value == "escalation"

    def test_breakdown(self):
        assert CrisisPhase.BREAKDOWN.value == "breakdown"

    def test_new_information(self):
        assert CrisisPhase.NEW_INFORMATION.value == "new_information"

    def test_resolution(self):
        assert CrisisPhase.RESOLUTION.value == "resolution"

    def test_count(self):
        assert len(CrisisPhase) == 6


class TestHostageCondition:

    def test_healthy(self):
        assert HostageCondition.HEALTHY.value == "healthy"

    def test_stressed(self):
        assert HostageCondition.STRESSED.value == "stressed"

    def test_injured(self):
        assert HostageCondition.INJURED.value == "injured"

    def test_critical(self):
        assert HostageCondition.CRITICAL.value == "critical"

    def test_released(self):
        assert HostageCondition.RELEASED.value == "released"

    def test_deceased(self):
        assert HostageCondition.DECEASED.value == "deceased"

    def test_count(self):
        assert len(HostageCondition) == 6


class TestCommunicationTone:

    def test_empathetic(self):
        assert CommunicationTone.EMPATHETIC.value == "empathetic"

    def test_neutral(self):
        assert CommunicationTone.NEUTRAL.value == "neutral"

    def test_firm(self):
        assert CommunicationTone.FIRM.value == "firm"

    def test_aggressive(self):
        assert CommunicationTone.AGGRESSIVE.value == "aggressive"

    def test_count(self):
        assert len(CommunicationTone) == 4


class TestConcessionType:

    def test_food(self):
        assert ConcessionType.FOOD.value == "food"

    def test_water(self):
        assert ConcessionType.WATER.value == "water"

    def test_medical(self):
        assert ConcessionType.MEDICAL.value == "medical"

    def test_phone_call(self):
        assert ConcessionType.PHONE_CALL.value == "phone_call"

    def test_media_access(self):
        assert ConcessionType.MEDIA_ACCESS.value == "media_access"

    def test_count(self):
        assert len(ConcessionType) == 5


class TestResolutionType:

    def test_peaceful(self):
        assert ResolutionType.PEACEFUL_SURRENDER.value == "peaceful_surrender"

    def test_tactical(self):
        assert ResolutionType.TACTICAL_ENTRY.value == "tactical_entry"

    def test_escape(self):
        assert ResolutionType.SUSPECT_ESCAPE.value == "suspect_escape"

    def test_ongoing(self):
        assert ResolutionType.ONGOING.value == "ongoing"

    def test_count(self):
        assert len(ResolutionType) == 4


# ── Hostage ─────────────────────────────────────────────────────────

class TestHostage:

    def test_create_basic(self):
        h = Hostage(id="h01", name="Alice", age=30, occupation="Teacher")
        assert h.name == "Alice"
        assert h.age == 30
        assert h.condition == HostageCondition.HEALTHY

    def test_defaults(self):
        h = Hostage(id="h01", name="Alice", age=30, occupation="Teacher")
        assert h.has_medical_issue is False
        assert h.released is False
        assert h.hour_released == -1
        assert h.medical_details == ""

    def test_to_dict(self):
        h = Hostage(id="h01", name="Alice", age=30, occupation="Teacher")
        d = h.to_dict()
        assert d["id"] == "h01"
        assert d["name"] == "Alice"
        assert d["condition"] == "healthy"
        assert d["released"] is False

    def test_from_dict(self):
        d = {
            "id": "h02", "name": "Bob", "age": 65,
            "occupation": "Retired", "condition": "injured",
            "has_medical_issue": True, "medical_details": "Heart",
            "released": False, "hour_released": -1,
        }
        h = Hostage.from_dict(d)
        assert h.name == "Bob"
        assert h.condition == HostageCondition.INJURED
        assert h.has_medical_issue is True

    def test_roundtrip(self):
        h = Hostage(
            id="h03", name="Carol", age=8,
            occupation="Child",
            has_medical_issue=True,
            medical_details="Asthma",
        )
        h.condition = HostageCondition.STRESSED
        h.released = True
        h.hour_released = 5
        d = h.to_dict()
        h2 = Hostage.from_dict(d)
        assert h2.name == "Carol"
        assert h2.condition == HostageCondition.STRESSED
        assert h2.released is True
        assert h2.hour_released == 5
        assert h2.medical_details == "Asthma"

    def test_from_dict_defaults(self):
        d = {"id": "h04", "name": "Dan", "age": 40, "occupation": "Clerk"}
        h = Hostage.from_dict(d)
        assert h.condition == HostageCondition.HEALTHY
        assert h.has_medical_issue is False


# ── Suspect ─────────────────────────────────────────────────────────

class TestSuspect:

    def test_create(self):
        s = Suspect(name="Daniel", age=38, backstory="Lost custody")
        assert s.name == "Daniel"
        assert s.trust_level == 30.0
        assert s.agitation_level == 60.0

    def test_defaults(self):
        s = Suspect(name="Daniel", age=38, backstory="Test")
        assert s.has_criminal_history is False
        assert s.is_desperate is True
        assert s.armed is True
        assert s.weapon_type == "handgun"
        assert s.has_harmed_hostage is False
        assert s.surrendered is False
        assert s.demands == []
        assert s.promises_made == []

    def test_to_dict(self):
        s = Suspect(
            name="Daniel", age=38, backstory="Test",
            demands=["cash", "vehicle"],
        )
        d = s.to_dict()
        assert d["name"] == "Daniel"
        assert d["trust_level"] == 30.0
        assert d["demands"] == ["cash", "vehicle"]

    def test_from_dict(self):
        d = {
            "name": "Daniel", "age": 38, "backstory": "Test",
            "demands": ["cash"], "trust_level": 55.0,
            "agitation_level": 40.0, "surrendered": True,
        }
        s = Suspect.from_dict(d)
        assert s.trust_level == 55.0
        assert s.agitation_level == 40.0
        assert s.surrendered is True

    def test_roundtrip(self):
        s = Suspect(name="Daniel", age=38, backstory="Story")
        s.trust_level = 75.0
        s.agitation_level = 25.0
        s.promises_made = ["food", "call"]
        s.promises_broken = ["food"]
        d = s.to_dict()
        s2 = Suspect.from_dict(d)
        assert s2.trust_level == 75.0
        assert s2.promises_broken == ["food"]


# ── SwatCommander ───────────────────────────────────────────────────

class TestSwatCommander:

    def test_defaults(self):
        sc = SwatCommander()
        assert sc.name == "Commander Reeves"
        assert sc.patience == 70.0
        assert sc.push_for_entry is False
        assert sc.tactical_ready is True

    def test_to_dict(self):
        sc = SwatCommander()
        d = sc.to_dict()
        assert d["name"] == "Commander Reeves"
        assert d["patience"] == 70.0

    def test_from_dict(self):
        d = {"name": "Cmdr Test", "patience": 30.0,
             "push_for_entry": True, "entry_recommended_hour": 10,
             "tactical_ready": True}
        sc = SwatCommander.from_dict(d)
        assert sc.patience == 30.0
        assert sc.push_for_entry is True

    def test_roundtrip(self):
        sc = SwatCommander()
        sc.patience = 15.0
        sc.push_for_entry = True
        sc.entry_recommended_hour = 12
        d = sc.to_dict()
        sc2 = SwatCommander.from_dict(d)
        assert sc2.patience == 15.0
        assert sc2.entry_recommended_hour == 12


# ── MediaPresence ───────────────────────────────────────────────────

class TestMediaPresence:

    def test_defaults(self):
        m = MediaPresence()
        assert m.outlets_present == 8
        assert m.public_sentiment == 50.0
        assert m.leaks_count == 0

    def test_to_dict(self):
        m = MediaPresence()
        d = m.to_dict()
        assert d["outlets_present"] == 8
        assert d["public_sentiment"] == 50.0

    def test_from_dict(self):
        d = {"outlets_present": 12, "public_sentiment": 75.0,
             "coverage_intensity": 80.0, "leaks_count": 3,
             "briefings_given": 5, "honest_briefings": 3,
             "dishonest_briefings": 2}
        m = MediaPresence.from_dict(d)
        assert m.outlets_present == 12
        assert m.leaks_count == 3
        assert m.honest_briefings == 3

    def test_roundtrip(self):
        m = MediaPresence()
        m.leaks_count = 5
        m.public_sentiment = 80.0
        d = m.to_dict()
        m2 = MediaPresence.from_dict(d)
        assert m2.leaks_count == 5
        assert m2.public_sentiment == 80.0


# ── HourlyEvent ─────────────────────────────────────────────────────

class TestHourlyEvent:

    def test_create(self):
        ev = HourlyEvent(hour=0, title="Start", description="Crisis begins")
        assert ev.hour == 0
        assert ev.triggered is False

    def test_to_dict(self):
        ev = HourlyEvent(hour=5, title="Backstory",
                          description="Details emerge",
                          is_mandatory=True)
        d = ev.to_dict()
        assert d["hour"] == 5
        assert d["is_mandatory"] is True

    def test_from_dict(self):
        d = {"hour": 10, "title": "SWAT", "description": "Push",
             "triggered": True, "is_mandatory": True, "outcome": "resolved"}
        ev = HourlyEvent.from_dict(d)
        assert ev.triggered is True
        assert ev.outcome == "resolved"

    def test_roundtrip(self):
        ev = HourlyEvent(hour=3, title="Contact",
                          description="First contact")
        ev.triggered = True
        ev.outcome = "suspect answered"
        d = ev.to_dict()
        ev2 = HourlyEvent.from_dict(d)
        assert ev2.triggered is True
        assert ev2.outcome == "suspect answered"


# ── NegotiationState ────────────────────────────────────────────────

class TestNegotiationState:

    def test_defaults(self):
        ns = NegotiationState()
        assert ns.hostages_freed == 0
        assert ns.hostages_remaining == 15
        assert ns.rapport_score == 20.0
        assert ns.decisive_action_score == 0.0
        assert ns.authority_score == 50.0
        assert ns.resolution == ResolutionType.ONGOING

    def test_to_dict(self):
        ns = NegotiationState()
        ns.hostages_freed = 5
        d = ns.to_dict()
        assert d["hostages_freed"] == 5
        assert d["resolution"] == "ongoing"

    def test_from_dict(self):
        d = {
            "hostages_freed": 10, "hostages_remaining": 5,
            "hostages_injured": 2, "hostages_deceased": 0,
            "hours_elapsed": 18, "concessions_offered": 4,
            "concessions_fulfilled": 3, "communications_count": 20,
            "rapport_score": 65.0, "decisive_action_score": 10.0,
            "authority_score": 55.0, "resolution": "peaceful_surrender",
        }
        ns = NegotiationState.from_dict(d)
        assert ns.hostages_freed == 10
        assert ns.resolution == ResolutionType.PEACEFUL_SURRENDER
        assert ns.rapport_score == 65.0

    def test_roundtrip(self):
        ns = NegotiationState()
        ns.hostages_freed = 8
        ns.rapport_score = 70.5
        ns.resolution = ResolutionType.TACTICAL_ENTRY
        d = ns.to_dict()
        ns2 = NegotiationState.from_dict(d)
        assert ns2.hostages_freed == 8
        assert ns2.rapport_score == 70.5
        assert ns2.resolution == ResolutionType.TACTICAL_ENTRY
