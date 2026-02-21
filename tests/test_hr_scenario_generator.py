"""Tests for simulations/hr_ethics/scenario_generator.py."""

import random
import pytest
from simulations.hr_ethics.scenario_generator import ScenarioGenerator
from simulations.hr_ethics.models import (
    Employee, Complaint, DailyEvent, CompanyState,
    ComplaintType, ComplaintSeverity, EmployeeLevel,
    EmployeePerformance,
)


@pytest.fixture
def gen():
    return ScenarioGenerator(random.Random(42))


# ── generate_employees ────────────────────────────────────────────

class TestGenerateEmployees:

    def test_returns_list(self, gen):
        employees = gen.generate_employees()
        assert isinstance(employees, list)

    def test_employee_count(self, gen):
        assert len(gen.generate_employees()) >= 10

    def test_all_employees(self, gen):
        for e in gen.generate_employees():
            assert isinstance(e, Employee)

    def test_unique_ids(self, gen):
        employees = gen.generate_employees()
        ids = [e.id for e in employees]
        assert len(ids) == len(set(ids))

    def test_has_executives(self, gen):
        execs = [e for e in gen.generate_employees() if e.is_executive]
        assert len(execs) == 5

    def test_has_c_suite(self, gen):
        levels = {e.level for e in gen.generate_employees()}
        assert EmployeeLevel.C_SUITE in levels

    def test_has_vp(self, gen):
        levels = {e.level for e in gen.generate_employees()}
        assert EmployeeLevel.VP in levels

    def test_has_junior(self, gen):
        levels = {e.level for e in gen.generate_employees()}
        assert EmployeeLevel.JUNIOR in levels

    def test_has_top_performers(self, gen):
        perfs = {e.performance for e in gen.generate_employees()}
        assert EmployeePerformance.TOP_PERFORMER in perfs

    def test_has_whistleblower(self, gen):
        whistle = [e for e in gen.generate_employees() if e.is_whistleblower]
        assert len(whistle) >= 1

    def test_no_terminations_initially(self, gen):
        for e in gen.generate_employees():
            assert e.terminated is False

    def test_no_retaliation_initially(self, gen):
        for e in gen.generate_employees():
            assert e.retaliated_against is False

    def test_no_protection_initially(self, gen):
        for e in gen.generate_employees():
            assert e.protected is False

    def test_has_ceo(self, gen):
        ids = {e.id for e in gen.generate_employees()}
        assert "emp_ceo_harris" in ids

    def test_has_cto(self, gen):
        ids = {e.id for e in gen.generate_employees()}
        assert "emp_cto_nakamura" in ids

    def test_has_whistleblower_pratt(self, gen):
        ids = {e.id for e in gen.generate_employees()}
        assert "emp_sr_legal_pratt" in ids

    def test_multiple_departments(self, gen):
        depts = {e.department for e in gen.generate_employees()}
        assert len(depts) >= 5

    def test_deterministic(self):
        g1 = ScenarioGenerator(random.Random(99))
        g2 = ScenarioGenerator(random.Random(99))
        e1 = g1.generate_employees()
        e2 = g2.generate_employees()
        assert len(e1) == len(e2)
        for a, b in zip(e1, e2):
            assert a.id == b.id


# ── generate_complaints ──────────────────────────────────────────

class TestGenerateComplaints:

    def test_returns_list(self, gen):
        complaints = gen.generate_complaints()
        assert isinstance(complaints, list)

    def test_complaint_count(self, gen):
        complaints = gen.generate_complaints()
        assert len(complaints) >= 12

    def test_all_complaints(self, gen):
        for c in gen.generate_complaints():
            assert isinstance(c, Complaint)

    def test_unique_ids(self, gen):
        complaints = gen.generate_complaints()
        ids = [c.id for c in complaints]
        assert len(ids) == len(set(ids))

    def test_has_discrimination(self, gen):
        types = {c.complaint_type for c in gen.generate_complaints()}
        assert ComplaintType.DISCRIMINATION in types

    def test_has_sexual_harassment(self, gen):
        types = {c.complaint_type for c in gen.generate_complaints()}
        assert ComplaintType.SEXUAL_HARASSMENT in types

    def test_has_wrongful_termination(self, gen):
        types = {c.complaint_type for c in gen.generate_complaints()}
        assert ComplaintType.WRONGFUL_TERMINATION in types

    def test_has_whistleblower_retaliation(self, gen):
        types = {c.complaint_type for c in gen.generate_complaints()}
        assert ComplaintType.WHISTLEBLOWER_RETALIATION in types

    def test_has_executive_misconduct(self, gen):
        types = {c.complaint_type for c in gen.generate_complaints()}
        assert ComplaintType.EXECUTIVE_MISCONDUCT in types

    def test_has_hostile_work_environment(self, gen):
        types = {c.complaint_type for c in gen.generate_complaints()}
        assert ComplaintType.HOSTILE_WORK_ENVIRONMENT in types

    def test_has_pay_inequity(self, gen):
        types = {c.complaint_type for c in gen.generate_complaints()}
        assert ComplaintType.PAY_INEQUITY in types

    def test_severity_range(self, gen):
        sevs = {c.severity for c in gen.generate_complaints()}
        assert ComplaintSeverity.CRITICAL in sevs
        assert ComplaintSeverity.HIGH in sevs

    def test_early_complaints_small_days(self, gen):
        complaints = gen.generate_complaints()
        early = [c for c in complaints if c.day_filed <= 5]
        assert len(early) >= 3

    def test_late_complaints(self, gen):
        complaints = gen.generate_complaints()
        late = [c for c in complaints if c.day_filed >= 21]
        assert len(late) >= 2

    def test_has_executive_complaints(self, gen):
        exec_comps = [c for c in gen.generate_complaints()
                      if c.involves_executive]
        assert len(exec_comps) >= 5

    def test_has_high_performer_complaints(self, gen):
        hp_comps = [c for c in gen.generate_complaints()
                    if c.involves_high_performer]
        assert len(hp_comps) >= 3

    def test_complaints_not_resolved_initially(self, gen):
        from simulations.hr_ethics.models import ComplaintStatus
        for c in gen.generate_complaints():
            assert c.status == ComplaintStatus.FILED

    def test_no_investigations_initially(self, gen):
        from simulations.hr_ethics.models import InvestigationStatus
        for c in gen.generate_complaints():
            assert c.investigation_status == InvestigationStatus.NOT_STARTED

    def test_no_hearings_initially(self, gen):
        for c in gen.generate_complaints():
            assert c.hearing_held is False

    def test_no_rulings_initially(self, gen):
        for c in gen.generate_complaints():
            assert c.ruling is None

    def test_deterministic(self):
        g1 = ScenarioGenerator(random.Random(99))
        g2 = ScenarioGenerator(random.Random(99))
        c1 = g1.generate_complaints()
        c2 = g2.generate_complaints()
        assert len(c1) == len(c2)
        for a, b in zip(c1, c2):
            assert a.id == b.id


# ── generate_events ──────────────────────────────────────────────

class TestGenerateEvents:

    def test_returns_list(self, gen):
        events = gen.generate_events()
        assert isinstance(events, list)

    def test_event_count(self, gen):
        assert len(gen.generate_events()) >= 15

    def test_all_daily_events(self, gen):
        for ev in gen.generate_events():
            assert isinstance(ev, DailyEvent)

    def test_has_mandatory_events(self, gen):
        mandatory = [ev for ev in gen.generate_events() if ev.is_mandatory]
        assert len(mandatory) >= 10

    def test_first_day_event(self, gen):
        events = gen.generate_events()
        day1 = [ev for ev in events if ev.day == 1]
        assert len(day1) >= 1

    def test_last_day_event(self, gen):
        events = gen.generate_events()
        day30 = [ev for ev in events if ev.day == 30]
        assert len(day30) >= 1

    def test_harassment_event(self, gen):
        events = gen.generate_events()
        harass = [ev for ev in events
                  if "harassment" in ev.title.lower()
                  or "harassment" in ev.description.lower()]
        assert len(harass) >= 1

    def test_whistleblower_event(self, gen):
        events = gen.generate_events()
        whistle = [ev for ev in events
                   if "whistleblower" in ev.title.lower()
                   or "whistleblower" in ev.description.lower()
                   or "retaliat" in ev.description.lower()]
        assert len(whistle) >= 1

    def test_board_event(self, gen):
        events = gen.generate_events()
        board = [ev for ev in events
                 if "board" in ev.title.lower()
                 or "board" in ev.description.lower()]
        assert len(board) >= 1

    def test_events_not_triggered(self, gen):
        for ev in gen.generate_events():
            assert ev.triggered is False


# ── generate_company_state ────────────────────────────────────────

class TestGenerateCompanyState:

    def test_returns_company_state(self, gen):
        s = gen.generate_company_state()
        assert isinstance(s, CompanyState)

    def test_initial_values(self, gen):
        s = gen.generate_company_state()
        assert s.employee_count == 5000
        assert s.retention_score == 85.0
        assert s.complaints_received == 0
