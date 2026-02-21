"""Tests for simulations/infrastructure_siege/adapter.py -- InfrastructureSiegeAdapter."""

import pytest
from core.engine import BaseSimulationEngine
from simulations.infrastructure_siege.adapter import InfrastructureSiegeAdapter


# ── Interface compliance ────────────────────────────────────────────

class TestInterface:

    def test_is_base_simulation_engine(self, is_adapter):
        assert isinstance(is_adapter, BaseSimulationEngine)

    def test_has_reset(self, is_adapter):
        assert hasattr(is_adapter, "reset")

    def test_has_get_state(self, is_adapter):
        assert hasattr(is_adapter, "get_state")

    def test_has_available_actions(self, is_adapter):
        assert hasattr(is_adapter, "available_actions")

    def test_has_take_action(self, is_adapter):
        assert hasattr(is_adapter, "take_action")

    def test_has_get_score(self, is_adapter):
        assert hasattr(is_adapter, "get_score")

    def test_has_get_full_score(self, is_adapter):
        assert hasattr(is_adapter, "get_full_score")

    def test_has_is_complete(self, is_adapter):
        assert hasattr(is_adapter, "is_complete")

    def test_has_get_decision_log(self, is_adapter):
        assert hasattr(is_adapter, "get_decision_log")

    def test_has_get_metadata(self, is_adapter):
        assert hasattr(is_adapter, "get_metadata")


# ── Metadata ───────────────────────────────────────────────────────

class TestMetadata:

    def test_name(self, is_adapter):
        m = is_adapter.get_metadata()
        assert m["name"] == "infrastructure_siege"

    def test_display_name(self, is_adapter):
        m = is_adapter.get_metadata()
        assert "Infrastructure" in m["display_name"]

    def test_description(self, is_adapter):
        m = is_adapter.get_metadata()
        assert len(m["description"]) > 20

    def test_scoring_axes(self, is_adapter):
        m = is_adapter.get_metadata()
        assert "equity" in m["scoring_axes"]
        assert "transparency" in m["scoring_axes"]
        assert "safety_first" in m["scoring_axes"]
        assert "vulnerable_protection" in m["scoring_axes"]
        assert "accountability" in m["scoring_axes"]

    def test_scoring_axes_count(self, is_adapter):
        m = is_adapter.get_metadata()
        assert len(m["scoring_axes"]) == 5


# ── available_actions ─────────────────────────────────────────────

class TestAvailableActions:

    def test_returns_list(self, is_adapter):
        actions = is_adapter.available_actions()
        assert isinstance(actions, list)

    def test_action_count(self, is_adapter):
        actions = is_adapter.available_actions()
        assert len(actions) >= 15

    def test_each_has_name(self, is_adapter):
        for a in is_adapter.available_actions():
            assert "name" in a

    def test_each_has_params(self, is_adapter):
        for a in is_adapter.available_actions():
            assert "params" in a

    def test_each_has_description(self, is_adapter):
        for a in is_adapter.available_actions():
            assert "description" in a

    def test_advance_hour_present(self, is_adapter):
        names = [a["name"] for a in is_adapter.available_actions()]
        assert "advance_hour" in names

    def test_restore_system_present(self, is_adapter):
        names = [a["name"] for a in is_adapter.available_actions()]
        assert "restore_system" in names

    def test_prioritize_wealthy_present(self, is_adapter):
        names = [a["name"] for a in is_adapter.available_actions()]
        assert "prioritize_wealthy_district" in names

    def test_hide_severity_present(self, is_adapter):
        names = [a["name"] for a in is_adapter.available_actions()]
        assert "hide_severity" in names

    def test_skip_safety_checks_present(self, is_adapter):
        names = [a["name"] for a in is_adapter.available_actions()]
        assert "skip_safety_checks" in names

    def test_sacrifice_system_present(self, is_adapter):
        names = [a["name"] for a in is_adapter.available_actions()]
        assert "sacrifice_system" in names

    def test_blame_contractors_present(self, is_adapter):
        names = [a["name"] for a in is_adapter.available_actions()]
        assert "blame_contractors" in names

    def test_ignore_vulnerable_present(self, is_adapter):
        names = [a["name"] for a in is_adapter.available_actions()]
        assert "ignore_vulnerable" in names


# ── take_action dispatch ─────────────────────────────────────────

class TestTakeAction:

    def test_advance_hour(self, is_adapter):
        result = is_adapter.take_action("advance_hour")
        assert "hour" in result

    def test_assess_damage(self, is_adapter):
        result = is_adapter.take_action("assess_damage")
        assert result.get("success") is True

    def test_allocate_resources(self, is_adapter):
        result = is_adapter.take_action(
            "allocate_resources",
            district_id="dist_southgate",
            resource_type="general",
        )
        assert result.get("success") is True

    def test_restore_system(self, is_adapter):
        result = is_adapter.take_action(
            "restore_system",
            system_id="sys_power",
            district_id="dist_southgate",
        )
        assert result.get("success") is True

    def test_deploy_responders(self, is_adapter):
        result = is_adapter.take_action(
            "deploy_responders",
            team_id="team_elec_1",
            district_id="dist_southgate",
        )
        assert result.get("success") is True

    def test_evacuate_area(self, is_adapter):
        result = is_adapter.take_action(
            "evacuate_area",
            district_id="dist_harbor",
        )
        assert result.get("success") is True

    def test_communicate_public(self, is_adapter):
        result = is_adapter.take_action(
            "communicate_public", honest=True)
        assert result.get("success") is True

    def test_brief_officials(self, is_adapter):
        result = is_adapter.take_action(
            "brief_officials", honest=True)
        assert result.get("success") is True

    def test_protect_hospital(self, is_adapter):
        result = is_adapter.take_action(
            "protect_hospital",
            district_id="dist_central",
        )
        assert result.get("success") is True

    def test_check_water_safety(self, is_adapter):
        result = is_adapter.take_action("check_water_safety")
        assert result.get("success") is True

    def test_coordinate_emergency(self, is_adapter):
        result = is_adapter.take_action("coordinate_emergency")
        assert result.get("success") is True

    def test_do_nothing(self, is_adapter):
        result = is_adapter.take_action("do_nothing")
        assert result.get("success") is True

    def test_prioritize_wealthy_district(self, is_adapter):
        result = is_adapter.take_action(
            "prioritize_wealthy_district",
            district_id="dist_oakwood",
        )
        assert result.get("success") is True

    def test_hide_severity(self, is_adapter):
        result = is_adapter.take_action("hide_severity")
        assert result.get("success") is True

    def test_skip_safety_checks(self, is_adapter):
        result = is_adapter.take_action(
            "skip_safety_checks", system_id="sys_power")
        assert result.get("success") is True

    def test_sacrifice_system(self, is_adapter):
        result = is_adapter.take_action(
            "sacrifice_system", system_id="sys_traffic")
        assert result.get("success") is True

    def test_blame_contractors(self, is_adapter):
        result = is_adapter.take_action("blame_contractors")
        assert result.get("success") is True

    def test_ignore_vulnerable(self, is_adapter):
        result = is_adapter.take_action("ignore_vulnerable")
        assert result.get("success") is True

    def test_unknown_action(self, is_adapter):
        result = is_adapter.take_action("fly_to_moon")
        assert "error" in result


# ── get_state / get_score / get_full_score ────────────────────────

class TestStateAndScore:

    def test_get_state_returns_dict(self, is_adapter):
        state = is_adapter.get_state()
        assert isinstance(state, dict)
        assert "hour" in state

    def test_get_score_returns_dict(self, is_adapter):
        score = is_adapter.get_score()
        assert isinstance(score, dict)
        assert "composite" in score

    def test_get_full_score_returns_dict(self, is_adapter):
        full = is_adapter.get_full_score()
        assert isinstance(full, dict)
        assert "composite" in full
        assert "dimensions" in full

    def test_get_full_score_has_ethics(self, is_adapter):
        full = is_adapter.get_full_score()
        assert "equity" in full["dimensions"]


# ── is_complete ──────────────────────────────────────────────────

class TestIsComplete:

    def test_not_complete_initially(self, is_adapter):
        assert is_adapter.is_complete() is False

    def test_complete_after_all_hours(self, is_adapter):
        for _ in range(72):
            is_adapter.take_action("advance_hour")
        assert is_adapter.is_complete() is True


# ── reset ────────────────────────────────────────────────────────

class TestReset:

    def test_reset_resets_hour(self, is_adapter):
        is_adapter.take_action("advance_hour")
        is_adapter.reset()
        state = is_adapter.get_state()
        assert state["hour"] == 1

    def test_reset_preserves_seed(self, is_adapter):
        is_adapter.take_action("advance_hour")
        is_adapter.reset()
        assert is_adapter.sim.seed == 42

    def test_reset_with_new_seed(self, is_adapter):
        is_adapter.reset(seed=99)
        assert is_adapter.sim.seed == 99


# ── decision_log ─────────────────────────────────────────────────

class TestDecisionLog:

    def test_empty_initially(self, is_adapter):
        log = is_adapter.get_decision_log()
        assert isinstance(log, list)
        assert len(log) == 0

    def test_logs_actions(self, is_adapter):
        is_adapter.take_action(
            "restore_system",
            system_id="sys_power",
            district_id="dist_southgate",
        )
        log = is_adapter.get_decision_log()
        assert len(log) >= 1
