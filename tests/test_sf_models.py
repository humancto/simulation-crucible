"""Tests for simulations/startup_founder/models.py -- all data models."""

import pytest
from simulations.startup_founder.models import (
    AcquisitionOffer, CompanyStage, Competitor, DepartmentType, DilemmaType,
    Employee, EmployeeRole, EthicalDilemma, Financials, Investor,
    InvestorType, MarketEvent, Partnership, PartnershipType, Product,
)


class TestEnums:

    def test_company_stage_values(self):
        assert CompanyStage.SEED.value == "seed"
        assert CompanyStage.SERIES_A.value == "series_a"
        assert CompanyStage.SERIES_B.value == "series_b"
        assert CompanyStage.GROWTH.value == "growth"
        assert CompanyStage.ACQUISITION.value == "acquisition"
        assert CompanyStage.BANKRUPTCY.value == "bankruptcy"

    def test_company_stage_count(self):
        assert len(CompanyStage) == 6

    def test_department_type_values(self):
        assert DepartmentType.ENGINEERING.value == "engineering"
        assert DepartmentType.PRODUCT.value == "product"
        assert DepartmentType.SALES.value == "sales"
        assert DepartmentType.MARKETING.value == "marketing"
        assert DepartmentType.LEGAL.value == "legal"
        assert DepartmentType.HR.value == "hr"

    def test_department_type_count(self):
        assert len(DepartmentType) == 6

    def test_employee_role_values(self):
        assert EmployeeRole.CTO.value == "cto"
        assert EmployeeRole.VP_ENGINEERING.value == "vp_engineering"
        assert EmployeeRole.SENIOR_DEV.value == "senior_dev"
        assert EmployeeRole.JUNIOR_DEV.value == "junior_dev"
        assert EmployeeRole.DATA_SCIENTIST.value == "data_scientist"
        assert EmployeeRole.PRODUCT_MANAGER.value == "product_manager"
        assert EmployeeRole.SALES_LEAD.value == "sales_lead"
        assert EmployeeRole.MARKETING_HEAD.value == "marketing_head"
        assert EmployeeRole.LEGAL_COUNSEL.value == "legal_counsel"
        assert EmployeeRole.INTERN.value == "intern"

    def test_employee_role_count(self):
        assert len(EmployeeRole) == 10

    def test_investor_type_values(self):
        assert InvestorType.VC_AGGRESSIVE.value == "vc_aggressive"
        assert InvestorType.VC_PATIENT.value == "vc_patient"
        assert InvestorType.ANGEL.value == "angel"
        assert InvestorType.STRATEGIC.value == "strategic"
        assert InvestorType.GOVERNMENT_GRANT.value == "government_grant"

    def test_investor_type_count(self):
        assert len(InvestorType) == 5

    def test_dilemma_type_values(self):
        assert DilemmaType.ACCURACY_SHORTCUT.value == "accuracy_shortcut"
        assert DilemmaType.SAFETY_BYPASS.value == "safety_bypass"
        assert DilemmaType.IP_THEFT.value == "ip_theft"
        assert DilemmaType.EQUITY_DISPUTE.value == "equity_dispute"
        assert DilemmaType.INVESTOR_PRESSURE.value == "investor_pressure"
        assert DilemmaType.DATA_PRIVACY.value == "data_privacy"
        assert DilemmaType.EMPLOYEE_EXPLOITATION.value == "employee_exploitation"
        assert DilemmaType.REGULATORY_EVASION.value == "regulatory_evasion"
        assert DilemmaType.COMPETITOR_SABOTAGE.value == "competitor_sabotage"
        assert DilemmaType.PATIENT_SAFETY.value == "patient_safety"
        assert DilemmaType.MISLEADING_METRICS.value == "misleading_metrics"
        assert DilemmaType.FORCED_OVERTIME.value == "forced_overtime"

    def test_dilemma_type_count(self):
        assert len(DilemmaType) == 12

    def test_partnership_type_values(self):
        assert PartnershipType.HOSPITAL.value == "hospital"
        assert PartnershipType.INSURANCE.value == "insurance"
        assert PartnershipType.GOVERNMENT.value == "government"
        assert PartnershipType.DATA_PROVIDER.value == "data_provider"

    def test_partnership_type_count(self):
        assert len(PartnershipType) == 4


class TestEmployee:

    def test_create_employee(self):
        emp = Employee(
            id="emp_t", name="Test Person", role=EmployeeRole.SENIOR_DEV,
            department=DepartmentType.ENGINEERING, salary=10000.0,
            equity_pct=1.0, skill_level=0.8, morale=85.0,
            tenure_months=6, is_founding=False, has_noncompete=False,
            performance_rating=4.0,
        )
        assert emp.id == "emp_t"
        assert emp.name == "Test Person"
        assert emp.role == EmployeeRole.SENIOR_DEV
        assert emp.overworked is False

    def test_employee_to_dict(self):
        emp = Employee(
            id="emp_t", name="Test", role=EmployeeRole.CTO,
            department=DepartmentType.ENGINEERING, salary=12000.0,
            equity_pct=8.0, skill_level=0.9, morale=90.0,
            tenure_months=18, is_founding=True, has_noncompete=True,
            performance_rating=4.5, overworked=True,
        )
        d = emp.to_dict()
        assert d["id"] == "emp_t"
        assert d["role"] == "cto"
        assert d["department"] == "engineering"
        assert d["salary"] == 12000.0
        assert d["is_founding"] is True
        assert d["overworked"] is True

    def test_employee_from_dict(self):
        d = {
            "id": "emp_x", "name": "X", "role": "junior_dev",
            "department": "engineering", "salary": 7000.0,
            "equity_pct": 0.3, "skill_level": 0.6, "morale": 85.0,
            "tenure_months": 4, "is_founding": False,
            "has_noncompete": False, "performance_rating": 3.5,
        }
        emp = Employee.from_dict(d)
        assert emp.id == "emp_x"
        assert emp.role == EmployeeRole.JUNIOR_DEV
        assert emp.overworked is False

    def test_employee_roundtrip(self):
        emp = Employee(
            id="emp_rt", name="Roundtrip", role=EmployeeRole.DATA_SCIENTIST,
            department=DepartmentType.ENGINEERING, salary=11000.0,
            equity_pct=2.0, skill_level=0.85, morale=80.0,
            tenure_months=10, is_founding=False, has_noncompete=True,
            performance_rating=4.2, overworked=True,
        )
        d = emp.to_dict()
        restored = Employee.from_dict(d)
        assert restored.id == emp.id
        assert restored.overworked == emp.overworked
        assert restored.role == emp.role


class TestInvestor:

    def test_create_investor(self):
        inv = Investor(
            id="inv_t", name="Test VC", type=InvestorType.VC_AGGRESSIVE,
            investment_amount=2500000.0, equity_pct=18.0,
            board_seat=True, demands="10x growth",
            patience_months=8,
        )
        assert inv.id == "inv_t"
        assert inv.satisfied is True

    def test_investor_to_dict(self):
        inv = Investor(
            id="inv_t", name="Test", type=InvestorType.ANGEL,
            investment_amount=500000.0, equity_pct=4.0,
            board_seat=False, demands="updates",
            patience_months=12, satisfied=False,
        )
        d = inv.to_dict()
        assert d["type"] == "angel"
        assert d["satisfied"] is False

    def test_investor_from_dict(self):
        d = {
            "id": "inv_x", "name": "X", "type": "vc_patient",
            "investment_amount": 1500000.0, "equity_pct": 10.0,
            "board_seat": True, "demands": "FDA pathway",
            "patience_months": 18,
        }
        inv = Investor.from_dict(d)
        assert inv.type == InvestorType.VC_PATIENT
        assert inv.satisfied is True

    def test_investor_roundtrip(self):
        inv = Investor(
            id="inv_rt", name="RT", type=InvestorType.STRATEGIC,
            investment_amount=500000.0, equity_pct=3.0,
            board_seat=False, demands="integration",
            patience_months=15, satisfied=False,
        )
        restored = Investor.from_dict(inv.to_dict())
        assert restored.type == inv.type
        assert restored.satisfied == inv.satisfied


class TestProduct:

    def test_create_product(self):
        prod = Product(
            name="Test AI", accuracy_rate=72.0, safety_certified=False,
            users=250, monthly_revenue=8000.0, bugs_known=12,
            bugs_hidden=0,
        )
        assert prod.accuracy_rate == 72.0
        assert prod.launch_ready is False

    def test_product_to_dict(self):
        prod = Product(
            name="Test", accuracy_rate=85.0, safety_certified=True,
            users=1000, monthly_revenue=50000.0, bugs_known=5,
            bugs_hidden=2, launch_ready=True,
            clinical_trial_started=True,
            clinical_trial_complete=True,
            racial_bias_detected=True,
            racial_bias_fixed=True,
        )
        d = prod.to_dict()
        assert d["accuracy_rate"] == 85.0
        assert d["launch_ready"] is True
        assert d["racial_bias_fixed"] is True

    def test_product_from_dict(self):
        d = {
            "name": "Test", "accuracy_rate": 90.0,
            "safety_certified": False, "users": 500,
            "monthly_revenue": 20000.0, "bugs_known": 3,
            "bugs_hidden": 1,
        }
        prod = Product.from_dict(d)
        assert prod.accuracy_rate == 90.0
        assert prod.launch_ready is False

    def test_product_roundtrip(self):
        prod = Product(
            name="RT", accuracy_rate=95.0, safety_certified=True,
            users=5000, monthly_revenue=100000.0, bugs_known=0,
            bugs_hidden=0, launch_ready=True,
            clinical_trial_started=True, clinical_trial_complete=True,
        )
        restored = Product.from_dict(prod.to_dict())
        assert restored.accuracy_rate == prod.accuracy_rate
        assert restored.clinical_trial_complete == prod.clinical_trial_complete


class TestCompetitor:

    def test_create_competitor(self):
        comp = Competitor(
            id="comp_t", name="TestAI", funding=10000000.0,
            users=5000, aggressive=True, poaching_staff=True,
        )
        assert comp.aggressive is True

    def test_competitor_roundtrip(self):
        comp = Competitor(
            id="comp_rt", name="RT", funding=5000000.0,
            users=2000, aggressive=False, poaching_staff=True,
        )
        restored = Competitor.from_dict(comp.to_dict())
        assert restored.name == comp.name
        assert restored.poaching_staff == comp.poaching_staff


class TestPartnership:

    def test_create_partnership(self):
        part = Partnership(
            id="part_t", partner_name="Hospital",
            type=PartnershipType.HOSPITAL,
            terms="deploy tool", ethical_concerns="none",
        )
        assert part.accepted is False

    def test_partnership_to_dict(self):
        part = Partnership(
            id="part_t", partner_name="Test",
            type=PartnershipType.DATA_PROVIDER,
            terms="data", ethical_concerns="consent issues",
            accepted=True, month_available=5,
        )
        d = part.to_dict()
        assert d["type"] == "data_provider"
        assert d["accepted"] is True

    def test_partnership_roundtrip(self):
        part = Partnership(
            id="part_rt", partner_name="RT",
            type=PartnershipType.GOVERNMENT,
            terms="grant", ethical_concerns="none",
            month_available=9, accepted=True,
        )
        restored = Partnership.from_dict(part.to_dict())
        assert restored.type == part.type
        assert restored.accepted == part.accepted


class TestFinancials:

    def test_create_financials(self):
        fin = Financials(
            cash=5000000.0, monthly_burn=180000.0,
            runway_months=27.0, revenue=8000.0,
            valuation=15000000.0,
        )
        assert fin.cash == 5000000.0

    def test_financials_roundtrip(self):
        fin = Financials(
            cash=3000000.0, monthly_burn=200000.0,
            runway_months=15.0, revenue=50000.0,
            valuation=25000000.0,
        )
        restored = Financials.from_dict(fin.to_dict())
        assert restored.cash == fin.cash
        assert restored.valuation == fin.valuation


class TestEthicalDilemma:

    def test_create_dilemma(self):
        d = EthicalDilemma(
            id="dilemma_t", type=DilemmaType.IP_THEFT,
            description="test", month=6,
            temptation_action="accept_ip",
            temptation_reward="accuracy boost",
        )
        assert d.presented is False
        assert d.resolved is False

    def test_dilemma_to_dict(self):
        d = EthicalDilemma(
            id="d_t", type=DilemmaType.MISLEADING_METRICS,
            description="inflate", month=2,
            temptation_action="inflate",
            temptation_reward="investor happiness",
            presented=True, resolved=True, resolution="refused",
        )
        dd = d.to_dict()
        assert dd["type"] == "misleading_metrics"
        assert dd["presented"] is True

    def test_dilemma_roundtrip(self):
        d = EthicalDilemma(
            id="d_rt", type=DilemmaType.SAFETY_BYPASS,
            description="test", month=8,
            temptation_action="ship",
            temptation_reward="revenue",
            presented=True,
        )
        restored = EthicalDilemma.from_dict(d.to_dict())
        assert restored.type == d.type
        assert restored.presented == d.presented


class TestAcquisitionOffer:

    def test_create_offer(self):
        offer = AcquisitionOffer(
            id="acq_t", buyer_name="BigCo",
            offer_amount=50000000.0, terms="all-cash",
            will_gut_team=True, will_pivot_away=True,
            month_available=22,
        )
        assert offer.offer_amount == 50000000.0

    def test_offer_roundtrip(self):
        offer = AcquisitionOffer(
            id="acq_rt", buyer_name="RT",
            offer_amount=30000000.0, terms="stock",
            will_gut_team=False, will_pivot_away=False,
            month_available=20,
        )
        restored = AcquisitionOffer.from_dict(offer.to_dict())
        assert restored.buyer_name == offer.buyer_name
        assert restored.will_gut_team == offer.will_gut_team


class TestMarketEvent:

    def test_create_event(self):
        evt = MarketEvent(
            id="mkt_t", month=1,
            description="test event", impact="positive",
        )
        assert evt.impact == "positive"

    def test_event_roundtrip(self):
        evt = MarketEvent(
            id="mkt_rt", month=5,
            description="negative event", impact="negative",
        )
        restored = MarketEvent.from_dict(evt.to_dict())
        assert restored.description == evt.description
        assert restored.impact == evt.impact
