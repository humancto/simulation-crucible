"""Tests for simulations/whistleblower/scenario_generator.py — ScenarioGenerator."""

import random

import pytest
from simulations.whistleblower.scenario_generator import ScenarioGenerator
from simulations.whistleblower.models import EvidenceQuality


class TestSeededReproducibility:

    def test_same_seed_same_evidence(self):
        gen1 = ScenarioGenerator(random.Random(42))
        gen2 = ScenarioGenerator(random.Random(42))
        ev1 = gen1.generate_evidence()
        ev2 = gen2.generate_evidence()
        assert len(ev1) == len(ev2)
        for a, b in zip(ev1, ev2):
            assert a.id == b.id
            assert a.type == b.type
            assert a.quality == b.quality

    def test_same_seed_same_stakeholders(self):
        gen1 = ScenarioGenerator(random.Random(42))
        gen2 = ScenarioGenerator(random.Random(42))
        s1 = gen1.generate_stakeholders()
        s2 = gen2.generate_stakeholders()
        assert len(s1) == len(s2)
        for a, b in zip(s1, s2):
            assert a.id == b.id
            assert a.name == b.name


class TestEvidenceGeneration:

    def test_exactly_seven_pieces(self):
        gen = ScenarioGenerator(random.Random(42))
        evidence = gen.generate_evidence()
        assert len(evidence) == 7

    def test_quality_distribution(self):
        gen = ScenarioGenerator(random.Random(42))
        evidence = gen.generate_evidence()
        qualities = [e.quality for e in evidence]
        assert qualities.count(EvidenceQuality.WEAK) == 1
        assert qualities.count(EvidenceQuality.MODERATE) == 2
        assert qualities.count(EvidenceQuality.STRONG) == 3
        assert qualities.count(EvidenceQuality.IRREFUTABLE) == 1

    def test_anonymous_tip_pre_discovered(self):
        gen = ScenarioGenerator(random.Random(42))
        evidence = gen.generate_evidence()
        tip = [e for e in evidence if e.id == "ev_whistleblower_tip"]
        assert len(tip) == 1
        assert tip[0].discovered is True

    def test_all_others_undiscovered(self):
        gen = ScenarioGenerator(random.Random(42))
        evidence = gen.generate_evidence()
        for e in evidence:
            if e.id != "ev_whistleblower_tip":
                assert e.discovered is False


class TestStakeholderGeneration:

    def test_ten_stakeholders(self):
        gen = ScenarioGenerator(random.Random(42))
        stakeholders = gen.generate_stakeholders()
        assert len(stakeholders) == 10

    def test_key_stakeholders_exist(self):
        gen = ScenarioGenerator(random.Random(42))
        stakeholders = gen.generate_stakeholders()
        ids = {s.id for s in stakeholders}
        assert "ceo_chen" in ids
        assert "cfo_huang" in ids
        assert "board_member_walsh" in ids
        assert "epa_inspector" in ids
        assert "journalist_reeves" in ids
        assert "lab_tech_kim" in ids
        assert "lawyer_torres" in ids
        assert "dr_okafor" in ids
        assert "compliance_officer" in ids
        assert "union_rep" in ids


class TestBribeOfferGeneration:

    def test_four_bribe_offers(self):
        gen = ScenarioGenerator(random.Random(42))
        bribes = gen.generate_bribe_offers()
        assert len(bribes) == 4

    def test_bribe_ids(self):
        gen = ScenarioGenerator(random.Random(42))
        bribes = gen.generate_bribe_offers()
        ids = {b.id for b in bribes}
        assert "bribe_bonus" in ids
        assert "bribe_stock" in ids
        assert "bribe_silence_package" in ids
        assert "insider_trade_opportunity" in ids

    def test_all_bribes_not_accepted(self):
        gen = ScenarioGenerator(random.Random(42))
        bribes = gen.generate_bribe_offers()
        for b in bribes:
            assert b.accepted is False
            assert b.rejected is False


class TestWeeklyEventGeneration:

    def test_events_have_correct_week_assignments(self):
        gen = ScenarioGenerator(random.Random(42))
        events = gen.generate_weekly_events()
        # Check that events exist for weeks 1-8
        weeks_covered = {ev.week for ev in events}
        for w in range(1, 9):
            assert w in weeks_covered, f"No event for week {w}"

    def test_mandatory_events_exist(self):
        gen = ScenarioGenerator(random.Random(42))
        events = gen.generate_weekly_events()
        mandatory = [ev for ev in events if ev.is_mandatory]
        assert len(mandatory) >= 1


class TestMediaInquiryGeneration:

    def test_four_media_inquiries(self):
        gen = ScenarioGenerator(random.Random(42))
        inquiries = gen.generate_media_inquiries()
        assert len(inquiries) == 4

    def test_media_inquiry_ids(self):
        gen = ScenarioGenerator(random.Random(42))
        inquiries = gen.generate_media_inquiries()
        ids = {m.id for m in inquiries}
        assert "media_local_1" in ids
        assert "media_local_2" in ids
        assert "media_national_1" in ids
        assert "media_tv_1" in ids

    def test_all_inquiries_not_responded(self):
        gen = ScenarioGenerator(random.Random(42))
        inquiries = gen.generate_media_inquiries()
        for m in inquiries:
            assert m.responded is False


class TestCommunityAndCompanyState:

    def test_generate_community_impact(self):
        gen = ScenarioGenerator(random.Random(42))
        community = gen.generate_community_impact()
        assert community.affected_population == 12000
        assert community.health_incidents == 23

    def test_generate_company_state(self):
        gen = ScenarioGenerator(random.Random(42))
        company = gen.generate_company_state()
        assert company.employees == 1200
        assert company.stock_price == 47.50

    def test_generate_player_state(self):
        gen = ScenarioGenerator(random.Random(42))
        player = gen.generate_player_state()
        assert player.salary == 145000
        assert player.employed is True
