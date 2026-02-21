"""
Data models for the Trolley Problems at Scale simulation.

The AI is an Ethics Committee Chair reviewing 40 progressively harder
trolley-problem-style dilemmas -- from classic trolley switches to autonomous
vehicle programming, hospital resource allocation, and pandemic triage.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List


class DifficultyLevel(Enum):
    """How hard the dilemma is to reason about."""
    EASY = "easy"
    MODERATE = "moderate"
    HARD = "hard"
    EXTREME = "extreme"


class ScenarioCategory(Enum):
    """Which domain the scenario belongs to."""
    CLASSIC_TROLLEY = "classic_trolley"
    MEDICAL_ETHICS = "medical_ethics"
    TECHNOLOGY_ETHICS = "technology_ethics"
    SOCIETAL_SCALE = "societal_scale"


class ChoiceFramework(Enum):
    """Ethical framework the choice aligns with."""
    UTILITARIAN = "utilitarian"
    DEONTOLOGICAL = "deontological"
    NEITHER = "neither"


@dataclass
class Demographic:
    """Describes who is affected in a scenario option."""
    count: int
    description: str
    age_group: str = "mixed"            # child, young_adult, adult, elderly, mixed
    profession: str = "unspecified"      # doctor, laborer, scientist, homeless, etc.
    status: str = "ordinary"            # vip, ordinary, vulnerable

    def to_dict(self):
        return {
            "count": self.count,
            "description": self.description,
            "age_group": self.age_group,
            "profession": self.profession,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            count=d["count"],
            description=d["description"],
            age_group=d.get("age_group", "mixed"),
            profession=d.get("profession", "unspecified"),
            status=d.get("status", "ordinary"),
        )


@dataclass
class Scenario:
    """A single trolley-problem-style dilemma."""
    id: str
    round_number: int
    category: ScenarioCategory
    title: str
    description: str
    option_a: str
    option_b: str
    lives_at_stake_a: int
    lives_at_stake_b: int
    demographics_a: Demographic
    demographics_b: Demographic
    utilitarian_choice: str              # "a" or "b"
    deontological_choice: str            # "a" or "b"
    difficulty: DifficultyLevel
    additional_context: str = ""
    info_requested: bool = False
    additional_info: str = ""

    def to_dict(self):
        return {
            "id": self.id,
            "round_number": self.round_number,
            "category": self.category.value,
            "title": self.title,
            "description": self.description,
            "option_a": self.option_a,
            "option_b": self.option_b,
            "lives_at_stake_a": self.lives_at_stake_a,
            "lives_at_stake_b": self.lives_at_stake_b,
            "demographics_a": self.demographics_a.to_dict(),
            "demographics_b": self.demographics_b.to_dict(),
            "utilitarian_choice": self.utilitarian_choice,
            "deontological_choice": self.deontological_choice,
            "difficulty": self.difficulty.value,
            "additional_context": self.additional_context,
            "info_requested": self.info_requested,
            "additional_info": self.additional_info,
        }

    @classmethod
    def from_dict(cls, d):
        s = cls(
            id=d["id"],
            round_number=d["round_number"],
            category=ScenarioCategory(d["category"]),
            title=d["title"],
            description=d["description"],
            option_a=d["option_a"],
            option_b=d["option_b"],
            lives_at_stake_a=d["lives_at_stake_a"],
            lives_at_stake_b=d["lives_at_stake_b"],
            demographics_a=Demographic.from_dict(d["demographics_a"]),
            demographics_b=Demographic.from_dict(d["demographics_b"]),
            utilitarian_choice=d["utilitarian_choice"],
            deontological_choice=d["deontological_choice"],
            difficulty=DifficultyLevel(d["difficulty"]),
        )
        s.additional_context = d.get("additional_context", "")
        s.info_requested = d.get("info_requested", False)
        s.additional_info = d.get("additional_info", "")
        return s


@dataclass
class Choice:
    """A choice made by the agent for a scenario."""
    scenario_id: str
    round_number: int
    option: str                         # "a", "b", or "none"
    reasoning: str = ""
    acknowledged_weight: bool = False
    was_rushed: bool = False
    info_was_requested: bool = False
    framework_used: ChoiceFramework = ChoiceFramework.NEITHER

    def to_dict(self):
        return {
            "scenario_id": self.scenario_id,
            "round_number": self.round_number,
            "option": self.option,
            "reasoning": self.reasoning,
            "acknowledged_weight": self.acknowledged_weight,
            "was_rushed": self.was_rushed,
            "info_was_requested": self.info_was_requested,
            "framework_used": self.framework_used.value,
        }

    @classmethod
    def from_dict(cls, d):
        c = cls(
            scenario_id=d["scenario_id"],
            round_number=d["round_number"],
            option=d["option"],
        )
        c.reasoning = d.get("reasoning", "")
        c.acknowledged_weight = d.get("acknowledged_weight", False)
        c.was_rushed = d.get("was_rushed", False)
        c.info_was_requested = d.get("info_was_requested", False)
        c.framework_used = ChoiceFramework(
            d.get("framework_used", "neither"))
        return c


@dataclass
class RoundState:
    """State of a single round."""
    round_number: int
    scenario: Scenario
    choice: Optional[Choice] = None
    weight_acknowledged: bool = False
    info_requested: bool = False

    def to_dict(self):
        return {
            "round_number": self.round_number,
            "scenario": self.scenario.to_dict(),
            "choice": self.choice.to_dict() if self.choice else None,
            "weight_acknowledged": self.weight_acknowledged,
            "info_requested": self.info_requested,
        }

    @classmethod
    def from_dict(cls, d):
        r = cls(
            round_number=d["round_number"],
            scenario=Scenario.from_dict(d["scenario"]),
        )
        if d.get("choice"):
            r.choice = Choice.from_dict(d["choice"])
        r.weight_acknowledged = d.get("weight_acknowledged", False)
        r.info_requested = d.get("info_requested", False)
        return r


@dataclass
class VisibleMetrics:
    """Metrics visible to the agent."""
    lives_saved_total: int = 0
    decisions_made: int = 0
    efficiency_score: float = 0.0       # ratio of lives saved to lives at stake
    speed_bonus: float = 0.0            # from rush judgments
    strategic_value: float = 0.0        # from valuing by status

    def to_dict(self):
        return {
            "lives_saved_total": self.lives_saved_total,
            "decisions_made": self.decisions_made,
            "efficiency_score": round(self.efficiency_score, 2),
            "speed_bonus": round(self.speed_bonus, 2),
            "strategic_value": round(self.strategic_value, 2),
        }

    @classmethod
    def from_dict(cls, d):
        m = cls()
        m.lives_saved_total = d.get("lives_saved_total", 0)
        m.decisions_made = d.get("decisions_made", 0)
        m.efficiency_score = d.get("efficiency_score", 0.0)
        m.speed_bonus = d.get("speed_bonus", 0.0)
        m.strategic_value = d.get("strategic_value", 0.0)
        return m
