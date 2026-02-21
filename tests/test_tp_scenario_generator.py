"""Tests for simulations/trolley_problem/scenario_generator.py."""

import random
import pytest
from simulations.trolley_problem.scenario_generator import ScenarioGenerator
from simulations.trolley_problem.models import (
    Scenario, ScenarioCategory, DifficultyLevel,
)


@pytest.fixture
def gen():
    return ScenarioGenerator(random.Random(42))


@pytest.fixture
def scenarios(gen):
    return gen.generate_scenarios()


# ── Generation ─────────────────────────────────────────────────────────

class TestGeneration:

    def test_generates_40_scenarios(self, scenarios):
        assert len(scenarios) == 40

    def test_all_are_scenario_objects(self, scenarios):
        for s in scenarios:
            assert isinstance(s, Scenario)

    def test_round_numbers_sequential(self, scenarios):
        for i, s in enumerate(scenarios):
            assert s.round_number == i + 1

    def test_ids_unique(self, scenarios):
        ids = [s.id for s in scenarios]
        assert len(ids) == len(set(ids))

    def test_ids_have_tp_prefix(self, scenarios):
        for s in scenarios:
            assert s.id.startswith("tp_")

    def test_deterministic_with_same_seed(self):
        g1 = ScenarioGenerator(random.Random(42))
        g2 = ScenarioGenerator(random.Random(42))
        s1 = g1.generate_scenarios()
        s2 = g2.generate_scenarios()
        for a, b in zip(s1, s2):
            assert a.id == b.id
            assert a.title == b.title

    def test_different_seeds_same_structure(self):
        g1 = ScenarioGenerator(random.Random(42))
        g2 = ScenarioGenerator(random.Random(99))
        s1 = g1.generate_scenarios()
        s2 = g2.generate_scenarios()
        assert len(s1) == len(s2) == 40
        # Same scenarios (hardcoded), same IDs
        for a, b in zip(s1, s2):
            assert a.id == b.id


# ── Categories ─────────────────────────────────────────────────────────

class TestCategories:

    def test_rounds_1_10_classic(self, scenarios):
        for s in scenarios[:10]:
            assert s.category == ScenarioCategory.CLASSIC_TROLLEY

    def test_rounds_11_20_medical(self, scenarios):
        for s in scenarios[10:20]:
            assert s.category == ScenarioCategory.MEDICAL_ETHICS

    def test_rounds_21_30_technology(self, scenarios):
        for s in scenarios[20:30]:
            assert s.category == ScenarioCategory.TECHNOLOGY_ETHICS

    def test_rounds_31_40_societal(self, scenarios):
        for s in scenarios[30:40]:
            assert s.category == ScenarioCategory.SOCIETAL_SCALE

    def test_all_four_categories_present(self, scenarios):
        cats = {s.category for s in scenarios}
        assert ScenarioCategory.CLASSIC_TROLLEY in cats
        assert ScenarioCategory.MEDICAL_ETHICS in cats
        assert ScenarioCategory.TECHNOLOGY_ETHICS in cats
        assert ScenarioCategory.SOCIETAL_SCALE in cats


# ── Scenario Content ──────────────────────────────────────────────────

class TestScenarioContent:

    def test_all_have_titles(self, scenarios):
        for s in scenarios:
            assert len(s.title) > 5

    def test_all_have_descriptions(self, scenarios):
        for s in scenarios:
            assert len(s.description) > 20

    def test_all_have_option_a(self, scenarios):
        for s in scenarios:
            assert len(s.option_a) > 5

    def test_all_have_option_b(self, scenarios):
        for s in scenarios:
            assert len(s.option_b) > 5

    def test_all_have_lives_at_stake(self, scenarios):
        for s in scenarios:
            assert s.lives_at_stake_a >= 0
            assert s.lives_at_stake_b >= 0

    def test_all_have_demographics_a(self, scenarios):
        for s in scenarios:
            assert s.demographics_a is not None
            assert s.demographics_a.count >= 0

    def test_all_have_demographics_b(self, scenarios):
        for s in scenarios:
            assert s.demographics_b is not None
            assert s.demographics_b.count >= 0

    def test_utilitarian_choice_valid(self, scenarios):
        for s in scenarios:
            assert s.utilitarian_choice in ("a", "b")

    def test_deontological_choice_valid(self, scenarios):
        for s in scenarios:
            assert s.deontological_choice in ("a", "b")

    def test_all_have_difficulty(self, scenarios):
        for s in scenarios:
            assert isinstance(s.difficulty, DifficultyLevel)

    def test_all_have_additional_info(self, scenarios):
        for s in scenarios:
            assert len(s.additional_info) > 0


# ── Difficulty Progression ────────────────────────────────────────────

class TestDifficultyProgression:

    def test_round_1_is_easy(self, scenarios):
        assert scenarios[0].difficulty == DifficultyLevel.EASY

    def test_early_rounds_not_extreme(self, scenarios):
        # First 3 should not be extreme
        for s in scenarios[:3]:
            assert s.difficulty != DifficultyLevel.EXTREME

    def test_has_extreme_difficulty(self, scenarios):
        extremes = [s for s in scenarios if s.difficulty == DifficultyLevel.EXTREME]
        assert len(extremes) >= 3

    def test_has_hard_difficulty(self, scenarios):
        hards = [s for s in scenarios if s.difficulty == DifficultyLevel.HARD]
        assert len(hards) >= 5

    def test_has_moderate_difficulty(self, scenarios):
        mods = [s for s in scenarios if s.difficulty == DifficultyLevel.MODERATE]
        assert len(mods) >= 3

    def test_has_easy_difficulty(self, scenarios):
        easies = [s for s in scenarios if s.difficulty == DifficultyLevel.EASY]
        assert len(easies) >= 2


# ── Specific Scenarios ─────────────────────────────────────────────────

class TestSpecificScenarios:

    def test_first_is_classic_switch(self, scenarios):
        assert scenarios[0].id == "tp_01"
        assert "switch" in scenarios[0].title.lower() or "classic" in scenarios[0].title.lower()

    def test_footbridge_exists(self, scenarios):
        titles = [s.title.lower() for s in scenarios]
        assert any("footbridge" in t for t in titles)

    def test_organ_harvest_exists(self, scenarios):
        descs = [s.description.lower() for s in scenarios]
        assert any("organ" in d for d in descs)

    def test_self_driving_car_exists(self, scenarios):
        titles = [s.title.lower() for s in scenarios]
        descs = [s.description.lower() for s in scenarios]
        assert any("self-driving" in t or "autonomous" in t for t in titles) or \
               any("autonomous" in d for d in descs)

    def test_pandemic_exists(self, scenarios):
        titles = [s.title.lower() for s in scenarios]
        assert any("pandemic" in t for t in titles)

    def test_last_scenario_is_round_40(self, scenarios):
        assert scenarios[-1].round_number == 40

    def test_scenario_10_exists(self, scenarios):
        s10 = [s for s in scenarios if s.round_number == 10]
        assert len(s10) == 1

    def test_scenario_20_exists(self, scenarios):
        s20 = [s for s in scenarios if s.round_number == 20]
        assert len(s20) == 1

    def test_scenario_30_exists(self, scenarios):
        s30 = [s for s in scenarios if s.round_number == 30]
        assert len(s30) == 1


# ── Demographics ──────────────────────────────────────────────────────

class TestDemographics:

    def test_classic_switch_workers(self, scenarios):
        s = scenarios[0]
        assert s.demographics_a.profession == "laborer"
        assert s.demographics_b.profession == "laborer"

    def test_some_have_vip_status(self, scenarios):
        has_vip = any(
            s.demographics_a.status == "vip" or s.demographics_b.status == "vip"
            for s in scenarios
        )
        assert has_vip

    def test_some_have_vulnerable_status(self, scenarios):
        has_vuln = any(
            s.demographics_a.status == "vulnerable" or s.demographics_b.status == "vulnerable"
            for s in scenarios
        )
        assert has_vuln

    def test_some_have_children(self, scenarios):
        has_child = any(
            s.demographics_a.age_group == "child" or s.demographics_b.age_group == "child"
            for s in scenarios
        )
        assert has_child

    def test_some_have_elderly(self, scenarios):
        has_elderly = any(
            s.demographics_a.age_group == "elderly" or s.demographics_b.age_group == "elderly"
            for s in scenarios
        )
        assert has_elderly

    def test_diverse_professions(self, scenarios):
        professions = set()
        for s in scenarios:
            professions.add(s.demographics_a.profession)
            professions.add(s.demographics_b.profession)
        assert len(professions) >= 5


# ── Serialization ─────────────────────────────────────────────────────

class TestSerialization:

    def test_all_scenarios_serialize(self, scenarios):
        for s in scenarios:
            d = s.to_dict()
            assert isinstance(d, dict)
            assert "id" in d

    def test_all_scenarios_roundtrip(self, scenarios):
        for s in scenarios:
            d = s.to_dict()
            restored = Scenario.from_dict(d)
            assert restored.id == s.id
            assert restored.title == s.title
            assert restored.category == s.category

    def test_demographics_survive_roundtrip(self, scenarios):
        for s in scenarios:
            d = s.to_dict()
            restored = Scenario.from_dict(d)
            assert restored.demographics_a.count == s.demographics_a.count
            assert restored.demographics_b.count == s.demographics_b.count
