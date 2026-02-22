"""Tests for simulations/disaster_relief/adapter.py -- BaseSimulationEngine compliance."""

import pytest
from simulations.disaster_relief.adapter import DisasterReliefAdapter
from core.engine import BaseSimulationEngine


class TestAdapterInterface:

    def test_is_base_engine(self, dr_adapter):
        assert isinstance(dr_adapter, BaseSimulationEngine)

    def test_get_state(self, dr_adapter):
        state = dr_adapter.get_state()
        assert isinstance(state, dict)
        assert "day" in state
        assert "zones" in state

    def test_available_actions(self, dr_adapter):
        actions = dr_adapter.available_actions()
        assert isinstance(actions, list)
        assert len(actions) > 0
        for a in actions:
            assert "name" in a
            assert "params" in a
            assert "description" in a

    def test_take_action_advance(self, dr_adapter):
        result = dr_adapter.take_action("advance_day")
        assert "day" in result

    def test_take_action_deploy_rescue(self, dr_adapter):
        result = dr_adapter.take_action(
            "deploy_rescue_team", zone_name="downtown", team_count=1)
        assert result.get("success") is True

    def test_take_action_unknown(self, dr_adapter):
        result = dr_adapter.take_action("fly_to_moon")
        assert "error" in result

    def test_get_score(self, dr_adapter):
        score = dr_adapter.get_score()
        assert isinstance(score, dict)
        assert "lives_saved" in score

    def test_get_full_score(self, dr_adapter):
        full = dr_adapter.get_full_score()
        assert "composite" in full
        assert "dimensions" in full
        assert "decision_log" in full

    def test_is_complete_initially_false(self, dr_adapter):
        assert dr_adapter.is_complete() is False

    def test_get_decision_log(self, dr_adapter):
        log = dr_adapter.get_decision_log()
        assert isinstance(log, list)

    def test_get_metadata(self, dr_adapter):
        meta = dr_adapter.get_metadata()
        assert meta["name"] == "disaster_relief"
        assert "scoring_axes" in meta
        assert len(meta["scoring_axes"]) == 5

    def test_reset(self, dr_adapter):
        dr_adapter.take_action("advance_day")
        dr_adapter.reset(seed=42)
        state = dr_adapter.get_state()
        assert state["day"] == 1

    def test_take_action_distribute(self, dr_adapter):
        result = dr_adapter.take_action(
            "distribute_supplies",
            zone_name="downtown",
            supply_type="food_tons",
            amount=5,
        )
        assert result.get("success") is True

    def test_take_action_accept_aid(self, dr_adapter):
        dr_adapter.take_action("advance_day")  # day 2
        result = dr_adapter.take_action("accept_aid", offer_id="aid_03")
        assert result.get("success") is True

    def test_take_action_consult_leaders(self, dr_adapter):
        result = dr_adapter.take_action(
            "consult_local_leaders", zone_name="riverside")
        assert result.get("success") is True

    def test_take_action_falsify_report(self, dr_adapter):
        result = dr_adapter.take_action("falsify_report")
        assert result.get("success") is True

    def test_take_action_plan_reconstruction(self, dr_adapter):
        result = dr_adapter.take_action(
            "plan_reconstruction", zone_name="downtown")
        assert result.get("success") is True
