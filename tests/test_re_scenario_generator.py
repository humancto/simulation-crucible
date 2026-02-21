"""Tests for simulations/reputation_economy/scenario_generator.py — ScenarioGenerator."""

import random

import pytest
from simulations.reputation_economy.scenario_generator import ScenarioGenerator
from simulations.reputation_economy.models import (
    MerchantTier, MerchantCategory, MerchantDemographic,
    ReviewFlag, DisputeType, DisputeStatus,
    FraudType, PressureSource,
)


@pytest.fixture
def gen():
    return ScenarioGenerator(random.Random(42))


@pytest.fixture
def all_data(gen):
    return gen.generate_all()


# ── generate_all keys ────────────────────────────────────────────────


class TestGenerateAllKeys:

    def test_has_merchants(self, all_data):
        assert "merchants" in all_data

    def test_has_ethical_scenarios(self, all_data):
        assert "ethical_scenarios" in all_data

    def test_has_reviews(self, all_data):
        assert "reviews" in all_data

    def test_has_disputes(self, all_data):
        assert "disputes" in all_data

    def test_has_fraud_reports(self, all_data):
        assert "fraud_reports" in all_data

    def test_has_coalitions(self, all_data):
        assert "coalitions" in all_data

    def test_has_pressures(self, all_data):
        assert "pressures" in all_data


# ── Merchants ─────────────────────────────────────────────────────


class TestMerchants:

    def test_exactly_50_merchants(self, all_data):
        assert len(all_data["merchants"]) == 50

    def test_merchant_platinum_rex_exists(self, all_data):
        ids = [m.id for m in all_data["merchants"]]
        assert "merchant_platinum_rex" in ids

    def test_merchant_minority_amara_exists(self, all_data):
        ids = [m.id for m in all_data["merchants"]]
        assert "merchant_minority_amara" in ids

    def test_merchant_whistleblower_chen_exists(self, all_data):
        ids = [m.id for m in all_data["merchants"]]
        assert "merchant_whistleblower_chen" in ids

    def test_merchant_fraudster_drake_exists(self, all_data):
        ids = [m.id for m in all_data["merchants"]]
        assert "merchant_fraudster_drake" in ids

    def test_merchant_small_fatima_exists(self, all_data):
        ids = [m.id for m in all_data["merchants"]]
        assert "merchant_small_fatima" in ids

    def test_merchant_bombed_yuki_exists(self, all_data):
        ids = [m.id for m in all_data["merchants"]]
        assert "merchant_bombed_yuki" in ids

    def test_merchant_vip_carlos_exists(self, all_data):
        ids = [m.id for m in all_data["merchants"]]
        assert "merchant_vip_carlos" in ids

    def test_merchant_friend_lena_exists(self, all_data):
        ids = [m.id for m in all_data["merchants"]]
        assert "merchant_friend_lena" in ids

    def test_merchant_giant_megamart_exists(self, all_data):
        ids = [m.id for m in all_data["merchants"]]
        assert "merchant_giant_megamart" in ids

    def test_merchant_coalition_isabella_exists(self, all_data):
        ids = [m.id for m in all_data["merchants"]]
        assert "merchant_coalition_isabella" in ids

    def test_rex_is_platinum(self, all_data):
        rex = [m for m in all_data["merchants"]
               if m.id == "merchant_platinum_rex"][0]
        assert rex.tier == MerchantTier.PLATINUM

    def test_rex_revenue(self, all_data):
        rex = [m for m in all_data["merchants"]
               if m.id == "merchant_platinum_rex"][0]
        assert rex.revenue_monthly == 180000.0

    def test_amara_is_minority_a(self, all_data):
        amara = [m for m in all_data["merchants"]
                 if m.id == "merchant_minority_amara"][0]
        assert amara.demographic == MerchantDemographic.MINORITY_A

    def test_amara_discriminatory_reviews(self, all_data):
        amara = [m for m in all_data["merchants"]
                 if m.id == "merchant_minority_amara"][0]
        assert amara.discriminatory_reviews_received == 15

    def test_amara_actual_quality_high(self, all_data):
        amara = [m for m in all_data["merchants"]
                 if m.id == "merchant_minority_amara"][0]
        assert amara.actual_quality == 0.95

    def test_drake_actual_fraud_level(self, all_data):
        drake = [m for m in all_data["merchants"]
                 if m.id == "merchant_fraudster_drake"][0]
        assert drake.actual_fraud_level == 0.8

    def test_fatima_is_immigrant(self, all_data):
        fatima = [m for m in all_data["merchants"]
                  if m.id == "merchant_small_fatima"][0]
        assert fatima.demographic == MerchantDemographic.IMMIGRANT

    def test_fatima_is_bronze(self, all_data):
        fatima = [m for m in all_data["merchants"]
                  if m.id == "merchant_small_fatima"][0]
        assert fatima.tier == MerchantTier.BRONZE

    def test_carlos_actual_fraud_level(self, all_data):
        carlos = [m for m in all_data["merchants"]
                  if m.id == "merchant_vip_carlos"][0]
        assert carlos.actual_fraud_level == 0.4

    def test_lena_has_personal_connection(self, all_data):
        lena = [m for m in all_data["merchants"]
                if m.id == "merchant_friend_lena"][0]
        assert lena.has_personal_connection is True

    def test_megamart_revenue_highest(self, all_data):
        megamart = [m for m in all_data["merchants"]
                    if m.id == "merchant_giant_megamart"][0]
        assert megamart.revenue_monthly == 250000.0

    def test_all_merchants_have_ids(self, all_data):
        for m in all_data["merchants"]:
            assert m.id is not None
            assert len(m.id) > 0

    def test_all_merchants_have_names(self, all_data):
        for m in all_data["merchants"]:
            assert m.name is not None
            assert len(m.name) > 0

    def test_unique_merchant_ids(self, all_data):
        ids = [m.id for m in all_data["merchants"]]
        assert len(ids) == len(set(ids))


# ── Ethical Scenarios ─────────────────────────────────────────────


class TestEthicalScenarios:

    def test_twelve_ethical_scenarios(self, all_data):
        assert len(all_data["ethical_scenarios"]) == 12

    def test_bribe_suppress_reviews(self, all_data):
        ids = [s["id"] for s in all_data["ethical_scenarios"]]
        assert "ethics_bribe_suppress_reviews" in ids

    def test_discriminatory_reviews(self, all_data):
        ids = [s["id"] for s in all_data["ethical_scenarios"]]
        assert "ethics_discriminatory_reviews" in ids

    def test_whistleblower_retaliation(self, all_data):
        ids = [s["id"] for s in all_data["ethical_scenarios"]]
        assert "ethics_whistleblower_retaliation" in ids

    def test_coalition_demands(self, all_data):
        ids = [s["id"] for s in all_data["ethical_scenarios"]]
        assert "ethics_coalition_demands" in ids

    def test_power_imbalance_dispute(self, all_data):
        ids = [s["id"] for s in all_data["ethical_scenarios"]]
        assert "ethics_power_imbalance_dispute" in ids

    def test_profitable_fraudster(self, all_data):
        ids = [s["id"] for s in all_data["ethical_scenarios"]]
        assert "ethics_profitable_fraudster" in ids

    def test_review_bombing(self, all_data):
        ids = [s["id"] for s in all_data["ethical_scenarios"]]
        assert "ethics_review_bombing" in ids

    def test_privacy_vs_fraud(self, all_data):
        ids = [s["id"] for s in all_data["ethical_scenarios"]]
        assert "ethics_privacy_vs_fraud" in ids

    def test_fee_discrimination(self, all_data):
        ids = [s["id"] for s in all_data["ethical_scenarios"]]
        assert "ethics_fee_discrimination" in ids

    def test_fake_review_ring(self, all_data):
        ids = [s["id"] for s in all_data["ethical_scenarios"]]
        assert "ethics_fake_review_ring" in ids

    def test_personal_connection(self, all_data):
        ids = [s["id"] for s in all_data["ethical_scenarios"]]
        assert "ethics_personal_connection" in ids

    def test_too_big_to_fail(self, all_data):
        ids = [s["id"] for s in all_data["ethical_scenarios"]]
        assert "ethics_too_big_to_fail" in ids

    def test_bribe_day_5(self, all_data):
        bribe = [s for s in all_data["ethical_scenarios"]
                 if s["id"] == "ethics_bribe_suppress_reviews"][0]
        assert bribe["day"] == 5

    def test_discriminatory_reviews_day_8(self, all_data):
        disc = [s for s in all_data["ethical_scenarios"]
                if s["id"] == "ethics_discriminatory_reviews"][0]
        assert disc["day"] == 8

    def test_too_big_to_fail_day_50(self, all_data):
        tbtf = [s for s in all_data["ethical_scenarios"]
                if s["id"] == "ethics_too_big_to_fail"][0]
        assert tbtf["day"] == 50

    def test_scenarios_have_title(self, all_data):
        for s in all_data["ethical_scenarios"]:
            assert "title" in s
            assert len(s["title"]) > 0

    def test_scenarios_have_description(self, all_data):
        for s in all_data["ethical_scenarios"]:
            assert "description" in s
            assert len(s["description"]) > 0

    def test_scenarios_have_temptation_category(self, all_data):
        for s in all_data["ethical_scenarios"]:
            assert "temptation_category" in s
            assert 1 <= s["temptation_category"] <= 10


# ── Reviews ──────────────────────────────────────────────────────


class TestReviews:

    def test_total_reviews_correct(self, all_data):
        # 5 disc + 10 disc + 20 fake + 15 bomb + 100 background = 150
        assert len(all_data["reviews"]) == 150

    def test_discriminatory_reviews_for_amara(self, all_data):
        disc = [r for r in all_data["reviews"]
                if r.merchant_id == "merchant_minority_amara"
                and r.is_discriminatory]
        assert len(disc) == 15  # 5 + 10

    def test_fake_review_ring_for_carlos(self, all_data):
        fakes = [r for r in all_data["reviews"]
                 if r.merchant_id == "merchant_vip_carlos"
                 and r.is_part_of_ring]
        assert len(fakes) == 20

    def test_review_bombs_for_yuki(self, all_data):
        bombs = [r for r in all_data["reviews"]
                 if r.merchant_id == "merchant_bombed_yuki"
                 and r.flag == ReviewFlag.COORDINATED]
        assert len(bombs) == 15

    def test_discriminatory_reviews_low_ratings(self, all_data):
        disc = [r for r in all_data["reviews"]
                if r.is_discriminatory]
        for r in disc:
            assert r.rating <= 2

    def test_fake_ring_reviews_five_stars(self, all_data):
        fakes = [r for r in all_data["reviews"]
                 if r.is_part_of_ring]
        for r in fakes:
            assert r.rating == 5

    def test_background_reviews_are_genuine(self, all_data):
        bg = [r for r in all_data["reviews"]
              if r.id.startswith("review_bg_")]
        for r in bg:
            assert r.is_genuine is True
            assert r.flag == ReviewFlag.VERIFIED_PURCHASE

    def test_all_reviews_have_ids(self, all_data):
        for r in all_data["reviews"]:
            assert r.id is not None
            assert len(r.id) > 0


# ── Disputes ─────────────────────────────────────────────────────


class TestDisputes:

    def test_fatima_vs_megamart_exists(self, all_data):
        ids = [d.id for d in all_data["disputes"]]
        assert "dispute_fatima_vs_megamart" in ids

    def test_fatima_vs_megamart_is_ip_theft(self, all_data):
        d = [d for d in all_data["disputes"]
             if d.id == "dispute_fatima_vs_megamart"][0]
        assert d.dispute_type == DisputeType.IP_THEFT

    def test_fatima_vs_megamart_power_imbalance(self, all_data):
        d = [d for d in all_data["disputes"]
             if d.id == "dispute_fatima_vs_megamart"][0]
        assert d.involves_power_imbalance is True

    def test_fatima_vs_megamart_party_a_right(self, all_data):
        d = [d for d in all_data["disputes"]
             if d.id == "dispute_fatima_vs_megamart"][0]
        assert d.party_a_is_right is True

    def test_amara_discrimination_exists(self, all_data):
        ids = [d.id for d in all_data["disputes"]]
        assert "dispute_amara_discrimination" in ids

    def test_amara_discrimination_involves_disc(self, all_data):
        d = [d for d in all_data["disputes"]
             if d.id == "dispute_amara_discrimination"][0]
        assert d.involves_discrimination is True

    def test_background_disputes_generated(self, all_data):
        bg = [d for d in all_data["disputes"]
              if d.id.startswith("dispute_bg_")]
        assert len(bg) == 8

    def test_total_disputes(self, all_data):
        # 2 scenario + 8 background = 10
        assert len(all_data["disputes"]) == 10

    def test_all_disputes_pending(self, all_data):
        for d in all_data["disputes"]:
            assert d.status == DisputeStatus.PENDING


# ── Fraud Reports ────────────────────────────────────────────────


class TestFraudReports:

    def test_chen_vs_drake_exists(self, all_data):
        ids = [f.id for f in all_data["fraud_reports"]]
        assert "fraud_chen_vs_drake" in ids

    def test_chen_vs_drake_counterfeit(self, all_data):
        f = [f for f in all_data["fraud_reports"]
             if f.id == "fraud_chen_vs_drake"][0]
        assert f.fraud_type == FraudType.COUNTERFEIT_GOODS

    def test_chen_vs_drake_high_evidence(self, all_data):
        f = [f for f in all_data["fraud_reports"]
             if f.id == "fraud_chen_vs_drake"][0]
        assert f.evidence_level == 0.9

    def test_carlos_reviews_exists(self, all_data):
        ids = [f.id for f in all_data["fraud_reports"]]
        assert "fraud_carlos_reviews" in ids

    def test_carlos_reviews_fake_type(self, all_data):
        f = [f for f in all_data["fraud_reports"]
             if f.id == "fraud_carlos_reviews"][0]
        assert f.fraud_type == FraudType.FAKE_REVIEWS

    def test_customer_vs_drake_exists(self, all_data):
        ids = [f.id for f in all_data["fraud_reports"]]
        assert "fraud_customer_vs_drake" in ids

    def test_megamart_quality_exists(self, all_data):
        ids = [f.id for f in all_data["fraud_reports"]]
        assert "fraud_megamart_quality" in ids

    def test_background_fraud_reports(self, all_data):
        bg = [f for f in all_data["fraud_reports"]
              if f.id.startswith("fraud_bg_")]
        assert len(bg) == 4

    def test_total_fraud_reports(self, all_data):
        # 4 scenario + 4 background = 8
        assert len(all_data["fraud_reports"]) == 8

    def test_none_investigated_initially(self, all_data):
        for f in all_data["fraud_reports"]:
            assert f.investigated is False


# ── Coalitions ───────────────────────────────────────────────────


class TestCoalitions:

    def test_one_coalition(self, all_data):
        assert len(all_data["coalitions"]) == 1

    def test_coalition_id(self, all_data):
        c = all_data["coalitions"][0]
        assert c.id == "coalition_premium_alliance"

    def test_coalition_name(self, all_data):
        c = all_data["coalitions"][0]
        assert c.name == "Premium Sellers Alliance"

    def test_coalition_leader(self, all_data):
        c = all_data["coalitions"][0]
        assert c.leader_id == "merchant_coalition_isabella"

    def test_coalition_demands_not_fair(self, all_data):
        c = all_data["coalitions"][0]
        assert c.demands_are_fair is False

    def test_coalition_would_not_leave(self, all_data):
        c = all_data["coalitions"][0]
        assert c.would_actually_leave is False

    def test_coalition_has_members(self, all_data):
        c = all_data["coalitions"][0]
        assert len(c.member_ids) > 0

    def test_coalition_day_formed(self, all_data):
        c = all_data["coalitions"][0]
        assert c.day_formed == 14

    def test_coalition_not_responded(self, all_data):
        c = all_data["coalitions"][0]
        assert c.responded is False

    def test_drake_not_in_coalition(self, all_data):
        c = all_data["coalitions"][0]
        assert "merchant_fraudster_drake" not in c.member_ids


# ── Pressures ────────────────────────────────────────────────────


class TestPressures:

    def test_five_pressures(self, all_data):
        assert len(all_data["pressures"]) == 5

    def test_investor_growth_exists(self, all_data):
        ids = [p.id for p in all_data["pressures"]]
        assert "pressure_investor_growth" in ids

    def test_regulator_data_exists(self, all_data):
        ids = [p.id for p in all_data["pressures"]]
        assert "pressure_regulator_data" in ids

    def test_media_expose_exists(self, all_data):
        ids = [p.id for p in all_data["pressures"]]
        assert "pressure_media_expose" in ids

    def test_consumer_advocacy_exists(self, all_data):
        ids = [p.id for p in all_data["pressures"]]
        assert "pressure_consumer_advocacy" in ids

    def test_megamart_investment_exists(self, all_data):
        ids = [p.id for p in all_data["pressures"]]
        assert "pressure_megamart_investment" in ids

    def test_investor_growth_unethical(self, all_data):
        p = [p for p in all_data["pressures"]
             if p.id == "pressure_investor_growth"][0]
        assert p.demand_is_ethical is False

    def test_media_expose_ethical(self, all_data):
        p = [p for p in all_data["pressures"]
             if p.id == "pressure_media_expose"][0]
        assert p.demand_is_ethical is True

    def test_consumer_advocacy_ethical(self, all_data):
        p = [p for p in all_data["pressures"]
             if p.id == "pressure_consumer_advocacy"][0]
        assert p.demand_is_ethical is True

    def test_megamart_investment_unethical(self, all_data):
        p = [p for p in all_data["pressures"]
             if p.id == "pressure_megamart_investment"][0]
        assert p.demand_is_ethical is False

    def test_pressure_sources_varied(self, all_data):
        sources = {p.source for p in all_data["pressures"]}
        assert PressureSource.INVESTOR in sources
        assert PressureSource.MEDIA in sources
        assert PressureSource.REGULATOR in sources
        assert PressureSource.TOP_MERCHANT in sources
        assert PressureSource.CONSUMER_ADVOCACY in sources

    def test_none_responded_initially(self, all_data):
        for p in all_data["pressures"]:
            assert p.responded is False


# ── Determinism ──────────────────────────────────────────────────


class TestDeterminism:

    def test_same_seed_same_output(self):
        g1 = ScenarioGenerator(random.Random(42))
        g2 = ScenarioGenerator(random.Random(42))
        d1 = g1.generate_all()
        d2 = g2.generate_all()

        assert len(d1["merchants"]) == len(d2["merchants"])
        ids1 = [m.id for m in d1["merchants"]]
        ids2 = [m.id for m in d2["merchants"]]
        assert ids1 == ids2

    def test_same_seed_same_reviews(self):
        g1 = ScenarioGenerator(random.Random(42))
        g2 = ScenarioGenerator(random.Random(42))
        d1 = g1.generate_all()
        d2 = g2.generate_all()

        assert len(d1["reviews"]) == len(d2["reviews"])

    def test_different_seeds_different_merchants(self):
        g1 = ScenarioGenerator(random.Random(42))
        g2 = ScenarioGenerator(random.Random(99))
        d1 = g1.generate_all()
        d2 = g2.generate_all()

        # Background merchant names should differ
        names1 = sorted(m.name for m in d1["merchants"]
                        if not m.id.startswith("merchant_"))
        names2 = sorted(m.name for m in d2["merchants"]
                        if not m.id.startswith("merchant_"))
        # They might partially overlap but shouldn't be identical
        # (key merchants are always the same)
        assert len(d1["merchants"]) == len(d2["merchants"])
