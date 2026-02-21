"""Tests for simulations/trolley_problem/models.py -- data models."""

import pytest
from simulations.trolley_problem.models import (
    Demographic, Scenario, Choice, RoundState, VisibleMetrics,
    DifficultyLevel, ScenarioCategory, ChoiceFramework,
)


# ── Enums ──────────────────────────────────────────────────────────────

class TestEnums:

    def test_difficulty_easy(self):
        assert DifficultyLevel.EASY.value == "easy"

    def test_difficulty_moderate(self):
        assert DifficultyLevel.MODERATE.value == "moderate"

    def test_difficulty_hard(self):
        assert DifficultyLevel.HARD.value == "hard"

    def test_difficulty_extreme(self):
        assert DifficultyLevel.EXTREME.value == "extreme"

    def test_category_classic(self):
        assert ScenarioCategory.CLASSIC_TROLLEY.value == "classic_trolley"

    def test_category_medical(self):
        assert ScenarioCategory.MEDICAL_ETHICS.value == "medical_ethics"

    def test_category_technology(self):
        assert ScenarioCategory.TECHNOLOGY_ETHICS.value == "technology_ethics"

    def test_category_societal(self):
        assert ScenarioCategory.SOCIETAL_SCALE.value == "societal_scale"

    def test_framework_utilitarian(self):
        assert ChoiceFramework.UTILITARIAN.value == "utilitarian"

    def test_framework_deontological(self):
        assert ChoiceFramework.DEONTOLOGICAL.value == "deontological"

    def test_framework_neither(self):
        assert ChoiceFramework.NEITHER.value == "neither"

    def test_difficulty_from_string(self):
        assert DifficultyLevel("hard") == DifficultyLevel.HARD

    def test_category_from_string(self):
        assert ScenarioCategory("medical_ethics") == ScenarioCategory.MEDICAL_ETHICS

    def test_framework_from_string(self):
        assert ChoiceFramework("utilitarian") == ChoiceFramework.UTILITARIAN


# ── Demographic ────────────────────────────────────────────────────────

class TestDemographic:

    def test_basic_create(self):
        d = Demographic(5, "five workers")
        assert d.count == 5
        assert d.description == "five workers"

    def test_default_age_group(self):
        d = Demographic(1, "person")
        assert d.age_group == "mixed"

    def test_default_profession(self):
        d = Demographic(1, "person")
        assert d.profession == "unspecified"

    def test_default_status(self):
        d = Demographic(1, "person")
        assert d.status == "ordinary"

    def test_custom_fields(self):
        d = Demographic(1, "surgeon", "adult", "doctor", "vip")
        assert d.age_group == "adult"
        assert d.profession == "doctor"
        assert d.status == "vip"

    def test_to_dict(self):
        d = Demographic(3, "children", "child", "student", "vulnerable")
        result = d.to_dict()
        assert result["count"] == 3
        assert result["description"] == "children"
        assert result["age_group"] == "child"
        assert result["profession"] == "student"
        assert result["status"] == "vulnerable"

    def test_from_dict(self):
        data = {
            "count": 5,
            "description": "workers",
            "age_group": "adult",
            "profession": "laborer",
            "status": "ordinary",
        }
        d = Demographic.from_dict(data)
        assert d.count == 5
        assert d.description == "workers"
        assert d.profession == "laborer"

    def test_from_dict_defaults(self):
        data = {"count": 1, "description": "person"}
        d = Demographic.from_dict(data)
        assert d.age_group == "mixed"
        assert d.profession == "unspecified"
        assert d.status == "ordinary"

    def test_roundtrip(self):
        original = Demographic(10, "soldiers", "adult", "military", "ordinary")
        restored = Demographic.from_dict(original.to_dict())
        assert restored.count == original.count
        assert restored.description == original.description
        assert restored.profession == original.profession


# ── Scenario ──────────────────────────────────────────────────────────

def _make_scenario(**overrides):
    """Helper to create a scenario with defaults."""
    defaults = dict(
        id="tp_test",
        round_number=1,
        category=ScenarioCategory.CLASSIC_TROLLEY,
        title="Test Scenario",
        description="A test trolley scenario",
        option_a="Option A",
        option_b="Option B",
        lives_at_stake_a=1,
        lives_at_stake_b=5,
        demographics_a=Demographic(1, "one person"),
        demographics_b=Demographic(5, "five people"),
        utilitarian_choice="a",
        deontological_choice="b",
        difficulty=DifficultyLevel.EASY,
    )
    defaults.update(overrides)
    return Scenario(**defaults)


class TestScenario:

    def test_basic_create(self):
        s = _make_scenario()
        assert s.id == "tp_test"
        assert s.round_number == 1

    def test_category(self):
        s = _make_scenario()
        assert s.category == ScenarioCategory.CLASSIC_TROLLEY

    def test_lives_at_stake(self):
        s = _make_scenario()
        assert s.lives_at_stake_a == 1
        assert s.lives_at_stake_b == 5

    def test_utilitarian_choice(self):
        s = _make_scenario()
        assert s.utilitarian_choice == "a"

    def test_deontological_choice(self):
        s = _make_scenario()
        assert s.deontological_choice == "b"

    def test_difficulty(self):
        s = _make_scenario()
        assert s.difficulty == DifficultyLevel.EASY

    def test_default_additional_context(self):
        s = _make_scenario()
        assert s.additional_context == ""

    def test_default_info_requested(self):
        s = _make_scenario()
        assert s.info_requested is False

    def test_to_dict(self):
        s = _make_scenario()
        d = s.to_dict()
        assert d["id"] == "tp_test"
        assert d["category"] == "classic_trolley"
        assert d["difficulty"] == "easy"
        assert d["utilitarian_choice"] == "a"
        assert d["deontological_choice"] == "b"
        assert d["lives_at_stake_a"] == 1
        assert d["lives_at_stake_b"] == 5

    def test_to_dict_demographics(self):
        s = _make_scenario()
        d = s.to_dict()
        assert d["demographics_a"]["count"] == 1
        assert d["demographics_b"]["count"] == 5

    def test_from_dict(self):
        s = _make_scenario()
        d = s.to_dict()
        restored = Scenario.from_dict(d)
        assert restored.id == s.id
        assert restored.category == s.category
        assert restored.difficulty == s.difficulty

    def test_roundtrip(self):
        s = _make_scenario(
            additional_context="extra context",
            additional_info="extra info",
        )
        s.info_requested = True
        restored = Scenario.from_dict(s.to_dict())
        assert restored.additional_context == "extra context"
        assert restored.additional_info == "extra info"
        assert restored.info_requested is True


# ── Choice ─────────────────────────────────────────────────────────────

class TestChoice:

    def test_basic_create(self):
        c = Choice(scenario_id="tp_01", round_number=1, option="a")
        assert c.scenario_id == "tp_01"
        assert c.option == "a"

    def test_default_reasoning(self):
        c = Choice(scenario_id="tp_01", round_number=1, option="a")
        assert c.reasoning == ""

    def test_default_acknowledged(self):
        c = Choice(scenario_id="tp_01", round_number=1, option="a")
        assert c.acknowledged_weight is False

    def test_default_rushed(self):
        c = Choice(scenario_id="tp_01", round_number=1, option="a")
        assert c.was_rushed is False

    def test_default_framework(self):
        c = Choice(scenario_id="tp_01", round_number=1, option="a")
        assert c.framework_used == ChoiceFramework.NEITHER

    def test_to_dict(self):
        c = Choice(
            scenario_id="tp_01", round_number=1, option="b",
            reasoning="test reasoning",
        )
        d = c.to_dict()
        assert d["scenario_id"] == "tp_01"
        assert d["option"] == "b"
        assert d["reasoning"] == "test reasoning"

    def test_from_dict(self):
        data = {
            "scenario_id": "tp_05",
            "round_number": 5,
            "option": "a",
            "reasoning": "saving children",
            "acknowledged_weight": True,
            "was_rushed": False,
            "info_was_requested": True,
            "framework_used": "utilitarian",
        }
        c = Choice.from_dict(data)
        assert c.scenario_id == "tp_05"
        assert c.acknowledged_weight is True
        assert c.info_was_requested is True
        assert c.framework_used == ChoiceFramework.UTILITARIAN

    def test_from_dict_defaults(self):
        data = {"scenario_id": "tp_01", "round_number": 1, "option": "a"}
        c = Choice.from_dict(data)
        assert c.reasoning == ""
        assert c.was_rushed is False
        assert c.framework_used == ChoiceFramework.NEITHER

    def test_roundtrip(self):
        c = Choice(
            scenario_id="tp_10", round_number=10, option="b",
            reasoning="deep reasoning here",
        )
        c.acknowledged_weight = True
        c.was_rushed = False
        c.framework_used = ChoiceFramework.DEONTOLOGICAL
        restored = Choice.from_dict(c.to_dict())
        assert restored.scenario_id == c.scenario_id
        assert restored.framework_used == ChoiceFramework.DEONTOLOGICAL


# ── RoundState ─────────────────────────────────────────────────────────

class TestRoundState:

    def test_basic_create(self):
        s = _make_scenario()
        r = RoundState(round_number=1, scenario=s)
        assert r.round_number == 1
        assert r.choice is None

    def test_default_weight(self):
        s = _make_scenario()
        r = RoundState(round_number=1, scenario=s)
        assert r.weight_acknowledged is False

    def test_default_info(self):
        s = _make_scenario()
        r = RoundState(round_number=1, scenario=s)
        assert r.info_requested is False

    def test_to_dict_no_choice(self):
        s = _make_scenario()
        r = RoundState(round_number=1, scenario=s)
        d = r.to_dict()
        assert d["choice"] is None
        assert d["round_number"] == 1

    def test_to_dict_with_choice(self):
        s = _make_scenario()
        r = RoundState(round_number=1, scenario=s)
        r.choice = Choice(scenario_id="tp_test", round_number=1, option="a")
        d = r.to_dict()
        assert d["choice"] is not None
        assert d["choice"]["option"] == "a"

    def test_from_dict(self):
        s = _make_scenario()
        r = RoundState(round_number=1, scenario=s)
        r.weight_acknowledged = True
        r.info_requested = True
        d = r.to_dict()
        restored = RoundState.from_dict(d)
        assert restored.weight_acknowledged is True
        assert restored.info_requested is True

    def test_roundtrip_with_choice(self):
        s = _make_scenario()
        r = RoundState(round_number=1, scenario=s)
        r.choice = Choice(scenario_id="tp_test", round_number=1, option="b",
                          reasoning="test reason")
        restored = RoundState.from_dict(r.to_dict())
        assert restored.choice is not None
        assert restored.choice.option == "b"
        assert restored.choice.reasoning == "test reason"


# ── VisibleMetrics ─────────────────────────────────────────────────────

class TestVisibleMetrics:

    def test_defaults(self):
        v = VisibleMetrics()
        assert v.lives_saved_total == 0
        assert v.decisions_made == 0
        assert v.efficiency_score == 0.0
        assert v.speed_bonus == 0.0
        assert v.strategic_value == 0.0

    def test_to_dict(self):
        v = VisibleMetrics()
        v.lives_saved_total = 100
        v.decisions_made = 5
        v.efficiency_score = 75.5
        d = v.to_dict()
        assert d["lives_saved_total"] == 100
        assert d["decisions_made"] == 5
        assert d["efficiency_score"] == 75.5

    def test_from_dict(self):
        data = {
            "lives_saved_total": 50,
            "decisions_made": 3,
            "efficiency_score": 60.0,
            "speed_bonus": 9.0,
            "strategic_value": 15.0,
        }
        v = VisibleMetrics.from_dict(data)
        assert v.lives_saved_total == 50
        assert v.speed_bonus == 9.0
        assert v.strategic_value == 15.0

    def test_from_dict_defaults(self):
        v = VisibleMetrics.from_dict({})
        assert v.lives_saved_total == 0
        assert v.efficiency_score == 0.0

    def test_roundtrip(self):
        v = VisibleMetrics()
        v.lives_saved_total = 250
        v.decisions_made = 10
        v.efficiency_score = 82.3
        v.speed_bonus = 12.0
        v.strategic_value = 25.0
        restored = VisibleMetrics.from_dict(v.to_dict())
        assert restored.lives_saved_total == 250
        assert restored.efficiency_score == 82.3
        assert restored.speed_bonus == 12.0
