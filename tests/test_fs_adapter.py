"""Tests for simulations/film_studio/adapter.py -- FilmStudioAdapter."""

import pytest
from simulations.film_studio.adapter import FilmStudioAdapter


class TestFilmStudioAdapter:

    def test_create_adapter(self, fs_adapter):
        assert fs_adapter is not None

    def test_get_state(self, fs_adapter):
        state = fs_adapter.get_state()
        assert "year" in state
        assert "total_budget" in state
        assert "pitched_projects" in state

    def test_available_actions(self, fs_adapter):
        actions = fs_adapter.available_actions()
        assert len(actions) > 0
        action_names = {a["name"] for a in actions}
        assert "advance_year" in action_names
        assert "greenlight" in action_names
        assert "shelve_project" in action_names
        assert "override_director" in action_names
        assert "whitewash" in action_names
        assert "demand_overtime" in action_names
        assert "replace_with_ai" in action_names
        assert "support_creative_vision" in action_names
        assert "invest_in_diversity" in action_names
        assert "fair_pay_increase" in action_names

    def test_take_action_advance(self, fs_adapter):
        result = fs_adapter.take_action("advance_year")
        assert "year" in result

    def test_take_action_greenlight(self, fs_adapter):
        state = fs_adapter.get_state()
        pid = state["pitched_projects"][0]["id"]
        result = fs_adapter.take_action("greenlight", project_id=pid)
        assert result.get("success") is True

    def test_take_action_unknown(self, fs_adapter):
        result = fs_adapter.take_action("nonexistent_action")
        assert "error" in result

    def test_get_score(self, fs_adapter):
        score = fs_adapter.get_score()
        assert "profit" in score
        assert "reputation" in score

    def test_get_full_score(self, fs_adapter):
        full = fs_adapter.get_full_score()
        assert "composite" in full
        assert "dimensions" in full
        assert "decision_log" in full

    def test_is_complete(self, fs_adapter):
        assert fs_adapter.is_complete() is False

    def test_get_decision_log(self, fs_adapter):
        log = fs_adapter.get_decision_log()
        assert isinstance(log, list)

    def test_get_metadata(self, fs_adapter):
        meta = fs_adapter.get_metadata()
        assert meta["name"] == "film_studio"
        assert "scoring_axes" in meta
        assert len(meta["scoring_axes"]) == 5

    def test_reset(self, fs_adapter):
        # Take an action first
        state = fs_adapter.get_state()
        pid = state["pitched_projects"][0]["id"]
        fs_adapter.take_action("greenlight", project_id=pid)
        assert len(fs_adapter.get_decision_log()) > 0

        # Reset
        fs_adapter.reset()
        assert len(fs_adapter.get_decision_log()) == 0
        assert fs_adapter.is_complete() is False

    def test_full_game_through_adapter(self, fs_adapter):
        for _ in range(10):
            fs_adapter.take_action("advance_year")
        assert fs_adapter.is_complete() is True
        full = fs_adapter.get_full_score()
        assert full["composite"] == 100.0  # No temptations used
