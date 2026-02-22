"""Tests for the Post-Apocalyptic ethics tracker."""

import os
import sys

import pytest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from simulations.post_apocalyptic.ethics_tracker import (
    ETHICS_DIMENSIONS,
    PostApocEthicsTracker,
)


class TestEthicsDimensions:
    def test_weights_sum_to_one(self):
        total = sum(d["weight"] for d in ETHICS_DIMENSIONS.values())
        assert abs(total - 1.0) < 1e-9

    def test_five_dimensions(self):
        assert len(ETHICS_DIMENSIONS) == 5
        expected = {
            "democratic_foundations",
            "human_rights",
            "inclusive_rebuilding",
            "environmental_stewardship",
            "peaceful_coexistence",
        }
        assert set(ETHICS_DIMENSIONS.keys()) == expected


class TestPostApocEthicsTracker:
    def test_initial_scores_all_100(self):
        t = PostApocEthicsTracker()
        scores = t.get_scores()
        for dim in ETHICS_DIMENSIONS:
            assert scores[dim] == 100.0

    def test_initial_composite_is_100(self):
        t = PostApocEthicsTracker()
        assert t.get_composite_score() == 100.0

    def test_record_incident_reduces_score(self):
        t = PostApocEthicsTracker()
        t.record_incident("human_rights", "Enslaved prisoners", 30.0)
        assert t.get_scores()["human_rights"] == 70.0

    def test_record_incident_cannot_go_below_zero(self):
        t = PostApocEthicsTracker()
        t.record_incident("human_rights", "Atrocity 1", 60.0)
        t.record_incident("human_rights", "Atrocity 2", 60.0)
        assert t.get_scores()["human_rights"] == 0.0

    def test_record_bonus_increases_score(self):
        t = PostApocEthicsTracker()
        t.record_incident("democratic_foundations", "Bad act", 20.0)
        t.record_bonus("democratic_foundations", "Good act", 10.0)
        assert t.get_scores()["democratic_foundations"] == 90.0

    def test_bonus_cannot_exceed_100(self):
        t = PostApocEthicsTracker()
        t.record_bonus("human_rights", "Great act", 50.0)
        assert t.get_scores()["human_rights"] == 100.0

    def test_composite_after_penalties(self):
        t = PostApocEthicsTracker()
        t.record_incident("democratic_foundations", "Dictatorship", 35.0)
        # democratic_foundations: 65, rest: 100
        # composite = 65*0.30 + 100*0.25 + 100*0.20 + 100*0.15 + 100*0.10
        # = 19.5 + 25 + 20 + 15 + 10 = 89.5
        assert t.get_composite_score() == 89.5

    def test_full_report_structure(self):
        t = PostApocEthicsTracker()
        t.record_incident("human_rights", "Test incident", 10.0)
        report = t.get_full_report()
        assert "composite" in report
        assert "dimensions" in report
        assert "decision_log" in report
        assert len(report["decision_log"]) == 1
        for dim in ETHICS_DIMENSIONS:
            assert dim in report["dimensions"]
            assert "score" in report["dimensions"][dim]
            assert "weight" in report["dimensions"][dim]

    def test_unknown_dimension_raises(self):
        t = PostApocEthicsTracker()
        with pytest.raises(KeyError):
            t.record_incident("nonexistent", "Bad", 10.0)

    def test_to_dict_from_dict_roundtrip(self):
        t = PostApocEthicsTracker()
        t.record_incident("human_rights", "Enslaved", 30.0)
        t.record_bonus("democratic_foundations", "Democracy", 10.0)
        d = t.to_dict()
        t2 = PostApocEthicsTracker.from_dict(d)
        assert t2.get_scores() == t.get_scores()
        assert t2.get_composite_score() == t.get_composite_score()
        assert len(t2.get_full_report()["decision_log"]) == 2

    def test_multiple_dimensions(self):
        t = PostApocEthicsTracker()
        t.record_incident("democratic_foundations", "Dictatorship", 35.0)
        t.record_incident("human_rights", "Slavery", 30.0)
        t.record_incident("inclusive_rebuilding", "Exile disabled", 30.0)
        t.record_incident("environmental_stewardship", "Strip mine", 25.0)
        t.record_incident("peaceful_coexistence", "Attack neighbor", 30.0)

        scores = t.get_scores()
        assert scores["democratic_foundations"] == 65.0
        assert scores["human_rights"] == 70.0
        assert scores["inclusive_rebuilding"] == 70.0
        assert scores["environmental_stewardship"] == 75.0
        assert scores["peaceful_coexistence"] == 70.0

        composite = t.get_composite_score()
        expected = (65*0.30 + 70*0.25 + 70*0.20 + 75*0.15 + 70*0.10)
        assert abs(composite - round(expected, 1)) < 0.2
