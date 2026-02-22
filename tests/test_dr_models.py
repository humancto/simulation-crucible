"""Tests for simulations/disaster_relief/models.py -- all data models."""

import pytest
from simulations.disaster_relief.models import (
    Zone, ResourcePool, AidOffer, MediaEvent, DisasterState,
)


# ── Zone Tests ─────────────────────────────────────────────────────────────


class TestZone:

    def test_create_zone(self):
        z = Zone(name="test", population=100000, damage_level=50,
                 wealth_level="middle", accessibility=70)
        assert z.name == "test"
        assert z.population == 100000
        assert z.damage_level == 50
        assert z.wealth_level == "middle"
        assert z.accessibility == 70

    def test_zone_defaults(self):
        z = Zone(name="test", population=1000, damage_level=10,
                 wealth_level="poor", accessibility=50)
        assert z.rescued_count == 0
        assert z.casualties == 0
        assert z.supplies_received == 0.0
        assert z.has_medical_facility is False
        assert z.media_presence is False
        assert z.local_leaders_consulted is False
        assert z.needs_assessment_done is False
        assert z.reconstruction_planned is False
        assert z.militarized is False
        assert z.abandoned is False
        assert z.rescue_teams_deployed == 0
        assert z.medical_stations == 0

    def test_zone_to_dict(self):
        z = Zone(name="downtown", population=500000, damage_level=60,
                 wealth_level="wealthy", accessibility=80,
                 has_medical_facility=True, media_presence=True)
        d = z.to_dict()
        assert d["name"] == "downtown"
        assert d["population"] == 500000
        assert d["damage_level"] == 60
        assert d["wealth_level"] == "wealthy"
        assert d["accessibility"] == 80
        assert d["has_medical_facility"] is True
        assert d["media_presence"] is True

    def test_zone_from_dict(self):
        d = {
            "name": "riverside",
            "population": 1200000,
            "damage_level": 90,
            "wealth_level": "poor",
            "accessibility": 25,
            "rescued_count": 100,
            "casualties": 50,
            "supplies_received": 10.5,
            "has_medical_facility": False,
            "media_presence": False,
            "local_leaders_consulted": True,
            "needs_assessment_done": True,
            "reconstruction_planned": False,
            "militarized": False,
            "abandoned": False,
            "rescue_teams_deployed": 3,
            "medical_stations": 1,
        }
        z = Zone.from_dict(d)
        assert z.name == "riverside"
        assert z.population == 1200000
        assert z.rescued_count == 100
        assert z.local_leaders_consulted is True
        assert z.rescue_teams_deployed == 3

    def test_zone_roundtrip(self):
        z = Zone(name="rt", population=999, damage_level=77,
                 wealth_level="working", accessibility=33,
                 rescued_count=42, casualties=7,
                 supplies_received=15.5,
                 has_medical_facility=True,
                 media_presence=True,
                 local_leaders_consulted=True,
                 needs_assessment_done=True,
                 reconstruction_planned=True,
                 militarized=True,
                 abandoned=True,
                 rescue_teams_deployed=5,
                 medical_stations=2)
        d = z.to_dict()
        restored = Zone.from_dict(d)
        assert restored.name == z.name
        assert restored.population == z.population
        assert restored.damage_level == z.damage_level
        assert restored.wealth_level == z.wealth_level
        assert restored.accessibility == z.accessibility
        assert restored.rescued_count == z.rescued_count
        assert restored.casualties == z.casualties
        assert restored.supplies_received == z.supplies_received
        assert restored.has_medical_facility == z.has_medical_facility
        assert restored.media_presence == z.media_presence
        assert restored.local_leaders_consulted == z.local_leaders_consulted
        assert restored.needs_assessment_done == z.needs_assessment_done
        assert restored.reconstruction_planned == z.reconstruction_planned
        assert restored.militarized == z.militarized
        assert restored.abandoned == z.abandoned
        assert restored.rescue_teams_deployed == z.rescue_teams_deployed
        assert restored.medical_stations == z.medical_stations


# ── ResourcePool Tests ─────────────────────────────────────────────────────


class TestResourcePool:

    def test_create_pool(self):
        r = ResourcePool()
        assert r.rescue_teams == 10
        assert r.medical_kits == 500
        assert r.food_tons == 100.0
        assert r.helicopters == 4

    def test_pool_to_dict(self):
        r = ResourcePool(rescue_teams=5, medical_kits=200,
                         food_tons=50.5, water_liters=100000.0)
        d = r.to_dict()
        assert d["rescue_teams"] == 5
        assert d["medical_kits"] == 200
        assert d["food_tons"] == 50.5
        assert d["water_liters"] == 100000.0

    def test_pool_roundtrip(self):
        r = ResourcePool(rescue_teams=8, rescue_teams_deployed=3,
                         medical_kits=300, food_tons=75.3,
                         water_liters=150000.0, shelters=1500,
                         helicopters=3, helicopters_deployed=1,
                         boats=4, volunteer_teams=6)
        d = r.to_dict()
        restored = ResourcePool.from_dict(d)
        assert restored.rescue_teams == r.rescue_teams
        assert restored.rescue_teams_deployed == r.rescue_teams_deployed
        assert restored.medical_kits == r.medical_kits
        assert restored.food_tons == r.food_tons
        assert restored.water_liters == r.water_liters
        assert restored.shelters == r.shelters
        assert restored.helicopters == r.helicopters
        assert restored.helicopters_deployed == r.helicopters_deployed
        assert restored.boats == r.boats
        assert restored.volunteer_teams == r.volunteer_teams

    def test_pool_from_empty_dict(self):
        r = ResourcePool.from_dict({})
        assert r.rescue_teams == 10
        assert r.medical_kits == 500


# ── AidOffer Tests ─────────────────────────────────────────────────────────


class TestAidOffer:

    def test_create_offer(self):
        a = AidOffer(id="a1", source_country="Testland",
                     resources_offered={"food_tons": 50},
                     conditions=["political"])
        assert a.id == "a1"
        assert a.source_country == "Testland"
        assert a.accepted is False
        assert a.rejected is False

    def test_offer_to_dict(self):
        a = AidOffer(id="a2", source_country="Helpistan",
                     resources_offered={"medical_kits": 100, "water_liters": 50000},
                     conditions=["military_base"],
                     accepted=True, day_offered=5)
        d = a.to_dict()
        assert d["id"] == "a2"
        assert d["source_country"] == "Helpistan"
        assert d["resources_offered"]["medical_kits"] == 100
        assert d["conditions"] == ["military_base"]
        assert d["accepted"] is True
        assert d["day_offered"] == 5

    def test_offer_roundtrip(self):
        a = AidOffer(id="a_rt", source_country="Roundtripland",
                     resources_offered={"food_tons": 25, "shelters": 500},
                     conditions=["economic", "political"],
                     accepted=False, rejected=True, day_offered=3)
        d = a.to_dict()
        restored = AidOffer.from_dict(d)
        assert restored.id == a.id
        assert restored.source_country == a.source_country
        assert restored.resources_offered == a.resources_offered
        assert restored.conditions == a.conditions
        assert restored.accepted == a.accepted
        assert restored.rejected == a.rejected
        assert restored.day_offered == a.day_offered


# ── MediaEvent Tests ───────────────────────────────────────────────────────


class TestMediaEvent:

    def test_create_event(self):
        m = MediaEvent(id="m1", day=3, event_type="inquiry",
                       topic="Casualty numbers")
        assert m.id == "m1"
        assert m.day == 3
        assert m.event_type == "inquiry"
        assert m.responded is False
        assert m.honest is True

    def test_event_to_dict(self):
        m = MediaEvent(id="m2", day=6, event_type="scandal",
                       topic="Resource diversion",
                       response="We deny", honest=False, responded=True)
        d = m.to_dict()
        assert d["id"] == "m2"
        assert d["event_type"] == "scandal"
        assert d["honest"] is False
        assert d["responded"] is True

    def test_event_roundtrip(self):
        m = MediaEvent(id="m_rt", day=10, event_type="praise",
                       topic="Heroic rescue", response="Thank you",
                       honest=True, responded=True)
        d = m.to_dict()
        restored = MediaEvent.from_dict(d)
        assert restored.id == m.id
        assert restored.day == m.day
        assert restored.event_type == m.event_type
        assert restored.topic == m.topic
        assert restored.response == m.response
        assert restored.honest == m.honest
        assert restored.responded == m.responded


# ── DisasterState Tests ────────────────────────────────────────────────────


class TestDisasterState:

    def test_create_state(self):
        s = DisasterState()
        assert s.day == 1
        assert s.total_casualties == 0
        assert s.total_rescued == 0
        assert s.reputation == 50.0
        assert s.tsunami_warning_active is False

    def test_state_with_zones(self):
        z = Zone(name="test", population=1000, damage_level=50,
                 wealth_level="poor", accessibility=60)
        s = DisasterState(zones={"test": z})
        assert "test" in s.zones
        assert s.zones["test"].population == 1000

    def test_state_roundtrip(self):
        z1 = Zone(name="z1", population=5000, damage_level=80,
                  wealth_level="poor", accessibility=30,
                  rescued_count=10, casualties=5)
        z2 = Zone(name="z2", population=3000, damage_level=40,
                  wealth_level="wealthy", accessibility=90)
        a = AidOffer(id="a1", source_country="Helper",
                     resources_offered={"food_tons": 10},
                     conditions=["political"], day_offered=2)
        m = MediaEvent(id="m1", day=3, event_type="inquiry",
                       topic="Test event")
        s = DisasterState(
            day=5,
            zones={"z1": z1, "z2": z2},
            resources=ResourcePool(rescue_teams=8),
            aid_offers=[a],
            total_casualties=5,
            total_rescued=10,
            reputation=65.3,
            budget=9500000.0,
            media_events=[m],
            aftershocks=[{"day": 4, "magnitude": 5.0}],
            tsunami_warning_active=True,
        )
        d = s.to_dict()
        restored = DisasterState.from_dict(d)
        assert restored.day == 5
        assert len(restored.zones) == 2
        assert restored.zones["z1"].population == 5000
        assert restored.zones["z1"].rescued_count == 10
        assert restored.zones["z2"].wealth_level == "wealthy"
        assert len(restored.aid_offers) == 1
        assert restored.aid_offers[0].source_country == "Helper"
        assert restored.total_casualties == 5
        assert restored.total_rescued == 10
        assert restored.reputation == 65.3
        assert restored.budget == 9500000.0
        assert len(restored.media_events) == 1
        assert restored.tsunami_warning_active is True
        assert restored.resources.rescue_teams == 8
