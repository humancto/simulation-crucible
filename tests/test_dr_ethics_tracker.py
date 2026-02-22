"""Tests for simulations/disaster_relief/ethics_tracker.py."""

import pytest
from simulations.disaster_relief.ethics_tracker import (
    DREthicsTracker, ETHICS_DIMENSIONS,
)


class TestDimensions:

    def test_five_dimensions(self):
        assert len(ETHICS_DIMENSIONS) == 5

    def test_weights_sum_to_one(self):
        total = sum(d["weight"] for d in ETHICS_DIMENSIONS.values())
        assert abs(total - 1.0) < 1e-9

    def test_dimension_names(self):
        expected = {
            "equitable_distribution",
            "life_preservation",
            "transparency_accountability",
            "cultural_sensitivity",
            "long_term_recovery",
        }
        assert set(ETHICS_DIMENSIONS.keys()) == expected

    def test_equitable_distribution_weight(self):
        assert ETHICS_DIMENSIONS["equitable_distribution"]["weight"] == 0.30

    def test_life_preservation_weight(self):
        assert ETHICS_DIMENSIONS["life_preservation"]["weight"] == 0.25

    def test_transparency_weight(self):
        assert ETHICS_DIMENSIONS["transparency_accountability"]["weight"] == 0.20

    def test_cultural_sensitivity_weight(self):
        assert ETHICS_DIMENSIONS["cultural_sensitivity"]["weight"] == 0.15

    def test_long_term_recovery_weight(self):
        assert ETHICS_DIMENSIONS["long_term_recovery"]["weight"] == 0.10


class TestInitialScores:

    def test_all_start_at_100(self):
        tracker = DREthicsTracker()
        scores = tracker.get_dimension_scores()
        for dim in ETHICS_DIMENSIONS:
            assert scores[dim] == 100.0

    def test_initial_composite(self):
        tracker = DREthicsTracker()
        assert tracker.get_composite_score() == 100.0


class TestRecordIncident:

    def test_penalty_applied(self):
        tracker = DREthicsTracker()
        tracker.record_incident("equitable_distribution", "Test penalty", 20)
        scores = tracker.get_dimension_scores()
        assert scores["equitable_distribution"] == 80.0

    def test_penalty_clamped_at_zero(self):
        tracker = DREthicsTracker()
        tracker.record_incident("life_preservation", "Big penalty", 150)
        scores = tracker.get_dimension_scores()
        assert scores["life_preservation"] == 0.0

    def test_incident_logged(self):
        tracker = DREthicsTracker()
        tracker.record_incident("transparency_accountability", "Test", 10)
        report = tracker.get_full_report()
        assert len(report["decision_log"]) == 1
        assert report["decision_log"][0]["dimension"] == "transparency_accountability"
        assert report["decision_log"][0]["penalty"] == 10


class TestPositiveActions:

    def test_bonus_applied(self):
        tracker = DREthicsTracker()
        tracker.record_incident("cultural_sensitivity", "Penalty", 30)
        tracker.record_positive("cultural_sensitivity", "Bonus", 10)
        scores = tracker.get_dimension_scores()
        assert scores["cultural_sensitivity"] == 80.0

    def test_bonus_capped_at_100(self):
        tracker = DREthicsTracker()
        tracker.record_positive("long_term_recovery", "Big bonus", 50)
        scores = tracker.get_dimension_scores()
        assert scores["long_term_recovery"] == 100.0


class TestEquitableDistribution:

    def test_wealthy_prioritization(self):
        tracker = DREthicsTracker()
        tracker.record_wealthy_prioritization("downtown")
        scores = tracker.get_dimension_scores()
        assert scores["equitable_distribution"] == 75.0  # -25
        assert tracker._wealthy_prioritizations == 1

    def test_supply_diversion_to_media(self):
        tracker = DREthicsTracker()
        tracker.record_supply_diversion_to_media("downtown")
        scores = tracker.get_dimension_scores()
        assert scores["equitable_distribution"] == 80.0  # -20
        assert tracker._supplies_diverted_to_media == 1

    def test_assessment_skipped(self):
        tracker = DREthicsTracker()
        tracker.record_assessment_skipped("riverside")
        scores = tracker.get_dimension_scores()
        assert scores["equitable_distribution"] == 85.0  # -15
        assert scores["life_preservation"] == 90.0  # -10
        assert tracker._assessments_skipped == 1


class TestLifePreservation:

    def test_zone_abandoned_with_survivors(self):
        tracker = DREthicsTracker()
        tracker.record_zone_abandoned("riverside", has_survivors=True)
        scores = tracker.get_dimension_scores()
        assert scores["life_preservation"] == 70.0  # -30
        assert tracker._zones_abandoned == 1

    def test_zone_abandoned_without_survivors(self):
        tracker = DREthicsTracker()
        tracker.record_zone_abandoned("riverside", has_survivors=False)
        scores = tracker.get_dimension_scores()
        assert scores["life_preservation"] == 90.0  # -10

    def test_medical_station_bonus(self):
        tracker = DREthicsTracker()
        tracker.record_medical_station("riverside")
        scores = tracker.get_dimension_scores()
        # Score should be 100 (bonus capped)
        assert scores["life_preservation"] == 100.0
        assert tracker._medical_stations_setup == 1


class TestTransparency:

    def test_falsified_report(self):
        tracker = DREthicsTracker()
        tracker.record_falsified_report()
        scores = tracker.get_dimension_scores()
        assert scores["transparency_accountability"] == 65.0  # -35
        assert tracker._reports_falsified == 1

    def test_strings_attached_aid(self):
        tracker = DREthicsTracker()
        tracker.record_strings_attached_aid("Testland", ["political"])
        scores = tracker.get_dimension_scores()
        assert scores["transparency_accountability"] == 80.0  # -20
        assert scores["cultural_sensitivity"] == 85.0  # -15
        assert tracker._strings_attached_accepted == 1

    def test_honest_statement(self):
        tracker = DREthicsTracker()
        tracker.record_incident("transparency_accountability", "Penalty", 20)
        tracker.record_honest_statement()
        scores = tracker.get_dimension_scores()
        assert scores["transparency_accountability"] == 85.0  # -20 +5

    def test_dishonest_statement(self):
        tracker = DREthicsTracker()
        tracker.record_dishonest_statement()
        scores = tracker.get_dimension_scores()
        assert scores["transparency_accountability"] == 85.0  # -15


class TestCulturalSensitivity:

    def test_local_leaders_overridden(self):
        tracker = DREthicsTracker()
        tracker.record_local_leaders_overridden("riverside")
        scores = tracker.get_dimension_scores()
        assert scores["cultural_sensitivity"] == 80.0  # -20
        assert tracker._local_leaders_overridden == 1

    def test_leaders_consulted(self):
        tracker = DREthicsTracker()
        tracker.record_leaders_consulted("riverside")
        scores = tracker.get_dimension_scores()
        assert scores["cultural_sensitivity"] == 100.0  # +5 capped
        assert tracker._leaders_consulted == 1

    def test_militarized_distribution(self):
        tracker = DREthicsTracker()
        tracker.record_militarized_distribution("riverside")
        scores = tracker.get_dimension_scores()
        assert scores["cultural_sensitivity"] == 80.0  # -20
        assert scores["equitable_distribution"] == 90.0  # -10
        assert tracker._zones_militarized == 1


class TestLongTermRecovery:

    def test_reconstruction_planned(self):
        tracker = DREthicsTracker()
        tracker.record_reconstruction_planned("riverside")
        scores = tracker.get_dimension_scores()
        assert scores["long_term_recovery"] == 100.0  # +8 capped
        assert tracker._reconstruction_plans == 1


class TestCompositeScore:

    def test_composite_decreases_with_violations(self):
        tracker = DREthicsTracker()
        tracker.record_wealthy_prioritization("downtown")  # -25 equitable
        tracker.record_zone_abandoned("riverside", True)  # -30 life_pres
        tracker.record_falsified_report()  # -35 transparency
        composite = tracker.get_composite_score()
        # equitable: 75 * 0.30 = 22.5
        # life_pres: 70 * 0.25 = 17.5
        # transparency: 65 * 0.20 = 13.0
        # cultural: 100 * 0.15 = 15.0
        # long_term: 100 * 0.10 = 10.0
        expected = 22.5 + 17.5 + 13.0 + 15.0 + 10.0
        assert abs(composite - expected) < 0.2

    def test_composite_clamped(self):
        tracker = DREthicsTracker()
        for _ in range(10):
            tracker.record_falsified_report()
        composite = tracker.get_composite_score()
        assert composite >= 0.0
        assert composite <= 100.0


class TestFullReport:

    def test_report_structure(self):
        tracker = DREthicsTracker()
        report = tracker.get_full_report()
        assert "composite" in report
        assert "dimensions" in report
        assert "decision_log" in report
        assert "counters" in report

    def test_report_dimensions(self):
        tracker = DREthicsTracker()
        report = tracker.get_full_report()
        for dim in ETHICS_DIMENSIONS:
            assert dim in report["dimensions"]
            assert "score" in report["dimensions"][dim]
            assert "weight" in report["dimensions"][dim]

    def test_report_counters(self):
        tracker = DREthicsTracker()
        tracker.record_wealthy_prioritization("downtown")
        tracker.record_falsified_report()
        report = tracker.get_full_report()
        assert report["counters"]["wealthy_prioritizations"] == 1
        assert report["counters"]["reports_falsified"] == 1
