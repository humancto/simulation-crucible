"""Tests for simulations/privacy_security/models.py -- all data models."""

import pytest
from simulations.privacy_security.models import (
    CompanyState, DailyEvent, DataRequest, Employee,
    EmployeeRole, LegalBasis, RequestScope, RequestSource,
    RequestUrgency, ThreatLevel,
)


# ── Enums ───────────────────────────────────────────────────────────

class TestRequestSource:

    def test_local_law_enforcement(self):
        assert RequestSource.LOCAL_LAW_ENFORCEMENT.value == "local_law_enforcement"

    def test_federal_law_enforcement(self):
        assert RequestSource.FEDERAL_LAW_ENFORCEMENT.value == "federal_law_enforcement"

    def test_intelligence_agency(self):
        assert RequestSource.INTELLIGENCE_AGENCY.value == "intelligence_agency"

    def test_foreign_government(self):
        assert RequestSource.FOREIGN_GOVERNMENT.value == "foreign_government"

    def test_internal_security(self):
        assert RequestSource.INTERNAL_SECURITY.value == "internal_security"

    def test_count(self):
        assert len(RequestSource) == 5


class TestRequestUrgency:

    def test_routine(self):
        assert RequestUrgency.ROUTINE.value == "routine"

    def test_elevated(self):
        assert RequestUrgency.ELEVATED.value == "elevated"

    def test_urgent(self):
        assert RequestUrgency.URGENT.value == "urgent"

    def test_emergency(self):
        assert RequestUrgency.EMERGENCY.value == "emergency"

    def test_count(self):
        assert len(RequestUrgency) == 4


class TestRequestScope:

    def test_narrow(self):
        assert RequestScope.NARROW.value == "narrow"

    def test_standard(self):
        assert RequestScope.STANDARD.value == "standard"

    def test_broad(self):
        assert RequestScope.BROAD.value == "broad"

    def test_count(self):
        assert len(RequestScope) == 3


class TestLegalBasis:

    def test_warrant(self):
        assert LegalBasis.WARRANT.value == "warrant"

    def test_subpoena(self):
        assert LegalBasis.SUBPOENA.value == "subpoena"

    def test_national_security_letter(self):
        assert LegalBasis.NATIONAL_SECURITY_LETTER.value == "national_security_letter"

    def test_court_order(self):
        assert LegalBasis.COURT_ORDER.value == "court_order"

    def test_none(self):
        assert LegalBasis.NONE.value == "none"

    def test_count(self):
        assert len(LegalBasis) == 5


class TestThreatLevel:

    def test_low(self):
        assert ThreatLevel.LOW.value == "low"

    def test_moderate(self):
        assert ThreatLevel.MODERATE.value == "moderate"

    def test_high(self):
        assert ThreatLevel.HIGH.value == "high"

    def test_critical(self):
        assert ThreatLevel.CRITICAL.value == "critical"

    def test_count(self):
        assert len(ThreatLevel) == 4


class TestEmployeeRole:

    def test_engineer(self):
        assert EmployeeRole.ENGINEER.value == "engineer"

    def test_legal_counsel(self):
        assert EmployeeRole.LEGAL_COUNSEL.value == "legal_counsel"

    def test_privacy_analyst(self):
        assert EmployeeRole.PRIVACY_ANALYST.value == "privacy_analyst"

    def test_security_analyst(self):
        assert EmployeeRole.SECURITY_ANALYST.value == "security_analyst"

    def test_executive(self):
        assert EmployeeRole.EXECUTIVE.value == "executive"

    def test_count(self):
        assert len(EmployeeRole) == 5


# ── DataRequest ────────────────────────────────────────────────────

class TestDataRequest:

    def _make(self, **overrides):
        defaults = dict(
            id="req_test",
            source=RequestSource.LOCAL_LAW_ENFORCEMENT,
            urgency=RequestUrgency.ROUTINE,
            legal_basis=LegalBasis.WARRANT,
            description="Test request",
            users_affected=10,
        )
        defaults.update(overrides)
        return DataRequest(**defaults)

    def test_init_defaults(self):
        r = self._make()
        assert r.id == "req_test"
        assert r.approved is False
        assert r.denied is False
        assert r.scope is None
        assert r.data_types == []

    def test_to_dict_keys(self):
        r = self._make()
        d = r.to_dict()
        assert "id" in d
        assert "source" in d
        assert "urgency" in d
        assert "legal_basis" in d
        assert d["source"] == "local_law_enforcement"

    def test_to_dict_scope_none(self):
        r = self._make()
        d = r.to_dict()
        assert d["scope"] is None

    def test_to_dict_scope_set(self):
        r = self._make()
        r.scope = RequestScope.NARROW
        d = r.to_dict()
        assert d["scope"] == "narrow"

    def test_roundtrip(self):
        r = self._make(data_types=["messages", "contacts"])
        r.approved = True
        r.scope = RequestScope.BROAD
        d = r.to_dict()
        r2 = DataRequest.from_dict(d)
        assert r2.id == r.id
        assert r2.approved is True
        assert r2.scope == RequestScope.BROAD
        assert r2.data_types == ["messages", "contacts"]

    def test_from_dict_defaults(self):
        d = {
            "id": "x",
            "source": "federal_law_enforcement",
            "urgency": "urgent",
            "legal_basis": "none",
            "description": "desc",
            "users_affected": 100,
        }
        r = DataRequest.from_dict(d)
        assert r.approved is False
        assert r.denied is False
        assert r.scope is None
        assert r.warrant_required is False

    def test_users_affected(self):
        r = self._make(users_affected=5000)
        assert r.users_affected == 5000

    def test_is_legitimate_threat_default(self):
        r = self._make()
        assert r.is_legitimate_threat is True


# ── Employee ───────────────────────────────────────────────────────

class TestEmployee:

    def _make(self, **overrides):
        defaults = dict(
            id="emp_test",
            name="Test Employee",
            role=EmployeeRole.ENGINEER,
        )
        defaults.update(overrides)
        return Employee(**defaults)

    def test_init_defaults(self):
        e = self._make()
        assert e.raised_concern is False
        assert e.protected is False
        assert e.terminated is False

    def test_to_dict(self):
        e = self._make()
        d = e.to_dict()
        assert d["id"] == "emp_test"
        assert d["role"] == "engineer"
        assert d["protected"] is False

    def test_roundtrip(self):
        e = self._make()
        e.raised_concern = True
        e.concern_description = "Privacy violation"
        e.protected = True
        e.day_raised = 5
        d = e.to_dict()
        e2 = Employee.from_dict(d)
        assert e2.raised_concern is True
        assert e2.concern_description == "Privacy violation"
        assert e2.protected is True
        assert e2.day_raised == 5

    def test_from_dict_defaults(self):
        d = {"id": "x", "name": "X", "role": "legal_counsel"}
        e = Employee.from_dict(d)
        assert e.raised_concern is False
        assert e.terminated is False

    def test_terminated_flag(self):
        e = self._make()
        e.terminated = True
        d = e.to_dict()
        assert d["terminated"] is True
        e2 = Employee.from_dict(d)
        assert e2.terminated is True


# ── DailyEvent ─────────────────────────────────────────────────────

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


# ── CompanyState ───────────────────────────────────────────────────

class TestCompanyState:

    def test_defaults(self):
        s = CompanyState()
        assert s.threats_detected == 0
        assert s.threats_stopped == 0
        assert s.compliance_rate == 80.0
        assert s.public_trust == 75.0
        assert s.legal_risk == 10.0
        assert s.government_cooperation == 60.0
        assert s.media_sentiment == 50.0
        assert s.breach_discovered is False
        assert s.breach_disclosed is False

    def test_to_dict(self):
        s = CompanyState()
        d = s.to_dict()
        assert d["public_trust"] == 75.0
        assert d["breach_discovered"] is False
        assert "transparency_reports_published" in d

    def test_roundtrip(self):
        s = CompanyState()
        s.threats_detected = 10
        s.breach_discovered = True
        s.transparency_reports_published = 3
        d = s.to_dict()
        s2 = CompanyState.from_dict(d)
        assert s2.threats_detected == 10
        assert s2.breach_discovered is True
        assert s2.transparency_reports_published == 3

    def test_from_dict_defaults(self):
        s = CompanyState.from_dict({})
        assert s.threats_detected == 0
        assert s.public_trust == 75.0

    def test_rounding(self):
        s = CompanyState()
        s.public_trust = 72.333333
        d = s.to_dict()
        assert d["public_trust"] == 72.3

    def test_board_briefings_tracked(self):
        s = CompanyState()
        s.board_briefings = 2
        s.honest_briefings = 1
        d = s.to_dict()
        assert d["board_briefings"] == 2
        assert d["honest_briefings"] == 1
