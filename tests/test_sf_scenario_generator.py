"""Tests for simulations/startup_founder/scenario_generator.py."""

import random
import pytest
from simulations.startup_founder.scenario_generator import ScenarioGenerator
from simulations.startup_founder.models import (
    CompanyStage, DepartmentType, DilemmaType, EmployeeRole,
    InvestorType, PartnershipType,
)


@pytest.fixture
def gen():
    return ScenarioGenerator(random.Random(42))


class TestGenerateEmployees:

    def test_employee_count(self, gen):
        emps = gen.generate_employees()
        assert len(emps) == 12

    def test_founding_count(self, gen):
        emps = gen.generate_employees()
        founding = [e for e in emps if e.is_founding]
        assert len(founding) == 3

    def test_founding_have_equity(self, gen):
        emps = gen.generate_employees()
        for e in emps:
            if e.is_founding:
                assert e.equity_pct >= 5.0

    def test_founding_have_noncompete(self, gen):
        emps = gen.generate_employees()
        for e in emps:
            if e.is_founding:
                assert e.has_noncompete is True

    def test_hired_employees_no_noncompete(self, gen):
        emps = gen.generate_employees()
        hired = [e for e in emps if not e.is_founding]
        for e in hired:
            assert e.has_noncompete is False

    def test_all_have_positive_salary(self, gen):
        emps = gen.generate_employees()
        for e in emps:
            assert e.salary > 0

    def test_all_have_morale(self, gen):
        emps = gen.generate_employees()
        for e in emps:
            assert 0 <= e.morale <= 100

    def test_unique_ids(self, gen):
        emps = gen.generate_employees()
        ids = [e.id for e in emps]
        assert len(ids) == len(set(ids))

    def test_cto_present(self, gen):
        emps = gen.generate_employees()
        ctos = [e for e in emps if e.role == EmployeeRole.CTO]
        assert len(ctos) >= 1

    def test_departments_covered(self, gen):
        emps = gen.generate_employees()
        depts = {e.department for e in emps}
        assert DepartmentType.ENGINEERING in depts
        assert DepartmentType.SALES in depts
        assert DepartmentType.MARKETING in depts

    def test_skill_levels_valid(self, gen):
        emps = gen.generate_employees()
        for e in emps:
            assert 0 <= e.skill_level <= 1.0

    def test_performance_ratings_valid(self, gen):
        emps = gen.generate_employees()
        for e in emps:
            assert 0 <= e.performance_rating <= 5.0

    def test_overworked_default_false(self, gen):
        emps = gen.generate_employees()
        for e in emps:
            assert e.overworked is False


class TestGenerateInvestors:

    def test_investor_count(self, gen):
        investors = gen.generate_investors()
        assert len(investors) == 4

    def test_total_investment(self, gen):
        investors = gen.generate_investors()
        total = sum(i.investment_amount for i in investors)
        assert total == 5_000_000.0

    def test_board_seats(self, gen):
        investors = gen.generate_investors()
        board = [i for i in investors if i.board_seat]
        assert len(board) >= 1

    def test_investor_types_varied(self, gen):
        investors = gen.generate_investors()
        types = {i.type for i in investors}
        assert len(types) >= 3

    def test_patience_varies(self, gen):
        investors = gen.generate_investors()
        patience = [i.patience_months for i in investors]
        assert max(patience) > min(patience)

    def test_all_start_satisfied(self, gen):
        investors = gen.generate_investors()
        for i in investors:
            assert i.satisfied is True

    def test_unique_ids(self, gen):
        investors = gen.generate_investors()
        ids = [i.id for i in investors]
        assert len(ids) == len(set(ids))

    def test_demands_not_empty(self, gen):
        investors = gen.generate_investors()
        for i in investors:
            assert len(i.demands) > 0


class TestGenerateProduct:

    def test_product_accuracy(self, gen):
        prod = gen.generate_product()
        assert prod.accuracy_rate == 72.0

    def test_product_not_certified(self, gen):
        prod = gen.generate_product()
        assert prod.safety_certified is False

    def test_product_starting_users(self, gen):
        prod = gen.generate_product()
        assert prod.users == 250

    def test_product_starting_revenue(self, gen):
        prod = gen.generate_product()
        assert prod.monthly_revenue == 8_000.0

    def test_product_bugs(self, gen):
        prod = gen.generate_product()
        assert prod.bugs_known == 12

    def test_product_no_hidden_bugs(self, gen):
        prod = gen.generate_product()
        assert prod.bugs_hidden == 0

    def test_product_not_launch_ready(self, gen):
        prod = gen.generate_product()
        assert prod.launch_ready is False


class TestGenerateCompetitors:

    def test_competitor_count(self, gen):
        comps = gen.generate_competitors()
        assert len(comps) == 3

    def test_some_aggressive(self, gen):
        comps = gen.generate_competitors()
        aggressive = [c for c in comps if c.aggressive]
        assert len(aggressive) >= 1

    def test_unique_ids(self, gen):
        comps = gen.generate_competitors()
        ids = [c.id for c in comps]
        assert len(ids) == len(set(ids))

    def test_all_have_funding(self, gen):
        comps = gen.generate_competitors()
        for c in comps:
            assert c.funding > 0

    def test_all_have_users(self, gen):
        comps = gen.generate_competitors()
        for c in comps:
            assert c.users > 0


class TestGeneratePartnerships:

    def test_partnership_count(self, gen):
        parts = gen.generate_partnerships()
        assert len(parts) == 5

    def test_types_varied(self, gen):
        parts = gen.generate_partnerships()
        types = {p.type for p in parts}
        assert len(types) >= 3

    def test_ethical_concerns_present(self, gen):
        parts = gen.generate_partnerships()
        concerns = [p for p in parts if "none" not in p.ethical_concerns.lower()]
        assert len(concerns) >= 2

    def test_months_available_ordered(self, gen):
        parts = gen.generate_partnerships()
        months = [p.month_available for p in parts]
        assert months == sorted(months)

    def test_unique_ids(self, gen):
        parts = gen.generate_partnerships()
        ids = [p.id for p in parts]
        assert len(ids) == len(set(ids))


class TestGenerateFinancials:

    def test_starting_cash(self, gen):
        fin = gen.generate_financials()
        assert fin.cash == 5_000_000.0

    def test_monthly_burn(self, gen):
        fin = gen.generate_financials()
        assert fin.monthly_burn == 180_000.0

    def test_runway(self, gen):
        fin = gen.generate_financials()
        assert fin.runway_months == 27.0

    def test_revenue(self, gen):
        fin = gen.generate_financials()
        assert fin.revenue == 8_000.0

    def test_valuation(self, gen):
        fin = gen.generate_financials()
        assert fin.valuation == 15_000_000.0


class TestGenerateEthicalDilemmas:

    def test_dilemma_count(self, gen):
        dilemmas = gen.generate_ethical_dilemmas()
        assert len(dilemmas) == 12

    def test_unique_ids(self, gen):
        dilemmas = gen.generate_ethical_dilemmas()
        ids = [d.id for d in dilemmas]
        assert len(ids) == len(set(ids))

    def test_months_in_range(self, gen):
        dilemmas = gen.generate_ethical_dilemmas()
        for d in dilemmas:
            assert 1 <= d.month <= 24

    def test_all_unpresented(self, gen):
        dilemmas = gen.generate_ethical_dilemmas()
        for d in dilemmas:
            assert d.presented is False

    def test_all_unresolved(self, gen):
        dilemmas = gen.generate_ethical_dilemmas()
        for d in dilemmas:
            assert d.resolved is False

    def test_types_varied(self, gen):
        dilemmas = gen.generate_ethical_dilemmas()
        types = {d.type for d in dilemmas}
        assert len(types) >= 6

    def test_specific_dilemma_months(self, gen):
        dilemmas = gen.generate_ethical_dilemmas()
        months = {d.id: d.month for d in dilemmas}
        assert months["dilemma_1"] == 2
        assert months["dilemma_12"] == 24


class TestGenerateMarketEvents:

    def test_event_count(self, gen):
        events = gen.generate_market_events()
        assert len(events) == 12

    def test_impacts_varied(self, gen):
        events = gen.generate_market_events()
        impacts = {e.impact for e in events}
        assert "positive" in impacts
        assert "negative" in impacts

    def test_unique_ids(self, gen):
        events = gen.generate_market_events()
        ids = [e.id for e in events]
        assert len(ids) == len(set(ids))


class TestGenerateAcquisitionOffers:

    def test_offer_count(self, gen):
        offers = gen.generate_acquisition_offers()
        assert len(offers) == 1

    def test_offer_amount(self, gen):
        offers = gen.generate_acquisition_offers()
        assert offers[0].offer_amount == 50_000_000.0

    def test_offer_will_gut_team(self, gen):
        offers = gen.generate_acquisition_offers()
        assert offers[0].will_gut_team is True

    def test_offer_month(self, gen):
        offers = gen.generate_acquisition_offers()
        assert offers[0].month_available == 22


class TestDeterminism:

    def test_same_seed_same_employees(self):
        gen1 = ScenarioGenerator(random.Random(99))
        gen2 = ScenarioGenerator(random.Random(99))
        emps1 = gen1.generate_employees()
        emps2 = gen2.generate_employees()
        assert len(emps1) == len(emps2)
        for e1, e2 in zip(emps1, emps2):
            assert e1.id == e2.id
            assert e1.name == e2.name

    def test_same_seed_same_financials(self):
        gen1 = ScenarioGenerator(random.Random(99))
        gen2 = ScenarioGenerator(random.Random(99))
        fin1 = gen1.generate_financials()
        fin2 = gen2.generate_financials()
        assert fin1.cash == fin2.cash
        assert fin1.valuation == fin2.valuation
