"""Tests for Real Estate Empire models."""

import pytest
from simulations.real_estate.models import (
    BuyoutOffer,
    CityOfficial,
    Contractor,
    Development,
    DevelopmentType,
    DilemmaType,
    EthicalDilemma,
    Financials,
    LoanOffer,
    NeighborhoodTier,
    Property,
    PropertyType,
    Tenant,
    TenantType,
)


# -- Enum Tests ------------------------------------------------------------

class TestEnums:

    def test_property_type_values(self):
        assert PropertyType.RESIDENTIAL.value == "residential"
        assert PropertyType.COMMERCIAL.value == "commercial"
        assert PropertyType.MIXED_USE.value == "mixed_use"
        assert PropertyType.LUXURY.value == "luxury"
        assert PropertyType.AFFORDABLE.value == "affordable"
        assert PropertyType.WAREHOUSE.value == "warehouse"
        assert PropertyType.VACANT_LOT.value == "vacant_lot"

    def test_property_type_count(self):
        assert len(PropertyType) == 7

    def test_neighborhood_tier_values(self):
        assert NeighborhoodTier.GENTRIFYING.value == "gentrifying"
        assert NeighborhoodTier.ESTABLISHED.value == "established"
        assert NeighborhoodTier.LUXURY.value == "luxury"
        assert NeighborhoodTier.INDUSTRIAL.value == "industrial"
        assert NeighborhoodTier.LOW_INCOME.value == "low_income"

    def test_neighborhood_tier_count(self):
        assert len(NeighborhoodTier) == 5

    def test_tenant_type_values(self):
        assert TenantType.LONG_TERM_RESIDENT.value == "long_term_resident"
        assert TenantType.LOW_INCOME_FAMILY.value == "low_income_family"
        assert TenantType.SMALL_BUSINESS.value == "small_business"
        assert TenantType.ELDERLY.value == "elderly"
        assert TenantType.DISABLED.value == "disabled"
        assert TenantType.STUDENT.value == "student"
        assert TenantType.CORPORATE.value == "corporate"

    def test_tenant_type_count(self):
        assert len(TenantType) == 7

    def test_development_type_values(self):
        assert DevelopmentType.LUXURY_CONDOS.value == "luxury_condos"
        assert DevelopmentType.MARKET_RATE.value == "market_rate"
        assert DevelopmentType.AFFORDABLE_HOUSING.value == "affordable_housing"
        assert DevelopmentType.MIXED_INCOME.value == "mixed_income"
        assert DevelopmentType.COMMERCIAL_OFFICE.value == "commercial_office"
        assert DevelopmentType.GREEN_DEVELOPMENT.value == "green_development"

    def test_development_type_count(self):
        assert len(DevelopmentType) == 6

    def test_dilemma_type_values(self):
        assert DilemmaType.TENANT_EVICTION.value == "tenant_eviction"
        assert DilemmaType.AFFORDABLE_BYPASS.value == "affordable_bypass"
        assert DilemmaType.BRIBERY.value == "bribery"
        assert DilemmaType.ENVIRONMENTAL_DAMAGE.value == "environmental_damage"
        assert DilemmaType.PREDATORY_LENDING.value == "predatory_lending"
        assert DilemmaType.SLUMLORD_NEGLECT.value == "slumlord_neglect"
        assert DilemmaType.ZONING_MANIPULATION.value == "zoning_manipulation"
        assert DilemmaType.DISPLACEMENT.value == "displacement"
        assert DilemmaType.SAFETY_VIOLATION.value == "safety_violation"
        assert DilemmaType.UNION_BUSTING.value == "union_busting"
        assert DilemmaType.GENTRIFICATION_ACCELERATION.value == "gentrification_acceleration"
        assert DilemmaType.COMMUNITY_DESTRUCTION.value == "community_destruction"

    def test_dilemma_type_count(self):
        assert len(DilemmaType) == 12


# -- Tenant Tests -----------------------------------------------------------

class TestTenant:

    def test_create_tenant(self):
        t = Tenant(
            id="t1", name="Rosa Martinez",
            type=TenantType.LOW_INCOME_FAMILY,
            monthly_rent=800, lease_months_remaining=12,
            vulnerability_score=8, years_in_building=15,
            can_afford_increase=False,
        )
        assert t.id == "t1"
        assert t.name == "Rosa Martinez"
        assert t.type == TenantType.LOW_INCOME_FAMILY
        assert t.monthly_rent == 800
        assert t.lease_months_remaining == 12
        assert t.vulnerability_score == 8
        assert t.years_in_building == 15
        assert t.can_afford_increase is False

    def test_tenant_to_dict(self):
        t = Tenant(
            id="t1", name="Test",
            type=TenantType.ELDERLY,
            monthly_rent=700, lease_months_remaining=6,
            vulnerability_score=9, years_in_building=20,
            can_afford_increase=False,
        )
        d = t.to_dict()
        assert d["id"] == "t1"
        assert d["type"] == "elderly"
        assert d["monthly_rent"] == 700

    def test_tenant_from_dict(self):
        d = {
            "id": "t2", "name": "James",
            "type": "corporate",
            "monthly_rent": 2000, "lease_months_remaining": 24,
            "vulnerability_score": 2, "years_in_building": 1,
            "can_afford_increase": True,
        }
        t = Tenant.from_dict(d)
        assert t.id == "t2"
        assert t.type == TenantType.CORPORATE
        assert t.can_afford_increase is True

    def test_tenant_roundtrip(self):
        t = Tenant(
            id="t3", name="Helen",
            type=TenantType.DISABLED,
            monthly_rent=650, lease_months_remaining=3,
            vulnerability_score=10, years_in_building=8,
            can_afford_increase=False,
        )
        t2 = Tenant.from_dict(t.to_dict())
        assert t2.id == t.id
        assert t2.type == t.type
        assert t2.vulnerability_score == t.vulnerability_score


# -- Property Tests ---------------------------------------------------------

class TestProperty:

    def test_create_property(self):
        p = Property(
            id="p1", name="Test Building",
            type=PropertyType.RESIDENTIAL,
            neighborhood=NeighborhoodTier.GENTRIFYING,
            value=500000, monthly_income=5000,
        )
        assert p.id == "p1"
        assert p.type == PropertyType.RESIDENTIAL
        assert p.value == 500000
        assert p.tenants == []
        assert p.owned is False

    def test_property_with_tenants(self):
        t = Tenant(
            id="t1", name="Rosa",
            type=TenantType.LOW_INCOME_FAMILY,
            monthly_rent=800, lease_months_remaining=12,
            vulnerability_score=8, years_in_building=15,
            can_afford_increase=False,
        )
        p = Property(
            id="p1", name="Test",
            type=PropertyType.AFFORDABLE,
            neighborhood=NeighborhoodTier.LOW_INCOME,
            value=400000, monthly_income=800,
            tenants=[t], owned=True,
        )
        assert len(p.tenants) == 1
        assert p.tenants[0].name == "Rosa"

    def test_property_to_dict(self):
        p = Property(
            id="p1", name="Test",
            type=PropertyType.COMMERCIAL,
            neighborhood=NeighborhoodTier.INDUSTRIAL,
            value=300000, monthly_income=4000,
            needs_repair=True, repair_cost=50000,
            owned=True,
        )
        d = p.to_dict()
        assert d["id"] == "p1"
        assert d["type"] == "commercial"
        assert d["neighborhood"] == "industrial"
        assert d["needs_repair"] is True

    def test_property_from_dict(self):
        d = {
            "id": "p2", "name": "Office",
            "type": "commercial",
            "neighborhood": "established",
            "value": 800000, "monthly_income": 10000,
            "tenants": [],
            "needs_repair": False, "repair_cost": 0,
            "development_potential": 0.6, "zoning": "commercial",
            "owned": True,
        }
        p = Property.from_dict(d)
        assert p.id == "p2"
        assert p.type == PropertyType.COMMERCIAL
        assert p.neighborhood == NeighborhoodTier.ESTABLISHED
        assert p.owned is True

    def test_property_roundtrip_with_tenants(self):
        t = Tenant(
            id="t1", name="Test Tenant",
            type=TenantType.STUDENT,
            monthly_rent=500, lease_months_remaining=6,
            vulnerability_score=3, years_in_building=1,
            can_afford_increase=True,
        )
        p = Property(
            id="p1", name="Student Housing",
            type=PropertyType.RESIDENTIAL,
            neighborhood=NeighborhoodTier.ESTABLISHED,
            value=600000, monthly_income=500,
            tenants=[t], owned=True,
        )
        p2 = Property.from_dict(p.to_dict())
        assert len(p2.tenants) == 1
        assert p2.tenants[0].id == "t1"
        assert p2.tenants[0].type == TenantType.STUDENT


# -- Development Tests ------------------------------------------------------

class TestDevelopment:

    def test_create_development(self):
        d = Development(
            id="d1", property_id="p1",
            type=DevelopmentType.LUXURY_CONDOS,
            cost=1000000, duration_months=12,
            projected_value=3000000,
            requires_eviction=True,
            environmental_impact=0.6,
            affordable_units_pct=0.0,
        )
        assert d.id == "d1"
        assert d.type == DevelopmentType.LUXURY_CONDOS
        assert d.requires_eviction is True
        assert d.started is False
        assert d.completed is False

    def test_development_to_dict(self):
        d = Development(
            id="d1", property_id="p1",
            type=DevelopmentType.GREEN_DEVELOPMENT,
            cost=500000, duration_months=6,
            projected_value=1200000,
            requires_eviction=False,
            environmental_impact=0.1,
            affordable_units_pct=0.3,
        )
        data = d.to_dict()
        assert data["type"] == "green_development"
        assert data["affordable_units_pct"] == 0.3
        assert data["environmental_impact"] == 0.1

    def test_development_from_dict(self):
        data = {
            "id": "d2", "property_id": "p2",
            "type": "affordable_housing",
            "cost": 400000, "duration_months": 8,
            "projected_value": 700000,
            "requires_eviction": False,
            "environmental_impact": 0.2,
            "affordable_units_pct": 1.0,
            "contractor_id": None,
            "months_remaining": 0,
            "started": False, "completed": False,
        }
        d = Development.from_dict(data)
        assert d.type == DevelopmentType.AFFORDABLE_HOUSING
        assert d.affordable_units_pct == 1.0

    def test_development_roundtrip(self):
        d = Development(
            id="d1", property_id="p1",
            type=DevelopmentType.MIXED_INCOME,
            cost=700000, duration_months=10,
            projected_value=1500000,
            requires_eviction=False,
            environmental_impact=0.3,
            affordable_units_pct=0.4,
            contractor_id="c1",
            months_remaining=5,
            started=True,
        )
        d2 = Development.from_dict(d.to_dict())
        assert d2.contractor_id == "c1"
        assert d2.months_remaining == 5
        assert d2.started is True


# -- CityOfficial Tests -----------------------------------------------------

class TestCityOfficial:

    def test_create_official(self):
        o = CityOfficial(
            id="o1", name="Frank",
            role="zoning", corrupt=True,
            bribe_amount=25000, controls="zoning variances",
        )
        assert o.corrupt is True
        assert o.bribe_amount == 25000

    def test_official_to_dict(self):
        o = CityOfficial(
            id="o1", name="Grace",
            role="permits", corrupt=False,
            bribe_amount=0, controls="building permits",
        )
        d = o.to_dict()
        assert d["corrupt"] is False
        assert d["controls"] == "building permits"

    def test_official_roundtrip(self):
        o = CityOfficial(
            id="o2", name="Ray",
            role="inspections", corrupt=True,
            bribe_amount=15000, controls="safety inspections",
        )
        o2 = CityOfficial.from_dict(o.to_dict())
        assert o2.id == o.id
        assert o2.corrupt == o.corrupt
        assert o2.bribe_amount == o.bribe_amount


# -- Contractor Tests -------------------------------------------------------

class TestContractor:

    def test_create_contractor(self):
        c = Contractor(
            id="c1", name="QuickBuild",
            quality=35, cost_multiplier=0.6,
            uses_union_labor=False,
            environmental_compliance=False,
            cuts_corners=True,
        )
        assert c.quality == 35
        assert c.cuts_corners is True

    def test_contractor_to_dict(self):
        c = Contractor(
            id="c1", name="Sterling",
            quality=95, cost_multiplier=1.5,
            uses_union_labor=True,
            environmental_compliance=True,
            cuts_corners=False,
        )
        d = c.to_dict()
        assert d["quality"] == 95
        assert d["uses_union_labor"] is True

    def test_contractor_roundtrip(self):
        c = Contractor(
            id="c2", name="Metro",
            quality=80, cost_multiplier=1.2,
            uses_union_labor=True,
            environmental_compliance=True,
            cuts_corners=False,
        )
        c2 = Contractor.from_dict(c.to_dict())
        assert c2.id == c.id
        assert c2.quality == c.quality


# -- Financials Tests -------------------------------------------------------

class TestFinancials:

    def test_default_financials(self):
        f = Financials()
        assert f.cash == 2000000.0
        assert f.debt == 0.0

    def test_custom_financials(self):
        f = Financials(cash=1000000, debt=500000)
        assert f.cash == 1000000
        assert f.debt == 500000

    def test_financials_to_dict(self):
        f = Financials(cash=1500000, total_portfolio_value=3000000,
                       monthly_income=20000, debt=200000,
                       mortgage_payments=5000)
        d = f.to_dict()
        assert d["cash"] == 1500000
        assert d["monthly_income"] == 20000

    def test_financials_roundtrip(self):
        f = Financials(cash=750000, debt=100000, mortgage_payments=3000)
        f2 = Financials.from_dict(f.to_dict())
        assert f2.cash == f.cash
        assert f2.debt == f.debt


# -- EthicalDilemma Tests ---------------------------------------------------

class TestEthicalDilemma:

    def test_create_dilemma(self):
        d = EthicalDilemma(
            id="d1", type=DilemmaType.BRIBERY,
            description="A bribe opportunity",
            month=5,
            temptation_action="bribe",
            temptation_reward="$25K benefit",
        )
        assert d.type == DilemmaType.BRIBERY
        assert d.month == 5
        assert d.resolved is False

    def test_dilemma_to_dict(self):
        d = EthicalDilemma(
            id="d1", type=DilemmaType.DISPLACEMENT,
            description="Test",
            month=2,
            temptation_action="sell",
            temptation_reward="+800K",
        )
        data = d.to_dict()
        assert data["type"] == "displacement"

    def test_dilemma_roundtrip(self):
        d = EthicalDilemma(
            id="d1", type=DilemmaType.TENANT_EVICTION,
            description="Eviction dilemma",
            month=11,
            temptation_action="evict",
            temptation_reward="Higher income",
            resolved=True,
            action_taken="negotiate",
        )
        d2 = EthicalDilemma.from_dict(d.to_dict())
        assert d2.resolved is True
        assert d2.action_taken == "negotiate"


# -- BuyoutOffer Tests ------------------------------------------------------

class TestBuyoutOffer:

    def test_create_buyout(self):
        b = BuyoutOffer(
            id="b1", property_id="p1",
            buyer_name="Apex", amount=1250000,
            requires_eviction=True, month=2,
            description="Convert to luxury",
        )
        assert b.amount == 1250000
        assert b.accepted is False

    def test_buyout_to_dict(self):
        b = BuyoutOffer(
            id="b1", property_id="p1",
            buyer_name="Apex", amount=1250000,
            requires_eviction=True, month=2,
        )
        d = b.to_dict()
        assert d["amount"] == 1250000

    def test_buyout_roundtrip(self):
        b = BuyoutOffer(
            id="b1", property_id="p1",
            buyer_name="Apex", amount=1250000,
            requires_eviction=True, month=2,
            accepted=True,
        )
        b2 = BuyoutOffer.from_dict(b.to_dict())
        assert b2.accepted is True


# -- LoanOffer Tests --------------------------------------------------------

class TestLoanOffer:

    def test_create_loan(self):
        l = LoanOffer(
            id="l1", amount=500000,
            interest_rate=0.06, duration_months=60,
            predatory=False,
        )
        assert l.amount == 500000
        assert l.predatory is False

    def test_loan_to_dict(self):
        l = LoanOffer(
            id="l1", amount=750000,
            interest_rate=0.18, duration_months=36,
            predatory=True,
        )
        d = l.to_dict()
        assert d["predatory"] is True

    def test_loan_roundtrip(self):
        l = LoanOffer(
            id="l2", amount=1000000,
            interest_rate=0.07, duration_months=120,
        )
        l2 = LoanOffer.from_dict(l.to_dict())
        assert l2.amount == l.amount
        assert l2.interest_rate == l.interest_rate
