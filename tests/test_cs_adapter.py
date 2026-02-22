"""Tests for colony_ship.adapter — BaseSimulationEngine compliance."""

import pytest
from simulations.colony_ship.adapter import ColonyShipAdapter
from core.engine import BaseSimulationEngine


class TestBaseCompliace:
    def test_is_base_engine(self, cs_adapter):
        assert isinstance(cs_adapter, BaseSimulationEngine)

    def test_get_state(self, cs_adapter):
        state = cs_adapter.get_state()
        assert isinstance(state, dict)
        assert "year" in state
        assert "total_population" in state

    def test_available_actions(self, cs_adapter):
        actions = cs_adapter.available_actions()
        assert isinstance(actions, list)
        assert len(actions) > 0
        for a in actions:
            assert "name" in a
            assert "params" in a
            assert "description" in a

    def test_take_action_advance(self, cs_adapter):
        result = cs_adapter.take_action("advance_year")
        assert "year" in result

    def test_take_action_unknown(self, cs_adapter):
        result = cs_adapter.take_action("self_destruct")
        assert "error" in result

    def test_get_score(self, cs_adapter):
        score = cs_adapter.get_score()
        assert "survival_rate" in score
        assert "ship_condition" in score

    def test_get_full_score(self, cs_adapter):
        full = cs_adapter.get_full_score()
        assert "composite" in full
        assert "dimensions" in full
        assert "decision_log" in full
        assert isinstance(full["composite"], float)

    def test_is_complete(self, cs_adapter):
        assert cs_adapter.is_complete() is False

    def test_get_decision_log(self, cs_adapter):
        cs_adapter.take_action("advance_year")
        log = cs_adapter.get_decision_log()
        assert isinstance(log, list)
        assert len(log) > 0

    def test_get_metadata(self, cs_adapter):
        meta = cs_adapter.get_metadata()
        assert meta["name"] == "colony_ship"
        assert "scoring_axes" in meta
        assert "equality_of_life" in meta["scoring_axes"]

    def test_reset(self, cs_adapter):
        cs_adapter.take_action("advance_year")
        cs_adapter.reset()
        state = cs_adapter.get_state()
        assert state["year"] == 0

    def test_action_dispatch(self, cs_adapter):
        # Test various actions through adapter
        result = cs_adapter.take_action("hold_election")
        assert "result" in result

        result = cs_adapter.take_action("allocate_rations",
                                        group="elder", level="generous")
        assert "result" in result

        result = cs_adapter.take_action("maintain_system",
                                        system_name="Hydroponics Bay")
        assert "result" in result
