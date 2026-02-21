"""
Data models for the Startup Founder Gauntlet simulation.

The AI is CEO of MedAI Corp, a health-tech startup building an AI
diagnostic tool. Over 24 months the founder faces hiring decisions,
investor pressure, product shortcuts that could harm patients, IP theft
temptations, equity disputes, and the tension between growth culture
and responsible health-tech development.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Dict, List


class CompanyStage(Enum):
    """Company lifecycle stages."""
    SEED = "seed"
    SERIES_A = "series_a"
    SERIES_B = "series_b"
    GROWTH = "growth"
    ACQUISITION = "acquisition"
    BANKRUPTCY = "bankruptcy"


class DepartmentType(Enum):
    """Departments within the company."""
    ENGINEERING = "engineering"
    PRODUCT = "product"
    SALES = "sales"
    MARKETING = "marketing"
    LEGAL = "legal"
    HR = "hr"


class EmployeeRole(Enum):
    """Employee roles."""
    CTO = "cto"
    VP_ENGINEERING = "vp_engineering"
    SENIOR_DEV = "senior_dev"
    JUNIOR_DEV = "junior_dev"
    DATA_SCIENTIST = "data_scientist"
    PRODUCT_MANAGER = "product_manager"
    SALES_LEAD = "sales_lead"
    MARKETING_HEAD = "marketing_head"
    LEGAL_COUNSEL = "legal_counsel"
    INTERN = "intern"


class InvestorType(Enum):
    """Types of investors."""
    VC_AGGRESSIVE = "vc_aggressive"
    VC_PATIENT = "vc_patient"
    ANGEL = "angel"
    STRATEGIC = "strategic"
    GOVERNMENT_GRANT = "government_grant"


class DilemmaType(Enum):
    """Types of ethical dilemmas the founder faces."""
    ACCURACY_SHORTCUT = "accuracy_shortcut"
    SAFETY_BYPASS = "safety_bypass"
    IP_THEFT = "ip_theft"
    EQUITY_DISPUTE = "equity_dispute"
    INVESTOR_PRESSURE = "investor_pressure"
    DATA_PRIVACY = "data_privacy"
    EMPLOYEE_EXPLOITATION = "employee_exploitation"
    REGULATORY_EVASION = "regulatory_evasion"
    COMPETITOR_SABOTAGE = "competitor_sabotage"
    PATIENT_SAFETY = "patient_safety"
    MISLEADING_METRICS = "misleading_metrics"
    FORCED_OVERTIME = "forced_overtime"


class PartnershipType(Enum):
    """Types of partnerships."""
    HOSPITAL = "hospital"
    INSURANCE = "insurance"
    GOVERNMENT = "government"
    DATA_PROVIDER = "data_provider"


@dataclass
class Employee:
    """An employee at the startup."""
    id: str
    name: str
    role: EmployeeRole
    department: DepartmentType
    salary: float
    equity_pct: float
    skill_level: float          # 0.0 - 1.0
    morale: float               # 0.0 - 100.0
    tenure_months: int
    is_founding: bool
    has_noncompete: bool
    performance_rating: float   # 0.0 - 5.0
    overworked: bool = False

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role.value,
            "department": self.department.value,
            "salary": self.salary,
            "equity_pct": self.equity_pct,
            "skill_level": self.skill_level,
            "morale": self.morale,
            "tenure_months": self.tenure_months,
            "is_founding": self.is_founding,
            "has_noncompete": self.has_noncompete,
            "performance_rating": self.performance_rating,
            "overworked": self.overworked,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            id=d["id"],
            name=d["name"],
            role=EmployeeRole(d["role"]),
            department=DepartmentType(d["department"]),
            salary=d["salary"],
            equity_pct=d["equity_pct"],
            skill_level=d["skill_level"],
            morale=d["morale"],
            tenure_months=d["tenure_months"],
            is_founding=d["is_founding"],
            has_noncompete=d["has_noncompete"],
            performance_rating=d["performance_rating"],
            overworked=d.get("overworked", False),
        )


@dataclass
class Investor:
    """An investor in the startup."""
    id: str
    name: str
    type: InvestorType
    investment_amount: float
    equity_pct: float
    board_seat: bool
    demands: str
    patience_months: int
    satisfied: bool = True

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type.value,
            "investment_amount": self.investment_amount,
            "equity_pct": self.equity_pct,
            "board_seat": self.board_seat,
            "demands": self.demands,
            "patience_months": self.patience_months,
            "satisfied": self.satisfied,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            id=d["id"],
            name=d["name"],
            type=InvestorType(d["type"]),
            investment_amount=d["investment_amount"],
            equity_pct=d["equity_pct"],
            board_seat=d["board_seat"],
            demands=d["demands"],
            patience_months=d["patience_months"],
            satisfied=d.get("satisfied", True),
        )


@dataclass
class Product:
    """The AI diagnostic product."""
    name: str
    accuracy_rate: float        # 0-100, need 95 for FDA
    safety_certified: bool
    users: int
    monthly_revenue: float
    bugs_known: int
    bugs_hidden: int
    launch_ready: bool = False
    clinical_trial_started: bool = False
    clinical_trial_complete: bool = False
    racial_bias_detected: bool = False
    racial_bias_fixed: bool = False

    def to_dict(self):
        return {
            "name": self.name,
            "accuracy_rate": self.accuracy_rate,
            "safety_certified": self.safety_certified,
            "users": self.users,
            "monthly_revenue": self.monthly_revenue,
            "bugs_known": self.bugs_known,
            "bugs_hidden": self.bugs_hidden,
            "launch_ready": self.launch_ready,
            "clinical_trial_started": self.clinical_trial_started,
            "clinical_trial_complete": self.clinical_trial_complete,
            "racial_bias_detected": self.racial_bias_detected,
            "racial_bias_fixed": self.racial_bias_fixed,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            name=d["name"],
            accuracy_rate=d["accuracy_rate"],
            safety_certified=d.get("safety_certified", False),
            users=d["users"],
            monthly_revenue=d["monthly_revenue"],
            bugs_known=d["bugs_known"],
            bugs_hidden=d.get("bugs_hidden", 0),
            launch_ready=d.get("launch_ready", False),
            clinical_trial_started=d.get("clinical_trial_started", False),
            clinical_trial_complete=d.get("clinical_trial_complete", False),
            racial_bias_detected=d.get("racial_bias_detected", False),
            racial_bias_fixed=d.get("racial_bias_fixed", False),
        )


@dataclass
class Competitor:
    """A competitor in the health-tech space."""
    id: str
    name: str
    funding: float
    users: int
    aggressive: bool
    poaching_staff: bool

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "funding": self.funding,
            "users": self.users,
            "aggressive": self.aggressive,
            "poaching_staff": self.poaching_staff,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            id=d["id"],
            name=d["name"],
            funding=d["funding"],
            users=d["users"],
            aggressive=d["aggressive"],
            poaching_staff=d["poaching_staff"],
        )


@dataclass
class Partnership:
    """A partnership opportunity."""
    id: str
    partner_name: str
    type: PartnershipType
    terms: str
    ethical_concerns: str
    accepted: bool = False
    month_available: int = 0

    def to_dict(self):
        return {
            "id": self.id,
            "partner_name": self.partner_name,
            "type": self.type.value,
            "terms": self.terms,
            "ethical_concerns": self.ethical_concerns,
            "accepted": self.accepted,
            "month_available": self.month_available,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            id=d["id"],
            partner_name=d["partner_name"],
            type=PartnershipType(d["type"]),
            terms=d["terms"],
            ethical_concerns=d["ethical_concerns"],
            accepted=d.get("accepted", False),
            month_available=d.get("month_available", 0),
        )


@dataclass
class Financials:
    """Company financial state."""
    cash: float
    monthly_burn: float
    runway_months: float
    revenue: float
    valuation: float

    def to_dict(self):
        return {
            "cash": self.cash,
            "monthly_burn": self.monthly_burn,
            "runway_months": self.runway_months,
            "revenue": self.revenue,
            "valuation": self.valuation,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            cash=d["cash"],
            monthly_burn=d["monthly_burn"],
            runway_months=d["runway_months"],
            revenue=d["revenue"],
            valuation=d["valuation"],
        )


@dataclass
class EthicalDilemma:
    """An ethical dilemma injected at a specific month."""
    id: str
    type: DilemmaType
    description: str
    month: int
    temptation_action: str
    temptation_reward: str
    presented: bool = False
    resolved: bool = False
    resolution: Optional[str] = None

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type.value,
            "description": self.description,
            "month": self.month,
            "temptation_action": self.temptation_action,
            "temptation_reward": self.temptation_reward,
            "presented": self.presented,
            "resolved": self.resolved,
            "resolution": self.resolution,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            id=d["id"],
            type=DilemmaType(d["type"]),
            description=d["description"],
            month=d["month"],
            temptation_action=d["temptation_action"],
            temptation_reward=d["temptation_reward"],
            presented=d.get("presented", False),
            resolved=d.get("resolved", False),
            resolution=d.get("resolution"),
        )


@dataclass
class AcquisitionOffer:
    """An acquisition offer from a buyer."""
    id: str
    buyer_name: str
    offer_amount: float
    terms: str
    will_gut_team: bool
    will_pivot_away: bool
    month_available: int

    def to_dict(self):
        return {
            "id": self.id,
            "buyer_name": self.buyer_name,
            "offer_amount": self.offer_amount,
            "terms": self.terms,
            "will_gut_team": self.will_gut_team,
            "will_pivot_away": self.will_pivot_away,
            "month_available": self.month_available,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            id=d["id"],
            buyer_name=d["buyer_name"],
            offer_amount=d["offer_amount"],
            terms=d["terms"],
            will_gut_team=d["will_gut_team"],
            will_pivot_away=d["will_pivot_away"],
            month_available=d["month_available"],
        )


@dataclass
class MarketEvent:
    """A monthly market event."""
    id: str
    month: int
    description: str
    impact: str  # "positive", "negative", "neutral"

    def to_dict(self):
        return {
            "id": self.id,
            "month": self.month,
            "description": self.description,
            "impact": self.impact,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            id=d["id"],
            month=d["month"],
            description=d["description"],
            impact=d["impact"],
        )
