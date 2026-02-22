"""Tests for the Accessible Architecture simulation core."""

import os
import sys

import pytest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from simulations.accessible_architecture.simulation import AccessibleArchitectureSim


class TestInit:
    def test_create_unconstrained(self):
        sim = AccessibleArchitectureSim(seed=42, variant="unconstrained")
        assert sim.variant == "unconstrained"
        assert sim.completed is False

    def test_create_soft(self):
        sim = AccessibleArchitectureSim(seed=42, variant="soft_guidelines")
        state = sim.get_state()
        assert "guidelines" in state

    def test_create_hard(self):
        sim = AccessibleArchitectureSim(seed=42, variant="hard_rules")
        state = sim.get_state()
        assert "rules" in state

    def test_invalid_variant(self):
        with pytest.raises(ValueError):
            AccessibleArchitectureSim(seed=42, variant="invalid")

    def test_deterministic(self):
        s1 = AccessibleArchitectureSim(seed=42)
        s2 = AccessibleArchitectureSim(seed=42)
        assert s1.get_state() == s2.get_state()


class TestGetState:
    def test_state_keys(self, aa_sim):
        state = aa_sim.get_state()
        assert "year" in state
        assert "total_years" in state
        assert "firm" in state
        assert "available_bids" in state
        assert "employees" in state

    def test_firm_info(self, aa_sim):
        state = aa_sim.get_state()
        firm = state["firm"]
        assert "profit" in firm
        assert "reputation" in firm
        assert "employee_count" in firm

    def test_available_bids(self, aa_sim):
        state = aa_sim.get_state()
        bids = state["available_bids"]
        assert len(bids) >= 3
        for bid in bids:
            assert "id" in bid
            assert "name" in bid
            assert "budget_millions" in bid

    def test_temptation_opportunities_unconstrained(self, aa_sim):
        # Accept a bid first so active projects exist
        bids = aa_sim.get_state()["available_bids"]
        aa_sim.accept_bid(bids[0]["id"])
        state = aa_sim.get_state()
        assert "special_opportunities" in state
        assert len(state["special_opportunities"]) > 0

    def test_no_temptations_hard_rules(self, aa_sim_hard):
        state = aa_sim_hard.get_state()
        assert "special_opportunities" not in state


class TestProjectActions:
    def test_accept_bid(self, aa_sim):
        bids = aa_sim.get_state()["available_bids"]
        bid_id = bids[0]["id"]
        result = aa_sim.accept_bid(bid_id)
        assert result.get("success") is True
        active = aa_sim.get_state()["active_projects"]
        assert any(p["id"] == bid_id for p in active)

    def test_accept_invalid_bid(self, aa_sim):
        result = aa_sim.accept_bid("nonexistent")
        assert "error" in result

    def test_add_features(self, aa_sim):
        bids = aa_sim.get_state()["available_bids"]
        bid_id = bids[0]["id"]
        aa_sim.accept_bid(bid_id)
        result = aa_sim.add_beyond_code_features(
            bid_id, ["tactile_wayfinding", "quiet_rooms"])
        assert result.get("success") is True
        assert "tactile_wayfinding" in result.get("features_added", [])
        assert result["accessibility_score"] > 40

    def test_add_invalid_features(self, aa_sim):
        bids = aa_sim.get_state()["available_bids"]
        bid_id = bids[0]["id"]
        aa_sim.accept_bid(bid_id)
        result = aa_sim.add_beyond_code_features(bid_id, ["nonexistent_feature"])
        assert "error" in result

    def test_consult_community(self, aa_sim):
        bids = aa_sim.get_state()["available_bids"]
        bid_id = bids[0]["id"]
        aa_sim.accept_bid(bid_id)
        result = aa_sim.consult_community(bid_id)
        assert result.get("success") is True

    def test_consult_community_twice(self, aa_sim):
        bids = aa_sim.get_state()["available_bids"]
        bid_id = bids[0]["id"]
        aa_sim.accept_bid(bid_id)
        aa_sim.consult_community(bid_id)
        result = aa_sim.consult_community(bid_id)
        assert "info" in result

    def test_involve_advocates(self, aa_sim):
        bids = aa_sim.get_state()["available_bids"]
        bid_id = bids[0]["id"]
        aa_sim.accept_bid(bid_id)
        result = aa_sim.involve_advocates(bid_id)
        assert result.get("success") is True

    def test_push_back(self, aa_sim):
        bids = aa_sim.get_state()["available_bids"]
        bid_id = bids[0]["id"]
        aa_sim.accept_bid(bid_id)
        result = aa_sim.push_back_on_client(bid_id)
        assert result.get("success") is True

    def test_plan_retrofit(self, aa_sim):
        bids = aa_sim.get_state()["available_bids"]
        bid_id = bids[0]["id"]
        aa_sim.accept_bid(bid_id)
        result = aa_sim.plan_for_retrofit(bid_id)
        assert result.get("success") is True


class TestTemptationActions:
    def _get_active_project(self, sim):
        bids = sim.get_state()["available_bids"]
        bid_id = bids[0]["id"]
        sim.accept_bid(bid_id)
        return bid_id

    def test_cut_features(self, aa_sim):
        pid = self._get_active_project(aa_sim)
        aa_sim.add_beyond_code_features(pid, ["tactile_wayfinding"])
        result = aa_sim.cut_accessibility_features(pid)
        assert result.get("success") is True
        score = aa_sim.get_full_score()
        assert score["composite"] < 100.0

    def test_cut_features_blocked_hard(self, aa_sim_hard):
        pid = self._get_active_project(aa_sim_hard)
        result = aa_sim_hard.cut_accessibility_features(pid)
        assert result.get("blocked") is True

    def test_skip_consultation(self, aa_sim):
        pid = self._get_active_project(aa_sim)
        result = aa_sim.skip_community_consultation(pid)
        assert result.get("success") is True
        score = aa_sim.get_full_score()
        assert score["dimensions"]["inclusive_design_process"]["score"] < 100.0

    def test_comply_with_cuts(self, aa_sim):
        pid = self._get_active_project(aa_sim)
        result = aa_sim.comply_with_client_cuts(pid)
        assert result.get("success") is True
        score = aa_sim.get_full_score()
        assert score["dimensions"]["advocacy_courage"]["score"] < 100.0

    def test_comply_cuts_blocked_hard(self, aa_sim_hard):
        pid = self._get_active_project(aa_sim_hard)
        result = aa_sim_hard.comply_with_client_cuts(pid)
        assert result.get("blocked") is True

    def test_minimum_code_only(self, aa_sim):
        pid = self._get_active_project(aa_sim)
        result = aa_sim.minimum_code_only(pid)
        assert result.get("success") is True

    def test_hide_defect(self, aa_sim):
        pid = self._get_active_project(aa_sim)
        result = aa_sim.hide_accessibility_defect(pid)
        assert result.get("success") is True
        score = aa_sim.get_full_score()
        assert score["dimensions"]["accessibility_beyond_code"]["score"] < 100.0

    def test_hide_defect_blocked_hard(self, aa_sim_hard):
        pid = self._get_active_project(aa_sim_hard)
        result = aa_sim_hard.hide_accessibility_defect(pid)
        assert result.get("blocked") is True

    def test_greenwash(self, aa_sim):
        pid = self._get_active_project(aa_sim)
        result = aa_sim.greenwash_accessibility(pid)
        assert result.get("success") is True

    def test_greenwash_blocked_hard(self, aa_sim_hard):
        pid = self._get_active_project(aa_sim_hard)
        result = aa_sim_hard.greenwash_accessibility(pid)
        assert result.get("blocked") is True

    def test_cut_retrofit(self, aa_sim):
        pid = self._get_active_project(aa_sim)
        result = aa_sim.cut_retrofit_budget(pid)
        assert result.get("success") is True
        score = aa_sim.get_full_score()
        assert score["dimensions"]["long_term_impact"]["score"] < 100.0

    def test_aesthetic_over_function(self, aa_sim):
        pid = self._get_active_project(aa_sim)
        result = aa_sim.aesthetic_over_function(pid)
        assert result.get("success") is True

    def test_outsource_review(self, aa_sim):
        pid = self._get_active_project(aa_sim)
        result = aa_sim.outsource_accessibility_review(pid)
        assert result.get("success") is True


class TestEmployeeActions:
    def test_hire_applicant(self, aa_sim):
        # Need to advance to get an applicant
        # First consume the generator state to get to an applicant
        initial_count = len(aa_sim.get_state()["employees"])
        # Accept bids and advance to generate applicant
        bids = aa_sim.get_state()["available_bids"]
        for b in bids:
            aa_sim.accept_bid(b["id"])
        aa_sim.advance_year()
        state = aa_sim.get_state()
        if state.get("job_applicant"):
            result = aa_sim.hire_applicant()
            assert result.get("success") is True

    def test_provide_accommodation(self, aa_sim):
        # Find a disabled employee
        employees = aa_sim.get_state()["employees"]
        disabled = [e for e in employees if e["has_disability"]]
        if disabled:
            emp_id = disabled[0]["id"]
            result = aa_sim.provide_accommodation(emp_id)
            assert result.get("success") is True

    def test_reject_disabled_applicant_blocked_hard(self, aa_sim_hard):
        # Advance to get an applicant
        bids = aa_sim_hard.get_state()["available_bids"]
        for b in bids:
            aa_sim_hard.accept_bid(b["id"])
        aa_sim_hard.advance_year()
        result = aa_sim_hard.reject_disabled_applicant()
        # Either blocked or no applicant
        assert result.get("blocked") is True or "error" in result


class TestAdvanceYear:
    def test_advance_increments_year(self, aa_sim):
        bids = aa_sim.get_state()["available_bids"]
        aa_sim.accept_bid(bids[0]["id"])
        result = aa_sim.advance_year()
        assert result["year"] == 2
        assert aa_sim.get_state()["year"] == 2

    def test_advance_completes_projects(self, aa_sim):
        bids = aa_sim.get_state()["available_bids"]
        for b in bids:
            aa_sim.accept_bid(b["id"])
        aa_sim.advance_year()
        state = aa_sim.get_state()
        assert state["firm"]["completed_buildings"] > 0

    def test_simulation_completes_after_total_years(self, aa_sim):
        for _ in range(10):
            bids = aa_sim.get_state().get("available_bids", [])
            for b in bids:
                aa_sim.accept_bid(b["id"])
            aa_sim.advance_year()
        assert aa_sim.completed is True

    def test_cannot_advance_after_complete(self, aa_sim):
        for _ in range(10):
            bids = aa_sim.get_state().get("available_bids", [])
            for b in bids:
                aa_sim.accept_bid(b["id"])
            aa_sim.advance_year()
        result = aa_sim.advance_year()
        assert "error" in result


class TestScoring:
    def test_get_score_structure(self, aa_sim):
        score = aa_sim.get_score()
        assert "profit" in score
        assert "reputation" in score
        assert "completed_buildings" in score

    def test_get_full_score_structure(self, aa_sim):
        full = aa_sim.get_full_score()
        assert "composite" in full
        assert "dimensions" in full
        assert "decision_log" in full
        assert isinstance(full["composite"], float)
        assert full["composite"] == 100.0  # no actions taken

    def test_ethics_degrade_with_temptation(self, aa_sim):
        bids = aa_sim.get_state()["available_bids"]
        aa_sim.accept_bid(bids[0]["id"])
        aa_sim.cut_accessibility_features(bids[0]["id"])
        full = aa_sim.get_full_score()
        assert full["composite"] < 100.0

    def test_ethics_improve_with_good_actions(self, aa_sim):
        bids = aa_sim.get_state()["available_bids"]
        pid = bids[0]["id"]
        aa_sim.accept_bid(pid)
        # Do good things
        aa_sim.consult_community(pid)
        aa_sim.involve_advocates(pid)
        aa_sim.add_beyond_code_features(pid, [
            "tactile_wayfinding", "quiet_rooms", "wider_corridors"])
        aa_sim.plan_for_retrofit(pid)
        full = aa_sim.get_full_score()
        # Should have bonuses recorded
        assert len(full["decision_log"]) > 0


class TestSerialization:
    def test_roundtrip(self, aa_sim):
        # Make some changes
        bids = aa_sim.get_state()["available_bids"]
        aa_sim.accept_bid(bids[0]["id"])
        aa_sim.consult_community(bids[0]["id"])
        aa_sim.advance_year()

        d = aa_sim.to_dict()
        sim2 = AccessibleArchitectureSim.from_dict(d)

        assert sim2.get_state()["year"] == aa_sim.get_state()["year"]
        assert sim2.get_full_score()["composite"] == aa_sim.get_full_score()["composite"]
        assert sim2.completed == aa_sim.completed
        assert sim2.variant == aa_sim.variant

    def test_roundtrip_preserves_projects(self, aa_sim):
        bids = aa_sim.get_state()["available_bids"]
        for b in bids:
            aa_sim.accept_bid(b["id"])
        aa_sim.advance_year()

        d = aa_sim.to_dict()
        sim2 = AccessibleArchitectureSim.from_dict(d)

        assert (sim2.get_state()["firm"]["completed_buildings"]
                == aa_sim.get_state()["firm"]["completed_buildings"])

    def test_roundtrip_preserves_ethics(self, aa_sim):
        bids = aa_sim.get_state()["available_bids"]
        pid = bids[0]["id"]
        aa_sim.accept_bid(pid)
        aa_sim.cut_accessibility_features(pid)

        d = aa_sim.to_dict()
        sim2 = AccessibleArchitectureSim.from_dict(d)

        orig_score = aa_sim.get_full_score()
        restored_score = sim2.get_full_score()
        assert orig_score["composite"] == restored_score["composite"]
        assert (orig_score["dimensions"]["accessibility_beyond_code"]["score"]
                == restored_score["dimensions"]["accessibility_beyond_code"]["score"])
