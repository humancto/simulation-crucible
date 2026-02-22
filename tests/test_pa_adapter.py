"""Tests for the Post-Apocalyptic adapter (BaseSimulationEngine compliance)."""

import os
import sys

import pytest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from core.engine import BaseSimulationEngine
from simulations.post_apocalyptic.adapter import PostApocalypticAdapter


@pytest.fixture
def adapter():
    return PostApocalypticAdapter(seed=42, years=5, variant="unconstrained")


class TestBaseEngineCompliance:
    def test_is_base_engine_subclass(self):
        assert issubclass(PostApocalypticAdapter, BaseSimulationEngine)

    def test_reset(self, adapter):
        adapter.take_action("advance_year")
        adapter.reset(seed=42)
        state = adapter.get_state()
        assert state["year"] == 1

    def test_get_state_returns_dict(self, adapter):
        state = adapter.get_state()
        assert isinstance(state, dict)
        assert "year" in state

    def test_available_actions_returns_list(self, adapter):
        actions = adapter.available_actions()
        assert isinstance(actions, list)
        assert len(actions) > 10
        for a in actions:
            assert "name" in a
            assert "params" in a
            assert "description" in a

    def test_take_action_advance_year(self, adapter):
        result = adapter.take_action("advance_year")
        assert "new_year" in result

    def test_take_action_unknown(self, adapter):
        result = adapter.take_action("nonexistent_action")
        assert "error" in result

    def test_take_action_build(self, adapter):
        result = adapter.take_action("build_structure",
                                      structure_type="farm")
        assert result.get("success")

    def test_take_action_set_governance(self, adapter):
        result = adapter.take_action("set_governance",
                                      gov_type="democracy")
        assert result.get("success")

    def test_get_score_returns_dict(self, adapter):
        score = adapter.get_score()
        assert isinstance(score, dict)
        assert "population" in score

    def test_get_full_score(self, adapter):
        score = adapter.get_full_score()
        assert "composite" in score
        assert "dimensions" in score
        assert "decision_log" in score

    def test_is_complete_initially_false(self, adapter):
        assert adapter.is_complete() is False

    def test_get_decision_log(self, adapter):
        adapter.take_action("advance_year")
        log = adapter.get_decision_log()
        assert isinstance(log, list)
        assert len(log) >= 1

    def test_get_metadata(self, adapter):
        meta = adapter.get_metadata()
        assert meta["name"] == "post_apocalyptic"
        assert "scoring_axes" in meta
        assert len(meta["scoring_axes"]) == 5
