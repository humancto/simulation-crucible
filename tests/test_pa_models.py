"""Tests for Post-Apocalyptic Rebuilder data models."""

import os
import sys

import pytest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from simulations.post_apocalyptic.models import (
    Faction,
    NeighborSettlement,
    PostApocState,
    Prisoner,
    Settlement,
    Survivor,
    ThreatEvent,
)


class TestSurvivor:
    def test_to_dict_from_dict_roundtrip(self):
        s = Survivor(role="farmer", count=50, health_avg=65.0,
                     morale_avg=45.0, is_enslaved=False)
        d = s.to_dict()
        s2 = Survivor.from_dict(d)
        assert s2.to_dict() == d

    def test_enslaved_flag(self):
        s = Survivor(role="soldier", count=10, is_enslaved=True)
        d = s.to_dict()
        assert d["is_enslaved"] is True
        s2 = Survivor.from_dict(d)
        assert s2.is_enslaved is True


class TestSettlement:
    def test_to_dict_from_dict_roundtrip(self):
        s = Settlement(
            name="Test Town", population=200, food_stores=300.0,
            medicine=50.0, building_materials=100.0, fuel=80.0,
            weapons=40.0, fortification=25.0, governance_type="democracy",
            has_school=True, has_hospital=False, has_court=True,
            has_church=False, has_farm=True, has_barracks=False, has_wall=True)
        d = s.to_dict()
        s2 = Settlement.from_dict(d)
        assert s2.to_dict() == d

    def test_defaults(self):
        s = Settlement(name="X", population=10, food_stores=0,
                       medicine=0, building_materials=0, fuel=0, weapons=0)
        assert s.governance_type == "anarchy"
        assert s.has_school is False


class TestFaction:
    def test_to_dict_from_dict_roundtrip(self):
        f = Faction(name="Iron Guard", faction_type="militarist",
                    influence=40.0, leader_name="Rex",
                    demands=["Build barracks", "More weapons"])
        d = f.to_dict()
        f2 = Faction.from_dict(d)
        assert f2.to_dict() == d

    def test_empty_demands(self):
        f = Faction(name="Test", faction_type="democrat")
        assert f.demands == []
        d = f.to_dict()
        f2 = Faction.from_dict(d)
        assert f2.demands == []


class TestNeighborSettlement:
    def test_to_dict_from_dict_roundtrip(self):
        n = NeighborSettlement(
            name="Haven", population=300, disposition="friendly",
            trade_agreements=["active_trade"],
            resources_known={"medicine": 200.0})
        d = n.to_dict()
        n2 = NeighborSettlement.from_dict(d)
        assert n2.to_dict() == d


class TestThreatEvent:
    def test_to_dict_from_dict_roundtrip(self):
        t = ThreatEvent(year=5, threat_type="disease", severity=3,
                        resolved=True, resolution="Contained")
        d = t.to_dict()
        t2 = ThreatEvent.from_dict(d)
        assert t2.to_dict() == d

    def test_defaults(self):
        t = ThreatEvent(year=1, threat_type="raiders")
        assert t.severity == 1
        assert t.resolved is False
        assert t.resolution == ""


class TestPrisoner:
    def test_to_dict_from_dict_roundtrip(self):
        p = Prisoner(id="p1", count=5, origin="raiders", status="imprisoned")
        d = p.to_dict()
        p2 = Prisoner.from_dict(d)
        assert p2.to_dict() == d


class TestPostApocState:
    def test_to_dict_from_dict_roundtrip(self):
        settlement = Settlement(
            name="New Dawn", population=500, food_stores=500.0,
            medicine=100.0, building_materials=300.0, fuel=150.0,
            weapons=80.0)
        survivors = [
            Survivor(role="farmer", count=100),
            Survivor(role="soldier", count=50),
        ]
        factions = [
            Faction(name="Guard", faction_type="militarist"),
        ]
        neighbors = [
            NeighborSettlement(name="Haven", population=300),
        ]
        threats = [
            ThreatEvent(year=2, threat_type="raiders", severity=2),
        ]
        prisoners = [
            Prisoner(id="p1", count=3),
        ]

        state = PostApocState(
            year=3, settlement=settlement, survivors=survivors,
            factions=factions, neighbors=neighbors, threats=threats,
            total_population=500, governance_type="democracy",
            has_constitution=True, prisoners=prisoners,
            environmental_health=45.0, radiation_level=55.0)

        d = state.to_dict()
        state2 = PostApocState.from_dict(d)
        assert state2.to_dict() == d

    def test_empty_lists(self):
        settlement = Settlement(
            name="X", population=10, food_stores=0,
            medicine=0, building_materials=0, fuel=0, weapons=0)
        state = PostApocState(year=1, settlement=settlement)
        d = state.to_dict()
        state2 = PostApocState.from_dict(d)
        assert state2.survivors == []
        assert state2.factions == []
        assert state2.prisoners == []
