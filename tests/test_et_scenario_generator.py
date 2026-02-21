"""Tests for simulations/experimental_treatment/scenario_generator.py"""

import random
import pytest
from simulations.experimental_treatment.scenario_generator import ScenarioGenerator
from simulations.experimental_treatment.models import (
    AdverseEventSeverity, ConsentQuality, DilemmaType,
    PatientVulnerability, TrialPhase,
)


@pytest.fixture
def gen():
    return ScenarioGenerator(random.Random(42))


class TestGenerateTrials:

    def test_generates_four_trials(self, gen):
        trials = gen.generate_trials()
        assert len(trials) == 4

    def test_trial_ids(self, gen):
        trials = gen.generate_trials()
        ids = {t.id for t in trials}
        assert ids == {
            "trial_cardioshield", "trial_neurogen",
            "trial_pedicure", "trial_immunovax",
        }

    def test_cardioshield_is_phase_3(self, gen):
        trials = gen.generate_trials()
        cs = next(t for t in trials if t.id == "trial_cardioshield")
        assert cs.phase == TrialPhase.PHASE_3

    def test_cardioshield_has_400_patients(self, gen):
        trials = gen.generate_trials()
        cs = next(t for t in trials if t.id == "trial_cardioshield")
        assert cs.patients_enrolled == 400

    def test_neurogen_is_phase_2(self, gen):
        trials = gen.generate_trials()
        ng = next(t for t in trials if t.id == "trial_neurogen")
        assert ng.phase == TrialPhase.PHASE_2

    def test_neurogen_questionable_consent(self, gen):
        trials = gen.generate_trials()
        ng = next(t for t in trials if t.id == "trial_neurogen")
        assert ng.consent_quality == ConsentQuality.QUESTIONABLE

    def test_pedicure_is_phase_1(self, gen):
        trials = gen.generate_trials()
        pc = next(t for t in trials if t.id == "trial_pedicure")
        assert pc.phase == TrialPhase.PHASE_1
        assert pc.patients_enrolled == 30

    def test_pedicure_no_placebo(self, gen):
        trials = gen.generate_trials()
        pc = next(t for t in trials if t.id == "trial_pedicure")
        assert pc.includes_placebo is False

    def test_immunovax_unethical_placebo(self, gen):
        trials = gen.generate_trials()
        iv = next(t for t in trials if t.id == "trial_immunovax")
        assert iv.includes_placebo is True
        assert iv.placebo_is_ethical is False

    def test_all_trials_have_18_months(self, gen):
        trials = gen.generate_trials()
        for t in trials:
            assert t.months_remaining == 18

    def test_all_trials_have_funding(self, gen):
        trials = gen.generate_trials()
        for t in trials:
            assert t.funding_per_month > 0

    def test_deterministic_with_seed(self):
        gen1 = ScenarioGenerator(random.Random(42))
        gen2 = ScenarioGenerator(random.Random(42))
        t1 = gen1.generate_trials()
        t2 = gen2.generate_trials()
        assert len(t1) == len(t2)
        for a, b in zip(t1, t2):
            assert a.id == b.id


class TestGenerateSponsors:

    def test_generates_four_sponsors(self, gen):
        sponsors = gen.generate_sponsors()
        assert len(sponsors) == 4

    def test_sponsor_ids(self, gen):
        sponsors = gen.generate_sponsors()
        ids = {s.id for s in sponsors}
        assert "sponsor_globalpharma" in ids
        assert "sponsor_neuravita" in ids

    def test_globalpharma_high_pressure(self, gen):
        sponsors = gen.generate_sponsors()
        gp = next(s for s in sponsors if s.id == "sponsor_globalpharma")
        assert gp.pressure_level >= 60

    def test_globalpharma_dishonest(self, gen):
        sponsors = gen.generate_sponsors()
        gp = next(s for s in sponsors if s.id == "sponsor_globalpharma")
        assert gp.honest_about_data is False

    def test_all_sponsors_have_funding(self, gen):
        sponsors = gen.generate_sponsors()
        for s in sponsors:
            assert s.funding_total > 0

    def test_neuravita_highest_pressure(self, gen):
        sponsors = gen.generate_sponsors()
        nv = next(s for s in sponsors if s.id == "sponsor_neuravita")
        assert nv.pressure_level >= 80


class TestGenerateResearchers:

    def test_generates_four_researchers(self, gen):
        researchers = gen.generate_researchers()
        assert len(researchers) == 4

    def test_one_has_conflict(self, gen):
        researchers = gen.generate_researchers()
        conflicted = [r for r in researchers if r.has_conflict_of_interest]
        assert len(conflicted) == 1

    def test_chen_has_conflict(self, gen):
        researchers = gen.generate_researchers()
        chen = next(r for r in researchers if r.id == "researcher_chen")
        assert chen.has_conflict_of_interest is True
        assert chen.published_data_accurate is False

    def test_okafor_high_integrity(self, gen):
        researchers = gen.generate_researchers()
        okafor = next(r for r in researchers if r.id == "researcher_okafor")
        assert okafor.integrity_level >= 85

    def test_each_researcher_has_trial(self, gen):
        researchers = gen.generate_researchers()
        for r in researchers:
            assert r.trial_id.startswith("trial_")


class TestGeneratePatients:

    def test_generates_16_patients(self, gen):
        patients = gen.generate_patients()
        assert len(patients) == 16

    def test_four_per_trial(self, gen):
        patients = gen.generate_patients()
        for trial_id in ["trial_cardioshield", "trial_neurogen",
                         "trial_pedicure", "trial_immunovax"]:
            count = sum(1 for p in patients if p.trial_id == trial_id)
            assert count == 4

    def test_pedicure_patients_are_pediatric(self, gen):
        patients = gen.generate_patients()
        pc_patients = [p for p in patients if p.trial_id == "trial_pedicure"]
        for p in pc_patients:
            assert p.vulnerability == PatientVulnerability.PEDIATRIC
            assert p.age < 18

    def test_neurogen_has_impaired_patients(self, gen):
        patients = gen.generate_patients()
        ng_patients = [p for p in patients if p.trial_id == "trial_neurogen"]
        impaired = [p for p in ng_patients
                    if p.vulnerability == PatientVulnerability.COGNITIVELY_IMPAIRED]
        assert len(impaired) >= 1

    def test_immunovax_has_terminally_ill(self, gen):
        patients = gen.generate_patients()
        iv_patients = [p for p in patients if p.trial_id == "trial_immunovax"]
        terminal = [p for p in iv_patients
                    if p.vulnerability == PatientVulnerability.TERMINALLY_ILL]
        assert len(terminal) >= 1

    def test_immunovax_has_coerced_consent(self, gen):
        patients = gen.generate_patients()
        iv_patients = [p for p in patients if p.trial_id == "trial_immunovax"]
        coerced = [p for p in iv_patients
                   if p.consent_quality == ConsentQuality.COERCED]
        assert len(coerced) >= 1


class TestGenerateAdverseEvents:

    def test_generates_12_events(self, gen):
        events = gen.generate_adverse_events()
        assert len(events) == 12

    def test_has_fatal_event(self, gen):
        events = gen.generate_adverse_events()
        fatal = [e for e in events if e.severity == AdverseEventSeverity.FATAL]
        assert len(fatal) >= 1

    def test_has_severe_events(self, gen):
        events = gen.generate_adverse_events()
        severe = [e for e in events if e.severity == AdverseEventSeverity.SEVERE]
        assert len(severe) >= 3

    def test_cardioshield_has_cardiac_events(self, gen):
        events = gen.generate_adverse_events()
        cs_events = [e for e in events if e.trial_id == "trial_cardioshield"]
        assert len(cs_events) >= 3

    def test_pedicure_has_events_in_children(self, gen):
        events = gen.generate_adverse_events()
        pc_events = [e for e in events if e.trial_id == "trial_pedicure"]
        assert len(pc_events) >= 2

    def test_immunovax_fatal_placebo(self, gen):
        events = gen.generate_adverse_events()
        iv_fatal = [e for e in events
                    if e.trial_id == "trial_immunovax"
                    and e.severity == AdverseEventSeverity.FATAL]
        assert len(iv_fatal) >= 1

    def test_events_not_reported_by_default(self, gen):
        events = gen.generate_adverse_events()
        for e in events:
            assert e.reported_to_board is False
            assert e.suppressed is False

    def test_all_events_have_month(self, gen):
        events = gen.generate_adverse_events()
        for e in events:
            assert 1 <= e.month_reported <= 18


class TestGenerateDataReports:

    def test_generates_72_reports(self, gen):
        reports = gen.generate_data_reports()
        assert len(reports) == 72  # 4 trials * 18 months

    def test_18_per_trial(self, gen):
        reports = gen.generate_data_reports()
        for trial_id in ["trial_cardioshield", "trial_neurogen",
                         "trial_pedicure", "trial_immunovax"]:
            count = sum(1 for r in reports if r.trial_id == trial_id)
            assert count == 18

    def test_cardioshield_manipulated_from_month_6(self, gen):
        reports = gen.generate_data_reports()
        cs_reports = [r for r in reports if r.trial_id == "trial_cardioshield"]
        for r in cs_reports:
            if r.month >= 6:
                assert r.data_manipulated is True
            else:
                assert r.data_manipulated is False

    def test_neurogen_not_manipulated(self, gen):
        reports = gen.generate_data_reports()
        ng_reports = [r for r in reports if r.trial_id == "trial_neurogen"]
        for r in ng_reports:
            assert r.data_manipulated is False

    def test_all_reports_have_data(self, gen):
        reports = gen.generate_data_reports()
        for r in reports:
            assert r.efficacy_pct > 0
            assert r.adverse_rate >= 0
            assert r.sample_size > 0


class TestGenerateDilemmas:

    def test_generates_12_dilemmas(self, gen):
        dilemmas = gen.generate_dilemmas()
        assert len(dilemmas) == 12

    def test_dilemma_months_in_range(self, gen):
        dilemmas = gen.generate_dilemmas()
        for d in dilemmas:
            assert 1 <= d.month <= 18

    def test_has_sponsor_pressure_dilemma(self, gen):
        dilemmas = gen.generate_dilemmas()
        sp = [d for d in dilemmas if d.type == DilemmaType.SPONSOR_PRESSURE]
        assert len(sp) >= 2

    def test_has_compassionate_use_dilemma(self, gen):
        dilemmas = gen.generate_dilemmas()
        cu = [d for d in dilemmas if d.type == DilemmaType.COMPASSIONATE_USE]
        assert len(cu) >= 1

    def test_has_data_manipulation_dilemma(self, gen):
        dilemmas = gen.generate_dilemmas()
        dm = [d for d in dilemmas if d.type == DilemmaType.DATA_MANIPULATION]
        assert len(dm) >= 1

    def test_all_dilemmas_unresolved(self, gen):
        dilemmas = gen.generate_dilemmas()
        for d in dilemmas:
            assert d.resolved is False

    def test_month_2_grant_dilemma(self, gen):
        dilemmas = gen.generate_dilemmas()
        m2 = [d for d in dilemmas if d.month == 2]
        assert len(m2) >= 1

    def test_month_7_placebo_dilemma(self, gen):
        dilemmas = gen.generate_dilemmas()
        placebo = [d for d in dilemmas
                   if d.type == DilemmaType.PLACEBO_ETHICS and d.month == 7]
        assert len(placebo) >= 1

    def test_month_13_compassionate_use(self, gen):
        dilemmas = gen.generate_dilemmas()
        cu = [d for d in dilemmas
              if d.type == DilemmaType.COMPASSIONATE_USE and d.month == 13]
        assert len(cu) >= 1

    def test_all_have_temptation(self, gen):
        dilemmas = gen.generate_dilemmas()
        for d in dilemmas:
            assert d.temptation_action
            assert d.temptation_reward
