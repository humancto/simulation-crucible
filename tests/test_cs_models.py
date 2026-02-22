"""Tests for colony_ship.models — to_dict/from_dict roundtrips."""

import pytest
from simulations.colony_ship.models import (
    Colonist,
    ColonyState,
    CrisisEvent,
    Deck,
    DemographicGroup,
    ShipSystem,
)


class TestDemographicGroupRoundtrip:
    def test_default_roundtrip(self):
        g = DemographicGroup(role="scientist", count=800)
        d = g.to_dict()
        g2 = DemographicGroup.from_dict(d)
        assert g2.role == g.role
        assert g2.count == g.count
        assert g2.avg_health == g.avg_health
        assert g2.to_dict() == d

    def test_full_roundtrip(self):
        g = DemographicGroup(
            role="child", count=2000, avg_age=8.0, avg_health=92.0,
            avg_morale=80.0, avg_genetic_fitness=78.0,
            rations_level="generous", pregnant_count=0,
            has_voted=True, working=True, work_task="hydroponics",
        )
        d = g.to_dict()
        g2 = DemographicGroup.from_dict(d)
        assert g2.to_dict() == d


class TestDeckRoundtrip:
    def test_default_roundtrip(self):
        deck = Deck(name="Deck-A")
        d = deck.to_dict()
        deck2 = Deck.from_dict(d)
        assert deck2.name == "Deck-A"
        assert deck2.to_dict() == d

    def test_sealed_deck(self):
        deck = Deck(name="Deck-G", capacity=1000, current_population=0,
                    sealed=True, has_life_support=False, condition=45.0)
        d = deck.to_dict()
        deck2 = Deck.from_dict(d)
        assert deck2.sealed is True
        assert deck2.has_life_support is False
        assert deck2.to_dict() == d


class TestShipSystemRoundtrip:
    def test_roundtrip(self):
        s = ShipSystem(name="Fusion Reactor", type="energy",
                       efficiency=85.0, degradation_rate=1.0,
                       last_maintained_year=5, critical=False)
        d = s.to_dict()
        s2 = ShipSystem.from_dict(d)
        assert s2.name == "Fusion Reactor"
        assert s2.efficiency == 85.0
        assert s2.to_dict() == d

    def test_critical_system(self):
        s = ShipSystem(name="Oxygen Generator", type="oxygen",
                       efficiency=20.0, critical=True)
        d = s.to_dict()
        s2 = ShipSystem.from_dict(d)
        assert s2.critical is True
        assert s2.to_dict() == d


class TestCrisisEventRoundtrip:
    def test_roundtrip(self):
        c = CrisisEvent(year=5, type="disease", severity=3,
                        affected_deck="Deck-C",
                        description="Outbreak on Deck-C")
        d = c.to_dict()
        c2 = CrisisEvent.from_dict(d)
        assert c2.year == 5
        assert c2.type == "disease"
        assert c2.to_dict() == d

    def test_resolved_crisis(self):
        c = CrisisEvent(year=12, type="system_failure", severity=4,
                        resolved=True, resolution_method="maintenance")
        d = c.to_dict()
        c2 = CrisisEvent.from_dict(d)
        assert c2.resolved is True
        assert c2.to_dict() == d


class TestColonyStateRoundtrip:
    def test_default_roundtrip(self):
        cs = ColonyState(year=10, total_population=9500)
        d = cs.to_dict()
        cs2 = ColonyState.from_dict(d)
        assert cs2.year == 10
        assert cs2.total_population == 9500
        assert cs2.to_dict() == d

    def test_full_state_roundtrip(self):
        cs = ColonyState(
            year=25, total_population=11000,
            food_reserves=60.0, water_reserves=75.0,
            martial_law=True, population_policy="restricted",
            arts_funded=False, eugenics_active=True,
        )
        d = cs.to_dict()
        cs2 = ColonyState.from_dict(d)
        assert cs2.martial_law is True
        assert cs2.eugenics_active is True
        assert cs2.to_dict() == d


class TestColonistRoundtrip:
    def test_roundtrip(self):
        c = Colonist(id="c001", name="Ava Chen", age=35,
                     role="scientist", deck="Deck-A",
                     health=90.0, morale=75.0, is_pregnant=True)
        d = c.to_dict()
        c2 = Colonist.from_dict(d)
        assert c2.name == "Ava Chen"
        assert c2.is_pregnant is True
        assert c2.to_dict() == d
