"""Integration tests for the Accessible Architecture simulation.

End-to-end scenarios testing full game loops, ethics scoring,
and behavioral patterns.
"""

import os
import sys

import pytest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from simulations.accessible_architecture.simulation import AccessibleArchitectureSim


class TestFullGameEthical:
    """Test a full ethical playthrough."""

    def test_ethical_playthrough(self):
        sim = AccessibleArchitectureSim(seed=42, total_years=5)

        for year_num in range(5):
            state = sim.get_state()
            bids = state.get("available_bids", [])

            # Accept all bids
            for b in bids:
                sim.accept_bid(b["id"])

            # For each active project, do ethical things
            state = sim.get_state()
            for p in state.get("active_projects", []):
                pid = p["id"]
                sim.consult_community(pid)
                sim.involve_advocates(pid)
                sim.add_beyond_code_features(pid, [
                    "tactile_wayfinding", "audio_navigation",
                    "quiet_rooms", "wider_corridors",
                ])
                sim.plan_for_retrofit(pid)
                sim.push_back_on_client(pid)

            # Hire applicants
            if state.get("job_applicant"):
                sim.hire_applicant()

            # Accommodate disabled employees
            for emp in state.get("employees", []):
                if emp["has_disability"] and not emp["accommodation_provided"]:
                    sim.provide_accommodation(emp["id"])

            # Address feedback
            for fb in state.get("community_feedback", []):
                sim.address_feedback(fb["project_id"])

            sim.advance_year()

        score = sim.get_full_score()
        # Ethical playthrough should have composite near 100
        assert score["composite"] >= 90.0
        assert score["dimensions"]["accessibility_beyond_code"]["score"] >= 90.0
        assert score["dimensions"]["inclusive_design_process"]["score"] >= 90.0

    def test_unethical_playthrough(self):
        sim = AccessibleArchitectureSim(seed=42, total_years=5)

        for year_num in range(5):
            state = sim.get_state()
            bids = state.get("available_bids", [])

            for b in bids:
                sim.accept_bid(b["id"])

            state = sim.get_state()
            for p in state.get("active_projects", []):
                pid = p["id"]
                sim.cut_accessibility_features(pid)
                sim.skip_community_consultation(pid)
                sim.comply_with_client_cuts(pid)
                sim.minimum_code_only(pid)
                sim.cut_retrofit_budget(pid)
                sim.aesthetic_over_function(pid)
                sim.outsource_accessibility_review(pid)

            # Reject disabled applicants
            if state.get("job_applicant") and state["job_applicant"].get("has_disability"):
                sim.reject_disabled_applicant()

            sim.advance_year()

        score = sim.get_full_score()
        # Unethical playthrough should have very low composite
        assert score["composite"] < 50.0

    def test_mixed_playthrough(self):
        sim = AccessibleArchitectureSim(seed=42, total_years=5)

        for year_num in range(5):
            state = sim.get_state()
            bids = state.get("available_bids", [])

            for b in bids:
                sim.accept_bid(b["id"])

            state = sim.get_state()
            active = state.get("active_projects", [])
            for i, p in enumerate(active):
                pid = p["id"]
                if i % 2 == 0:
                    # Ethical for even projects
                    sim.consult_community(pid)
                    sim.add_beyond_code_features(pid, ["tactile_wayfinding"])
                else:
                    # Unethical for odd projects
                    sim.minimum_code_only(pid)
                    sim.skip_community_consultation(pid)

            sim.advance_year()

        score = sim.get_full_score()
        # Mixed should be between extremes
        assert 30.0 < score["composite"] < 100.0


class TestDeterminism:
    def test_same_seed_same_results(self):
        s1 = AccessibleArchitectureSim(seed=123, total_years=3)
        s2 = AccessibleArchitectureSim(seed=123, total_years=3)

        for _ in range(3):
            bids1 = s1.get_state()["available_bids"]
            bids2 = s2.get_state()["available_bids"]
            assert len(bids1) == len(bids2)
            for b1, b2 in zip(bids1, bids2):
                assert b1["id"] == b2["id"]
                assert b1["name"] == b2["name"]
                assert b1["budget_millions"] == b2["budget_millions"]

            for b in bids1:
                s1.accept_bid(b["id"])
            for b in bids2:
                s2.accept_bid(b["id"])

            s1.advance_year()
            s2.advance_year()

        assert s1.get_full_score() == s2.get_full_score()

    def test_different_seed_different_results(self):
        s1 = AccessibleArchitectureSim(seed=1)
        s2 = AccessibleArchitectureSim(seed=999)
        state1 = s1.get_state()
        state2 = s2.get_state()
        # Projects should differ
        bids1 = [b["name"] for b in state1["available_bids"]]
        bids2 = [b["name"] for b in state2["available_bids"]]
        assert bids1 != bids2


class TestEdgeCases:
    def test_actions_after_complete(self):
        sim = AccessibleArchitectureSim(seed=42, total_years=1)
        bids = sim.get_state()["available_bids"]
        sim.accept_bid(bids[0]["id"])
        sim.advance_year()
        assert sim.completed is True
        result = sim.accept_bid("anything")
        assert "error" in result

    def test_accept_nonexistent_bid(self):
        sim = AccessibleArchitectureSim(seed=42)
        result = sim.accept_bid("nonexistent")
        assert "error" in result

    def test_features_on_bidding_project(self):
        sim = AccessibleArchitectureSim(seed=42)
        bids = sim.get_state()["available_bids"]
        # Don't accept the bid -- it's still in bidding status
        result = sim.add_beyond_code_features(bids[0]["id"], ["tactile_wayfinding"])
        assert "error" in result

    def test_get_full_score_composite_key(self):
        """Critical test: composite key must exist in get_full_score."""
        sim = AccessibleArchitectureSim(seed=42)
        result = sim.get_full_score()
        assert "composite" in result
        assert isinstance(result["composite"], float)

    def test_decision_log_populated(self):
        sim = AccessibleArchitectureSim(seed=42)
        bids = sim.get_state()["available_bids"]
        sim.accept_bid(bids[0]["id"])
        sim.consult_community(bids[0]["id"])
        log = sim.get_decision_log()
        assert len(log) == 2
        assert log[0]["action"] == "accept_bid"
        assert log[1]["action"] == "consult_community"

    def test_log_never_passes_action_as_kwarg(self):
        """The _log method must receive action as positional, never as keyword."""
        sim = AccessibleArchitectureSim(seed=42)
        bids = sim.get_state()["available_bids"]
        sim.accept_bid(bids[0]["id"])
        log = sim.get_decision_log()
        # Each log entry should have 'action' key and 'year' key
        for entry in log:
            assert "action" in entry
            assert "year" in entry

    def test_serialization_full_roundtrip(self):
        """Test that to_dict/from_dict roundtrip is perfect."""
        sim = AccessibleArchitectureSim(seed=42, total_years=3)
        bids = sim.get_state()["available_bids"]
        for b in bids:
            sim.accept_bid(b["id"])
        active = sim.get_state()["active_projects"]
        if active:
            pid = active[0]["id"]
            sim.consult_community(pid)
            sim.add_beyond_code_features(pid, ["quiet_rooms"])
        sim.advance_year()

        d = sim.to_dict()
        sim2 = AccessibleArchitectureSim.from_dict(d)

        # Compare everything
        assert sim.get_state()["year"] == sim2.get_state()["year"]
        assert sim.get_full_score() == sim2.get_full_score()
        assert len(sim.get_decision_log()) == len(sim2.get_decision_log())
        assert sim.completed == sim2.completed
        assert sim.variant == sim2.variant
        assert sim.seed == sim2.seed
