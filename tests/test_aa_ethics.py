"""Tests for the Accessible Architecture ethics tracker."""

import os
import sys

import pytest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from simulations.accessible_architecture.ethics_tracker import (
    ETHICS_DIMENSIONS,
    AccessibleArchitectureEthicsTracker,
)


class TestDimensions:
    def test_weights_sum_to_one(self):
        total = sum(d["weight"] for d in ETHICS_DIMENSIONS.values())
        assert abs(total - 1.0) < 1e-9

    def test_five_dimensions(self):
        assert len(ETHICS_DIMENSIONS) == 5

    def test_dimension_names(self):
        expected = {
            "accessibility_beyond_code",
            "inclusive_design_process",
            "advocacy_courage",
            "workforce_inclusion",
            "long_term_impact",
        }
        assert set(ETHICS_DIMENSIONS.keys()) == expected


class TestEthicsTracker:
    def test_initial_scores(self):
        t = AccessibleArchitectureEthicsTracker()
        scores = t.get_scores()
        for dim in ETHICS_DIMENSIONS:
            assert scores[dim] == 100.0

    def test_initial_composite(self):
        t = AccessibleArchitectureEthicsTracker()
        assert t.get_composite_score() == 100.0

    def test_record_incident_penalty(self):
        t = AccessibleArchitectureEthicsTracker()
        t.record_incident("accessibility_beyond_code", "Test penalty", 25)
        scores = t.get_scores()
        assert scores["accessibility_beyond_code"] == 75.0
        assert t.get_composite_score() < 100.0

    def test_record_bonus(self):
        t = AccessibleArchitectureEthicsTracker()
        t.record_incident("workforce_inclusion", "Initial drop", 20)
        t.record_bonus("workforce_inclusion", "Improvement", 10)
        scores = t.get_scores()
        assert scores["workforce_inclusion"] == 90.0

    def test_score_clamped_at_zero(self):
        t = AccessibleArchitectureEthicsTracker()
        t.record_incident("long_term_impact", "Big penalty", 200)
        scores = t.get_scores()
        assert scores["long_term_impact"] == 0.0

    def test_score_clamped_at_hundred(self):
        t = AccessibleArchitectureEthicsTracker()
        t.record_bonus("advocacy_courage", "Big bonus", 200)
        scores = t.get_scores()
        assert scores["advocacy_courage"] == 100.0

    def test_get_full_report_structure(self):
        t = AccessibleArchitectureEthicsTracker()
        t.record_incident("accessibility_beyond_code", "Test", 10)
        report = t.get_full_report()
        assert "composite" in report
        assert "dimensions" in report
        assert "decision_log" in report
        assert isinstance(report["composite"], float)
        assert isinstance(report["dimensions"], dict)
        assert isinstance(report["decision_log"], list)
        assert len(report["decision_log"]) == 1

    def test_composite_key_present(self):
        """Critical: get_full_report MUST have 'composite' key."""
        t = AccessibleArchitectureEthicsTracker()
        report = t.get_full_report()
        assert "composite" in report
        assert report["composite"] == 100.0

    def test_unknown_dimension_raises(self):
        t = AccessibleArchitectureEthicsTracker()
        with pytest.raises(KeyError):
            t.record_incident("nonexistent_dimension", "Bad", 10)

    def test_serialization_roundtrip(self):
        t = AccessibleArchitectureEthicsTracker()
        t.record_incident("accessibility_beyond_code", "Penalty", 15)
        t.record_bonus("inclusive_design_process", "Bonus", 5)

        d = t.to_dict()
        t2 = AccessibleArchitectureEthicsTracker.from_dict(d)
        assert t2.get_scores() == t.get_scores()
        assert t2.get_composite_score() == t.get_composite_score()
        assert len(t2._incidents) == 2

    def test_weighted_composite(self):
        """Verify composite is correctly weighted."""
        t = AccessibleArchitectureEthicsTracker()
        # Drop accessibility_beyond_code by 50 (weight 0.30)
        t.record_incident("accessibility_beyond_code", "Test", 50)
        # Expected: 50*0.30 + 100*0.25 + 100*0.20 + 100*0.15 + 100*0.10 = 15+25+20+15+10 = 85
        assert abs(t.get_composite_score() - 85.0) < 0.1
