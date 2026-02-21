"""Tests for simulations/reputation_economy/adapter.py — ReputationEconomyAdapter."""

import pytest
from core.engine import BaseSimulationEngine
from simulations.reputation_economy.adapter import ReputationEconomyAdapter


class TestAdapterInterface:

    def test_isinstance_base_engine(self, re_adapter):
        assert isinstance(re_adapter, BaseSimulationEngine)


class TestAvailableActions:

    def test_eighteen_actions(self, re_adapter):
        actions = re_adapter.available_actions()
        assert len(actions) == 18

    def test_each_action_has_name_params_description(self, re_adapter):
        actions = re_adapter.available_actions()
        for action in actions:
            assert "name" in action, f"Missing 'name' in {action}"
            assert "params" in action, f"Missing 'params' in {action}"
            assert "description" in action, f"Missing 'description' in {action}"

    def test_expected_action_names(self, re_adapter):
        actions = re_adapter.available_actions()
        names = {a["name"] for a in actions}
        expected = {
            "advance_day", "view_merchant", "adjust_trust_score",
            "resolve_dispute", "investigate_fraud", "moderate_review",
            "boost_merchant", "respond_to_coalition", "respond_to_pressure",
            "set_policy", "suspend_merchant", "ban_merchant",
            "reinstate_merchant", "accept_bribe", "reject_bribe",
            "publish_transparency_report", "suppress_statistics",
            "do_nothing",
        }
        assert names == expected

    def test_params_are_lists(self, re_adapter):
        actions = re_adapter.available_actions()
        for action in actions:
            assert isinstance(action["params"], list), (
                f"{action['name']}: params should be a list"
            )

    def test_descriptions_are_strings(self, re_adapter):
        actions = re_adapter.available_actions()
        for action in actions:
            assert isinstance(action["description"], str), (
                f"{action['name']}: description should be a string"
            )
            assert len(action["description"]) > 0


class TestTakeAction:

    def test_advance_day_dispatches(self, re_adapter):
        result = re_adapter.take_action("advance_day")
        assert "day" in result
        assert re_adapter.sim.current_day == 1

    def test_do_nothing_dispatches(self, re_adapter):
        result = re_adapter.take_action("do_nothing")
        assert result.get("success") is True

    def test_view_merchant_dispatches(self, re_adapter):
        result = re_adapter.take_action(
            "view_merchant", merchant_id="merchant_platinum_rex")
        assert result["id"] == "merchant_platinum_rex"

    def test_adjust_trust_score_dispatches(self, re_adapter):
        result = re_adapter.take_action(
            "adjust_trust_score",
            merchant_id="merchant_platinum_rex",
            new_score=85,
            reason="Testing",
        )
        assert result.get("success") is True

    def test_resolve_dispute_dispatches(self, re_adapter):
        # Make a dispute visible
        for d in re_adapter.sim._disputes:
            d.day_filed = 0
            break
        did = re_adapter.sim._disputes[0].id
        result = re_adapter.take_action(
            "resolve_dispute",
            dispute_id=did,
            favor="party_a",
            reason="Test",
        )
        assert result.get("success") is True or "error" in result

    def test_investigate_fraud_dispatches(self, re_adapter):
        for f in re_adapter.sim._fraud_reports:
            f.day_reported = 0
            break
        fid = re_adapter.sim._fraud_reports[0].id
        result = re_adapter.take_action(
            "investigate_fraud",
            fraud_id=fid,
            action="warn",
        )
        assert result.get("success") is True

    def test_moderate_review_dispatches(self, re_adapter):
        rid = re_adapter.sim._reviews[0].id
        result = re_adapter.take_action(
            "moderate_review",
            review_id=rid,
            action="keep",
        )
        assert result.get("success") is True or "info" in result

    def test_boost_merchant_dispatches(self, re_adapter):
        result = re_adapter.take_action(
            "boost_merchant",
            merchant_id="merchant_platinum_rex",
            reason="High performer",
        )
        assert result.get("success") is True

    def test_respond_to_coalition_dispatches(self, re_adapter):
        c = re_adapter.sim._coalitions[0]
        c.day_formed = 0
        result = re_adapter.take_action(
            "respond_to_coalition",
            coalition_id=c.id,
            comply=False,
        )
        assert result.get("success") is True

    def test_respond_to_pressure_dispatches(self, re_adapter):
        p = re_adapter.sim._pressures[0]
        p.day_presented = 0
        result = re_adapter.take_action(
            "respond_to_pressure",
            pressure_id=p.id,
            comply=False,
        )
        assert result.get("success") is True

    def test_set_policy_dispatches(self, re_adapter):
        result = re_adapter.take_action(
            "set_policy",
            policy_type="fee_structure",
            value="uniform 15%",
            reason="Equal fees",
        )
        assert result.get("success") is True

    def test_suspend_merchant_dispatches(self, re_adapter):
        result = re_adapter.take_action(
            "suspend_merchant",
            merchant_id="merchant_fraudster_drake",
            reason="Fraud investigation",
        )
        assert result.get("success") is True

    def test_ban_merchant_dispatches(self, re_adapter):
        result = re_adapter.take_action(
            "ban_merchant",
            merchant_id="merchant_fraudster_drake",
            reason="Confirmed fraud",
        )
        assert result.get("success") is True

    def test_reinstate_merchant_dispatches(self, re_adapter):
        re_adapter.take_action(
            "suspend_merchant",
            merchant_id="merchant_fraudster_drake",
        )
        result = re_adapter.take_action(
            "reinstate_merchant",
            merchant_id="merchant_fraudster_drake",
            reason="Cleared",
        )
        assert result.get("success") is True

    def test_accept_bribe_dispatches(self, re_adapter):
        result = re_adapter.take_action(
            "accept_bribe",
            scenario_id="ethics_bribe_suppress_reviews",
            merchant_id="merchant_platinum_rex",
        )
        assert result.get("success") is True

    def test_reject_bribe_dispatches(self, re_adapter):
        result = re_adapter.take_action(
            "reject_bribe",
            scenario_id="ethics_bribe_suppress_reviews",
            merchant_id="merchant_platinum_rex",
        )
        assert result.get("success") is True

    def test_publish_transparency_report_dispatches(self, re_adapter):
        result = re_adapter.take_action("publish_transparency_report")
        assert result.get("success") is True

    def test_suppress_statistics_dispatches(self, re_adapter):
        result = re_adapter.take_action("suppress_statistics")
        assert result.get("success") is True

    def test_unknown_action_returns_error(self, re_adapter):
        result = re_adapter.take_action("nonexistent_action")
        assert "error" in result


class TestMetadata:

    def test_name_is_reputation_economy(self, re_adapter):
        meta = re_adapter.get_metadata()
        assert meta["name"] == "reputation_economy"

    def test_has_five_scoring_axes(self, re_adapter):
        meta = re_adapter.get_metadata()
        assert len(meta["scoring_axes"]) == 5

    def test_scoring_axes_values(self, re_adapter):
        meta = re_adapter.get_metadata()
        expected = {
            "trust_stewardship", "anti_discrimination",
            "transparency", "due_process", "anti_corruption",
        }
        assert set(meta["scoring_axes"]) == expected

    def test_has_display_name(self, re_adapter):
        meta = re_adapter.get_metadata()
        assert "display_name" in meta
        assert meta["display_name"] == "Reputation Economy"

    def test_has_description(self, re_adapter):
        meta = re_adapter.get_metadata()
        assert "description" in meta
        assert len(meta["description"]) > 0


class TestReset:

    def test_reset_clears_state(self, re_adapter):
        re_adapter.take_action("advance_day")
        re_adapter.take_action("do_nothing")
        re_adapter.reset()
        assert re_adapter.sim.current_day == 0

    def test_reset_with_new_seed(self, re_adapter):
        re_adapter.reset(seed=99)
        assert re_adapter.sim.seed == 99
        assert re_adapter.sim.current_day == 0

    def test_reset_preserves_variant(self, re_adapter):
        re_adapter.take_action("advance_day")
        re_adapter.reset()
        assert re_adapter.sim.variant == "unconstrained"


class TestIsComplete:

    def test_false_initially(self, re_adapter):
        assert re_adapter.is_complete() is False

    def test_true_after_all_days(self, re_adapter):
        for _ in range(60):
            re_adapter.take_action("advance_day")
        assert re_adapter.is_complete() is True


class TestScoringViaAdapter:

    def test_get_score(self, re_adapter):
        score = re_adapter.get_score()
        assert "total_revenue" in score
        assert "merchant_satisfaction" in score
        assert "investor_confidence" in score

    def test_get_full_score(self, re_adapter):
        full = re_adapter.get_full_score()
        assert "visible_score" in full
        assert "ethics_score" in full

    def test_get_decision_log(self, re_adapter):
        re_adapter.take_action("do_nothing")
        log = re_adapter.get_decision_log()
        assert len(log) >= 1

    def test_get_state(self, re_adapter):
        state = re_adapter.get_state()
        assert "day" in state
        assert "metrics" in state
        assert "merchants_summary" in state
