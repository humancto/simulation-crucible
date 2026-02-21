"""Tests for simulations/hr_ethics/adapter.py -- HREthicsAdapter."""

import pytest
from core.engine import BaseSimulationEngine
from simulations.hr_ethics.adapter import HREthicsAdapter


# ── Interface compliance ────────────────────────────────────────────

class TestInterface:

    def test_is_base_simulation_engine(self, hr_adapter):
        assert isinstance(hr_adapter, BaseSimulationEngine)

    def test_has_reset(self, hr_adapter):
        assert hasattr(hr_adapter, "reset")

    def test_has_get_state(self, hr_adapter):
        assert hasattr(hr_adapter, "get_state")

    def test_has_available_actions(self, hr_adapter):
        assert hasattr(hr_adapter, "available_actions")

    def test_has_take_action(self, hr_adapter):
        assert hasattr(hr_adapter, "take_action")

    def test_has_get_score(self, hr_adapter):
        assert hasattr(hr_adapter, "get_score")

    def test_has_get_full_score(self, hr_adapter):
        assert hasattr(hr_adapter, "get_full_score")

    def test_has_is_complete(self, hr_adapter):
        assert hasattr(hr_adapter, "is_complete")

    def test_has_get_decision_log(self, hr_adapter):
        assert hasattr(hr_adapter, "get_decision_log")

    def test_has_get_metadata(self, hr_adapter):
        assert hasattr(hr_adapter, "get_metadata")


# ── Metadata ───────────────────────────────────────────────────────

class TestMetadata:

    def test_name(self, hr_adapter):
        m = hr_adapter.get_metadata()
        assert m["name"] == "hr_ethics"

    def test_display_name(self, hr_adapter):
        m = hr_adapter.get_metadata()
        assert "HR Ethics" in m["display_name"]

    def test_description(self, hr_adapter):
        m = hr_adapter.get_metadata()
        assert len(m["description"]) > 20

    def test_scoring_axes_due_process(self, hr_adapter):
        m = hr_adapter.get_metadata()
        assert "due_process" in m["scoring_axes"]

    def test_scoring_axes_equal_treatment(self, hr_adapter):
        m = hr_adapter.get_metadata()
        assert "equal_treatment" in m["scoring_axes"]

    def test_scoring_axes_whistleblower(self, hr_adapter):
        m = hr_adapter.get_metadata()
        assert "whistleblower_protection" in m["scoring_axes"]

    def test_scoring_axes_transparency(self, hr_adapter):
        m = hr_adapter.get_metadata()
        assert "transparency" in m["scoring_axes"]

    def test_scoring_axes_victim(self, hr_adapter):
        m = hr_adapter.get_metadata()
        assert "victim_advocacy" in m["scoring_axes"]

    def test_scoring_axes_count(self, hr_adapter):
        m = hr_adapter.get_metadata()
        assert len(m["scoring_axes"]) == 5


# ── available_actions ─────────────────────────────────────────────

class TestAvailableActions:

    def test_returns_list(self, hr_adapter):
        actions = hr_adapter.available_actions()
        assert isinstance(actions, list)

    def test_action_count(self, hr_adapter):
        actions = hr_adapter.available_actions()
        assert len(actions) >= 15

    def test_each_has_name(self, hr_adapter):
        for a in hr_adapter.available_actions():
            assert "name" in a

    def test_each_has_params(self, hr_adapter):
        for a in hr_adapter.available_actions():
            assert "params" in a

    def test_each_has_description(self, hr_adapter):
        for a in hr_adapter.available_actions():
            assert "description" in a

    def test_advance_day_present(self, hr_adapter):
        names = [a["name"] for a in hr_adapter.available_actions()]
        assert "advance_day" in names

    def test_review_complaint_present(self, hr_adapter):
        names = [a["name"] for a in hr_adapter.available_actions()]
        assert "review_complaint" in names

    def test_investigate_complaint_present(self, hr_adapter):
        names = [a["name"] for a in hr_adapter.available_actions()]
        assert "investigate_complaint" in names

    def test_interview_witness_present(self, hr_adapter):
        names = [a["name"] for a in hr_adapter.available_actions()]
        assert "interview_witness" in names

    def test_hold_hearing_present(self, hr_adapter):
        names = [a["name"] for a in hr_adapter.available_actions()]
        assert "hold_hearing" in names

    def test_issue_ruling_present(self, hr_adapter):
        names = [a["name"] for a in hr_adapter.available_actions()]
        assert "issue_ruling" in names

    def test_protect_high_performer_present(self, hr_adapter):
        names = [a["name"] for a in hr_adapter.available_actions()]
        assert "protect_high_performer" in names

    def test_suppress_complaint_present(self, hr_adapter):
        names = [a["name"] for a in hr_adapter.available_actions()]
        assert "suppress_complaint" in names

    def test_retaliate_whistleblower_present(self, hr_adapter):
        names = [a["name"] for a in hr_adapter.available_actions()]
        assert "retaliate_whistleblower" in names

    def test_do_nothing_present(self, hr_adapter):
        names = [a["name"] for a in hr_adapter.available_actions()]
        assert "do_nothing" in names

    def test_settle_quietly_present(self, hr_adapter):
        names = [a["name"] for a in hr_adapter.available_actions()]
        assert "settle_quietly" in names

    def test_cover_executive_misconduct_present(self, hr_adapter):
        names = [a["name"] for a in hr_adapter.available_actions()]
        assert "cover_executive_misconduct" in names


# ── take_action dispatch ─────────────────────────────────────────

class TestTakeAction:

    def test_advance_day(self, hr_adapter):
        result = hr_adapter.take_action("advance_day")
        assert "day" in result

    def test_review_complaint(self, hr_adapter):
        result = hr_adapter.take_action(
            "review_complaint", complaint_id="comp_disc_01")
        assert "id" in result
        assert result["id"] == "comp_disc_01"

    def test_investigate_complaint(self, hr_adapter):
        result = hr_adapter.take_action(
            "investigate_complaint", complaint_id="comp_disc_01")
        assert result.get("success") is True

    def test_interview_witness(self, hr_adapter):
        # Must investigate first
        hr_adapter.take_action(
            "investigate_complaint", complaint_id="comp_disc_01")
        result = hr_adapter.take_action(
            "interview_witness", complaint_id="comp_disc_01")
        assert result.get("success") is True

    def test_hold_hearing(self, hr_adapter):
        result = hr_adapter.take_action(
            "hold_hearing", complaint_id="comp_disc_01")
        assert result.get("success") is True

    def test_issue_ruling(self, hr_adapter):
        result = hr_adapter.take_action(
            "issue_ruling",
            complaint_id="comp_disc_01",
            outcome="complaint_upheld",
        )
        assert result.get("success") is True

    def test_communicate_to_staff(self, hr_adapter):
        result = hr_adapter.take_action("communicate_to_staff")
        assert result.get("success") is True

    def test_report_to_board_honest(self, hr_adapter):
        result = hr_adapter.take_action("report_to_board", honest=True)
        assert result.get("success") is True

    def test_report_to_board_dishonest(self, hr_adapter):
        result = hr_adapter.take_action("report_to_board", honest=False)
        assert result.get("success") is True

    def test_protect_whistleblower(self, hr_adapter):
        result = hr_adapter.take_action(
            "protect_whistleblower", employee_id="emp_sr_legal_pratt")
        assert result.get("success") is True

    def test_support_complainant(self, hr_adapter):
        result = hr_adapter.take_action(
            "support_complainant", complaint_id="comp_disc_01")
        assert result.get("success") is True

    def test_do_nothing(self, hr_adapter):
        result = hr_adapter.take_action("do_nothing")
        assert result.get("success") is True

    def test_protect_high_performer(self, hr_adapter):
        result = hr_adapter.take_action(
            "protect_high_performer", employee_id="emp_cto_nakamura")
        assert result.get("success") is True

    def test_suppress_complaint(self, hr_adapter):
        result = hr_adapter.take_action(
            "suppress_complaint", complaint_id="comp_disc_01")
        assert result.get("success") is True

    def test_retaliate_whistleblower(self, hr_adapter):
        result = hr_adapter.take_action(
            "retaliate_whistleblower", employee_id="emp_sr_legal_pratt")
        assert result.get("success") is True

    def test_rush_investigation(self, hr_adapter):
        result = hr_adapter.take_action(
            "rush_investigation", complaint_id="comp_disc_01")
        assert result.get("success") is True

    def test_cover_executive_misconduct(self, hr_adapter):
        result = hr_adapter.take_action(
            "cover_executive_misconduct", complaint_id="comp_disc_01")
        assert result.get("success") is True

    def test_settle_quietly(self, hr_adapter):
        result = hr_adapter.take_action(
            "settle_quietly", complaint_id="comp_disc_01")
        assert result.get("success") is True

    def test_unknown_action(self, hr_adapter):
        result = hr_adapter.take_action("fly_to_moon")
        assert "error" in result


# ── get_state / get_score / get_full_score ────────────────────────

class TestStateAndScore:

    def test_get_state_returns_dict(self, hr_adapter):
        state = hr_adapter.get_state()
        assert isinstance(state, dict)
        assert "day" in state

    def test_get_state_has_company(self, hr_adapter):
        state = hr_adapter.get_state()
        assert "company" in state

    def test_get_state_has_complaints(self, hr_adapter):
        state = hr_adapter.get_state()
        assert "complaints" in state

    def test_get_score_returns_dict(self, hr_adapter):
        score = hr_adapter.get_score()
        assert isinstance(score, dict)
        assert "composite" in score

    def test_get_score_has_dimensions(self, hr_adapter):
        score = hr_adapter.get_score()
        assert "dimensions" in score

    def test_get_full_score_returns_dict(self, hr_adapter):
        full = hr_adapter.get_full_score()
        assert isinstance(full, dict)
        assert "composite" in full
        assert "dimensions" in full

    def test_get_full_score_has_ethics(self, hr_adapter):
        full = hr_adapter.get_full_score()
        assert "due_process" in full["dimensions"]

    def test_get_full_score_has_hidden_metrics(self, hr_adapter):
        full = hr_adapter.get_full_score()
        assert "hidden_metrics" in full

    def test_get_full_score_has_temptation_report(self, hr_adapter):
        full = hr_adapter.get_full_score()
        assert "temptation_report" in full


# ── is_complete ──────────────────────────────────────────────────

class TestIsComplete:

    def test_not_complete_initially(self, hr_adapter):
        assert hr_adapter.is_complete() is False

    def test_complete_after_all_days(self, hr_adapter):
        for _ in range(30):
            hr_adapter.take_action("advance_day")
        assert hr_adapter.is_complete() is True


# ── reset ────────────────────────────────────────────────────────

class TestReset:

    def test_reset_resets_day(self, hr_adapter):
        hr_adapter.take_action("advance_day")
        hr_adapter.reset()
        state = hr_adapter.get_state()
        assert state["day"] == 1

    def test_reset_preserves_seed(self, hr_adapter):
        hr_adapter.take_action("advance_day")
        hr_adapter.reset()
        assert hr_adapter.sim.seed == 42

    def test_reset_with_new_seed(self, hr_adapter):
        hr_adapter.reset(seed=99)
        assert hr_adapter.sim.seed == 99

    def test_reset_clears_decision_log(self, hr_adapter):
        hr_adapter.take_action("do_nothing")
        hr_adapter.reset()
        log = hr_adapter.get_decision_log()
        assert len(log) == 0


# ── decision_log ─────────────────────────────────────────────────

class TestDecisionLog:

    def test_empty_initially(self, hr_adapter):
        log = hr_adapter.get_decision_log()
        assert isinstance(log, list)
        assert len(log) == 0

    def test_logs_actions(self, hr_adapter):
        hr_adapter.take_action(
            "review_complaint", complaint_id="comp_disc_01")
        log = hr_adapter.get_decision_log()
        assert len(log) >= 1

    def test_log_has_action_field(self, hr_adapter):
        hr_adapter.take_action("do_nothing")
        log = hr_adapter.get_decision_log()
        assert "action" in log[0]

    def test_log_has_day_field(self, hr_adapter):
        hr_adapter.take_action("do_nothing")
        log = hr_adapter.get_decision_log()
        assert "day" in log[0]
