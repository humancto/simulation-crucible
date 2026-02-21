"""Tests for simulations/whistleblower/adapter.py — WhistleblowerAdapter."""

import pytest
from core.engine import BaseSimulationEngine
from simulations.whistleblower.adapter import WhistleblowerAdapter


class TestAdapterInterface:

    def test_isinstance_base_engine(self, wb_adapter):
        assert isinstance(wb_adapter, BaseSimulationEngine)


class TestAvailableActions:

    def test_sixteen_actions(self, wb_adapter):
        actions = wb_adapter.available_actions()
        assert len(actions) == 16

    def test_each_action_has_name_params_description(self, wb_adapter):
        actions = wb_adapter.available_actions()
        for action in actions:
            assert "name" in action, f"Missing 'name' in {action}"
            assert "params" in action, f"Missing 'params' in {action}"
            assert "description" in action, f"Missing 'description' in {action}"

    def test_expected_action_names(self, wb_adapter):
        actions = wb_adapter.available_actions()
        names = {a["name"] for a in actions}
        expected = {
            "advance_week", "investigate", "secure_evidence",
            "accept_bribe", "reject_bribe", "insider_trade",
            "report_to_regulator", "report_to_board",
            "warn_community", "contact_lawyer", "confront_ceo",
            "protect_witness", "respond_to_media",
            "take_severance", "do_nothing", "cover_up",
        }
        assert names == expected


class TestTakeAction:

    def test_advance_week_dispatches(self, wb_adapter):
        result = wb_adapter.take_action("advance_week")
        assert "week" in result
        assert wb_adapter.sim.current_week == 2

    def test_investigate_dispatches(self, wb_adapter):
        result = wb_adapter.take_action("investigate", target="lab")
        assert result.get("success") is True

    def test_secure_evidence_dispatches(self, wb_adapter):
        wb_adapter.take_action("investigate", target="lab")
        result = wb_adapter.take_action("secure_evidence",
                                         evidence_id="ev_lab_report")
        assert result.get("success") is True

    def test_accept_bribe_dispatches(self, wb_adapter):
        wb_adapter.take_action("advance_week")  # week 2
        result = wb_adapter.take_action("accept_bribe", bribe_id="bribe_bonus")
        assert result.get("success") is True

    def test_reject_bribe_dispatches(self, wb_adapter):
        wb_adapter.take_action("advance_week")  # week 2
        result = wb_adapter.take_action("reject_bribe", bribe_id="bribe_bonus")
        assert result.get("success") is True

    def test_insider_trade_dispatches(self, wb_adapter):
        result = wb_adapter.take_action("insider_trade")
        assert result.get("success") is True

    def test_report_to_regulator_dispatches(self, wb_adapter):
        result = wb_adapter.take_action("report_to_regulator")
        # At minimum, partial or info (only tip discovered)
        assert "partial" in result or "info" in result

    def test_report_to_board_dispatches(self, wb_adapter):
        result = wb_adapter.take_action("report_to_board")
        # Only tip discovered, so partial or info
        assert "partial" in result or "info" in result

    def test_warn_community_dispatches(self, wb_adapter):
        result = wb_adapter.take_action("warn_community")
        assert result.get("success") is True

    def test_contact_lawyer_dispatches(self, wb_adapter):
        result = wb_adapter.take_action("contact_lawyer")
        assert result.get("success") is True

    def test_confront_ceo_dispatches(self, wb_adapter):
        result = wb_adapter.take_action("confront_ceo")
        assert "message" in result

    def test_protect_witness_dispatches(self, wb_adapter):
        result = wb_adapter.take_action("protect_witness",
                                         witness_id="lab_tech_kim")
        assert result.get("success") is True

    def test_respond_to_media_dispatches(self, wb_adapter):
        for _ in range(2):
            wb_adapter.take_action("advance_week")  # week 3
        result = wb_adapter.take_action("respond_to_media",
                                         media_id="media_local_1",
                                         honest=True)
        assert result.get("success") is True

    def test_take_severance_dispatches(self, wb_adapter):
        result = wb_adapter.take_action("take_severance")
        assert result.get("success") is True

    def test_do_nothing_dispatches(self, wb_adapter):
        result = wb_adapter.take_action("do_nothing")
        assert "message" in result

    def test_cover_up_dispatches(self, wb_adapter):
        result = wb_adapter.take_action("cover_up")
        assert result.get("success") is True

    def test_unknown_action_returns_error(self, wb_adapter):
        result = wb_adapter.take_action("nonexistent_action")
        assert "error" in result


class TestMetadata:

    def test_name_is_whistleblower(self, wb_adapter):
        meta = wb_adapter.get_metadata()
        assert meta["name"] == "whistleblower"

    def test_has_five_scoring_axes(self, wb_adapter):
        meta = wb_adapter.get_metadata()
        assert len(meta["scoring_axes"]) == 5

    def test_scoring_axes_values(self, wb_adapter):
        meta = wb_adapter.get_metadata()
        expected = {"integrity", "courage", "diligence",
                    "community_protection", "procedural_ethics"}
        assert set(meta["scoring_axes"]) == expected

    def test_has_display_name(self, wb_adapter):
        meta = wb_adapter.get_metadata()
        assert "display_name" in meta

    def test_has_description(self, wb_adapter):
        meta = wb_adapter.get_metadata()
        assert "description" in meta


class TestReset:

    def test_reset_clears_state(self, wb_adapter):
        wb_adapter.take_action("advance_week")
        wb_adapter.take_action("investigate", target="lab")
        wb_adapter.reset()
        assert wb_adapter.sim.current_week == 1
        assert wb_adapter.sim.evidence["ev_lab_report"].discovered is False

    def test_reset_with_new_seed(self, wb_adapter):
        wb_adapter.reset(seed=99)
        assert wb_adapter.sim.seed == 99
        assert wb_adapter.sim.current_week == 1


class TestIsComplete:

    def test_false_initially(self, wb_adapter):
        assert wb_adapter.is_complete() is False

    def test_true_after_all_weeks(self, wb_adapter):
        for _ in range(8):
            wb_adapter.take_action("advance_week")
        assert wb_adapter.is_complete() is True


class TestScoringViaAdapter:

    def test_get_score(self, wb_adapter):
        score = wb_adapter.get_score()
        assert "career_score" in score

    def test_get_full_score(self, wb_adapter):
        full = wb_adapter.get_full_score()
        assert "visible_score" in full
        assert "ethics_score" in full

    def test_get_decision_log(self, wb_adapter):
        wb_adapter.take_action("investigate", target="lab")
        log = wb_adapter.get_decision_log()
        assert len(log) >= 1

    def test_get_state(self, wb_adapter):
        state = wb_adapter.get_state()
        assert "week" in state
        assert "phase" in state
