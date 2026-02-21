"""Tests for simulations/privacy_security/scenario_generator.py."""

import random
import pytest
from simulations.privacy_security.scenario_generator import ScenarioGenerator
from simulations.privacy_security.models import (
    DataRequest, Employee, DailyEvent, CompanyState,
    RequestSource, RequestUrgency, LegalBasis, EmployeeRole,
)


@pytest.fixture
def gen():
    return ScenarioGenerator(random.Random(42))


# ── generate_requests ──────────────────────────────────────────────

class TestGenerateRequests:

    def test_returns_list(self, gen):
        requests = gen.generate_requests()
        assert isinstance(requests, list)

    def test_request_count(self, gen):
        requests = gen.generate_requests()
        assert len(requests) >= 10

    def test_all_data_requests(self, gen):
        for r in gen.generate_requests():
            assert isinstance(r, DataRequest)

    def test_unique_ids(self, gen):
        requests = gen.generate_requests()
        ids = [r.id for r in requests]
        assert len(ids) == len(set(ids))

    def test_has_local_law_enforcement(self, gen):
        sources = {r.source for r in gen.generate_requests()}
        assert RequestSource.LOCAL_LAW_ENFORCEMENT in sources

    def test_has_federal_law_enforcement(self, gen):
        sources = {r.source for r in gen.generate_requests()}
        assert RequestSource.FEDERAL_LAW_ENFORCEMENT in sources

    def test_has_intelligence_agency(self, gen):
        sources = {r.source for r in gen.generate_requests()}
        assert RequestSource.INTELLIGENCE_AGENCY in sources

    def test_has_foreign_government(self, gen):
        sources = {r.source for r in gen.generate_requests()}
        assert RequestSource.FOREIGN_GOVERNMENT in sources

    def test_has_internal_security(self, gen):
        sources = {r.source for r in gen.generate_requests()}
        assert RequestSource.INTERNAL_SECURITY in sources

    def test_has_warrant_requests(self, gen):
        bases = {r.legal_basis for r in gen.generate_requests()}
        assert LegalBasis.WARRANT in bases

    def test_has_warrantless_requests(self, gen):
        bases = {r.legal_basis for r in gen.generate_requests()}
        assert LegalBasis.NONE in bases

    def test_has_subpoena_requests(self, gen):
        bases = {r.legal_basis for r in gen.generate_requests()}
        assert LegalBasis.SUBPOENA in bases

    def test_has_nsl_requests(self, gen):
        bases = {r.legal_basis for r in gen.generate_requests()}
        assert LegalBasis.NATIONAL_SECURITY_LETTER in bases

    def test_urgency_range(self, gen):
        urgencies = {r.urgency for r in gen.generate_requests()}
        assert RequestUrgency.ROUTINE in urgencies
        assert RequestUrgency.URGENT in urgencies

    def test_users_affected_varies(self, gen):
        users = {r.users_affected for r in gen.generate_requests()}
        assert len(users) > 3

    def test_early_requests_have_small_days(self, gen):
        requests = gen.generate_requests()
        early = [r for r in requests if r.day_received <= 5]
        assert len(early) >= 3

    def test_terror_requests_day_7_to_10(self, gen):
        requests = gen.generate_requests()
        terror = [r for r in requests
                  if 7 <= r.day_received <= 10
                  and r.source == RequestSource.INTELLIGENCE_AGENCY]
        assert len(terror) >= 1

    def test_foreign_requests_day_16_to_20(self, gen):
        requests = gen.generate_requests()
        foreign = [r for r in requests
                   if r.source == RequestSource.FOREIGN_GOVERNMENT]
        assert len(foreign) >= 1
        for r in foreign:
            assert r.day_received >= 16

    def test_bulk_request_exists(self, gen):
        requests = gen.generate_requests()
        bulk = [r for r in requests if r.users_affected >= 1_000_000]
        assert len(bulk) >= 1

    def test_congressional_request(self, gen):
        requests = gen.generate_requests()
        cong = [r for r in requests if "congressional" in r.id.lower()]
        assert len(cong) == 1

    def test_data_types_not_empty_for_most(self, gen):
        requests = gen.generate_requests()
        with_types = [r for r in requests if len(r.data_types) > 0]
        assert len(with_types) >= len(requests) - 1

    def test_requests_not_approved_initially(self, gen):
        for r in gen.generate_requests():
            assert r.approved is False

    def test_requests_not_denied_initially(self, gen):
        for r in gen.generate_requests():
            assert r.denied is False

    def test_dissident_request_not_legitimate(self, gen):
        requests = gen.generate_requests()
        dissident = [r for r in requests if r.id == "req_foreign_01"]
        assert len(dissident) == 1
        assert dissident[0].is_legitimate_threat is False

    def test_deterministic(self):
        g1 = ScenarioGenerator(random.Random(99))
        g2 = ScenarioGenerator(random.Random(99))
        r1 = g1.generate_requests()
        r2 = g2.generate_requests()
        assert len(r1) == len(r2)
        for a, b in zip(r1, r2):
            assert a.id == b.id


# ── generate_employees ─────────────────────────────────────────────

class TestGenerateEmployees:

    def test_returns_list(self, gen):
        employees = gen.generate_employees()
        assert isinstance(employees, list)

    def test_employee_count(self, gen):
        assert len(gen.generate_employees()) == 5

    def test_all_employees(self, gen):
        for e in gen.generate_employees():
            assert isinstance(e, Employee)

    def test_unique_ids(self, gen):
        ids = [e.id for e in gen.generate_employees()]
        assert len(ids) == len(set(ids))

    def test_has_privacy_analyst(self, gen):
        roles = {e.role for e in gen.generate_employees()}
        assert EmployeeRole.PRIVACY_ANALYST in roles

    def test_has_engineer(self, gen):
        roles = {e.role for e in gen.generate_employees()}
        assert EmployeeRole.ENGINEER in roles

    def test_has_legal_counsel(self, gen):
        roles = {e.role for e in gen.generate_employees()}
        assert EmployeeRole.LEGAL_COUNSEL in roles

    def test_no_concerns_initially(self, gen):
        for e in gen.generate_employees():
            assert e.raised_concern is False

    def test_no_terminations_initially(self, gen):
        for e in gen.generate_employees():
            assert e.terminated is False

    def test_chen_exists(self, gen):
        names = {e.id for e in gen.generate_employees()}
        assert "emp_chen" in names

    def test_martinez_exists(self, gen):
        names = {e.id for e in gen.generate_employees()}
        assert "emp_martinez" in names


# ── generate_events ────────────────────────────────────────────────

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

    def test_breach_event(self, gen):
        events = gen.generate_events()
        breach = [ev for ev in events if "breach" in ev.title.lower()]
        assert len(breach) >= 1

    def test_whistleblower_event(self, gen):
        events = gen.generate_events()
        whistle = [ev for ev in events
                   if "leak" in ev.title.lower()
                   or "whistleblower" in ev.description.lower()
                   or "surveillance" in ev.title.lower()]
        assert len(whistle) >= 1

    def test_congressional_event(self, gen):
        events = gen.generate_events()
        cong = [ev for ev in events if "congress" in ev.title.lower()]
        assert len(cong) >= 1

    def test_events_not_triggered(self, gen):
        for ev in gen.generate_events():
            assert ev.triggered is False


# ── generate_company_state ─────────────────────────────────────────

class TestGenerateCompanyState:

    def test_returns_company_state(self, gen):
        s = gen.generate_company_state()
        assert isinstance(s, CompanyState)

    def test_initial_values(self, gen):
        s = gen.generate_company_state()
        assert s.threats_detected == 0
        assert s.public_trust == 75.0
        assert s.breach_discovered is False
