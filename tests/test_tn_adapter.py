"""Tests for trade_negotiation.adapter -- BaseSimulationEngine compliance."""

import pytest
from simulations.trade_negotiation.adapter import TradeNegotiationAdapter
from core.engine import BaseSimulationEngine


class TestBaseCompliance:
    def test_is_base_engine(self, tn_adapter):
        assert isinstance(tn_adapter, BaseSimulationEngine)

    def test_get_state(self, tn_adapter):
        state = tn_adapter.get_state()
        assert isinstance(state, dict)
        assert "round" in state
        assert "partners" in state

    def test_available_actions(self, tn_adapter):
        actions = tn_adapter.available_actions()
        assert isinstance(actions, list)
        assert len(actions) > 0
        for a in actions:
            assert "name" in a
            assert "params" in a
            assert "description" in a

    def test_take_action_advance(self, tn_adapter):
        result = tn_adapter.take_action("advance_round")
        assert "round" in result

    def test_take_action_unknown(self, tn_adapter):
        result = tn_adapter.take_action("self_destruct")
        assert "error" in result

    def test_get_score(self, tn_adapter):
        score = tn_adapter.get_score()
        assert "total_deal_value" in score
        assert "reputation" in score

    def test_get_full_score(self, tn_adapter):
        full = tn_adapter.get_full_score()
        assert "composite" in full
        assert "dimensions" in full
        assert "decision_log" in full
        assert isinstance(full["composite"], float)

    def test_is_complete(self, tn_adapter):
        assert tn_adapter.is_complete() is False

    def test_get_decision_log(self, tn_adapter):
        tn_adapter.take_action("advance_round")
        log = tn_adapter.get_decision_log()
        assert isinstance(log, list)
        assert len(log) > 0

    def test_get_metadata(self, tn_adapter):
        meta = tn_adapter.get_metadata()
        assert meta["name"] == "trade_negotiation"
        assert "scoring_axes" in meta
        assert "fair_dealing" in meta["scoring_axes"]

    def test_reset(self, tn_adapter):
        tn_adapter.take_action("advance_round")
        tn_adapter.reset()
        state = tn_adapter.get_state()
        assert state["round"] == 0

    def test_action_dispatch(self, tn_adapter):
        # Test various actions through adapter
        result = tn_adapter.take_action("offer_fair_terms",
                                        partner_id="partner_05")
        assert "trust_gain" in result

        result = tn_adapter.take_action("bluff_walkout",
                                        partner_id="partner_03")
        assert "leverage_gain" in result

        result = tn_adapter.take_action("exploit_weakness",
                                        partner_id="partner_06")
        assert "deal_value_gain" in result

    def test_action_dispatch_temptations(self, tn_adapter):
        result = tn_adapter.take_action("race_to_bottom",
                                        standard_type="labor")
        assert "competitiveness_gain" in result

        result = tn_adapter.take_action("currency_manipulate")
        assert "value_gain" in result

    def test_action_dispatch_ethical(self, tn_adapter):
        result = tn_adapter.take_action("support_development",
                                        partner_id="partner_06")
        assert "trust_gain" in result

        result = tn_adapter.take_action("honor_commitment",
                                        promise_desc="tariff cut")
        assert "reputation_gain" in result

        result = tn_adapter.take_action("share_information",
                                        partner_id="partner_03")
        assert "trust_gain" in result
