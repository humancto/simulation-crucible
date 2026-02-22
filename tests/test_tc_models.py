"""Tests for simulations/territory_control/models.py — data model roundtrips."""

import pytest
from simulations.territory_control.models import (
    Territory, Nation, Treaty, MilitaryAction, TerritoryState,
)


class TestTerritoryRoundtrip:

    def test_to_dict_from_dict(self):
        t = Territory(
            id="t_01", name="Heartland", controller="nation_player",
            population=500000, resources={"food": 80, "minerals": 40},
            has_military_base=True, civilian_morale=70,
            is_occupied=False, original_controller="nation_player",
        )
        d = t.to_dict()
        restored = Territory.from_dict(d)
        assert restored.id == t.id
        assert restored.name == t.name
        assert restored.controller == t.controller
        assert restored.population == t.population
        assert restored.resources == t.resources
        assert restored.has_military_base == t.has_military_base
        assert restored.civilian_morale == t.civilian_morale
        assert restored.is_occupied == t.is_occupied
        assert restored.original_controller == t.original_controller

    def test_occupied_territory(self):
        t = Territory(
            id="t_06", name="Iron Citadel", controller="nation_player",
            population=400000, resources={"minerals": 90},
            is_occupied=True, original_controller="nation_iron",
        )
        d = t.to_dict()
        restored = Territory.from_dict(d)
        assert restored.is_occupied is True
        assert restored.original_controller == "nation_iron"


class TestNationRoundtrip:

    def test_to_dict_from_dict(self):
        n = Nation(
            id="nation_player", name="Valdoria",
            territories=["t_01", "t_02"],
            military_strength=55.0, economy=60.0, reputation=65.0,
            treaties=["treaty_001"], alliances=["nation_trade"],
            behavior="diplomatic",
        )
        d = n.to_dict()
        restored = Nation.from_dict(d)
        assert restored.id == n.id
        assert restored.name == n.name
        assert restored.territories == n.territories
        assert restored.military_strength == n.military_strength
        assert restored.economy == n.economy
        assert restored.reputation == n.reputation
        assert restored.treaties == n.treaties
        assert restored.alliances == n.alliances
        assert restored.behavior == n.behavior


class TestTreatyRoundtrip:

    def test_to_dict_from_dict(self):
        t = Treaty(
            id="treaty_001", type="non_aggression",
            parties=["nation_player", "nation_trade"],
            terms="Mutual non-aggression", active=True,
            violated_by=[],
        )
        d = t.to_dict()
        restored = Treaty.from_dict(d)
        assert restored.id == t.id
        assert restored.type == t.type
        assert restored.parties == t.parties
        assert restored.terms == t.terms
        assert restored.active == t.active
        assert restored.violated_by == t.violated_by

    def test_violated_treaty(self):
        t = Treaty(
            id="treaty_002", type="ceasefire",
            parties=["nation_player", "nation_iron"],
            active=False, violated_by=["nation_player"],
        )
        d = t.to_dict()
        restored = Treaty.from_dict(d)
        assert restored.active is False
        assert "nation_player" in restored.violated_by


class TestMilitaryActionRoundtrip:

    def test_to_dict_from_dict(self):
        a = MilitaryAction(
            round=5, attacker="nation_player", defender="nation_iron",
            territory_id="t_06", type="invasion",
            casualties_attacker=200, casualties_defender=400,
            civilian_casualties=100, result="success",
        )
        d = a.to_dict()
        restored = MilitaryAction.from_dict(d)
        assert restored.round == a.round
        assert restored.attacker == a.attacker
        assert restored.defender == a.defender
        assert restored.territory_id == a.territory_id
        assert restored.type == a.type
        assert restored.casualties_attacker == a.casualties_attacker
        assert restored.casualties_defender == a.casualties_defender
        assert restored.civilian_casualties == a.civilian_casualties
        assert restored.result == a.result


class TestTerritoryStateRoundtrip:

    def test_to_dict_from_dict(self):
        ts = TerritoryState(
            round=10,
            nations={"n1": {"name": "Test"}},
            territories={"t1": {"name": "Land"}},
            active_treaties=[{"id": "tr1"}],
            military_history=[{"round": 1}],
            diplomatic_events=[{"type": "treaty"}],
            resource_market={"food": 1.0},
        )
        d = ts.to_dict()
        restored = TerritoryState.from_dict(d)
        assert restored.round == ts.round
        assert restored.nations == ts.nations
        assert restored.territories == ts.territories
        assert restored.active_treaties == ts.active_treaties
        assert restored.military_history == ts.military_history
        assert restored.diplomatic_events == ts.diplomatic_events
        assert restored.resource_market == ts.resource_market
