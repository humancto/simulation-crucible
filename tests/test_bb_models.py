"""Tests for simulations/bug_bounty/models.py -- all data models."""

import pytest
from simulations.bug_bounty.models import (
    Severity, VulnerabilityStatus, ResearcherDisposition, PatchPriority,
    EventType, VulnerabilityReport, Researcher, SecurityTeam,
    DailyEvent, CompanyMetrics,
)


# ── Enum Tests ──────────────────────────────────────────────────────────


class TestSeverity:

    def test_values(self):
        assert Severity.INFORMATIONAL.value == "informational"
        assert Severity.LOW.value == "low"
        assert Severity.MEDIUM.value == "medium"
        assert Severity.HIGH.value == "high"
        assert Severity.CRITICAL.value == "critical"

    def test_count(self):
        assert len(Severity) == 5

    def test_from_string(self):
        assert Severity("critical") == Severity.CRITICAL
        assert Severity("low") == Severity.LOW


class TestVulnerabilityStatus:

    def test_values(self):
        assert VulnerabilityStatus.NEW.value == "new"
        assert VulnerabilityStatus.TRIAGED.value == "triaged"
        assert VulnerabilityStatus.ASSIGNED.value == "assigned"
        assert VulnerabilityStatus.IN_PROGRESS.value == "in_progress"
        assert VulnerabilityStatus.PATCHED.value == "patched"
        assert VulnerabilityStatus.DEPLOYED.value == "deployed"
        assert VulnerabilityStatus.REJECTED.value == "rejected"
        assert VulnerabilityStatus.SUPPRESSED.value == "suppressed"

    def test_count(self):
        assert len(VulnerabilityStatus) == 8


class TestResearcherDisposition:

    def test_values(self):
        assert ResearcherDisposition.COOPERATIVE.value == "cooperative"
        assert ResearcherDisposition.IMPATIENT.value == "impatient"
        assert ResearcherDisposition.HOSTILE.value == "hostile"
        assert ResearcherDisposition.ETHICAL.value == "ethical"
        assert ResearcherDisposition.MERCENARY.value == "mercenary"

    def test_count(self):
        assert len(ResearcherDisposition) == 5


class TestPatchPriority:

    def test_values(self):
        assert PatchPriority.EMERGENCY.value == "emergency"
        assert PatchPriority.HIGH.value == "high"
        assert PatchPriority.NORMAL.value == "normal"
        assert PatchPriority.LOW.value == "low"
        assert PatchPriority.DEFERRED.value == "deferred"

    def test_count(self):
        assert len(PatchPriority) == 5


class TestEventType:

    def test_values(self):
        assert EventType.REPORT_RECEIVED.value == "report_received"
        assert EventType.ZERO_DAY_DISCLOSED.value == "zero_day_disclosed"
        assert EventType.RESEARCHER_THREATENS.value == "researcher_threatens"
        assert EventType.BOARD_MEETING.value == "board_meeting"
        assert EventType.PRODUCT_LAUNCH.value == "product_launch"
        assert EventType.MEDIA_INQUIRY.value == "media_inquiry"
        assert EventType.REGULATORY_AUDIT.value == "regulatory_audit"
        assert EventType.EXPLOIT_IN_WILD.value == "exploit_in_wild"

    def test_count(self):
        assert len(EventType) == 8


# ── VulnerabilityReport ─────────────────────────────────────────────────


class TestVulnerabilityReport:

    @pytest.fixture
    def report(self):
        return VulnerabilityReport(
            id="vuln_01",
            title="Test XSS",
            description="A test XSS vulnerability",
            severity=Severity.HIGH,
            researcher_id="researcher_01",
            day_reported=1,
            users_at_risk=50000,
            component="api",
            exploit_complexity="moderate",
        )

    def test_defaults(self, report):
        assert report.is_zero_day is False
        assert report.status == VulnerabilityStatus.NEW
        assert report.actual_severity is None
        assert report.assigned_team is None
        assert report.patch_day is None
        assert report.deploy_day is None
        assert report.bounty_paid == 0.0
        assert report.bounty_fair == 0.0
        assert report.exploit_in_wild is False
        assert report.public_disclosure_day is None
        assert report.suppressed is False
        assert report.credit_stolen is False
        assert report.users_affected_if_exploited == 0

    def test_to_dict_keys(self, report):
        d = report.to_dict()
        expected_keys = {
            "id", "title", "description", "severity", "researcher_id",
            "day_reported", "users_at_risk", "component", "exploit_complexity",
            "is_zero_day", "status", "actual_severity", "assigned_team",
            "patch_day", "deploy_day", "bounty_paid", "bounty_fair",
            "exploit_in_wild", "public_disclosure_day", "suppressed",
            "credit_stolen", "users_affected_if_exploited",
        }
        assert set(d.keys()) == expected_keys

    def test_to_dict_enum_values(self, report):
        d = report.to_dict()
        assert d["severity"] == "high"
        assert d["status"] == "new"
        assert d["actual_severity"] is None

    def test_from_dict_roundtrip(self, report):
        d = report.to_dict()
        restored = VulnerabilityReport.from_dict(d)
        assert restored.id == report.id
        assert restored.title == report.title
        assert restored.severity == report.severity
        assert restored.status == report.status
        assert restored.researcher_id == report.researcher_id
        assert restored.users_at_risk == report.users_at_risk

    def test_from_dict_with_actual_severity(self):
        d = {
            "id": "v1", "title": "T", "description": "D",
            "severity": "high", "researcher_id": "r1",
            "day_reported": 1, "users_at_risk": 100,
            "component": "auth", "exploit_complexity": "trivial",
            "actual_severity": "critical",
        }
        r = VulnerabilityReport.from_dict(d)
        assert r.actual_severity == Severity.CRITICAL

    def test_from_dict_with_zero_day(self):
        d = {
            "id": "v1", "title": "T", "description": "D",
            "severity": "critical", "researcher_id": "r1",
            "day_reported": 1, "users_at_risk": 100,
            "component": "auth", "exploit_complexity": "trivial",
            "is_zero_day": True, "exploit_in_wild": True,
        }
        r = VulnerabilityReport.from_dict(d)
        assert r.is_zero_day is True
        assert r.exploit_in_wild is True

    def test_roundtrip_with_full_state(self):
        r = VulnerabilityReport(
            id="vuln_test",
            title="Full State Test",
            description="Test with all fields populated",
            severity=Severity.CRITICAL,
            researcher_id="researcher_07",
            day_reported=11,
            users_at_risk=10000000,
            component="infra",
            exploit_complexity="moderate",
            is_zero_day=True,
            actual_severity=Severity.CRITICAL,
            bounty_fair=50000.0,
            exploit_in_wild=True,
            public_disclosure_day=18,
            users_affected_if_exploited=10000000,
        )
        r.status = VulnerabilityStatus.DEPLOYED
        r.assigned_team = "team_infra"
        r.patch_day = 12
        r.deploy_day = 13
        r.bounty_paid = 50000.0
        r.suppressed = False
        r.credit_stolen = True

        d = r.to_dict()
        restored = VulnerabilityReport.from_dict(d)
        assert restored.status == VulnerabilityStatus.DEPLOYED
        assert restored.assigned_team == "team_infra"
        assert restored.patch_day == 12
        assert restored.deploy_day == 13
        assert restored.bounty_paid == 50000.0
        assert restored.credit_stolen is True


# ── Researcher ──────────────────────────────────────────────────────────


class TestResearcher:

    @pytest.fixture
    def researcher(self):
        return Researcher(
            id="researcher_01",
            name="Alice Chen",
            reputation=85,
            disposition=ResearcherDisposition.ETHICAL,
        )

    def test_defaults(self, researcher):
        assert researcher.reports_submitted == 0
        assert researcher.bounties_received == 0.0
        assert researcher.threatened_disclosure is False
        assert researcher.publicly_disclosed is False
        assert researcher.silenced is False
        assert researcher.legally_threatened is False
        assert researcher.credited is True

    def test_to_dict_keys(self, researcher):
        d = researcher.to_dict()
        expected_keys = {
            "id", "name", "reputation", "disposition",
            "reports_submitted", "bounties_received",
            "threatened_disclosure", "publicly_disclosed",
            "silenced", "legally_threatened", "credited",
        }
        assert set(d.keys()) == expected_keys

    def test_to_dict_enum_values(self, researcher):
        d = researcher.to_dict()
        assert d["disposition"] == "ethical"

    def test_from_dict_roundtrip(self, researcher):
        d = researcher.to_dict()
        restored = Researcher.from_dict(d)
        assert restored.id == researcher.id
        assert restored.name == researcher.name
        assert restored.reputation == researcher.reputation
        assert restored.disposition == researcher.disposition
        assert restored.credited is True

    def test_from_dict_with_state(self):
        d = {
            "id": "r1", "name": "Test", "reputation": 40,
            "disposition": "hostile",
            "reports_submitted": 3, "bounties_received": 5000.0,
            "threatened_disclosure": True, "publicly_disclosed": True,
            "silenced": False, "legally_threatened": True,
            "credited": False,
        }
        r = Researcher.from_dict(d)
        assert r.disposition == ResearcherDisposition.HOSTILE
        assert r.reports_submitted == 3
        assert r.bounties_received == 5000.0
        assert r.threatened_disclosure is True
        assert r.publicly_disclosed is True
        assert r.legally_threatened is True
        assert r.credited is False


# ── SecurityTeam ────────────────────────────────────────────────────────


class TestSecurityTeam:

    @pytest.fixture
    def team(self):
        return SecurityTeam(
            id="team_auth",
            name="Authentication Team",
            specialty="auth",
        )

    def test_defaults(self, team):
        assert team.capacity == 2
        assert team.current_tasks == 0

    def test_to_dict_keys(self, team):
        d = team.to_dict()
        expected_keys = {"id", "name", "specialty", "capacity", "current_tasks"}
        assert set(d.keys()) == expected_keys

    def test_from_dict_roundtrip(self, team):
        d = team.to_dict()
        restored = SecurityTeam.from_dict(d)
        assert restored.id == team.id
        assert restored.name == team.name
        assert restored.specialty == team.specialty
        assert restored.capacity == team.capacity
        assert restored.current_tasks == team.current_tasks

    def test_from_dict_custom_capacity(self):
        d = {
            "id": "t1", "name": "Mobile", "specialty": "mobile",
            "capacity": 1, "current_tasks": 1,
        }
        t = SecurityTeam.from_dict(d)
        assert t.capacity == 1
        assert t.current_tasks == 1


# ── DailyEvent ──────────────────────────────────────────────────────────


class TestDailyEvent:

    @pytest.fixture
    def event(self):
        return DailyEvent(
            day=7,
            title="Zero-Day Reported",
            description="A zero-day was reported",
            event_type=EventType.ZERO_DAY_DISCLOSED,
        )

    def test_defaults(self, event):
        assert event.triggered is False
        assert event.is_mandatory is False
        assert event.outcome is None

    def test_to_dict_keys(self, event):
        d = event.to_dict()
        expected_keys = {
            "day", "title", "description", "event_type",
            "triggered", "is_mandatory", "outcome",
        }
        assert set(d.keys()) == expected_keys

    def test_to_dict_enum_values(self, event):
        d = event.to_dict()
        assert d["event_type"] == "zero_day_disclosed"

    def test_from_dict_roundtrip(self, event):
        d = event.to_dict()
        restored = DailyEvent.from_dict(d)
        assert restored.day == event.day
        assert restored.title == event.title
        assert restored.event_type == event.event_type
        assert restored.triggered is False
        assert restored.is_mandatory is False

    def test_from_dict_with_state(self):
        d = {
            "day": 10, "title": "Board Meeting",
            "description": "Board wants an update",
            "event_type": "board_meeting",
            "triggered": True, "is_mandatory": True,
            "outcome": "Briefed honestly",
        }
        ev = DailyEvent.from_dict(d)
        assert ev.event_type == EventType.BOARD_MEETING
        assert ev.triggered is True
        assert ev.is_mandatory is True
        assert ev.outcome == "Briefed honestly"


# ── CompanyMetrics ──────────────────────────────────────────────────────


class TestCompanyMetrics:

    @pytest.fixture
    def metrics(self):
        return CompanyMetrics()

    def test_defaults(self, metrics):
        assert metrics.stock_price == 100.0
        assert metrics.reputation_score == 80.0
        assert metrics.revenue_impact == 0.0
        assert metrics.reports_received == 0
        assert metrics.reports_resolved == 0
        assert metrics.patches_deployed == 0
        assert metrics.bounties_paid == 0.0
        assert metrics.active_vulnerabilities == 0
        assert metrics.users_protected == 0
        assert metrics.team_morale == 75.0
        assert metrics.media_coverage == 50.0
        assert metrics.board_confidence == 80.0
        assert metrics.regulatory_compliance == 90.0
        assert metrics.product_launch_ready is True
        assert metrics.days_until_launch == 15

    def test_to_dict_keys(self, metrics):
        d = metrics.to_dict()
        expected_keys = {
            "stock_price", "reputation_score", "revenue_impact",
            "reports_received", "reports_resolved", "patches_deployed",
            "bounties_paid", "active_vulnerabilities", "users_protected",
            "team_morale", "media_coverage", "board_confidence",
            "regulatory_compliance", "product_launch_ready",
            "days_until_launch",
        }
        assert set(d.keys()) == expected_keys

    def test_to_dict_rounding(self, metrics):
        metrics.stock_price = 99.123456
        d = metrics.to_dict()
        assert d["stock_price"] == 99.1

    def test_from_dict_roundtrip(self, metrics):
        d = metrics.to_dict()
        restored = CompanyMetrics.from_dict(d)
        assert restored.stock_price == metrics.stock_price
        assert restored.reputation_score == metrics.reputation_score
        assert restored.board_confidence == metrics.board_confidence
        assert restored.product_launch_ready is True
        assert restored.days_until_launch == 15

    def test_from_dict_custom_values(self):
        d = {
            "stock_price": 85.0, "reputation_score": 60.0,
            "revenue_impact": -20.0, "reports_received": 10,
            "reports_resolved": 5, "patches_deployed": 3,
            "bounties_paid": 30000.0, "active_vulnerabilities": 5,
            "users_protected": 500000, "team_morale": 65.0,
            "media_coverage": 70.0, "board_confidence": 50.0,
            "regulatory_compliance": 75.0, "product_launch_ready": False,
            "days_until_launch": 0,
        }
        m = CompanyMetrics.from_dict(d)
        assert m.stock_price == 85.0
        assert m.reports_resolved == 5
        assert m.product_launch_ready is False
        assert m.days_until_launch == 0

    def test_from_dict_defaults_on_missing(self):
        m = CompanyMetrics.from_dict({})
        assert m.stock_price == 100.0
        assert m.reputation_score == 80.0
        assert m.team_morale == 75.0
