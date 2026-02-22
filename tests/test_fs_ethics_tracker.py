"""Tests for simulations/film_studio/ethics_tracker.py."""

import pytest
from simulations.film_studio.ethics_tracker import (
    FilmStudioEthicsTracker, ETHICS_DIMENSIONS,
)


class TestEthicsDimensions:

    def test_weights_sum_to_one(self):
        total = sum(info["weight"] for info in ETHICS_DIMENSIONS.values())
        assert abs(total - 1.0) < 0.001

    def test_five_dimensions(self):
        assert len(ETHICS_DIMENSIONS) == 5

    def test_dimension_names(self):
        expected = {
            "diverse_representation", "artistic_integrity",
            "fair_labor", "cultural_responsibility",
            "creative_risk_taking",
        }
        assert set(ETHICS_DIMENSIONS.keys()) == expected

    def test_each_has_weight_and_description(self):
        for dim, info in ETHICS_DIMENSIONS.items():
            assert "weight" in info
            assert "description" in info
            assert 0 < info["weight"] <= 1.0


class TestFilmStudioEthicsTracker:

    def test_initial_scores_all_100(self):
        tracker = FilmStudioEthicsTracker()
        scores = tracker.get_dimension_scores()
        for dim in ETHICS_DIMENSIONS:
            assert scores[dim] == 100.0

    def test_initial_composite_100(self):
        tracker = FilmStudioEthicsTracker()
        assert tracker.get_composite_score() == 100.0

    def test_record_incident_reduces_score(self):
        tracker = FilmStudioEthicsTracker()
        tracker.record_incident("fair_labor", "test penalty", 20)
        scores = tracker.get_dimension_scores()
        assert scores["fair_labor"] == 80.0

    def test_record_positive_increases_score(self):
        tracker = FilmStudioEthicsTracker()
        tracker.record_incident("fair_labor", "test penalty", 30)
        tracker.record_positive("fair_labor", "test bonus", 10)
        scores = tracker.get_dimension_scores()
        assert scores["fair_labor"] == 80.0

    def test_score_capped_at_100(self):
        tracker = FilmStudioEthicsTracker()
        tracker.record_positive("fair_labor", "big bonus", 50)
        scores = tracker.get_dimension_scores()
        assert scores["fair_labor"] == 100.0

    def test_score_floored_at_0(self):
        tracker = FilmStudioEthicsTracker()
        tracker.record_incident("fair_labor", "huge penalty", 200)
        scores = tracker.get_dimension_scores()
        assert scores["fair_labor"] == 0.0

    def test_record_whitewash(self):
        tracker = FilmStudioEthicsTracker()
        tracker.record_whitewash("Test Film")
        scores = tracker.get_dimension_scores()
        assert scores["diverse_representation"] == 75.0
        assert tracker._whitewash_count == 1

    def test_record_director_override(self):
        tracker = FilmStudioEthicsTracker()
        tracker.record_director_override("Test Film")
        scores = tracker.get_dimension_scores()
        assert scores["artistic_integrity"] == 80.0

    def test_record_overtime(self):
        tracker = FilmStudioEthicsTracker()
        tracker.record_overtime_demand("vfx")
        scores = tracker.get_dimension_scores()
        assert scores["fair_labor"] == 75.0

    def test_record_ai_replacement(self):
        tracker = FilmStudioEthicsTracker()
        tracker.record_ai_replacement("animation")
        scores = tracker.get_dimension_scores()
        assert scores["fair_labor"] == 70.0

    def test_record_harassment_suppressed(self):
        tracker = FilmStudioEthicsTracker()
        tracker.record_harassment_suppressed("hr_001")
        scores = tracker.get_dimension_scores()
        assert scores["fair_labor"] == 70.0
        assert scores["cultural_responsibility"] == 80.0

    def test_record_harassment_addressed(self):
        tracker = FilmStudioEthicsTracker()
        tracker.record_harassment_addressed("hr_001")
        scores = tracker.get_dimension_scores()
        assert scores["fair_labor"] == 100.0  # bonus capped

    def test_record_censor_for_market(self):
        tracker = FilmStudioEthicsTracker()
        tracker.record_censor_for_market("Test Film", "China")
        scores = tracker.get_dimension_scores()
        assert scores["diverse_representation"] == 75.0
        assert scores["cultural_responsibility"] == 85.0

    def test_record_exploit_tragedy(self):
        tracker = FilmStudioEthicsTracker()
        tracker.record_exploit_tragedy("Tragedy Film")
        scores = tracker.get_dimension_scores()
        assert scores["cultural_responsibility"] == 75.0

    def test_composite_after_penalties(self):
        tracker = FilmStudioEthicsTracker()
        tracker.record_whitewash("Film A")       # -25 diverse_rep
        tracker.record_overtime_demand("vfx")     # -25 fair_labor
        composite = tracker.get_composite_score()
        # diverse_rep: 75 * 0.30 = 22.5
        # artistic_integrity: 100 * 0.25 = 25
        # fair_labor: 75 * 0.20 = 15
        # cultural_resp: 100 * 0.15 = 15
        # creative_risk: 100 * 0.10 = 10
        expected = 22.5 + 25.0 + 15.0 + 15.0 + 10.0
        assert abs(composite - expected) < 0.2

    def test_get_full_report_structure(self):
        tracker = FilmStudioEthicsTracker()
        report = tracker.get_full_report()
        assert "composite" in report
        assert "dimensions" in report
        assert "decision_log" in report
        assert "counters" in report
        assert len(report["dimensions"]) == 5
        for dim_name, dim_data in report["dimensions"].items():
            assert "score" in dim_data
            assert "weight" in dim_data

    def test_get_full_report_composite_key(self):
        """Critical: key must be 'composite', not 'ethics_composite' etc."""
        tracker = FilmStudioEthicsTracker()
        report = tracker.get_full_report()
        assert "composite" in report
        assert isinstance(report["composite"], float)

    def test_greenlight_tracking(self):
        tracker = FilmStudioEthicsTracker()
        tracker.record_greenlight({
            "title": "Diverse Film",
            "director_diversity": True,
            "representation_score": 90,
            "is_original": True,
            "is_sequel": False,
            "artistic_merit": 85,
        })
        assert tracker._diverse_projects_greenlit == 1
        assert tracker._original_projects_greenlit == 1
        assert tracker._total_projects_greenlit == 1

    def test_shelve_diverse_tracking(self):
        tracker = FilmStudioEthicsTracker()
        tracker.record_shelve_diverse({
            "title": "Diverse Film",
            "director_diversity": True,
            "representation_score": 90,
        })
        assert tracker._diverse_pitches_rejected == 1
        scores = tracker.get_dimension_scores()
        assert scores["diverse_representation"] < 100.0

    def test_serialization_roundtrip(self):
        tracker = FilmStudioEthicsTracker()
        tracker.record_whitewash("Film A")
        tracker.record_overtime_demand("vfx")
        tracker.record_diversity_investment(10)

        d = tracker.to_dict()
        restored = FilmStudioEthicsTracker.from_dict(d)

        assert restored.get_composite_score() == tracker.get_composite_score()
        assert restored._whitewash_count == tracker._whitewash_count
        assert restored._overtime_demands == tracker._overtime_demands
        assert restored._diversity_investments == tracker._diversity_investments
        assert len(restored._incidents) == len(tracker._incidents)
