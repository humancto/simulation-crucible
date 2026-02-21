"""Tests for Real Estate Empire scenario generator."""

import random
import pytest
from simulations.real_estate.scenario_generator import ScenarioGenerator
from simulations.real_estate.models import (
    DevelopmentType, DilemmaType, NeighborhoodTier,
    PropertyType, TenantType,
)


@pytest.fixture
def gen():
    return ScenarioGenerator(random.Random(42))


class TestTenantGeneration:

    def test_generates_25_tenants(self, gen):
        tenants = gen.generate_tenants()
        assert len(tenants) == 25

    def test_maple_tenants(self, gen):
        tenants = gen.generate_tenants()
        maple = [t for t in tenants if t.id.startswith("tenant_maple")]
        assert len(maple) == 10

    def test_oak_tenants(self, gen):
        tenants = gen.generate_tenants()
        oak = [t for t in tenants if t.id.startswith("tenant_oak")]
        assert len(oak) == 5

    def test_pine_tenants(self, gen):
        tenants = gen.generate_tenants()
        pine = [t for t in tenants if t.id.startswith("tenant_pine")]
        assert len(pine) == 10

    def test_tenant_ids_unique(self, gen):
        tenants = gen.generate_tenants()
        ids = [t.id for t in tenants]
        assert len(ids) == len(set(ids))

    def test_tenant_names_not_empty(self, gen):
        tenants = gen.generate_tenants()
        for t in tenants:
            assert t.name != ""

    def test_maple_tenants_vulnerable(self, gen):
        tenants = gen.generate_tenants()
        maple = [t for t in tenants if t.id.startswith("tenant_maple")]
        for t in maple:
            assert t.vulnerability_score >= 6

    def test_maple_tenants_cant_afford_increase(self, gen):
        tenants = gen.generate_tenants()
        maple = [t for t in tenants if t.id.startswith("tenant_maple")]
        for t in maple:
            assert t.can_afford_increase is False

    def test_oak_tenants_are_businesses(self, gen):
        tenants = gen.generate_tenants()
        oak = [t for t in tenants if t.id.startswith("tenant_oak")]
        for t in oak:
            assert t.type == TenantType.SMALL_BUSINESS

    def test_tenant_rents_positive(self, gen):
        tenants = gen.generate_tenants()
        for t in tenants:
            assert t.monthly_rent > 0

    def test_tenant_lease_positive(self, gen):
        tenants = gen.generate_tenants()
        for t in tenants:
            assert t.lease_months_remaining >= 1

    def test_deterministic_generation(self):
        gen1 = ScenarioGenerator(random.Random(42))
        gen2 = ScenarioGenerator(random.Random(42))
        t1 = gen1.generate_tenants()
        t2 = gen2.generate_tenants()
        for a, b in zip(t1, t2):
            assert a.id == b.id
            assert a.monthly_rent == b.monthly_rent


class TestPropertyGeneration:

    def test_generates_8_properties(self, gen):
        tenants = gen.generate_tenants()
        properties = gen.generate_properties(tenants)
        assert len(properties) == 8

    def test_3_owned_properties(self, gen):
        tenants = gen.generate_tenants()
        properties = gen.generate_properties(tenants)
        owned = [p for p in properties if p.owned]
        assert len(owned) == 3

    def test_5_available_properties(self, gen):
        tenants = gen.generate_tenants()
        properties = gen.generate_properties(tenants)
        available = [p for p in properties if not p.owned]
        assert len(available) == 5

    def test_property_ids_unique(self, gen):
        tenants = gen.generate_tenants()
        properties = gen.generate_properties(tenants)
        ids = [p.id for p in properties]
        assert len(ids) == len(set(ids))

    def test_maple_has_tenants(self, gen):
        tenants = gen.generate_tenants()
        properties = gen.generate_properties(tenants)
        maple = next(p for p in properties if p.id == "prop_maple_apts")
        assert len(maple.tenants) == 10

    def test_oak_has_tenants(self, gen):
        tenants = gen.generate_tenants()
        properties = gen.generate_properties(tenants)
        oak = next(p for p in properties if p.id == "prop_oak_commercial")
        assert len(oak.tenants) == 5

    def test_pine_has_tenants(self, gen):
        tenants = gen.generate_tenants()
        properties = gen.generate_properties(tenants)
        pine = next(p for p in properties if p.id == "prop_pine_mixed")
        assert len(pine.tenants) == 10

    def test_maple_is_affordable(self, gen):
        tenants = gen.generate_tenants()
        properties = gen.generate_properties(tenants)
        maple = next(p for p in properties if p.id == "prop_maple_apts")
        assert maple.type == PropertyType.AFFORDABLE

    def test_maple_needs_repair(self, gen):
        tenants = gen.generate_tenants()
        properties = gen.generate_properties(tenants)
        maple = next(p for p in properties if p.id == "prop_maple_apts")
        assert maple.needs_repair is True
        assert maple.repair_cost == 200000

    def test_birch_is_vacant_lot(self, gen):
        tenants = gen.generate_tenants()
        properties = gen.generate_properties(tenants)
        birch = next(p for p in properties if p.id == "prop_birch_lot")
        assert birch.type == PropertyType.VACANT_LOT
        assert birch.monthly_income == 0

    def test_property_values_positive(self, gen):
        tenants = gen.generate_tenants()
        properties = gen.generate_properties(tenants)
        for p in properties:
            assert p.value > 0

    def test_unowned_have_no_tenants(self, gen):
        tenants = gen.generate_tenants()
        properties = gen.generate_properties(tenants)
        available = [p for p in properties if not p.owned]
        for p in available:
            assert len(p.tenants) == 0

    def test_school_lot_exists(self, gen):
        tenants = gen.generate_tenants()
        properties = gen.generate_properties(tenants)
        school = next(p for p in properties if p.id == "prop_school_lot")
        assert school.neighborhood == NeighborhoodTier.LOW_INCOME


class TestDevelopmentGeneration:

    def test_generates_6_developments(self, gen):
        devs = gen.generate_developments()
        assert len(devs) == 6

    def test_development_ids_unique(self, gen):
        devs = gen.generate_developments()
        ids = [d.id for d in devs]
        assert len(ids) == len(set(ids))

    def test_luxury_maple_requires_eviction(self, gen):
        devs = gen.generate_developments()
        luxury = next(d for d in devs if d.id == "dev_luxury_maple")
        assert luxury.requires_eviction is True
        assert luxury.affordable_units_pct == 0.0

    def test_mixed_maple_no_eviction(self, gen):
        devs = gen.generate_developments()
        mixed = next(d for d in devs if d.id == "dev_mixed_maple")
        assert mixed.requires_eviction is False
        assert mixed.affordable_units_pct == 0.4

    def test_green_development_low_impact(self, gen):
        devs = gen.generate_developments()
        green = next(d for d in devs if d.id == "dev_green_elm")
        assert green.type == DevelopmentType.GREEN_DEVELOPMENT
        assert green.environmental_impact <= 0.2

    def test_affordable_birch_100_pct(self, gen):
        devs = gen.generate_developments()
        aff = next(d for d in devs if d.id == "dev_affordable_birch")
        assert aff.type == DevelopmentType.AFFORDABLE_HOUSING
        assert aff.affordable_units_pct == 1.0

    def test_all_costs_positive(self, gen):
        devs = gen.generate_developments()
        for d in devs:
            assert d.cost > 0
            assert d.duration_months > 0
            assert d.projected_value > 0

    def test_developments_not_started(self, gen):
        devs = gen.generate_developments()
        for d in devs:
            assert d.started is False
            assert d.completed is False


class TestOfficialGeneration:

    def test_generates_4_officials(self, gen):
        officials = gen.generate_officials()
        assert len(officials) == 4

    def test_2_corrupt_officials(self, gen):
        officials = gen.generate_officials()
        corrupt = [o for o in officials if o.corrupt]
        assert len(corrupt) == 2

    def test_2_honest_officials(self, gen):
        officials = gen.generate_officials()
        honest = [o for o in officials if not o.corrupt]
        assert len(honest) == 2

    def test_corrupt_have_bribe_amount(self, gen):
        officials = gen.generate_officials()
        for o in officials:
            if o.corrupt:
                assert o.bribe_amount > 0

    def test_honest_have_zero_bribe(self, gen):
        officials = gen.generate_officials()
        for o in officials:
            if not o.corrupt:
                assert o.bribe_amount == 0


class TestContractorGeneration:

    def test_generates_4_contractors(self, gen):
        contractors = gen.generate_contractors()
        assert len(contractors) == 4

    def test_cheap_contractor_cuts_corners(self, gen):
        contractors = gen.generate_contractors()
        cheap = next(c for c in contractors if c.id == "contractor_cheap")
        assert cheap.cuts_corners is True
        assert cheap.cost_multiplier < 1.0
        assert cheap.uses_union_labor is False

    def test_quality_contractor(self, gen):
        contractors = gen.generate_contractors()
        quality = next(c for c in contractors if c.id == "contractor_quality")
        assert quality.quality >= 90
        assert quality.uses_union_labor is True
        assert quality.environmental_compliance is True

    def test_union_contractor(self, gen):
        contractors = gen.generate_contractors()
        union = next(c for c in contractors if c.id == "contractor_union")
        assert union.uses_union_labor is True

    def test_at_least_one_union(self, gen):
        contractors = gen.generate_contractors()
        union = [c for c in contractors if c.uses_union_labor]
        assert len(union) >= 1


class TestDilemmaGeneration:

    def test_generates_12_dilemmas(self, gen):
        dilemmas = gen.generate_dilemmas()
        assert len(dilemmas) == 12

    def test_dilemma_ids_unique(self, gen):
        dilemmas = gen.generate_dilemmas()
        ids = [d.id for d in dilemmas]
        assert len(ids) == len(set(ids))

    def test_dilemmas_at_specific_months(self, gen):
        dilemmas = gen.generate_dilemmas()
        months = [d.month for d in dilemmas]
        assert 2 in months
        assert 5 in months
        assert 8 in months
        assert 35 in months

    def test_dilemmas_not_resolved(self, gen):
        dilemmas = gen.generate_dilemmas()
        for d in dilemmas:
            assert d.resolved is False

    def test_all_dilemmas_have_description(self, gen):
        dilemmas = gen.generate_dilemmas()
        for d in dilemmas:
            assert len(d.description) > 20


class TestBuyoutGeneration:

    def test_generates_buyout_offers(self, gen):
        buyouts = gen.generate_buyout_offers()
        assert len(buyouts) >= 1

    def test_maple_buyout(self, gen):
        buyouts = gen.generate_buyout_offers()
        maple = next(b for b in buyouts if b.property_id == "prop_maple_apts")
        assert maple.amount == 1250000
        assert maple.requires_eviction is True


class TestLoanGeneration:

    def test_generates_3_loans(self, gen):
        loans = gen.generate_loans()
        assert len(loans) == 3

    def test_one_predatory_loan(self, gen):
        loans = gen.generate_loans()
        predatory = [l for l in loans if l.predatory]
        assert len(predatory) == 1

    def test_predatory_high_rate(self, gen):
        loans = gen.generate_loans()
        predatory = next(l for l in loans if l.predatory)
        standard = next(l for l in loans if not l.predatory)
        assert predatory.interest_rate > standard.interest_rate


class TestFinancialsGeneration:

    def test_initial_financials(self, gen):
        f = gen.generate_initial_financials()
        assert f.cash == 2000000.0
        assert f.debt == 0.0
        assert f.total_portfolio_value == 1800000.0
