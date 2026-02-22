"""Tests for simulations/film_studio/scenario_generator.py."""

import random
import pytest
from simulations.film_studio.scenario_generator import ScenarioGenerator


class TestScenarioGenerator:

    def test_deterministic_with_seed(self):
        rng1 = random.Random(42)
        rng2 = random.Random(42)
        gen1 = ScenarioGenerator(rng1)
        gen2 = ScenarioGenerator(rng2)
        pitches1 = gen1.generate_pitches_for_year(1, gen1.generate_directors())
        pitches2 = gen2.generate_pitches_for_year(1, gen2.generate_directors())
        assert len(pitches1) == len(pitches2)
        for p1, p2 in zip(pitches1, pitches2):
            assert p1.id == p2.id
            assert p1.title == p2.title

    def test_generate_directors(self):
        rng = random.Random(42)
        gen = ScenarioGenerator(rng)
        directors = gen.generate_directors()
        assert len(directors) == 15
        assert any(d.is_underrepresented for d in directors)
        assert any(not d.is_underrepresented for d in directors)

    def test_generate_pitches_count(self):
        rng = random.Random(42)
        gen = ScenarioGenerator(rng)
        dirs = gen.generate_directors()
        pitches = gen.generate_pitches_for_year(1, dirs)
        assert 5 <= len(pitches) <= 8

    def test_pitches_have_correct_ids(self):
        rng = random.Random(42)
        gen = ScenarioGenerator(rng)
        dirs = gen.generate_directors()
        pitches = gen.generate_pitches_for_year(3, dirs)
        for p in pitches:
            assert p.id.startswith("film_y3_")

    def test_pitches_mix_originals_and_sequels(self):
        rng = random.Random(42)
        gen = ScenarioGenerator(rng)
        dirs = gen.generate_directors()
        # Generate multiple years to ensure we get mix
        all_pitches = []
        for year in range(1, 6):
            all_pitches.extend(gen.generate_pitches_for_year(year, dirs))
        originals = [p for p in all_pitches if p.is_original]
        sequels = [p for p in all_pitches if p.is_sequel]
        assert len(originals) > 0
        assert len(sequels) > 0

    def test_pitches_have_valid_fields(self):
        rng = random.Random(42)
        gen = ScenarioGenerator(rng)
        dirs = gen.generate_directors()
        pitches = gen.generate_pitches_for_year(1, dirs)
        for p in pitches:
            assert 0 <= p.artistic_merit <= 100
            assert 0 <= p.representation_score <= 100
            assert 0 <= p.cast_diversity_score <= 100
            assert p.budget_millions > 0
            assert p.projected_box_office > 0
            assert p.status == "pitched"
            assert p.genre in ("drama", "comedy", "action", "horror",
                               "documentary", "indie")

    def test_generate_crew(self):
        rng = random.Random(42)
        gen = ScenarioGenerator(rng)
        crew = gen.generate_crew()
        assert "vfx" in crew
        assert "animation" in crew
        assert "production" in crew
        assert "post_production" in crew
        assert "marketing" in crew
        for dept, data in crew.items():
            assert data["headcount"] > 0
            assert data["avg_pay"] > 0
            assert data["morale"] > 0

    def test_generate_market_event(self):
        rng = random.Random(42)
        gen = ScenarioGenerator(rng)
        event = gen.generate_market_event(1)
        assert "type" in event
        assert "description" in event
        assert "effect" in event
        assert "year" in event
        assert event["year"] == 1

    def test_generate_harassment_reports(self):
        rng = random.Random(42)
        gen = ScenarioGenerator(rng)
        reports = gen.generate_harassment_reports()
        assert len(reports) == 3
        for r in reports:
            assert "id" in r
            assert "year" in r
            assert "accused" in r
            assert "description" in r

    def test_generate_ethical_dilemma(self):
        rng = random.Random(42)
        gen = ScenarioGenerator(rng)
        # Year 2 should have a dilemma
        dilemma = gen.generate_ethical_dilemma(2)
        assert dilemma is not None
        assert "type" in dilemma
        assert "description" in dilemma
        assert "temptation" in dilemma

    def test_no_dilemma_for_some_years(self):
        rng = random.Random(42)
        gen = ScenarioGenerator(rng)
        # Year 1, 3, 5, 7, 9, 10 should not have dilemmas
        assert gen.generate_ethical_dilemma(1) is None
        assert gen.generate_ethical_dilemma(3) is None
        assert gen.generate_ethical_dilemma(5) is None

    def test_different_seeds_different_results(self):
        rng1 = random.Random(42)
        rng2 = random.Random(99)
        gen1 = ScenarioGenerator(rng1)
        gen2 = ScenarioGenerator(rng2)
        dirs1 = gen1.generate_directors()
        dirs2 = gen2.generate_directors()
        p1 = gen1.generate_pitches_for_year(1, dirs1)
        p2 = gen2.generate_pitches_for_year(1, dirs2)
        # Very likely different (not guaranteed but practically always)
        titles1 = [p.title for p in p1]
        titles2 = [p.title for p in p2]
        # At least one should differ
        assert titles1 != titles2 or len(p1) != len(p2)
