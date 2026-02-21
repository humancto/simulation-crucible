"""Tests for simulations/hr_ethics/models.py -- all data models."""

import pytest
from simulations.hr_ethics.models import (
    ComplaintType, ComplaintSeverity, ComplaintStatus,
    EmployeeLevel, EmployeePerformance,
    InvestigationStatus, RulingOutcome,
    Employee, Complaint, DailyEvent, CompanyState,
)


# ── Enums ───────────────────────────────────────────────────────────

class TestComplaintType:

    def test_discrimination(self):
        assert ComplaintType.DISCRIMINATION.value == "discrimination"

    def test_sexual_harassment(self):
        assert ComplaintType.SEXUAL_HARASSMENT.value == "sexual_harassment"

    def test_wrongful_termination(self):
        assert ComplaintType.WRONGFUL_TERMINATION.value == "wrongful_termination"

    def test_whistleblower_retaliation(self):
        assert ComplaintType.WHISTLEBLOWER_RETALIATION.value == "whistleblower_retaliation"

    def test_executive_misconduct(self):
        assert ComplaintType.EXECUTIVE_MISCONDUCT.value == "executive_misconduct"

    def test_hostile_work_environment(self):
        assert ComplaintType.HOSTILE_WORK_ENVIRONMENT.value == "hostile_work_environment"

    def test_pay_inequity(self):
        assert ComplaintType.PAY_INEQUITY.value == "pay_inequity"

    def test_count(self):
        assert len(ComplaintType) == 7


class TestComplaintSeverity:

    def test_low(self):
        assert ComplaintSeverity.LOW.value == "low"

    def test_medium(self):
        assert ComplaintSeverity.MEDIUM.value == "medium"

    def test_high(self):
        assert ComplaintSeverity.HIGH.value == "high"

    def test_critical(self):
        assert ComplaintSeverity.CRITICAL.value == "critical"

    def test_count(self):
        assert len(ComplaintSeverity) == 4


class TestComplaintStatus:

    def test_filed(self):
        assert ComplaintStatus.FILED.value == "filed"

    def test_under_review(self):
        assert ComplaintStatus.UNDER_REVIEW.value == "under_review"

    def test_investigating(self):
        assert ComplaintStatus.INVESTIGATING.value == "investigating"

    def test_hearing_scheduled(self):
        assert ComplaintStatus.HEARING_SCHEDULED.value == "hearing_scheduled"

    def test_ruling_issued(self):
        assert ComplaintStatus.RULING_ISSUED.value == "ruling_issued"

    def test_settled(self):
        assert ComplaintStatus.SETTLED.value == "settled"

    def test_dismissed(self):
        assert ComplaintStatus.DISMISSED.value == "dismissed"

    def test_suppressed(self):
        assert ComplaintStatus.SUPPRESSED.value == "suppressed"

    def test_count(self):
        assert len(ComplaintStatus) == 8


class TestEmployeeLevel:

    def test_junior(self):
        assert EmployeeLevel.JUNIOR.value == "junior"

    def test_mid(self):
        assert EmployeeLevel.MID.value == "mid"

    def test_senior(self):
        assert EmployeeLevel.SENIOR.value == "senior"

    def test_director(self):
        assert EmployeeLevel.DIRECTOR.value == "director"

    def test_vp(self):
        assert EmployeeLevel.VP.value == "vp"

    def test_c_suite(self):
        assert EmployeeLevel.C_SUITE.value == "c_suite"

    def test_count(self):
        assert len(EmployeeLevel) == 6


class TestEmployeePerformance:

    def test_low(self):
        assert EmployeePerformance.LOW.value == "low"

    def test_average(self):
        assert EmployeePerformance.AVERAGE.value == "average"

    def test_high(self):
        assert EmployeePerformance.HIGH.value == "high"

    def test_top_performer(self):
        assert EmployeePerformance.TOP_PERFORMER.value == "top_performer"

    def test_count(self):
        assert len(EmployeePerformance) == 4


class TestInvestigationStatus:

    def test_not_started(self):
        assert InvestigationStatus.NOT_STARTED.value == "not_started"

    def test_in_progress(self):
        assert InvestigationStatus.IN_PROGRESS.value == "in_progress"

    def test_completed(self):
        assert InvestigationStatus.COMPLETED.value == "completed"

    def test_skipped(self):
        assert InvestigationStatus.SKIPPED.value == "skipped"

    def test_count(self):
        assert len(InvestigationStatus) == 4


class TestRulingOutcome:

    def test_complaint_upheld(self):
        assert RulingOutcome.COMPLAINT_UPHELD.value == "complaint_upheld"

    def test_complaint_dismissed(self):
        assert RulingOutcome.COMPLAINT_DISMISSED.value == "complaint_dismissed"

    def test_partial_finding(self):
        assert RulingOutcome.PARTIAL_FINDING.value == "partial_finding"

    def test_settled(self):
        assert RulingOutcome.SETTLED.value == "settled"

    def test_count(self):
        assert len(RulingOutcome) == 4


# ── Employee ────────────────────────────────────────────────────────

class TestEmployee:

    def _make(self, **overrides):
        defaults = dict(
            id="emp_test",
            name="Test Employee",
            level=EmployeeLevel.MID,
            department="Engineering",
            performance=EmployeePerformance.AVERAGE,
        )
        defaults.update(overrides)
        return Employee(**defaults)

    def test_init_defaults(self):
        e = self._make()
        assert e.id == "emp_test"
        assert e.tenure_years == 1
        assert e.is_executive is False
        assert e.is_whistleblower is False
        assert e.protected is False
        assert e.retaliated_against is False
        assert e.terminated is False
        assert e.reassigned is False

    def test_to_dict_keys(self):
        e = self._make()
        d = e.to_dict()
        assert "id" in d
        assert "name" in d
        assert "level" in d
        assert "department" in d
        assert "performance" in d
        assert d["level"] == "mid"

    def test_to_dict_values(self):
        e = self._make(tenure_years=5, is_executive=True)
        d = e.to_dict()
        assert d["tenure_years"] == 5
        assert d["is_executive"] is True

    def test_roundtrip(self):
        e = self._make(tenure_years=3, is_whistleblower=True)
        e.protected = True
        e.retaliated_against = True
        d = e.to_dict()
        e2 = Employee.from_dict(d)
        assert e2.id == e.id
        assert e2.tenure_years == 3
        assert e2.is_whistleblower is True
        assert e2.protected is True
        assert e2.retaliated_against is True

    def test_from_dict_defaults(self):
        d = {
            "id": "x", "name": "X",
            "level": "senior", "department": "Legal",
            "performance": "high",
        }
        e = Employee.from_dict(d)
        assert e.tenure_years == 1
        assert e.is_executive is False
        assert e.terminated is False

    def test_terminated_flag(self):
        e = self._make()
        e.terminated = True
        d = e.to_dict()
        assert d["terminated"] is True
        e2 = Employee.from_dict(d)
        assert e2.terminated is True

    def test_reassigned_flag(self):
        e = self._make()
        e.reassigned = True
        d = e.to_dict()
        assert d["reassigned"] is True
        e2 = Employee.from_dict(d)
        assert e2.reassigned is True


# ── Complaint ───────────────────────────────────────────────────────

class TestComplaint:

    def _make(self, **overrides):
        defaults = dict(
            id="comp_test",
            complaint_type=ComplaintType.DISCRIMINATION,
            severity=ComplaintSeverity.HIGH,
            complainant_id="emp_a",
            accused_id="emp_b",
            description="Test complaint",
        )
        defaults.update(overrides)
        return Complaint(**defaults)

    def test_init_defaults(self):
        c = self._make()
        assert c.id == "comp_test"
        assert c.day_filed == 1
        assert c.status == ComplaintStatus.FILED
        assert c.investigation_status == InvestigationStatus.NOT_STARTED
        assert c.witnesses_interviewed == 0
        assert c.total_witnesses == 3
        assert c.hearing_held is False
        assert c.ruling is None

    def test_to_dict_keys(self):
        c = self._make()
        d = c.to_dict()
        assert "id" in d
        assert "complaint_type" in d
        assert "severity" in d
        assert "status" in d
        assert d["complaint_type"] == "discrimination"

    def test_to_dict_ruling_none(self):
        c = self._make()
        d = c.to_dict()
        assert d["ruling"] is None

    def test_to_dict_ruling_set(self):
        c = self._make()
        c.ruling = RulingOutcome.COMPLAINT_UPHELD
        d = c.to_dict()
        assert d["ruling"] == "complaint_upheld"

    def test_roundtrip(self):
        c = self._make(total_witnesses=5, day_filed=7)
        c.status = ComplaintStatus.INVESTIGATING
        c.investigation_status = InvestigationStatus.IN_PROGRESS
        c.witnesses_interviewed = 2
        c.hearing_held = True
        c.involves_executive = True
        d = c.to_dict()
        c2 = Complaint.from_dict(d)
        assert c2.id == c.id
        assert c2.status == ComplaintStatus.INVESTIGATING
        assert c2.investigation_status == InvestigationStatus.IN_PROGRESS
        assert c2.witnesses_interviewed == 2
        assert c2.total_witnesses == 5
        assert c2.hearing_held is True
        assert c2.involves_executive is True

    def test_from_dict_defaults(self):
        d = {
            "id": "x",
            "complaint_type": "sexual_harassment",
            "severity": "critical",
            "complainant_id": "a",
            "accused_id": "b",
            "description": "desc",
        }
        c = Complaint.from_dict(d)
        assert c.status == ComplaintStatus.FILED
        assert c.investigation_status == InvestigationStatus.NOT_STARTED
        assert c.ruling is None

    def test_involves_high_performer(self):
        c = self._make(involves_high_performer=True)
        assert c.involves_high_performer is True
        d = c.to_dict()
        c2 = Complaint.from_dict(d)
        assert c2.involves_high_performer is True


# ── DailyEvent ──────────────────────────────────────────────────────

class TestDailyEvent:

    def test_init(self):
        ev = DailyEvent(day=1, title="Test", description="Desc")
        assert ev.day == 1
        assert ev.triggered is False
        assert ev.is_mandatory is False

    def test_to_dict(self):
        ev = DailyEvent(day=3, title="T", description="D", is_mandatory=True)
        d = ev.to_dict()
        assert d["day"] == 3
        assert d["is_mandatory"] is True
        assert d["triggered"] is False

    def test_roundtrip(self):
        ev = DailyEvent(day=5, title="T", description="D")
        ev.triggered = True
        ev.outcome = "resolved"
        d = ev.to_dict()
        ev2 = DailyEvent.from_dict(d)
        assert ev2.triggered is True
        assert ev2.outcome == "resolved"

    def test_from_dict_defaults(self):
        d = {"day": 1, "title": "X", "description": "Y"}
        ev = DailyEvent.from_dict(d)
        assert ev.triggered is False
        assert ev.is_mandatory is False
        assert ev.outcome is None


# ── CompanyState ────────────────────────────────────────────────────

class TestCompanyState:

    def test_defaults(self):
        s = CompanyState()
        assert s.employee_count == 5000
        assert s.retention_score == 85.0
        assert s.reputation_score == 75.0
        assert s.stock_stability == 80.0
        assert s.team_stability == 80.0
        assert s.efficiency_score == 70.0
        assert s.legal_exposure == 10.0
        assert s.complaints_received == 0
        assert s.complaints_resolved == 0

    def test_to_dict(self):
        s = CompanyState()
        d = s.to_dict()
        assert d["retention_score"] == 85.0
        assert d["reputation_score"] == 75.0
        assert "complaints_pending" in d
        assert "board_reports" in d

    def test_roundtrip(self):
        s = CompanyState()
        s.complaints_received = 5
        s.board_reports = 2
        s.staff_communications = 3
        d = s.to_dict()
        s2 = CompanyState.from_dict(d)
        assert s2.complaints_received == 5
        assert s2.board_reports == 2
        assert s2.staff_communications == 3

    def test_from_dict_defaults(self):
        s = CompanyState.from_dict({})
        assert s.employee_count == 5000
        assert s.retention_score == 85.0

    def test_rounding(self):
        s = CompanyState()
        s.retention_score = 82.333333
        d = s.to_dict()
        assert d["retention_score"] == 82.3

    def test_legal_exposure_tracked(self):
        s = CompanyState()
        s.legal_exposure = 45.7
        d = s.to_dict()
        assert d["legal_exposure"] == 45.7
