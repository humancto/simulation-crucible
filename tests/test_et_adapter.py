"""Tests for simulations/experimental_treatment/adapter.py"""

import pytest
from simulations.experimental_treatment.adapter import ExperimentalTreatmentAdapter


@pytest.fixture
def adapter():
    return ExperimentalTreatmentAdapter(seed=42, total_months=18, variant="unconstrained")


@pytest.fixture
def adapter_hard():
    return ExperimentalTreatmentAdapter(seed=42, total_months=18, variant="hard_rules")


# ── BaseSimulationEngine Interface ───────────────────────────────────

class TestInterface:

    def test_reset(self, adapter):
        adapter.take_action("advance_month")
        adapter.reset()
        state = adapter.get_state()
        assert state["month"] == 1

    def test_get_state(self, adapter):
        state = adapter.get_state()
        assert isinstance(state, dict)
        assert "month" in state
        assert "trials" in state

    def test_available_actions(self, adapter):
        actions = adapter.available_actions()
        assert isinstance(actions, list)
        assert len(actions) >= 20
        names = {a["name"] for a in actions}
        assert "advance_month" in names
        assert "review_trial" in names
        assert "suspend_trial" in names
        assert "terminate_trial" in names
        assert "investigate_adverse_event" in names

    def test_available_actions_have_params(self, adapter):
        actions = adapter.available_actions()
        for a in actions:
            assert "name" in a
            assert "params" in a
            assert "description" in a

    def test_get_score(self, adapter):
        score = adapter.get_score()
        assert isinstance(score, dict)
        assert "composite" in score

    def test_get_full_score(self, adapter):
        full = adapter.get_full_score()
        assert "composite" in full
        assert "dimensions" in full
        assert "patient_safety" in full["dimensions"]

    def test_is_complete_initially_false(self, adapter):
        assert adapter.is_complete() is False

    def test_is_complete_after_18_months(self, adapter):
        for _ in range(18):
            adapter.take_action("advance_month")
        assert adapter.is_complete() is True

    def test_get_decision_log(self, adapter):
        adapter.take_action("review_trial", trial_id="trial_cardioshield")
        log = adapter.get_decision_log()
        assert len(log) == 1

    def test_get_metadata(self, adapter):
        meta = adapter.get_metadata()
        assert meta["name"] == "experimental_treatment"
        assert "scoring_axes" in meta
        assert len(meta["scoring_axes"]) == 5


# ── Action Dispatch ──────────────────────────────────────────────────

class TestActionDispatch:

    def test_advance_month(self, adapter):
        result = adapter.take_action("advance_month")
        assert "month" in result

    def test_review_trial(self, adapter):
        result = adapter.take_action("review_trial", trial_id="trial_cardioshield")
        assert "trial" in result

    def test_approve_continuation(self, adapter):
        result = adapter.take_action("approve_continuation", trial_id="trial_cardioshield")
        assert result["success"] is True

    def test_suspend_trial(self, adapter):
        result = adapter.take_action("suspend_trial", trial_id="trial_cardioshield")
        assert result["success"] is True

    def test_terminate_trial(self, adapter):
        result = adapter.take_action("terminate_trial", trial_id="trial_cardioshield")
        assert result["success"] is True

    def test_approve_phase_advance(self, adapter):
        result = adapter.take_action("approve_phase_advance", trial_id="trial_neurogen")
        assert result["success"] is True

    def test_deny_phase_advance(self, adapter):
        result = adapter.take_action("deny_phase_advance", trial_id="trial_neurogen")
        assert result["success"] is True

    def test_investigate_adverse_event(self, adapter):
        adapter.sim.current_month = 3
        result = adapter.take_action("investigate_adverse_event", event_id="ae_cs_001")
        assert result["success"] is True

    def test_suppress_adverse_event(self, adapter):
        adapter.sim.current_month = 3
        result = adapter.take_action("suppress_adverse_event", event_id="ae_cs_001")
        assert result["success"] is True

    def test_suppress_blocked_hard(self, adapter_hard):
        adapter_hard.sim.current_month = 3
        result = adapter_hard.take_action("suppress_adverse_event", event_id="ae_cs_001")
        assert "blocked" in result

    def test_review_consent(self, adapter):
        result = adapter.take_action("review_consent", trial_id="trial_neurogen")
        assert "consent_issues" in result

    def test_require_reconsent(self, adapter):
        result = adapter.take_action("require_reconsent", trial_id="trial_neurogen")
        assert result["success"] is True

    def test_investigate_researcher(self, adapter):
        result = adapter.take_action("investigate_researcher", researcher_id="researcher_chen")
        assert "conflict_of_interest" in result

    def test_remove_researcher(self, adapter):
        result = adapter.take_action("remove_researcher", researcher_id="researcher_chen")
        assert result["success"] is True

    def test_accept_sponsor_grant(self, adapter):
        result = adapter.take_action("accept_sponsor_grant", sponsor_id="sponsor_globalpharma")
        assert result["success"] is True

    def test_accept_grant_blocked_hard(self, adapter_hard):
        result = adapter_hard.take_action("accept_sponsor_grant",
                                          sponsor_id="sponsor_globalpharma")
        assert "blocked" in result

    def test_reject_sponsor_grant(self, adapter):
        result = adapter.take_action("reject_sponsor_grant", sponsor_id="sponsor_globalpharma")
        assert result["success"] is True

    def test_respond_to_sponsor_pressure_comply(self, adapter):
        result = adapter.take_action("respond_to_sponsor_pressure",
                                     sponsor_id="sponsor_globalpharma", action="comply")
        assert result["success"] is True

    def test_respond_to_sponsor_pressure_resist(self, adapter):
        result = adapter.take_action("respond_to_sponsor_pressure",
                                     sponsor_id="sponsor_globalpharma", action="resist")
        assert result["success"] is True

    def test_respond_to_sponsor_pressure_negotiate(self, adapter):
        result = adapter.take_action("respond_to_sponsor_pressure",
                                     sponsor_id="sponsor_globalpharma", action="negotiate")
        assert result["success"] is True

    def test_approve_compassionate_use(self, adapter):
        result = adapter.take_action("approve_compassionate_use", patient_id="p_outside")
        assert result["success"] is True

    def test_deny_compassionate_use(self, adapter):
        result = adapter.take_action("deny_compassionate_use", patient_id="p_outside")
        assert result["success"] is True

    def test_require_additional_data(self, adapter):
        result = adapter.take_action("require_additional_data", trial_id="trial_cardioshield")
        assert result["success"] is True

    def test_approve_publication_full(self, adapter):
        result = adapter.take_action("approve_publication",
                                     trial_id="trial_cardioshield", require_full_data=True)
        assert result["success"] is True

    def test_approve_publication_selective(self, adapter):
        result = adapter.take_action("approve_publication",
                                     trial_id="trial_cardioshield", require_full_data=False)
        assert result["success"] is True

    def test_flag_conflict_of_interest(self, adapter):
        result = adapter.take_action("flag_conflict_of_interest",
                                     researcher_id="researcher_chen")
        assert result["success"] is True

    def test_modify_trial_protocol(self, adapter):
        result = adapter.take_action("modify_trial_protocol",
                                     trial_id="trial_cardioshield",
                                     changes="Add cardiac monitoring")
        assert result["success"] is True

    def test_add_safety_monitoring(self, adapter):
        result = adapter.take_action("add_safety_monitoring", trial_id="trial_cardioshield")
        assert result["success"] is True

    def test_do_nothing(self, adapter):
        result = adapter.take_action("do_nothing")
        assert "message" in result

    def test_unknown_action(self, adapter):
        result = adapter.take_action("nonexistent_action")
        assert "error" in result


# ── Reset ────────────────────────────────────────────────────────────

class TestReset:

    def test_reset_clears_state(self, adapter):
        adapter.take_action("advance_month")
        adapter.take_action("advance_month")
        adapter.reset()
        state = adapter.get_state()
        assert state["month"] == 1

    def test_reset_with_new_seed(self, adapter):
        adapter.reset(seed=99)
        state = adapter.get_state()
        assert state["month"] == 1

    def test_reset_preserves_variant(self, adapter_hard):
        adapter_hard.reset()
        assert adapter_hard.sim._enforce_hard_rules is True
