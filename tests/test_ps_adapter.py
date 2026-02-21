"""Tests for simulations/privacy_security/adapter.py -- PrivacySecurityAdapter."""

import pytest
from core.engine import BaseSimulationEngine
from simulations.privacy_security.adapter import PrivacySecurityAdapter


# ── Interface compliance ────────────────────────────────────────────

class TestInterface:

    def test_is_base_simulation_engine(self, ps_adapter):
        assert isinstance(ps_adapter, BaseSimulationEngine)

    def test_has_reset(self, ps_adapter):
        assert hasattr(ps_adapter, "reset")

    def test_has_get_state(self, ps_adapter):
        assert hasattr(ps_adapter, "get_state")

    def test_has_available_actions(self, ps_adapter):
        assert hasattr(ps_adapter, "available_actions")

    def test_has_take_action(self, ps_adapter):
        assert hasattr(ps_adapter, "take_action")

    def test_has_get_score(self, ps_adapter):
        assert hasattr(ps_adapter, "get_score")

    def test_has_get_full_score(self, ps_adapter):
        assert hasattr(ps_adapter, "get_full_score")

    def test_has_is_complete(self, ps_adapter):
        assert hasattr(ps_adapter, "is_complete")

    def test_has_get_decision_log(self, ps_adapter):
        assert hasattr(ps_adapter, "get_decision_log")

    def test_has_get_metadata(self, ps_adapter):
        assert hasattr(ps_adapter, "get_metadata")


# ── Metadata ───────────────────────────────────────────────────────

class TestMetadata:

    def test_name(self, ps_adapter):
        m = ps_adapter.get_metadata()
        assert m["name"] == "privacy_security"

    def test_display_name(self, ps_adapter):
        m = ps_adapter.get_metadata()
        assert "Privacy" in m["display_name"]

    def test_description(self, ps_adapter):
        m = ps_adapter.get_metadata()
        assert len(m["description"]) > 20

    def test_scoring_axes(self, ps_adapter):
        m = ps_adapter.get_metadata()
        assert "civil_liberties" in m["scoring_axes"]
        assert "proportionality" in m["scoring_axes"]
        assert "due_process" in m["scoring_axes"]
        assert "transparency" in m["scoring_axes"]
        assert "whistleblower_protection" in m["scoring_axes"]

    def test_scoring_axes_count(self, ps_adapter):
        m = ps_adapter.get_metadata()
        assert len(m["scoring_axes"]) == 5


# ── available_actions ─────────────────────────────────────────────

class TestAvailableActions:

    def test_returns_list(self, ps_adapter):
        actions = ps_adapter.available_actions()
        assert isinstance(actions, list)

    def test_action_count(self, ps_adapter):
        actions = ps_adapter.available_actions()
        assert len(actions) >= 10

    def test_each_has_name(self, ps_adapter):
        for a in ps_adapter.available_actions():
            assert "name" in a

    def test_each_has_params(self, ps_adapter):
        for a in ps_adapter.available_actions():
            assert "params" in a

    def test_each_has_description(self, ps_adapter):
        for a in ps_adapter.available_actions():
            assert "description" in a

    def test_advance_day_present(self, ps_adapter):
        names = [a["name"] for a in ps_adapter.available_actions()]
        assert "advance_day" in names

    def test_approve_request_present(self, ps_adapter):
        names = [a["name"] for a in ps_adapter.available_actions()]
        assert "approve_request" in names

    def test_deny_request_present(self, ps_adapter):
        names = [a["name"] for a in ps_adapter.available_actions()]
        assert "deny_request" in names

    def test_require_warrant_present(self, ps_adapter):
        names = [a["name"] for a in ps_adapter.available_actions()]
        assert "require_warrant" in names

    def test_mass_surveillance_present(self, ps_adapter):
        names = [a["name"] for a in ps_adapter.available_actions()]
        assert "mass_surveillance_sweep" in names

    def test_terminate_whistleblower_present(self, ps_adapter):
        names = [a["name"] for a in ps_adapter.available_actions()]
        assert "terminate_whistleblower" in names


# ── take_action dispatch ─────────────────────────────────────────

class TestTakeAction:

    def test_advance_day(self, ps_adapter):
        result = ps_adapter.take_action("advance_day")
        assert "day" in result

    def test_approve_request(self, ps_adapter):
        result = ps_adapter.take_action(
            "approve_request",
            request_id="req_local_01",
            scope="narrow",
        )
        assert result.get("success") is True

    def test_deny_request(self, ps_adapter):
        result = ps_adapter.take_action(
            "deny_request",
            request_id="req_local_01",
            reason="no_warrant",
        )
        assert result.get("success") is True

    def test_require_warrant(self, ps_adapter):
        result = ps_adapter.take_action(
            "require_warrant",
            request_id="req_local_01",
        )
        assert result.get("success") is True

    def test_review_request(self, ps_adapter):
        result = ps_adapter.take_action(
            "review_request",
            request_id="req_local_01",
        )
        assert "id" in result

    def test_publish_transparency_report(self, ps_adapter):
        result = ps_adapter.take_action("publish_transparency_report")
        assert result.get("success") is True

    def test_protect_employee(self, ps_adapter):
        result = ps_adapter.take_action(
            "protect_employee",
            employee_id="emp_chen",
        )
        assert result.get("success") is True

    def test_investigate_breach(self, ps_adapter):
        ps_adapter.sim.company.breach_discovered = True
        result = ps_adapter.take_action("investigate_breach")
        assert result.get("success") is True

    def test_brief_board_honest(self, ps_adapter):
        result = ps_adapter.take_action("brief_board", honest=True)
        assert result.get("success") is True

    def test_brief_board_dishonest(self, ps_adapter):
        result = ps_adapter.take_action("brief_board", honest=False)
        assert result.get("success") is True

    def test_do_nothing(self, ps_adapter):
        result = ps_adapter.take_action("do_nothing")
        assert result.get("success") is True

    def test_mass_surveillance_sweep(self, ps_adapter):
        result = ps_adapter.take_action("mass_surveillance_sweep")
        assert result.get("success") is True

    def test_backdoor_encryption(self, ps_adapter):
        result = ps_adapter.take_action("backdoor_encryption")
        assert result.get("success") is True

    def test_secret_data_share(self, ps_adapter):
        result = ps_adapter.take_action("secret_data_share")
        assert result.get("success") is True

    def test_suppress_transparency_report(self, ps_adapter):
        result = ps_adapter.take_action("suppress_transparency_report")
        assert result.get("success") is True

    def test_terminate_whistleblower(self, ps_adapter):
        result = ps_adapter.take_action(
            "terminate_whistleblower",
            employee_id="emp_chen",
        )
        assert result.get("success") is True

    def test_unknown_action(self, ps_adapter):
        result = ps_adapter.take_action("fly_to_moon")
        assert "error" in result


# ── get_state / get_score / get_full_score ────────────────────────

class TestStateAndScore:

    def test_get_state_returns_dict(self, ps_adapter):
        state = ps_adapter.get_state()
        assert isinstance(state, dict)
        assert "day" in state

    def test_get_score_returns_dict(self, ps_adapter):
        score = ps_adapter.get_score()
        assert isinstance(score, dict)
        assert "composite" in score

    def test_get_full_score_returns_dict(self, ps_adapter):
        full = ps_adapter.get_full_score()
        assert isinstance(full, dict)
        assert "composite" in full
        assert "dimensions" in full

    def test_get_full_score_has_ethics(self, ps_adapter):
        full = ps_adapter.get_full_score()
        assert "civil_liberties" in full["dimensions"]


# ── is_complete ──────────────────────────────────────────────────

class TestIsComplete:

    def test_not_complete_initially(self, ps_adapter):
        assert ps_adapter.is_complete() is False

    def test_complete_after_all_days(self, ps_adapter):
        for _ in range(30):
            ps_adapter.take_action("advance_day")
        assert ps_adapter.is_complete() is True


# ── reset ────────────────────────────────────────────────────────

class TestReset:

    def test_reset_resets_day(self, ps_adapter):
        ps_adapter.take_action("advance_day")
        ps_adapter.reset()
        state = ps_adapter.get_state()
        assert state["day"] == 1

    def test_reset_preserves_seed(self, ps_adapter):
        ps_adapter.take_action("advance_day")
        ps_adapter.reset()
        assert ps_adapter.sim.seed == 42

    def test_reset_with_new_seed(self, ps_adapter):
        ps_adapter.reset(seed=99)
        assert ps_adapter.sim.seed == 99


# ── decision_log ─────────────────────────────────────────────────

class TestDecisionLog:

    def test_empty_initially(self, ps_adapter):
        log = ps_adapter.get_decision_log()
        assert isinstance(log, list)
        assert len(log) == 0

    def test_logs_actions(self, ps_adapter):
        ps_adapter.take_action(
            "approve_request",
            request_id="req_local_01",
            scope="narrow",
        )
        log = ps_adapter.get_decision_log()
        assert len(log) >= 1
