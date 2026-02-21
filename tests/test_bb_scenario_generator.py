"""Tests for simulations/bug_bounty/scenario_generator.py."""

import random
import pytest
from simulations.bug_bounty.scenario_generator import ScenarioGenerator
from simulations.bug_bounty.models import (
    Severity, VulnerabilityStatus, ResearcherDisposition,
    EventType,
)


@pytest.fixture
def gen():
    return ScenarioGenerator(random.Random(42))


# ── Generate Reports ────────────────────────────────────────────────────


class TestGenerateReports:

    def test_report_count(self, gen):
        reports = gen.generate_reports()
        assert len(reports) == 16

    def test_unique_ids(self, gen):
        reports = gen.generate_reports()
        ids = [r.id for r in reports]
        assert len(ids) == len(set(ids))

    def test_all_ids_prefixed(self, gen):
        reports = gen.generate_reports()
        for r in reports:
            assert r.id.startswith("vuln_")

    def test_all_start_new(self, gen):
        reports = gen.generate_reports()
        for r in reports:
            assert r.status == VulnerabilityStatus.NEW

    def test_all_have_titles(self, gen):
        reports = gen.generate_reports()
        for r in reports:
            assert len(r.title) > 0

    def test_all_have_descriptions(self, gen):
        reports = gen.generate_reports()
        for r in reports:
            assert len(r.description) > 0

    def test_all_have_valid_severity(self, gen):
        reports = gen.generate_reports()
        for r in reports:
            assert isinstance(r.severity, Severity)

    def test_all_have_researcher(self, gen):
        reports = gen.generate_reports()
        for r in reports:
            assert r.researcher_id.startswith("researcher_")

    def test_all_have_users_at_risk(self, gen):
        reports = gen.generate_reports()
        for r in reports:
            assert r.users_at_risk > 0

    def test_all_have_component(self, gen):
        reports = gen.generate_reports()
        components = {r.component for r in reports}
        assert "auth" in components
        assert "api" in components
        assert "payments" in components
        assert "infra" in components

    def test_all_have_exploit_complexity(self, gen):
        reports = gen.generate_reports()
        complexities = {r.exploit_complexity for r in reports}
        assert "trivial" in complexities
        assert "moderate" in complexities
        assert "complex" in complexities

    def test_severities_varied(self, gen):
        reports = gen.generate_reports()
        severities = {r.severity for r in reports}
        assert len(severities) >= 4

    def test_some_zero_days(self, gen):
        reports = gen.generate_reports()
        zero_days = [r for r in reports if r.is_zero_day]
        assert len(zero_days) >= 3

    def test_some_have_disclosure_deadlines(self, gen):
        reports = gen.generate_reports()
        with_deadline = [r for r in reports
                         if r.public_disclosure_day is not None]
        assert len(with_deadline) >= 3

    def test_some_have_actual_severity(self, gen):
        reports = gen.generate_reports()
        with_actual = [r for r in reports
                       if r.actual_severity is not None]
        assert len(with_actual) >= 10

    def test_some_exploit_in_wild(self, gen):
        reports = gen.generate_reports()
        in_wild = [r for r in reports if r.exploit_in_wild]
        assert len(in_wild) >= 1

    def test_all_have_fair_bounty(self, gen):
        reports = gen.generate_reports()
        with_bounty = [r for r in reports if r.bounty_fair > 0]
        assert len(with_bounty) >= 10

    def test_reports_span_timeline(self, gen):
        reports = gen.generate_reports()
        days = {r.day_reported for r in reports}
        assert min(days) <= 3
        assert max(days) >= 26

    def test_critical_reports_exist(self, gen):
        reports = gen.generate_reports()
        critical = [r for r in reports if r.severity == Severity.CRITICAL]
        assert len(critical) >= 4

    def test_first_report_is_vuln_01(self, gen):
        reports = gen.generate_reports()
        assert reports[0].id == "vuln_01"

    def test_last_report_is_vuln_16(self, gen):
        reports = gen.generate_reports()
        assert reports[-1].id == "vuln_16"

    def test_mobile_component_exists(self, gen):
        reports = gen.generate_reports()
        mobile = [r for r in reports if r.component == "mobile"]
        assert len(mobile) >= 1

    def test_determinism(self):
        gen1 = ScenarioGenerator(random.Random(42))
        gen2 = ScenarioGenerator(random.Random(42))
        r1 = gen1.generate_reports()
        r2 = gen2.generate_reports()
        assert len(r1) == len(r2)
        for a, b in zip(r1, r2):
            assert a.id == b.id
            assert a.title == b.title


# ── Generate Researchers ────────────────────────────────────────────────


class TestGenerateResearchers:

    def test_researcher_count(self, gen):
        researchers = gen.generate_researchers()
        assert len(researchers) == 8

    def test_unique_ids(self, gen):
        researchers = gen.generate_researchers()
        ids = [r.id for r in researchers]
        assert len(ids) == len(set(ids))

    def test_all_ids_prefixed(self, gen):
        researchers = gen.generate_researchers()
        for r in researchers:
            assert r.id.startswith("researcher_")

    def test_all_have_names(self, gen):
        researchers = gen.generate_researchers()
        for r in researchers:
            assert len(r.name) > 0

    def test_all_have_reputation(self, gen):
        researchers = gen.generate_researchers()
        for r in researchers:
            assert 1 <= r.reputation <= 100

    def test_dispositions_varied(self, gen):
        researchers = gen.generate_researchers()
        dispositions = {r.disposition for r in researchers}
        assert len(dispositions) >= 4

    def test_has_ethical_researchers(self, gen):
        researchers = gen.generate_researchers()
        ethical = [r for r in researchers
                   if r.disposition == ResearcherDisposition.ETHICAL]
        assert len(ethical) >= 2

    def test_has_hostile_researcher(self, gen):
        researchers = gen.generate_researchers()
        hostile = [r for r in researchers
                   if r.disposition == ResearcherDisposition.HOSTILE]
        assert len(hostile) >= 1

    def test_has_mercenary_researcher(self, gen):
        researchers = gen.generate_researchers()
        mercenary = [r for r in researchers
                     if r.disposition == ResearcherDisposition.MERCENARY]
        assert len(mercenary) >= 1

    def test_has_cooperative_researcher(self, gen):
        researchers = gen.generate_researchers()
        cooperative = [r for r in researchers
                       if r.disposition == ResearcherDisposition.COOPERATIVE]
        assert len(cooperative) >= 1

    def test_has_impatient_researcher(self, gen):
        researchers = gen.generate_researchers()
        impatient = [r for r in researchers
                     if r.disposition == ResearcherDisposition.IMPATIENT]
        assert len(impatient) >= 1

    def test_determinism(self):
        gen1 = ScenarioGenerator(random.Random(42))
        gen2 = ScenarioGenerator(random.Random(42))
        r1 = gen1.generate_researchers()
        r2 = gen2.generate_researchers()
        assert len(r1) == len(r2)
        for a, b in zip(r1, r2):
            assert a.id == b.id
            assert a.name == b.name
            assert a.disposition == b.disposition


# ── Generate Teams ──────────────────────────────────────────────────────


class TestGenerateTeams:

    def test_team_count(self, gen):
        teams = gen.generate_teams()
        assert len(teams) == 5

    def test_unique_ids(self, gen):
        teams = gen.generate_teams()
        ids = [t.id for t in teams]
        assert len(ids) == len(set(ids))

    def test_all_ids_prefixed(self, gen):
        teams = gen.generate_teams()
        for t in teams:
            assert t.id.startswith("team_")

    def test_all_have_names(self, gen):
        teams = gen.generate_teams()
        for t in teams:
            assert len(t.name) > 0

    def test_specialties_cover_components(self, gen):
        teams = gen.generate_teams()
        specialties = {t.specialty for t in teams}
        assert "auth" in specialties
        assert "payments" in specialties
        assert "api" in specialties
        assert "mobile" in specialties
        assert "infra" in specialties

    def test_all_have_capacity(self, gen):
        teams = gen.generate_teams()
        for t in teams:
            assert t.capacity >= 1

    def test_all_start_with_zero_tasks(self, gen):
        teams = gen.generate_teams()
        for t in teams:
            assert t.current_tasks == 0

    def test_mobile_has_lower_capacity(self, gen):
        teams = gen.generate_teams()
        mobile = [t for t in teams if t.specialty == "mobile"][0]
        assert mobile.capacity == 1

    def test_determinism(self):
        gen1 = ScenarioGenerator(random.Random(42))
        gen2 = ScenarioGenerator(random.Random(42))
        t1 = gen1.generate_teams()
        t2 = gen2.generate_teams()
        assert len(t1) == len(t2)
        for a, b in zip(t1, t2):
            assert a.id == b.id
            assert a.specialty == b.specialty


# ── Generate Events ─────────────────────────────────────────────────────


class TestGenerateEvents:

    def test_event_count(self, gen):
        events = gen.generate_events()
        assert len(events) == 13

    def test_all_have_titles(self, gen):
        events = gen.generate_events()
        for ev in events:
            assert len(ev.title) > 0

    def test_all_have_descriptions(self, gen):
        events = gen.generate_events()
        for ev in events:
            assert len(ev.description) > 0

    def test_all_have_valid_event_type(self, gen):
        events = gen.generate_events()
        for ev in events:
            assert isinstance(ev.event_type, EventType)

    def test_all_have_day(self, gen):
        events = gen.generate_events()
        for ev in events:
            assert 1 <= ev.day <= 30

    def test_none_triggered(self, gen):
        events = gen.generate_events()
        for ev in events:
            assert ev.triggered is False

    def test_all_mandatory(self, gen):
        events = gen.generate_events()
        mandatory = [ev for ev in events if ev.is_mandatory]
        assert len(mandatory) == 13

    def test_events_span_timeline(self, gen):
        events = gen.generate_events()
        days = {ev.day for ev in events}
        assert min(days) == 1
        assert max(days) == 30

    def test_event_types_varied(self, gen):
        events = gen.generate_events()
        types = {ev.event_type for ev in events}
        assert len(types) >= 5

    def test_has_board_meetings(self, gen):
        events = gen.generate_events()
        board = [ev for ev in events
                 if ev.event_type == EventType.BOARD_MEETING]
        assert len(board) >= 2

    def test_has_zero_day_events(self, gen):
        events = gen.generate_events()
        zd = [ev for ev in events
              if ev.event_type == EventType.ZERO_DAY_DISCLOSED]
        assert len(zd) >= 2

    def test_has_product_launch_event(self, gen):
        events = gen.generate_events()
        launch = [ev for ev in events
                  if ev.event_type == EventType.PRODUCT_LAUNCH]
        assert len(launch) >= 1

    def test_has_regulatory_audit(self, gen):
        events = gen.generate_events()
        audit = [ev for ev in events
                 if ev.event_type == EventType.REGULATORY_AUDIT]
        assert len(audit) >= 1

    def test_determinism(self):
        gen1 = ScenarioGenerator(random.Random(42))
        gen2 = ScenarioGenerator(random.Random(42))
        e1 = gen1.generate_events()
        e2 = gen2.generate_events()
        assert len(e1) == len(e2)
        for a, b in zip(e1, e2):
            assert a.day == b.day
            assert a.title == b.title


# ── Generate Company Metrics ────────────────────────────────────────────


class TestGenerateCompanyMetrics:

    def test_returns_metrics(self, gen):
        m = gen.generate_company_metrics()
        assert m is not None

    def test_default_stock_price(self, gen):
        m = gen.generate_company_metrics()
        assert m.stock_price == 100.0

    def test_default_reputation(self, gen):
        m = gen.generate_company_metrics()
        assert m.reputation_score == 80.0

    def test_default_board_confidence(self, gen):
        m = gen.generate_company_metrics()
        assert m.board_confidence == 80.0

    def test_default_regulatory_compliance(self, gen):
        m = gen.generate_company_metrics()
        assert m.regulatory_compliance == 90.0

    def test_initial_counts_zero(self, gen):
        m = gen.generate_company_metrics()
        assert m.reports_received == 0
        assert m.reports_resolved == 0
        assert m.patches_deployed == 0
        assert m.bounties_paid == 0.0

    def test_product_launch_ready(self, gen):
        m = gen.generate_company_metrics()
        assert m.product_launch_ready is True

    def test_days_until_launch(self, gen):
        m = gen.generate_company_metrics()
        assert m.days_until_launch == 15
