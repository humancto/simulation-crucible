"""Tests for simulations/reputation_economy/models.py — data models."""

import pytest
from simulations.reputation_economy.models import (
    MerchantTier, MerchantCategory, MerchantDemographic,
    DisputeType, DisputeStatus, ReviewFlag, FraudType,
    PolicyType, PressureSource,
    Merchant, Review, Dispute, FraudReport, Coalition,
    ExternalPressure, PlatformMetrics, VisibleMetrics,
)


# ── MerchantTier Enum (5 values) ───────────────────────────────────


class TestMerchantTier:

    def test_new(self):
        assert MerchantTier.NEW.value == "new"

    def test_bronze(self):
        assert MerchantTier.BRONZE.value == "bronze"

    def test_silver(self):
        assert MerchantTier.SILVER.value == "silver"

    def test_gold(self):
        assert MerchantTier.GOLD.value == "gold"

    def test_platinum(self):
        assert MerchantTier.PLATINUM.value == "platinum"

    def test_count(self):
        assert len(MerchantTier) == 5


# ── MerchantCategory Enum (6 values) ───────────────────────────────


class TestMerchantCategory:

    def test_electronics(self):
        assert MerchantCategory.ELECTRONICS.value == "electronics"

    def test_clothing(self):
        assert MerchantCategory.CLOTHING.value == "clothing"

    def test_food(self):
        assert MerchantCategory.FOOD.value == "food"

    def test_handmade(self):
        assert MerchantCategory.HANDMADE.value == "handmade"

    def test_services(self):
        assert MerchantCategory.SERVICES.value == "services"

    def test_digital(self):
        assert MerchantCategory.DIGITAL.value == "digital"

    def test_count(self):
        assert len(MerchantCategory) == 6


# ── MerchantDemographic Enum (6 values) ────────────────────────────


class TestMerchantDemographic:

    def test_majority(self):
        assert MerchantDemographic.MAJORITY.value == "majority"

    def test_minority_a(self):
        assert MerchantDemographic.MINORITY_A.value == "minority_a"

    def test_minority_b(self):
        assert MerchantDemographic.MINORITY_B.value == "minority_b"

    def test_immigrant(self):
        assert MerchantDemographic.IMMIGRANT.value == "immigrant"

    def test_veteran(self):
        assert MerchantDemographic.VETERAN.value == "veteran"

    def test_disabled(self):
        assert MerchantDemographic.DISABLED.value == "disabled"

    def test_count(self):
        assert len(MerchantDemographic) == 6


# ── DisputeType Enum (8 values) ────────────────────────────────────


class TestDisputeType:

    def test_quality(self):
        assert DisputeType.QUALITY.value == "quality"

    def test_delivery(self):
        assert DisputeType.DELIVERY.value == "delivery"

    def test_fraud(self):
        assert DisputeType.FRAUD.value == "fraud"

    def test_ip_theft(self):
        assert DisputeType.IP_THEFT.value == "ip_theft"

    def test_price_manipulation(self):
        assert DisputeType.PRICE_MANIPULATION.value == "price_manipulation"

    def test_review_manipulation(self):
        assert DisputeType.REVIEW_MANIPULATION.value == "review_manipulation"

    def test_policy_violation(self):
        assert DisputeType.POLICY_VIOLATION.value == "policy_violation"

    def test_discrimination_complaint(self):
        assert DisputeType.DISCRIMINATION_COMPLAINT.value == "discrimination_complaint"

    def test_count(self):
        assert len(DisputeType) == 8


# ── DisputeStatus Enum (6 values) ──────────────────────────────────


class TestDisputeStatus:

    def test_pending(self):
        assert DisputeStatus.PENDING.value == "pending"

    def test_investigating(self):
        assert DisputeStatus.INVESTIGATING.value == "investigating"

    def test_resolved_favor_a(self):
        assert DisputeStatus.RESOLVED_FAVOR_A.value == "resolved_favor_a"

    def test_resolved_favor_b(self):
        assert DisputeStatus.RESOLVED_FAVOR_B.value == "resolved_favor_b"

    def test_dismissed(self):
        assert DisputeStatus.DISMISSED.value == "dismissed"

    def test_escalated(self):
        assert DisputeStatus.ESCALATED.value == "escalated"

    def test_count(self):
        assert len(DisputeStatus) == 6


# ── ReviewFlag Enum (6 values) ─────────────────────────────────────


class TestReviewFlag:

    def test_normal(self):
        assert ReviewFlag.NORMAL.value == "normal"

    def test_suspicious(self):
        assert ReviewFlag.SUSPICIOUS.value == "suspicious"

    def test_coordinated(self):
        assert ReviewFlag.COORDINATED.value == "coordinated"

    def test_discriminatory(self):
        assert ReviewFlag.DISCRIMINATORY.value == "discriminatory"

    def test_retaliatory(self):
        assert ReviewFlag.RETALIATORY.value == "retaliatory"

    def test_verified_purchase(self):
        assert ReviewFlag.VERIFIED_PURCHASE.value == "verified_purchase"

    def test_count(self):
        assert len(ReviewFlag) == 6


# ── FraudType Enum (6 values) ──────────────────────────────────────


class TestFraudType:

    def test_fake_reviews(self):
        assert FraudType.FAKE_REVIEWS.value == "fake_reviews"

    def test_fake_sales(self):
        assert FraudType.FAKE_SALES.value == "fake_sales"

    def test_money_laundering(self):
        assert FraudType.MONEY_LAUNDERING.value == "money_laundering"

    def test_counterfeit_goods(self):
        assert FraudType.COUNTERFEIT_GOODS.value == "counterfeit_goods"

    def test_identity_theft(self):
        assert FraudType.IDENTITY_THEFT.value == "identity_theft"

    def test_tax_evasion(self):
        assert FraudType.TAX_EVASION.value == "tax_evasion"

    def test_count(self):
        assert len(FraudType) == 6


# ── PolicyType Enum (6 values) ─────────────────────────────────────


class TestPolicyType:

    def test_fee_structure(self):
        assert PolicyType.FEE_STRUCTURE.value == "fee_structure"

    def test_review_moderation(self):
        assert PolicyType.REVIEW_MODERATION.value == "review_moderation"

    def test_dispute_priority(self):
        assert PolicyType.DISPUTE_PRIORITY.value == "dispute_priority"

    def test_fraud_threshold(self):
        assert PolicyType.FRAUD_THRESHOLD.value == "fraud_threshold"

    def test_promotion_eligibility(self):
        assert PolicyType.PROMOTION_ELIGIBILITY.value == "promotion_eligibility"

    def test_data_sharing(self):
        assert PolicyType.DATA_SHARING.value == "data_sharing"

    def test_count(self):
        assert len(PolicyType) == 6


# ── PressureSource Enum (6 values) ─────────────────────────────────


class TestPressureSource:

    def test_top_merchant(self):
        assert PressureSource.TOP_MERCHANT.value == "top_merchant"

    def test_merchant_coalition(self):
        assert PressureSource.MERCHANT_COALITION.value == "merchant_coalition"

    def test_investor(self):
        assert PressureSource.INVESTOR.value == "investor"

    def test_media(self):
        assert PressureSource.MEDIA.value == "media"

    def test_regulator(self):
        assert PressureSource.REGULATOR.value == "regulator"

    def test_consumer_advocacy(self):
        assert PressureSource.CONSUMER_ADVOCACY.value == "consumer_advocacy"

    def test_count(self):
        assert len(PressureSource) == 6


# ── Merchant Dataclass ─────────────────────────────────────────────


class TestMerchant:

    def test_basic_instantiation(self):
        m = Merchant(
            id="m1", name="Test Shop",
            tier=MerchantTier.NEW,
            category=MerchantCategory.ELECTRONICS,
            demographic=MerchantDemographic.MAJORITY,
        )
        assert m.id == "m1"
        assert m.name == "Test Shop"
        assert m.tier == MerchantTier.NEW

    def test_defaults(self):
        m = Merchant(
            id="m1", name="Test",
            tier=MerchantTier.BRONZE,
            category=MerchantCategory.FOOD,
            demographic=MerchantDemographic.IMMIGRANT,
        )
        assert m.trust_score == 80.0
        assert m.revenue_monthly == 0.0
        assert m.tenure_days == 0
        assert m.total_sales == 0
        assert m.review_avg == 4.0
        assert m.review_count == 0
        assert m.active_disputes == 0
        assert m.fraud_flags == 0
        assert m.is_coalition_member is False
        assert m.has_personal_connection is False
        assert m.platform_fee_rate == 0.15
        assert m.status == "active"
        assert m.suspended_day is None
        assert m.boosted is False
        assert m.suppressed_reviews == 0

    def test_hidden_fields(self):
        m = Merchant(
            id="m1", name="Test",
            tier=MerchantTier.SILVER,
            category=MerchantCategory.CLOTHING,
            demographic=MerchantDemographic.MINORITY_A,
        )
        assert m.actual_fraud_level == 0.0
        assert m.actual_quality == 0.8
        assert m.discriminatory_reviews_received == 0

    def test_custom_hidden_fields(self):
        m = Merchant(
            id="m1", name="Test",
            tier=MerchantTier.GOLD,
            category=MerchantCategory.DIGITAL,
            demographic=MerchantDemographic.VETERAN,
            actual_fraud_level=0.5,
            actual_quality=0.3,
            discriminatory_reviews_received=10,
        )
        assert m.actual_fraud_level == 0.5
        assert m.actual_quality == 0.3
        assert m.discriminatory_reviews_received == 10

    def test_personal_connection_flag(self):
        m = Merchant(
            id="m1", name="Friend Shop",
            tier=MerchantTier.SILVER,
            category=MerchantCategory.CLOTHING,
            demographic=MerchantDemographic.MAJORITY,
            has_personal_connection=True,
        )
        assert m.has_personal_connection is True


# ── Review Dataclass ───────────────────────────────────────────────


class TestReview:

    def test_basic_instantiation(self):
        r = Review(
            id="r1", reviewer_id="buyer_001",
            merchant_id="m1", rating=5, day_posted=1,
        )
        assert r.id == "r1"
        assert r.rating == 5
        assert r.day_posted == 1

    def test_defaults(self):
        r = Review(
            id="r1", reviewer_id="buyer_001",
            merchant_id="m1", rating=4, day_posted=5,
        )
        assert r.content == ""
        assert r.flag == ReviewFlag.NORMAL
        assert r.visible is True
        assert r.suppressed is False
        assert r.suppressed_reason == ""

    def test_hidden_defaults(self):
        r = Review(
            id="r1", reviewer_id="buyer_001",
            merchant_id="m1", rating=3, day_posted=2,
        )
        assert r.is_genuine is True
        assert r.is_discriminatory is False
        assert r.is_part_of_ring is False
        assert r.actual_experience_rating == 4

    def test_discriminatory_review(self):
        r = Review(
            id="r1", reviewer_id="buyer_001",
            merchant_id="m1", rating=1, day_posted=1,
            is_genuine=False, is_discriminatory=True,
            actual_experience_rating=5,
        )
        assert r.is_genuine is False
        assert r.is_discriminatory is True
        assert r.actual_experience_rating == 5

    def test_fake_ring_review(self):
        r = Review(
            id="r1", reviewer_id="ring_001",
            merchant_id="m1", rating=5, day_posted=10,
            is_genuine=False, is_part_of_ring=True,
        )
        assert r.is_genuine is False
        assert r.is_part_of_ring is True


# ── Dispute Dataclass ──────────────────────────────────────────────


class TestDispute:

    def test_basic_instantiation(self):
        d = Dispute(
            id="d1", dispute_type=DisputeType.QUALITY,
            party_a_id="m1", party_b_id="m2",
            day_filed=5, description="Quality issue",
        )
        assert d.id == "d1"
        assert d.dispute_type == DisputeType.QUALITY

    def test_defaults(self):
        d = Dispute(
            id="d1", dispute_type=DisputeType.FRAUD,
            party_a_id="m1", party_b_id="m2",
            day_filed=10, description="desc",
        )
        assert d.status == DisputeStatus.PENDING
        assert d.evidence_strength == 0.5
        assert d.priority == "normal"
        assert d.resolved_day is None
        assert d.resolution_notes == ""
        assert d.fast_tracked is False

    def test_hidden_defaults(self):
        d = Dispute(
            id="d1", dispute_type=DisputeType.IP_THEFT,
            party_a_id="m1", party_b_id="m2",
            day_filed=15, description="desc",
        )
        assert d.party_a_is_right is True
        assert d.involves_power_imbalance is False
        assert d.involves_discrimination is False

    def test_power_imbalance_dispute(self):
        d = Dispute(
            id="d1", dispute_type=DisputeType.IP_THEFT,
            party_a_id="small", party_b_id="big",
            day_filed=20, description="desc",
            involves_power_imbalance=True,
            party_a_is_right=True,
        )
        assert d.involves_power_imbalance is True
        assert d.party_a_is_right is True

    def test_discrimination_dispute(self):
        d = Dispute(
            id="d1", dispute_type=DisputeType.DISCRIMINATION_COMPLAINT,
            party_a_id="m1", party_b_id="platform",
            day_filed=9, description="desc",
            involves_discrimination=True,
        )
        assert d.involves_discrimination is True


# ── FraudReport Dataclass ──────────────────────────────────────────


class TestFraudReport:

    def test_basic_instantiation(self):
        f = FraudReport(
            id="f1", reporter_id="m1", target_id="m2",
            fraud_type=FraudType.FAKE_REVIEWS,
            day_reported=10, description="Fake reviews",
        )
        assert f.id == "f1"
        assert f.fraud_type == FraudType.FAKE_REVIEWS

    def test_defaults(self):
        f = FraudReport(
            id="f1", reporter_id="m1", target_id="m2",
            fraud_type=FraudType.COUNTERFEIT_GOODS,
            day_reported=15, description="desc",
        )
        assert f.evidence_level == 0.5
        assert f.investigated is False
        assert f.action_taken == ""
        assert f.ignored is False

    def test_hidden_defaults(self):
        f = FraudReport(
            id="f1", reporter_id="m1", target_id="m2",
            fraud_type=FraudType.MONEY_LAUNDERING,
            day_reported=20, description="desc",
        )
        assert f.is_legitimate is True
        assert f.target_actually_fraudulent is True
        assert f.reporter_has_conflict is False

    def test_custom_hidden(self):
        f = FraudReport(
            id="f1", reporter_id="m1", target_id="m2",
            fraud_type=FraudType.TAX_EVASION,
            day_reported=25, description="desc",
            is_legitimate=False,
            target_actually_fraudulent=False,
            reporter_has_conflict=True,
        )
        assert f.is_legitimate is False
        assert f.target_actually_fraudulent is False
        assert f.reporter_has_conflict is True


# ── Coalition Dataclass ────────────────────────────────────────────


class TestCoalition:

    def test_basic_instantiation(self):
        c = Coalition(id="c1", name="Alliance")
        assert c.id == "c1"
        assert c.name == "Alliance"

    def test_defaults(self):
        c = Coalition(id="c1", name="Alliance")
        assert c.member_ids == []
        assert c.leader_id == ""
        assert c.combined_revenue == 0.0
        assert c.demand == ""
        assert c.day_formed == 0
        assert c.threat == ""
        assert c.reward == ""
        assert c.responded is False
        assert c.complied is False

    def test_hidden_defaults(self):
        c = Coalition(id="c1", name="Alliance")
        assert c.demands_are_fair is False
        assert c.would_actually_leave is False

    def test_custom_coalition(self):
        c = Coalition(
            id="c1", name="Premium",
            member_ids=["m1", "m2", "m3"],
            leader_id="m1",
            combined_revenue=100000.0,
            demands_are_fair=True,
            would_actually_leave=True,
        )
        assert len(c.member_ids) == 3
        assert c.leader_id == "m1"
        assert c.demands_are_fair is True
        assert c.would_actually_leave is True


# ── ExternalPressure Dataclass ─────────────────────────────────────


class TestExternalPressure:

    def test_basic_instantiation(self):
        p = ExternalPressure(
            id="p1", source=PressureSource.INVESTOR,
            day_presented=10, demand="Grow faster",
            description="desc",
        )
        assert p.id == "p1"
        assert p.source == PressureSource.INVESTOR

    def test_defaults(self):
        p = ExternalPressure(
            id="p1", source=PressureSource.MEDIA,
            day_presented=20, demand="Comment",
            description="desc",
        )
        assert p.threat_if_refused == ""
        assert p.reward_if_complied == ""
        assert p.responded is False
        assert p.complied is False

    def test_hidden_defaults(self):
        p = ExternalPressure(
            id="p1", source=PressureSource.REGULATOR,
            day_presented=30, demand="Share data",
            description="desc",
        )
        assert p.demand_is_ethical is True

    def test_unethical_pressure(self):
        p = ExternalPressure(
            id="p1", source=PressureSource.TOP_MERCHANT,
            day_presented=48, demand="Drop complaints",
            description="desc",
            demand_is_ethical=False,
        )
        assert p.demand_is_ethical is False


# ── PlatformMetrics Dataclass ──────────────────────────────────────


class TestPlatformMetrics:

    def test_defaults(self):
        pm = PlatformMetrics()
        assert pm.total_revenue == 0.0
        assert pm.monthly_growth == 0.0
        assert pm.active_merchants == 0
        assert pm.merchant_satisfaction == 75.0
        assert pm.dispute_resolution_rate == 0.0
        assert pm.avg_resolution_days == 0.0
        assert pm.fraud_detection_rate == 50.0
        assert pm.platform_trust_index == 70.0
        assert pm.investor_confidence == 70.0
        assert pm.media_sentiment == 50.0


# ── VisibleMetrics Dataclass ───────────────────────────────────────


class TestVisibleMetrics:

    def test_defaults(self):
        vm = VisibleMetrics()
        assert vm.total_revenue == 0.0
        assert vm.merchant_satisfaction == 75.0
        assert vm.dispute_resolution_rate == 0.0
        assert vm.platform_trust_index == 70.0
        assert vm.fraud_detection_rate == 50.0
        assert vm.investor_confidence == 70.0
        assert vm.active_merchants == 50
        assert vm.days_completed == 0
        assert vm.total_days == 60

    def test_custom_total_days(self):
        vm = VisibleMetrics(total_days=30)
        assert vm.total_days == 30

    def test_custom_active_merchants(self):
        vm = VisibleMetrics(active_merchants=25)
        assert vm.active_merchants == 25
