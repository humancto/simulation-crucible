"""Tests for simulations/experimental_treatment/models.py — all enums and dataclasses."""

import pytest
from simulations.experimental_treatment.models import (
    AdverseEvent,
    AdverseEventSeverity,
    ConsentQuality,
    DataReport,
    DilemmaType,
    EthicalDilemma,
    Patient,
    PatientVulnerability,
    Researcher,
    Sponsor,
    Trial,
    TrialPhase,
)


# ── TrialPhase Enum ──────────────────────────────────────────────────

class TestTrialPhaseEnum:

    def test_has_six_values(self):
        assert len(TrialPhase) == 6

    def test_phase_1(self):
        assert TrialPhase.PHASE_1.value == "phase_1"

    def test_phase_2(self):
        assert TrialPhase.PHASE_2.value == "phase_2"

    def test_phase_3(self):
        assert TrialPhase.PHASE_3.value == "phase_3"

    def test_suspended(self):
        assert TrialPhase.SUSPENDED.value == "suspended"

    def test_terminated(self):
        assert TrialPhase.TERMINATED.value == "terminated"

    def test_completed(self):
        assert TrialPhase.COMPLETED.value == "completed"

    def test_from_string(self):
        assert TrialPhase("phase_1") == TrialPhase.PHASE_1


# ── AdverseEventSeverity Enum ────────────────────────────────────────

class TestAdverseEventSeverityEnum:

    def test_has_five_values(self):
        assert len(AdverseEventSeverity) == 5

    def test_mild(self):
        assert AdverseEventSeverity.MILD.value == "mild"

    def test_moderate(self):
        assert AdverseEventSeverity.MODERATE.value == "moderate"

    def test_severe(self):
        assert AdverseEventSeverity.SEVERE.value == "severe"

    def test_life_threatening(self):
        assert AdverseEventSeverity.LIFE_THREATENING.value == "life_threatening"

    def test_fatal(self):
        assert AdverseEventSeverity.FATAL.value == "fatal"


# ── PatientVulnerability Enum ────────────────────────────────────────

class TestPatientVulnerabilityEnum:

    def test_has_seven_values(self):
        assert len(PatientVulnerability) == 7

    def test_none(self):
        assert PatientVulnerability.NONE.value == "none"

    def test_elderly(self):
        assert PatientVulnerability.ELDERLY.value == "elderly"

    def test_pediatric(self):
        assert PatientVulnerability.PEDIATRIC.value == "pediatric"

    def test_pregnant(self):
        assert PatientVulnerability.PREGNANT.value == "pregnant"

    def test_cognitively_impaired(self):
        assert PatientVulnerability.COGNITIVELY_IMPAIRED.value == "cognitively_impaired"

    def test_terminally_ill(self):
        assert PatientVulnerability.TERMINALLY_ILL.value == "terminally_ill"

    def test_economically_coerced(self):
        assert PatientVulnerability.ECONOMICALLY_COERCED.value == "economically_coerced"


# ── ConsentQuality Enum ──────────────────────────────────────────────

class TestConsentQualityEnum:

    def test_has_five_values(self):
        assert len(ConsentQuality) == 5

    def test_fully_informed(self):
        assert ConsentQuality.FULLY_INFORMED.value == "fully_informed"

    def test_partial(self):
        assert ConsentQuality.PARTIAL.value == "partial"

    def test_coerced(self):
        assert ConsentQuality.COERCED.value == "coerced"

    def test_questionable(self):
        assert ConsentQuality.QUESTIONABLE.value == "questionable"

    def test_invalid(self):
        assert ConsentQuality.INVALID.value == "invalid"


# ── DilemmaType Enum ─────────────────────────────────────────────────

class TestDilemmaTypeEnum:

    def test_has_twelve_values(self):
        assert len(DilemmaType) == 12

    def test_adverse_event_suppression(self):
        assert DilemmaType.ADVERSE_EVENT_SUPPRESSION.value == "adverse_event_suppression"

    def test_informed_consent_shortcut(self):
        assert DilemmaType.INFORMED_CONSENT_SHORTCUT.value == "informed_consent_shortcut"

    def test_placebo_ethics(self):
        assert DilemmaType.PLACEBO_ETHICS.value == "placebo_ethics"

    def test_sponsor_pressure(self):
        assert DilemmaType.SPONSOR_PRESSURE.value == "sponsor_pressure"

    def test_data_manipulation(self):
        assert DilemmaType.DATA_MANIPULATION.value == "data_manipulation"

    def test_vulnerable_population(self):
        assert DilemmaType.VULNERABLE_POPULATION.value == "vulnerable_population"

    def test_early_termination(self):
        assert DilemmaType.EARLY_TERMINATION.value == "early_termination"

    def test_compassionate_use(self):
        assert DilemmaType.COMPASSIONATE_USE.value == "compassionate_use"

    def test_conflict_of_interest(self):
        assert DilemmaType.CONFLICT_OF_INTEREST.value == "conflict_of_interest"

    def test_publication_bias(self):
        assert DilemmaType.PUBLICATION_BIAS.value == "publication_bias"

    def test_control_group_harm(self):
        assert DilemmaType.CONTROL_GROUP_HARM.value == "control_group_harm"

    def test_economic_coercion(self):
        assert DilemmaType.ECONOMIC_COERCION.value == "economic_coercion"


# ── AdverseEvent Dataclass ───────────────────────────────────────────

class TestAdverseEvent:

    def test_creation(self):
        ae = AdverseEvent(
            id="ae1", trial_id="t1", patient_id="p1",
            severity=AdverseEventSeverity.SEVERE,
            description="Test event", month_reported=3,
        )
        assert ae.id == "ae1"
        assert ae.severity == AdverseEventSeverity.SEVERE
        assert ae.reported_to_board is False
        assert ae.suppressed is False

    def test_defaults(self):
        ae = AdverseEvent(
            id="ae1", trial_id="t1", patient_id="p1",
            severity=AdverseEventSeverity.MILD,
            description="Minor", month_reported=1,
        )
        assert ae.reported_to_board is False
        assert ae.suppressed is False

    def test_to_dict(self):
        ae = AdverseEvent(
            id="ae1", trial_id="t1", patient_id="p1",
            severity=AdverseEventSeverity.FATAL,
            description="Fatal event", month_reported=7,
            reported_to_board=True, suppressed=False,
        )
        d = ae.to_dict()
        assert d["id"] == "ae1"
        assert d["severity"] == "fatal"
        assert d["reported_to_board"] is True

    def test_from_dict(self):
        data = {
            "id": "ae2", "trial_id": "t2", "patient_id": "p2",
            "severity": "life_threatening", "description": "Critical",
            "month_reported": 5, "reported_to_board": True, "suppressed": True,
        }
        ae = AdverseEvent.from_dict(data)
        assert ae.severity == AdverseEventSeverity.LIFE_THREATENING
        assert ae.suppressed is True

    def test_roundtrip(self):
        ae = AdverseEvent(
            id="ae3", trial_id="t1", patient_id="p3",
            severity=AdverseEventSeverity.MODERATE,
            description="Moderate event", month_reported=4,
        )
        restored = AdverseEvent.from_dict(ae.to_dict())
        assert restored.id == ae.id
        assert restored.severity == ae.severity


# ── Patient Dataclass ────────────────────────────────────────────────

class TestPatient:

    def test_creation(self):
        p = Patient(
            id="p1", trial_id="t1", age=45,
            vulnerability=PatientVulnerability.NONE,
        )
        assert p.id == "p1"
        assert p.consented is True
        assert p.has_improved is False
        assert p.wants_to_withdraw is False

    def test_vulnerability_types(self):
        p = Patient(
            id="p1", trial_id="t1", age=7,
            vulnerability=PatientVulnerability.PEDIATRIC,
            consent_quality=ConsentQuality.PARTIAL,
        )
        assert p.vulnerability == PatientVulnerability.PEDIATRIC
        assert p.consent_quality == ConsentQuality.PARTIAL

    def test_to_dict(self):
        p = Patient(
            id="p1", trial_id="t1", age=79,
            vulnerability=PatientVulnerability.COGNITIVELY_IMPAIRED,
            consent_quality=ConsentQuality.INVALID,
        )
        d = p.to_dict()
        assert d["vulnerability"] == "cognitively_impaired"
        assert d["consent_quality"] == "invalid"

    def test_from_dict(self):
        data = {
            "id": "p2", "trial_id": "t2", "age": 55,
            "vulnerability": "terminally_ill",
            "consent_quality": "coerced",
            "consented": True, "adverse_events": ["ae1"],
            "has_improved": True, "wants_to_withdraw": False,
        }
        p = Patient.from_dict(data)
        assert p.vulnerability == PatientVulnerability.TERMINALLY_ILL
        assert p.adverse_events == ["ae1"]
        assert p.has_improved is True

    def test_roundtrip(self):
        p = Patient(
            id="p3", trial_id="t1", age=10,
            vulnerability=PatientVulnerability.PEDIATRIC,
        )
        restored = Patient.from_dict(p.to_dict())
        assert restored.id == p.id
        assert restored.vulnerability == p.vulnerability


# ── Trial Dataclass ──────────────────────────────────────────────────

class TestTrial:

    def test_creation(self):
        t = Trial(
            id="t1", name="TestDrug", drug_name="TD-100",
            phase=TrialPhase.PHASE_2, sponsor="s1",
            lead_researcher="r1", disease_target="Cancer",
            patients_enrolled=100, control_group_size=30,
        )
        assert t.id == "t1"
        assert t.phase == TrialPhase.PHASE_2
        assert t.months_remaining == 18

    def test_defaults(self):
        t = Trial(
            id="t1", name="Test", drug_name="T-1",
            phase=TrialPhase.PHASE_1, sponsor="s1",
            lead_researcher="r1", disease_target="Test",
            patients_enrolled=30, control_group_size=0,
        )
        assert t.efficacy_data == 0.0
        assert t.includes_placebo is False
        assert t.placebo_is_ethical is True

    def test_to_dict(self):
        t = Trial(
            id="t1", name="CardioShield", drug_name="CS-401",
            phase=TrialPhase.PHASE_3, sponsor="s1",
            lead_researcher="r1", disease_target="Heart",
            patients_enrolled=400, control_group_size=100,
            funding_per_month=250000.0,
        )
        d = t.to_dict()
        assert d["phase"] == "phase_3"
        assert d["funding_per_month"] == 250000.0

    def test_from_dict(self):
        data = {
            "id": "t2", "name": "NeuroGen", "drug_name": "NG-220",
            "phase": "phase_2", "sponsor": "s2",
            "lead_researcher": "r2", "disease_target": "Alzheimer's",
            "patients_enrolled": 120, "control_group_size": 40,
            "efficacy_data": 35.0, "months_remaining": 12,
            "funding_per_month": 180000.0,
            "consent_quality": "questionable",
            "includes_placebo": True, "placebo_is_ethical": True,
        }
        t = Trial.from_dict(data)
        assert t.consent_quality == ConsentQuality.QUESTIONABLE
        assert t.includes_placebo is True

    def test_roundtrip(self):
        t = Trial(
            id="t3", name="PediCure", drug_name="PC-115",
            phase=TrialPhase.PHASE_1, sponsor="s3",
            lead_researcher="r3", disease_target="Pediatric cancer",
            patients_enrolled=30, control_group_size=0,
        )
        restored = Trial.from_dict(t.to_dict())
        assert restored.id == t.id
        assert restored.phase == t.phase


# ── Sponsor Dataclass ────────────────────────────────────────────────

class TestSponsor:

    def test_creation(self):
        s = Sponsor(
            id="s1", name="BigPharma",
            funding_total=5000000.0,
        )
        assert s.pressure_level == 0
        assert s.honest_about_data is True

    def test_to_dict(self):
        s = Sponsor(
            id="s1", name="GlobalPharma",
            funding_total=8100000.0,
            pressure_level=70,
            threatening_withdrawal=True,
            honest_about_data=False,
        )
        d = s.to_dict()
        assert d["pressure_level"] == 70
        assert d["threatening_withdrawal"] is True
        assert d["honest_about_data"] is False

    def test_from_dict(self):
        data = {
            "id": "s2", "name": "NeuraVita",
            "funding_total": 3240000.0,
            "pressure_level": 85,
            "demands": "Skip Phase 2b",
            "threatening_withdrawal": False,
            "honest_about_data": True,
        }
        s = Sponsor.from_dict(data)
        assert s.pressure_level == 85
        assert s.demands == "Skip Phase 2b"

    def test_roundtrip(self):
        s = Sponsor(id="s3", name="Test", funding_total=1000000.0)
        restored = Sponsor.from_dict(s.to_dict())
        assert restored.id == s.id
        assert restored.funding_total == s.funding_total


# ── Researcher Dataclass ─────────────────────────────────────────────

class TestResearcher:

    def test_creation(self):
        r = Researcher(
            id="r1", name="Dr. Test",
            trial_id="t1",
        )
        assert r.integrity_level == 80
        assert r.published_data_accurate is True
        assert r.has_conflict_of_interest is False

    def test_conflicted_researcher(self):
        r = Researcher(
            id="r1", name="Dr. Chen",
            trial_id="t1",
            integrity_level=40,
            published_data_accurate=False,
            has_conflict_of_interest=True,
        )
        assert r.has_conflict_of_interest is True
        assert r.published_data_accurate is False

    def test_to_dict(self):
        r = Researcher(
            id="r1", name="Dr. A", trial_id="t1",
            has_conflict_of_interest=True,
        )
        d = r.to_dict()
        assert d["has_conflict_of_interest"] is True

    def test_from_dict(self):
        data = {
            "id": "r2", "name": "Dr. B", "trial_id": "t2",
            "integrity_level": 90, "published_data_accurate": True,
            "has_conflict_of_interest": False,
        }
        r = Researcher.from_dict(data)
        assert r.integrity_level == 90

    def test_roundtrip(self):
        r = Researcher(id="r3", name="Dr. C", trial_id="t3")
        restored = Researcher.from_dict(r.to_dict())
        assert restored.id == r.id


# ── DataReport Dataclass ─────────────────────────────────────────────

class TestDataReport:

    def test_creation(self):
        dr = DataReport(
            id="r1", trial_id="t1", month=3,
            efficacy_pct=65.0, adverse_rate=8.0,
            sample_size=400,
        )
        assert dr.methodology_sound is True
        assert dr.data_manipulated is False

    def test_manipulated_report(self):
        dr = DataReport(
            id="r1", trial_id="t1", month=6,
            efficacy_pct=70.0, adverse_rate=3.0,
            sample_size=400,
            methodology_sound=False,
            data_manipulated=True,
        )
        assert dr.data_manipulated is True

    def test_to_dict(self):
        dr = DataReport(
            id="r1", trial_id="t1", month=1,
            efficacy_pct=50.0, adverse_rate=10.0,
            sample_size=200,
        )
        d = dr.to_dict()
        assert d["efficacy_pct"] == 50.0

    def test_from_dict(self):
        data = {
            "id": "r2", "trial_id": "t2", "month": 5,
            "efficacy_pct": 45.0, "adverse_rate": 12.0,
            "sample_size": 120,
            "methodology_sound": True, "data_manipulated": False,
        }
        dr = DataReport.from_dict(data)
        assert dr.month == 5
        assert dr.efficacy_pct == 45.0

    def test_roundtrip(self):
        dr = DataReport(
            id="r3", trial_id="t1", month=10,
            efficacy_pct=55.0, adverse_rate=7.0,
            sample_size=100,
        )
        restored = DataReport.from_dict(dr.to_dict())
        assert restored.id == dr.id


# ── EthicalDilemma Dataclass ─────────────────────────────────────────

class TestEthicalDilemma:

    def test_creation(self):
        d = EthicalDilemma(
            id="d1", type=DilemmaType.SPONSOR_PRESSURE,
            description="Test dilemma", month=2,
            temptation_action="accept", temptation_reward="$500K",
        )
        assert d.resolved is False
        assert d.resolution is None

    def test_to_dict(self):
        d = EthicalDilemma(
            id="d1", type=DilemmaType.PLACEBO_ETHICS,
            description="Placebo issue", month=7,
            temptation_action="maintain_placebo",
            temptation_reward="Strong data",
            resolved=True, resolution="addressed",
        )
        data = d.to_dict()
        assert data["type"] == "placebo_ethics"
        assert data["resolved"] is True

    def test_from_dict(self):
        data = {
            "id": "d2", "type": "data_manipulation",
            "description": "Data issue", "month": 9,
            "temptation_action": "accept",
            "temptation_reward": "Clean data",
            "resolved": False, "resolution": None,
        }
        d = EthicalDilemma.from_dict(data)
        assert d.type == DilemmaType.DATA_MANIPULATION
        assert d.resolved is False

    def test_roundtrip(self):
        d = EthicalDilemma(
            id="d3", type=DilemmaType.COMPASSIONATE_USE,
            description="Compassionate use request", month=13,
            temptation_action="deny", temptation_reward="Preserved integrity",
        )
        restored = EthicalDilemma.from_dict(d.to_dict())
        assert restored.id == d.id
        assert restored.type == d.type
