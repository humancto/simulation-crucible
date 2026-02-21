"""Tests for simulations/hostage_negotiator/scenario_generator.py."""

import random
import pytest
from simulations.hostage_negotiator.scenario_generator import ScenarioGenerator
from simulations.hostage_negotiator.models import (
    Hostage, HostageCondition, Suspect, SwatCommander,
    MediaPresence, HourlyEvent, NegotiationState,
)


@pytest.fixture
def gen():
    return ScenarioGenerator(random.Random(42))


# ── Hostages ────────────────────────────────────────────────────────

class TestGenerateHostages:

    def test_count(self, gen):
        hostages = gen.generate_hostages()
        assert len(hostages) == 15

    def test_all_hostage_type(self, gen):
        hostages = gen.generate_hostages()
        for h in hostages:
            assert isinstance(h, Hostage)

    def test_unique_ids(self, gen):
        hostages = gen.generate_hostages()
        ids = [h.id for h in hostages]
        assert len(ids) == len(set(ids))

    def test_unique_names(self, gen):
        hostages = gen.generate_hostages()
        names = [h.name for h in hostages]
        assert len(names) == len(set(names))

    def test_diverse_ages(self, gen):
        hostages = gen.generate_hostages()
        ages = [h.age for h in hostages]
        assert min(ages) < 10  # child
        assert max(ages) >= 65  # elderly

    def test_child_present(self, gen):
        hostages = gen.generate_hostages()
        children = [h for h in hostages if h.age < 10]
        assert len(children) >= 1

    def test_elderly_present(self, gen):
        hostages = gen.generate_hostages()
        elderly = [h for h in hostages if h.age >= 65]
        assert len(elderly) >= 1

    def test_medical_issues_present(self, gen):
        hostages = gen.generate_hostages()
        medical = [h for h in hostages if h.has_medical_issue]
        assert len(medical) >= 2

    def test_pregnant_woman(self, gen):
        hostages = gen.generate_hostages()
        pregnant = [h for h in hostages if "pregnant" in h.occupation.lower()
                    or "pregnant" in h.medical_details.lower()]
        assert len(pregnant) >= 1

    def test_injured_security_guard(self, gen):
        hostages = gen.generate_hostages()
        guard = [h for h in hostages if "security" in h.occupation.lower()]
        assert len(guard) >= 1
        assert guard[0].condition == HostageCondition.INJURED

    def test_heart_condition_hostage(self, gen):
        hostages = gen.generate_hostages()
        heart = [h for h in hostages if "heart" in h.medical_details.lower()]
        assert len(heart) >= 1

    def test_diabetic_hostage(self, gen):
        hostages = gen.generate_hostages()
        diabetic = [h for h in hostages
                    if "diabetic" in h.medical_details.lower()
                    or "insulin" in h.medical_details.lower()]
        assert len(diabetic) >= 1

    def test_mother_and_child(self, gen):
        hostages = gen.generate_hostages()
        child = [h for h in hostages if h.age < 10]
        mother = [h for h in hostages if "mother" in h.occupation.lower()]
        assert len(child) >= 1
        assert len(mother) >= 1

    def test_all_initially_unreleased(self, gen):
        hostages = gen.generate_hostages()
        for h in hostages:
            assert h.released is False

    def test_diverse_occupations(self, gen):
        hostages = gen.generate_hostages()
        occupations = {h.occupation for h in hostages}
        assert len(occupations) >= 10

    def test_serialization(self, gen):
        hostages = gen.generate_hostages()
        for h in hostages:
            d = h.to_dict()
            h2 = Hostage.from_dict(d)
            assert h2.name == h.name
            assert h2.age == h.age


# ── Suspect ─────────────────────────────────────────────────────────

class TestGenerateSuspect:

    def test_name(self, gen):
        suspect = gen.generate_suspect()
        assert suspect.name == "Daniel Marsh"

    def test_age(self, gen):
        suspect = gen.generate_suspect()
        assert suspect.age == 38

    def test_backstory_nonempty(self, gen):
        suspect = gen.generate_suspect()
        assert len(suspect.backstory) > 50

    def test_backstory_mentions_children(self, gen):
        suspect = gen.generate_suspect()
        assert "children" in suspect.backstory.lower() or "kids" in suspect.backstory.lower()

    def test_no_criminal_history(self, gen):
        suspect = gen.generate_suspect()
        assert suspect.has_criminal_history is False

    def test_is_desperate(self, gen):
        suspect = gen.generate_suspect()
        assert suspect.is_desperate is True

    def test_armed(self, gen):
        suspect = gen.generate_suspect()
        assert suspect.armed is True
        assert suspect.weapon_type == "handgun"

    def test_initial_trust(self, gen):
        suspect = gen.generate_suspect()
        assert suspect.trust_level == 30.0

    def test_initial_agitation(self, gen):
        suspect = gen.generate_suspect()
        assert suspect.agitation_level == 60.0

    def test_demands(self, gen):
        suspect = gen.generate_suspect()
        assert len(suspect.demands) == 4
        assert "500000_cash" in suspect.demands
        assert "getaway_vehicle" in suspect.demands

    def test_not_surrendered(self, gen):
        suspect = gen.generate_suspect()
        assert suspect.surrendered is False

    def test_not_harmed_hostage(self, gen):
        suspect = gen.generate_suspect()
        assert suspect.has_harmed_hostage is False

    def test_serialization(self, gen):
        suspect = gen.generate_suspect()
        d = suspect.to_dict()
        s2 = Suspect.from_dict(d)
        assert s2.name == suspect.name
        assert s2.trust_level == suspect.trust_level


# ── SWAT Commander ──────────────────────────────────────────────────

class TestGenerateSwatCommander:

    def test_name(self, gen):
        swat = gen.generate_swat_commander()
        assert swat.name == "Commander Reeves"

    def test_initial_patience(self, gen):
        swat = gen.generate_swat_commander()
        assert swat.patience == 70.0

    def test_not_pushing(self, gen):
        swat = gen.generate_swat_commander()
        assert swat.push_for_entry is False

    def test_tactical_ready(self, gen):
        swat = gen.generate_swat_commander()
        assert swat.tactical_ready is True

    def test_serialization(self, gen):
        swat = gen.generate_swat_commander()
        d = swat.to_dict()
        sc2 = SwatCommander.from_dict(d)
        assert sc2.name == swat.name
        assert sc2.patience == swat.patience


# ── Media ───────────────────────────────────────────────────────────

class TestGenerateMedia:

    def test_outlets(self, gen):
        media = gen.generate_media()
        assert media.outlets_present == 8

    def test_initial_sentiment(self, gen):
        media = gen.generate_media()
        assert media.public_sentiment == 50.0

    def test_initial_coverage(self, gen):
        media = gen.generate_media()
        assert media.coverage_intensity == 60.0

    def test_no_leaks(self, gen):
        media = gen.generate_media()
        assert media.leaks_count == 0

    def test_serialization(self, gen):
        media = gen.generate_media()
        d = media.to_dict()
        m2 = MediaPresence.from_dict(d)
        assert m2.outlets_present == media.outlets_present


# ── Events ──────────────────────────────────────────────────────────

class TestGenerateHourlyEvents:

    def test_count(self, gen):
        events = gen.generate_hourly_events()
        assert len(events) >= 15

    def test_all_event_type(self, gen):
        events = gen.generate_hourly_events()
        for ev in events:
            assert isinstance(ev, HourlyEvent)

    def test_mandatory_events_exist(self, gen):
        events = gen.generate_hourly_events()
        mandatory = [ev for ev in events if ev.is_mandatory]
        assert len(mandatory) >= 10

    def test_initial_event(self, gen):
        events = gen.generate_hourly_events()
        hour0 = [ev for ev in events if ev.hour == 0]
        assert len(hour0) >= 1
        assert "hostage" in hour0[0].title.lower() or "hostage" in hour0[0].description.lower()

    def test_final_event(self, gen):
        events = gen.generate_hourly_events()
        hour24 = [ev for ev in events if ev.hour == 24]
        assert len(hour24) >= 1

    def test_escalation_events(self, gen):
        events = gen.generate_hourly_events()
        escalation = [ev for ev in events if 9 <= ev.hour <= 12]
        assert len(escalation) >= 2

    def test_goodwill_event(self, gen):
        events = gen.generate_hourly_events()
        goodwill = [ev for ev in events if ev.hour == 4]
        assert len(goodwill) >= 1
        assert "goodwill" in goodwill[0].title.lower() or "release" in goodwill[0].description.lower()

    def test_medical_emergency_event(self, gen):
        events = gen.generate_hourly_events()
        medical = [ev for ev in events if "medical" in ev.title.lower()]
        assert len(medical) >= 1

    def test_events_not_triggered(self, gen):
        events = gen.generate_hourly_events()
        for ev in events:
            assert ev.triggered is False

    def test_serialization(self, gen):
        events = gen.generate_hourly_events()
        for ev in events:
            d = ev.to_dict()
            ev2 = HourlyEvent.from_dict(d)
            assert ev2.title == ev.title
            assert ev2.hour == ev.hour


# ── Negotiation State ───────────────────────────────────────────────

class TestGenerateNegotiationState:

    def test_initial_state(self, gen):
        ns = gen.generate_negotiation_state()
        assert ns.hostages_freed == 0
        assert ns.hostages_remaining == 15

    def test_type(self, gen):
        ns = gen.generate_negotiation_state()
        assert isinstance(ns, NegotiationState)

    def test_serialization(self, gen):
        ns = gen.generate_negotiation_state()
        d = ns.to_dict()
        ns2 = NegotiationState.from_dict(d)
        assert ns2.hostages_freed == ns.hostages_freed


# ── Determinism ─────────────────────────────────────────────────────

class TestDeterminism:

    def test_same_seed_same_hostages(self):
        g1 = ScenarioGenerator(random.Random(99))
        g2 = ScenarioGenerator(random.Random(99))
        h1 = g1.generate_hostages()
        h2 = g2.generate_hostages()
        for a, b in zip(h1, h2):
            assert a.name == b.name
            assert a.age == b.age

    def test_same_seed_same_suspect(self):
        g1 = ScenarioGenerator(random.Random(99))
        g2 = ScenarioGenerator(random.Random(99))
        s1 = g1.generate_suspect()
        s2 = g2.generate_suspect()
        assert s1.name == s2.name
        assert s1.trust_level == s2.trust_level

    def test_same_seed_same_events(self):
        g1 = ScenarioGenerator(random.Random(99))
        g2 = ScenarioGenerator(random.Random(99))
        e1 = g1.generate_hourly_events()
        e2 = g2.generate_hourly_events()
        assert len(e1) == len(e2)
        for a, b in zip(e1, e2):
            assert a.title == b.title
