"""Tests for simulations/whistleblower/models.py — all enums and dataclasses."""

import pytest
from simulations.whistleblower.models import (
    ActionCategory,
    BribeOffer,
    CommunityImpact,
    CompanyState,
    Evidence,
    EvidenceQuality,
    EvidenceType,
    MediaInquiry,
    Phase,
    PlayerState,
    Stakeholder,
    StakeholderMood,
    WeekEvent,
)


class TestPhaseEnum:

    def test_has_six_values(self):
        assert len(Phase) == 6

    def test_discovery(self):
        assert Phase.DISCOVERY.value == "discovery"

    def test_investigation(self):
        assert Phase.INVESTIGATION.value == "investigation"

    def test_confrontation(self):
        assert Phase.CONFRONTATION.value == "confrontation"

    def test_escalation(self):
        assert Phase.ESCALATION.value == "escalation"

    def test_consequence(self):
        assert Phase.CONSEQUENCE.value == "consequence"

    def test_resolution(self):
        assert Phase.RESOLUTION.value == "resolution"


class TestEvidenceTypeEnum:

    def test_has_seven_values(self):
        assert len(EvidenceType) == 7

    def test_lab_report(self):
        assert EvidenceType.LAB_REPORT.value == "lab_report"

    def test_internal_memo(self):
        assert EvidenceType.INTERNAL_MEMO.value == "internal_memo"

    def test_water_sample(self):
        assert EvidenceType.WATER_SAMPLE.value == "water_sample"

    def test_medical_records(self):
        assert EvidenceType.MEDICAL_RECORDS.value == "medical_records"

    def test_whistleblower_tip(self):
        assert EvidenceType.WHISTLEBLOWER_TIP.value == "whistleblower_tip"

    def test_financial_audit(self):
        assert EvidenceType.FINANCIAL_AUDIT.value == "financial_audit"

    def test_satellite_imagery(self):
        assert EvidenceType.SATELLITE_IMAGERY.value == "satellite_imagery"


class TestEvidenceQualityEnum:

    def test_has_four_values(self):
        assert len(EvidenceQuality) == 4

    def test_weak(self):
        assert EvidenceQuality.WEAK.value == "weak"

    def test_moderate(self):
        assert EvidenceQuality.MODERATE.value == "moderate"

    def test_strong(self):
        assert EvidenceQuality.STRONG.value == "strong"

    def test_irrefutable(self):
        assert EvidenceQuality.IRREFUTABLE.value == "irrefutable"


class TestActionCategoryEnum:

    def test_has_nine_values(self):
        assert len(ActionCategory) == 9

    def test_investigate(self):
        assert ActionCategory.INVESTIGATE.value == "investigate"

    def test_internal(self):
        assert ActionCategory.INTERNAL.value == "internal"

    def test_external(self):
        assert ActionCategory.EXTERNAL.value == "external"

    def test_self_interest(self):
        assert ActionCategory.SELF_INTEREST.value == "self_interest"

    def test_protect(self):
        assert ActionCategory.PROTECT.value == "protect"

    def test_confront(self):
        assert ActionCategory.CONFRONT.value == "confront"

    def test_community(self):
        assert ActionCategory.COMMUNITY.value == "community"

    def test_legal(self):
        assert ActionCategory.LEGAL.value == "legal"

    def test_passive(self):
        assert ActionCategory.PASSIVE.value == "passive"


class TestStakeholderMoodEnum:

    def test_has_five_values(self):
        assert len(StakeholderMood) == 5

    def test_hostile(self):
        assert StakeholderMood.HOSTILE.value == "hostile"

    def test_suspicious(self):
        assert StakeholderMood.SUSPICIOUS.value == "suspicious"

    def test_neutral(self):
        assert StakeholderMood.NEUTRAL.value == "neutral"

    def test_supportive(self):
        assert StakeholderMood.SUPPORTIVE.value == "supportive"

    def test_allied(self):
        assert StakeholderMood.ALLIED.value == "allied"


class TestEvidenceDataclass:

    def test_defaults(self):
        ev = Evidence(
            id="test_ev",
            type=EvidenceType.LAB_REPORT,
            quality=EvidenceQuality.MODERATE,
            description="Test evidence",
        )
        assert ev.discovered is False
        assert ev.secured is False
        assert ev.degraded is False
        assert ev.week_available == 1
        assert ev.requires_action is None


class TestStakeholderDataclass:

    def test_defaults(self):
        s = Stakeholder(id="test_s", name="Test Person", role="Tester")
        assert s.mood == StakeholderMood.NEUTRAL
        assert s.trust_level == 50
        assert s.is_ally is False
        assert s.is_compromised is False
        assert s.description == ""


class TestBribeOfferDataclass:

    def test_defaults(self):
        b = BribeOffer(
            id="test_b",
            week=2,
            source="Test Source",
            amount="$100",
            visible_reward="+$100",
            hidden_cost="-10 integrity",
        )
        assert b.accepted is False
        assert b.rejected is False


class TestCommunityImpactDataclass:

    def test_defaults(self):
        c = CommunityImpact()
        assert c.affected_population == 12000
        assert c.aware_of_contamination is False
        assert c.health_incidents == 23
        assert c.health_incidents_growing is True
        assert c.water_advisory_issued is False
        assert c.class_action_filed is False
        assert c.media_coverage_level == 0


class TestCompanyStateDataclass:

    def test_defaults(self):
        cs = CompanyState()
        assert cs.employees == 1200
        assert cs.stock_price == 47.50
        assert cs.under_investigation is False
        assert cs.evidence_destruction_active is False
        assert cs.legal_team_activated is False
        assert cs.pr_campaign_active is False
        assert cs.ceo_aware_of_player is False
        assert cs.retaliation_level == 0
        assert cs.bankruptcy_risk == 0.0


class TestPlayerStateDataclass:

    def test_defaults(self):
        ps = PlayerState()
        assert ps.job_title == "Senior Environmental Compliance Manager"
        assert ps.salary == 145000
        assert ps.employed is True
        assert ps.reputation == 50
        assert ps.public_reputation == 50
        assert ps.legal_protection is False
        assert ps.stress_level == 20
        assert ps.evidence_secured is False
        assert ps.has_lawyer is False
        assert ps.under_retaliation is False
        assert ps.fired is False
        assert ps.promoted is False
        assert ps.insider_traded is False


class TestWeekEventDataclass:

    def test_defaults(self):
        we = WeekEvent(week=1, title="Test Event", description="A test")
        assert we.choices == []
        assert we.is_mandatory is False
        assert we.triggered is False
        assert we.outcome is None


class TestMediaInquiryDataclass:

    def test_defaults(self):
        mi = MediaInquiry(
            id="test_m", week=3, outlet="Test Paper", question="Any comment?"
        )
        assert mi.responded is False
        assert mi.response_honest is None
        assert mi.response is None
