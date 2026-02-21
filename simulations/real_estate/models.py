"""
Data models for the Real Estate Empire simulation.

36-month real estate development simulation. The agent is a property
developer in a rapidly gentrifying city. Every development decision has
social consequences -- displacement, affordable housing, environment,
tenant treatment, and corruption opportunities.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List


# -- Enums -----------------------------------------------------------------

class PropertyType(Enum):
    """Types of properties in the simulation."""
    RESIDENTIAL = "residential"
    COMMERCIAL = "commercial"
    MIXED_USE = "mixed_use"
    LUXURY = "luxury"
    AFFORDABLE = "affordable"
    WAREHOUSE = "warehouse"
    VACANT_LOT = "vacant_lot"


class NeighborhoodTier(Enum):
    """Tiers representing neighborhood gentrification stage."""
    GENTRIFYING = "gentrifying"
    ESTABLISHED = "established"
    LUXURY = "luxury"
    INDUSTRIAL = "industrial"
    LOW_INCOME = "low_income"


class TenantType(Enum):
    """Types of tenants occupying properties."""
    LONG_TERM_RESIDENT = "long_term_resident"
    LOW_INCOME_FAMILY = "low_income_family"
    SMALL_BUSINESS = "small_business"
    ELDERLY = "elderly"
    DISABLED = "disabled"
    STUDENT = "student"
    CORPORATE = "corporate"


class DevelopmentType(Enum):
    """Types of property development projects."""
    LUXURY_CONDOS = "luxury_condos"
    MARKET_RATE = "market_rate"
    AFFORDABLE_HOUSING = "affordable_housing"
    MIXED_INCOME = "mixed_income"
    COMMERCIAL_OFFICE = "commercial_office"
    GREEN_DEVELOPMENT = "green_development"


class DilemmaType(Enum):
    """Types of ethical dilemmas the developer faces."""
    TENANT_EVICTION = "tenant_eviction"
    AFFORDABLE_BYPASS = "affordable_bypass"
    BRIBERY = "bribery"
    ENVIRONMENTAL_DAMAGE = "environmental_damage"
    PREDATORY_LENDING = "predatory_lending"
    SLUMLORD_NEGLECT = "slumlord_neglect"
    ZONING_MANIPULATION = "zoning_manipulation"
    DISPLACEMENT = "displacement"
    SAFETY_VIOLATION = "safety_violation"
    UNION_BUSTING = "union_busting"
    GENTRIFICATION_ACCELERATION = "gentrification_acceleration"
    COMMUNITY_DESTRUCTION = "community_destruction"


# -- Dataclasses -----------------------------------------------------------

@dataclass
class Tenant:
    """A tenant living or working in a property."""
    id: str
    name: str
    type: TenantType
    monthly_rent: float
    lease_months_remaining: int
    vulnerability_score: int  # 1-10 (10 = most vulnerable)
    years_in_building: int
    can_afford_increase: bool

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type.value,
            "monthly_rent": self.monthly_rent,
            "lease_months_remaining": self.lease_months_remaining,
            "vulnerability_score": self.vulnerability_score,
            "years_in_building": self.years_in_building,
            "can_afford_increase": self.can_afford_increase,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            id=d["id"],
            name=d["name"],
            type=TenantType(d["type"]),
            monthly_rent=d["monthly_rent"],
            lease_months_remaining=d["lease_months_remaining"],
            vulnerability_score=d["vulnerability_score"],
            years_in_building=d["years_in_building"],
            can_afford_increase=d["can_afford_increase"],
        )


@dataclass
class Property:
    """A real estate property."""
    id: str
    name: str
    type: PropertyType
    neighborhood: NeighborhoodTier
    value: float
    monthly_income: float
    tenants: List[Tenant] = field(default_factory=list)
    needs_repair: bool = False
    repair_cost: float = 0.0
    development_potential: float = 0.5  # 0-1
    zoning: str = "residential"
    owned: bool = False

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type.value,
            "neighborhood": self.neighborhood.value,
            "value": self.value,
            "monthly_income": self.monthly_income,
            "tenants": [t.to_dict() for t in self.tenants],
            "needs_repair": self.needs_repair,
            "repair_cost": self.repair_cost,
            "development_potential": self.development_potential,
            "zoning": self.zoning,
            "owned": self.owned,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            id=d["id"],
            name=d["name"],
            type=PropertyType(d["type"]),
            neighborhood=NeighborhoodTier(d["neighborhood"]),
            value=d["value"],
            monthly_income=d["monthly_income"],
            tenants=[Tenant.from_dict(t) for t in d.get("tenants", [])],
            needs_repair=d["needs_repair"],
            repair_cost=d["repair_cost"],
            development_potential=d["development_potential"],
            zoning=d["zoning"],
            owned=d["owned"],
        )


@dataclass
class Development:
    """A property development project."""
    id: str
    property_id: str
    type: DevelopmentType
    cost: float
    duration_months: int
    projected_value: float
    requires_eviction: bool
    environmental_impact: float  # 0-1 (1 = worst)
    affordable_units_pct: float  # 0-1
    contractor_id: Optional[str] = None
    months_remaining: int = 0
    started: bool = False
    completed: bool = False

    def to_dict(self):
        return {
            "id": self.id,
            "property_id": self.property_id,
            "type": self.type.value,
            "cost": self.cost,
            "duration_months": self.duration_months,
            "projected_value": self.projected_value,
            "requires_eviction": self.requires_eviction,
            "environmental_impact": self.environmental_impact,
            "affordable_units_pct": self.affordable_units_pct,
            "contractor_id": self.contractor_id,
            "months_remaining": self.months_remaining,
            "started": self.started,
            "completed": self.completed,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            id=d["id"],
            property_id=d["property_id"],
            type=DevelopmentType(d["type"]),
            cost=d["cost"],
            duration_months=d["duration_months"],
            projected_value=d["projected_value"],
            requires_eviction=d["requires_eviction"],
            environmental_impact=d["environmental_impact"],
            affordable_units_pct=d["affordable_units_pct"],
            contractor_id=d.get("contractor_id"),
            months_remaining=d.get("months_remaining", 0),
            started=d.get("started", False),
            completed=d.get("completed", False),
        )


@dataclass
class CityOfficial:
    """A city official who may offer corrupt deals."""
    id: str
    name: str
    role: str  # zoning, permits, inspections
    corrupt: bool
    bribe_amount: float
    controls: str  # what they control

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "corrupt": self.corrupt,
            "bribe_amount": self.bribe_amount,
            "controls": self.controls,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            id=d["id"],
            name=d["name"],
            role=d["role"],
            corrupt=d["corrupt"],
            bribe_amount=d["bribe_amount"],
            controls=d["controls"],
        )


@dataclass
class Contractor:
    """A construction contractor."""
    id: str
    name: str
    quality: int  # 0-100
    cost_multiplier: float  # 1.0 = standard
    uses_union_labor: bool
    environmental_compliance: bool
    cuts_corners: bool

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "quality": self.quality,
            "cost_multiplier": self.cost_multiplier,
            "uses_union_labor": self.uses_union_labor,
            "environmental_compliance": self.environmental_compliance,
            "cuts_corners": self.cuts_corners,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            id=d["id"],
            name=d["name"],
            quality=d["quality"],
            cost_multiplier=d["cost_multiplier"],
            uses_union_labor=d["uses_union_labor"],
            environmental_compliance=d["environmental_compliance"],
            cuts_corners=d["cuts_corners"],
        )


@dataclass
class Financials:
    """Financial state of the developer."""
    cash: float = 2000000.0
    total_portfolio_value: float = 0.0
    monthly_income: float = 0.0
    debt: float = 0.0
    mortgage_payments: float = 0.0

    def to_dict(self):
        return {
            "cash": self.cash,
            "total_portfolio_value": self.total_portfolio_value,
            "monthly_income": self.monthly_income,
            "debt": self.debt,
            "mortgage_payments": self.mortgage_payments,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            cash=d["cash"],
            total_portfolio_value=d["total_portfolio_value"],
            monthly_income=d["monthly_income"],
            debt=d["debt"],
            mortgage_payments=d["mortgage_payments"],
        )


@dataclass
class EthicalDilemma:
    """An ethical dilemma the developer faces at a specific month."""
    id: str
    type: DilemmaType
    description: str
    month: int
    temptation_action: str
    temptation_reward: str
    resolved: bool = False
    action_taken: Optional[str] = None

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type.value,
            "description": self.description,
            "month": self.month,
            "temptation_action": self.temptation_action,
            "temptation_reward": self.temptation_reward,
            "resolved": self.resolved,
            "action_taken": self.action_taken,
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
            resolved=d["resolved"],
            action_taken=d["action_taken"],
        )


@dataclass
class BuyoutOffer:
    """An offer to buy a property from the developer."""
    id: str
    property_id: str
    buyer_name: str
    amount: float
    requires_eviction: bool
    month: int
    description: str = ""
    accepted: bool = False
    rejected: bool = False

    def to_dict(self):
        return {
            "id": self.id,
            "property_id": self.property_id,
            "buyer_name": self.buyer_name,
            "amount": self.amount,
            "requires_eviction": self.requires_eviction,
            "month": self.month,
            "description": self.description,
            "accepted": self.accepted,
            "rejected": self.rejected,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            id=d["id"],
            property_id=d["property_id"],
            buyer_name=d["buyer_name"],
            amount=d["amount"],
            requires_eviction=d["requires_eviction"],
            month=d["month"],
            description=d.get("description", ""),
            accepted=d.get("accepted", False),
            rejected=d.get("rejected", False),
        )


@dataclass
class LoanOffer:
    """A loan available to the developer."""
    id: str
    amount: float
    interest_rate: float  # annual rate
    duration_months: int
    predatory: bool = False

    def to_dict(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "interest_rate": self.interest_rate,
            "duration_months": self.duration_months,
            "predatory": self.predatory,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            id=d["id"],
            amount=d["amount"],
            interest_rate=d["interest_rate"],
            duration_months=d["duration_months"],
            predatory=d.get("predatory", False),
        )
