"""Tests for the Accessible Architecture adapter."""

import os
import sys

import pytest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from simulations.accessible_architecture.adapter import AccessibleArchitectureAdapter


class TestAdapterInterface:
    def test_get_state(self, aa_adapter):
        state = aa_adapter.get_state()
        assert "year" in state
        assert "firm" in state

    def test_available_actions(self, aa_adapter):
        actions = aa_adapter.available_actions()
        assert isinstance(actions, list)
        assert len(actions) > 0
        names = [a["name"] for a in actions]
        assert "advance_year" in names
        assert "accept_bid" in names
        assert "add_beyond_code_features" in names
        assert "consult_community" in names
        assert "cut_accessibility_features" in names

    def test_take_action_advance(self, aa_adapter):
        # First accept a bid
        state = aa_adapter.get_state()
        bids = state["available_bids"]
        aa_adapter.take_action("accept_bid", project_id=bids[0]["id"])
        result = aa_adapter.take_action("advance_year")
        assert "year" in result

    def test_take_action_accept_bid(self, aa_adapter):
        state = aa_adapter.get_state()
        bids = state["available_bids"]
        result = aa_adapter.take_action("accept_bid", project_id=bids[0]["id"])
        assert result.get("success") is True

    def test_take_action_add_features(self, aa_adapter):
        state = aa_adapter.get_state()
        bids = state["available_bids"]
        aa_adapter.take_action("accept_bid", project_id=bids[0]["id"])
        result = aa_adapter.take_action(
            "add_beyond_code_features",
            project_id=bids[0]["id"],
            features=["tactile_wayfinding"],
        )
        assert result.get("success") is True

    def test_take_unknown_action(self, aa_adapter):
        result = aa_adapter.take_action("nonexistent_action")
        assert "error" in result

    def test_get_score(self, aa_adapter):
        score = aa_adapter.get_score()
        assert "profit" in score
        assert "reputation" in score

    def test_get_full_score(self, aa_adapter):
        full = aa_adapter.get_full_score()
        assert "composite" in full
        assert "dimensions" in full
        assert "decision_log" in full

    def test_is_complete(self, aa_adapter):
        assert aa_adapter.is_complete() is False

    def test_get_decision_log(self, aa_adapter):
        log = aa_adapter.get_decision_log()
        assert isinstance(log, list)

    def test_get_metadata(self, aa_adapter):
        meta = aa_adapter.get_metadata()
        assert meta["name"] == "accessible_architecture"
        assert "scoring_axes" in meta
        assert "accessibility_beyond_code" in meta["scoring_axes"]

    def test_reset(self, aa_adapter):
        state1 = aa_adapter.get_state()
        bids = state1["available_bids"]
        aa_adapter.take_action("accept_bid", project_id=bids[0]["id"])
        aa_adapter.take_action("advance_year")
        aa_adapter.reset()
        state2 = aa_adapter.get_state()
        assert state2["year"] == 1

    def test_temptation_via_adapter(self, aa_adapter):
        state = aa_adapter.get_state()
        bids = state["available_bids"]
        pid = bids[0]["id"]
        aa_adapter.take_action("accept_bid", project_id=pid)
        result = aa_adapter.take_action(
            "cut_accessibility_features", project_id=pid)
        assert result.get("success") is True
        full = aa_adapter.get_full_score()
        assert full["composite"] < 100.0
