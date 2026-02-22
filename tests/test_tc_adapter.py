"""Tests for simulations/territory_control/adapter.py — TerritoryControlAdapter."""

import pytest
from simulations.territory_control.adapter import TerritoryControlAdapter


class TestAdapterInterface:

    def test_reset(self, tc_adapter):
        tc_adapter.take_action("advance_round")
        assert tc_adapter.sim.current_round == 1
        tc_adapter.reset()
        assert tc_adapter.sim.current_round == 0

    def test_reset_with_seed(self, tc_adapter):
        tc_adapter.reset(seed=99)
        assert tc_adapter.sim.seed == 99

    def test_get_state(self, tc_adapter):
        state = tc_adapter.get_state()
        assert "round" in state
        assert "player_nation" in state
        assert "territories" in state

    def test_available_actions(self, tc_adapter):
        actions = tc_adapter.available_actions()
        assert len(actions) > 0
        names = [a["name"] for a in actions]
        assert "advance_round" in names
        assert "invade_territory" in names
        assert "propose_treaty" in names
        assert "humanitarian_aid" in names

    def test_available_actions_have_params(self, tc_adapter):
        actions = tc_adapter.available_actions()
        for a in actions:
            assert "name" in a
            assert "params" in a
            assert "description" in a

    def test_is_complete_initially_false(self, tc_adapter):
        assert tc_adapter.is_complete() is False

    def test_get_score(self, tc_adapter):
        score = tc_adapter.get_score()
        assert "territory_count" in score
        assert "military_strength" in score

    def test_get_full_score(self, tc_adapter):
        full = tc_adapter.get_full_score()
        assert "composite" in full
        assert "dimensions" in full
        assert "decision_log" in full

    def test_get_decision_log(self, tc_adapter):
        log = tc_adapter.get_decision_log()
        assert isinstance(log, list)

    def test_get_metadata(self, tc_adapter):
        meta = tc_adapter.get_metadata()
        assert "name" in meta
        assert meta["name"] == "territory_control"
        assert "display_name" in meta
        assert "description" in meta
        assert "scoring_axes" in meta
        assert len(meta["scoring_axes"]) == 5


class TestAdapterActions:

    def test_advance_round(self, tc_adapter):
        result = tc_adapter.take_action("advance_round")
        assert result["round"] == 1

    def test_defend_territory(self, tc_adapter):
        result = tc_adapter.take_action(
            "defend_territory", territory_id="t_01")
        assert result.get("success") is True

    def test_invade_territory(self, tc_adapter):
        result = tc_adapter.take_action(
            "invade_territory", territory_id="t_06", force_level="standard")
        assert "result" in result

    def test_propose_treaty(self, tc_adapter):
        result = tc_adapter.take_action(
            "propose_treaty", target_nation="nation_trade",
            treaty_type="trade", terms="Food for tech")
        assert "error" not in result or "accepted" in result

    def test_trade_resources(self, tc_adapter):
        result = tc_adapter.take_action(
            "trade_resources", target_nation="nation_trade",
            give_resource="food", give_amount=10,
            get_resource="tech", get_amount=5)
        assert result.get("success") is True

    def test_spy_on(self, tc_adapter):
        result = tc_adapter.take_action(
            "spy_on", target_nation="nation_iron")
        assert "intel" in result

    def test_humanitarian_aid(self, tc_adapter):
        result = tc_adapter.take_action(
            "humanitarian_aid", territory_id="t_01")
        assert result.get("success") is True

    def test_hold_referendum(self, tc_adapter):
        result = tc_adapter.take_action(
            "hold_referendum", territory_id="t_01")
        assert result.get("success") is True

    def test_false_peace(self, tc_adapter):
        result = tc_adapter.take_action(
            "false_peace", target_nation="nation_iron")
        assert result.get("success") is True

    def test_puppet_government(self, tc_adapter):
        result = tc_adapter.take_action(
            "puppet_government", territory_id="t_01")
        assert result.get("success") is True

    def test_disproportionate_strike(self, tc_adapter):
        result = tc_adapter.take_action(
            "disproportionate_strike", territory_id="t_06")
        assert result.get("success") is True

    def test_arms_embargo_violation(self, tc_adapter):
        result = tc_adapter.take_action(
            "arms_embargo_violation", target_nation="nation_iron")
        assert result.get("success") is True

    def test_scorched_earth(self, tc_adapter):
        result = tc_adapter.take_action(
            "scorched_earth", territory_id="t_01")
        assert result.get("success") is True

    def test_ceasefire(self, tc_adapter):
        result = tc_adapter.take_action(
            "ceasefire", target_nation="nation_iron")
        # Either accepted or rejected, but should not error
        assert "error" not in result or "accepted" in result

    def test_unknown_action_errors(self, tc_adapter):
        result = tc_adapter.take_action("nonexistent_action")
        assert "error" in result


class TestAdapterCompletion:

    def test_30_rounds_completes(self, tc_adapter):
        for _ in range(30):
            tc_adapter.take_action("advance_round")
        assert tc_adapter.is_complete() is True

    def test_full_score_after_completion(self, tc_adapter):
        for _ in range(30):
            tc_adapter.take_action("advance_round")
        full = tc_adapter.get_full_score()
        assert "composite" in full
        assert 0.0 <= full["composite"] <= 100.0
