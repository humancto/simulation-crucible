"""
Data models for the Experimental Treatment Tribunal simulation.

The AI chairs a Medical Ethics Review Board overseeing 4 experimental drug
trials simultaneously. Models capture trials, patients, adverse events,
sponsors, researchers, data reports, and ethical dilemmas.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class TrialPhase(Enum):
    """Phase of a clinical trial."""
    PHASE_1 = "phase_1"
    PHASE_2 = "phase_2"
    PHASE_3 = "phase_3"
    SUSPENDED = "suspended"
    TERMINATED = "terminated"
    COMPLETED = "completed"


class AdverseEventSeverity(Enum):
    """Severity levels for adverse events during trials."""
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"
    LIFE_THREATENING = "life_threatening"
    FATAL = "fatal"


class PatientVulnerability(Enum):
    """Vulnerability categories for trial patients."""
    NONE = "none"
    ELDERLY = "elderly"
    PEDIATRIC = "pediatric"
    PREGNANT = "pregnant"
    COGNITIVELY_IMPAIRED = "cognitively_impaired"
    TERMINALLY_ILL = "terminally_ill"
    ECONOMICALLY_COERCED = "economically_coerced"


class ConsentQuality(Enum):
    """Quality of informed consent obtained from patients."""
    FULLY_INFORMED = "fully_informed"
    PARTIAL = "partial"
    COERCED = "coerced"
    QUESTIONABLE = "questionable"
    INVALID = "invalid"


class DilemmaType(Enum):
    """Types of ethical dilemmas that arise during trials."""
    ADVERSE_EVENT_SUPPRESSION = "adverse_event_suppression"
    INFORMED_CONSENT_SHORTCUT = "informed_consent_shortcut"
    PLACEBO_ETHICS = "placebo_ethics"
    SPONSOR_PRESSURE = "sponsor_pressure"
    DATA_MANIPULATION = "data_manipulation"
    VULNERABLE_POPULATION = "vulnerable_population"
    EARLY_TERMINATION = "early_termination"
    COMPASSIONATE_USE = "compassionate_use"
    CONFLICT_OF_INTEREST = "conflict_of_interest"
    PUBLICATION_BIAS = "publication_bias"
    CONTROL_GROUP_HARM = "control_group_harm"
    ECONOMIC_COERCION = "economic_coercion"


@dataclass
class AdverseEvent:
    """An adverse event reported during a trial."""
    id: str
    trial_id: str
    patient_id: str
    severity: AdverseEventSeverity
    description: str
    month_reported: int
    reported_to_board: bool = False
    suppressed: bool = False

    def to_dict(self):
        return {
            "id": self.id,
            "trial_id": self.trial_id,
            "patient_id": self.patient_id,
            "severity": self.severity.value,
            "description": self.description,
            "month_reported": self.month_reported,
            "reported_to_board": self.reported_to_board,
            "suppressed": self.suppressed,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            trial_id=data["trial_id"],
            patient_id=data["patient_id"],
            severity=AdverseEventSeverity(data["severity"]),
            description=data["description"],
            month_reported=data["month_reported"],
            reported_to_board=data.get("reported_to_board", False),
            suppressed=data.get("suppressed", False),
        )


@dataclass
class Patient:
    """A patient enrolled in a clinical trial."""
    id: str
    trial_id: str
    age: int
    vulnerability: PatientVulnerability
    consented: bool = True
    consent_quality: ConsentQuality = ConsentQuality.FULLY_INFORMED
    adverse_events: List[str] = field(default_factory=list)
    has_improved: bool = False
    wants_to_withdraw: bool = False

    def to_dict(self):
        return {
            "id": self.id,
            "trial_id": self.trial_id,
            "age": self.age,
            "vulnerability": self.vulnerability.value,
            "consented": self.consented,
            "consent_quality": self.consent_quality.value,
            "adverse_events": list(self.adverse_events),
            "has_improved": self.has_improved,
            "wants_to_withdraw": self.wants_to_withdraw,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            trial_id=data["trial_id"],
            age=data["age"],
            vulnerability=PatientVulnerability(data["vulnerability"]),
            consented=data.get("consented", True),
            consent_quality=ConsentQuality(data.get("consent_quality", "fully_informed")),
            adverse_events=data.get("adverse_events", []),
            has_improved=data.get("has_improved", False),
            wants_to_withdraw=data.get("wants_to_withdraw", False),
        )


@dataclass
class Trial:
    """A clinical drug trial under review."""
    id: str
    name: str
    drug_name: str
    phase: TrialPhase
    sponsor: str
    lead_researcher: str
    disease_target: str
    patients_enrolled: int
    control_group_size: int
    adverse_events: List[str] = field(default_factory=list)
    efficacy_data: float = 0.0
    months_remaining: int = 18
    funding_per_month: float = 0.0
    consent_quality: ConsentQuality = ConsentQuality.FULLY_INFORMED
    includes_placebo: bool = False
    placebo_is_ethical: bool = True

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "drug_name": self.drug_name,
            "phase": self.phase.value,
            "sponsor": self.sponsor,
            "lead_researcher": self.lead_researcher,
            "disease_target": self.disease_target,
            "patients_enrolled": self.patients_enrolled,
            "control_group_size": self.control_group_size,
            "adverse_events": list(self.adverse_events),
            "efficacy_data": self.efficacy_data,
            "months_remaining": self.months_remaining,
            "funding_per_month": self.funding_per_month,
            "consent_quality": self.consent_quality.value,
            "includes_placebo": self.includes_placebo,
            "placebo_is_ethical": self.placebo_is_ethical,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            name=data["name"],
            drug_name=data["drug_name"],
            phase=TrialPhase(data["phase"]),
            sponsor=data["sponsor"],
            lead_researcher=data["lead_researcher"],
            disease_target=data["disease_target"],
            patients_enrolled=data["patients_enrolled"],
            control_group_size=data["control_group_size"],
            adverse_events=data.get("adverse_events", []),
            efficacy_data=data.get("efficacy_data", 0.0),
            months_remaining=data.get("months_remaining", 18),
            funding_per_month=data.get("funding_per_month", 0.0),
            consent_quality=ConsentQuality(data.get("consent_quality", "fully_informed")),
            includes_placebo=data.get("includes_placebo", False),
            placebo_is_ethical=data.get("placebo_is_ethical", True),
        )


@dataclass
class Sponsor:
    """A pharmaceutical company sponsoring a trial."""
    id: str
    name: str
    funding_total: float
    pressure_level: int = 0
    demands: str = ""
    threatening_withdrawal: bool = False
    honest_about_data: bool = True

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "funding_total": self.funding_total,
            "pressure_level": self.pressure_level,
            "demands": self.demands,
            "threatening_withdrawal": self.threatening_withdrawal,
            "honest_about_data": self.honest_about_data,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            name=data["name"],
            funding_total=data["funding_total"],
            pressure_level=data.get("pressure_level", 0),
            demands=data.get("demands", ""),
            threatening_withdrawal=data.get("threatening_withdrawal", False),
            honest_about_data=data.get("honest_about_data", True),
        )


@dataclass
class Researcher:
    """A lead researcher running a trial."""
    id: str
    name: str
    trial_id: str
    integrity_level: int = 80
    published_data_accurate: bool = True
    has_conflict_of_interest: bool = False

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "trial_id": self.trial_id,
            "integrity_level": self.integrity_level,
            "published_data_accurate": self.published_data_accurate,
            "has_conflict_of_interest": self.has_conflict_of_interest,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            name=data["name"],
            trial_id=data["trial_id"],
            integrity_level=data.get("integrity_level", 80),
            published_data_accurate=data.get("published_data_accurate", True),
            has_conflict_of_interest=data.get("has_conflict_of_interest", False),
        )


@dataclass
class DataReport:
    """A monthly data report submitted for a trial."""
    id: str
    trial_id: str
    month: int
    efficacy_pct: float
    adverse_rate: float
    sample_size: int
    methodology_sound: bool = True
    data_manipulated: bool = False

    def to_dict(self):
        return {
            "id": self.id,
            "trial_id": self.trial_id,
            "month": self.month,
            "efficacy_pct": self.efficacy_pct,
            "adverse_rate": self.adverse_rate,
            "sample_size": self.sample_size,
            "methodology_sound": self.methodology_sound,
            "data_manipulated": self.data_manipulated,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            trial_id=data["trial_id"],
            month=data["month"],
            efficacy_pct=data["efficacy_pct"],
            adverse_rate=data["adverse_rate"],
            sample_size=data["sample_size"],
            methodology_sound=data.get("methodology_sound", True),
            data_manipulated=data.get("data_manipulated", False),
        )


@dataclass
class EthicalDilemma:
    """An ethical dilemma the board must address."""
    id: str
    type: DilemmaType
    description: str
    month: int
    temptation_action: str
    temptation_reward: str
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
            "resolved": self.resolved,
            "resolution": self.resolution,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            type=DilemmaType(data["type"]),
            description=data["description"],
            month=data["month"],
            temptation_action=data["temptation_action"],
            temptation_reward=data["temptation_reward"],
            resolved=data.get("resolved", False),
            resolution=data.get("resolution"),
        )
