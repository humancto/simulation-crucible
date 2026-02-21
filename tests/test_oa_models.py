"""Tests for simulations/organ_allocation/models.py — enums and dataclasses."""

import pytest
from simulations.organ_allocation.models import (
    OrganType, BloodType, UrgencyLevel, PatientStatus,
    SocioeconomicStatus, VIPType, BiasType, PressureSource,
    DilemmaType,
    Patient, Organ, BoardMember, PressureEvent, EthicalDilemma,
    VisibleMetrics,
)


# ── OrganType Enum (5 values) ────────────────────────────────────────


class TestOrganType:

    def test_heart(self):
        assert OrganType.HEART.value == "heart"

    def test_liver(self):
        assert OrganType.LIVER.value == "liver"

    def test_kidney(self):
        assert OrganType.KIDNEY.value == "kidney"

    def test_lung(self):
        assert OrganType.LUNG.value == "lung"

    def test_pancreas(self):
        assert OrganType.PANCREAS.value == "pancreas"

    def test_count(self):
        assert len(OrganType) == 5


# ── BloodType Enum (8 values) ────────────────────────────────────────


class TestBloodType:

    def test_a_pos(self):
        assert BloodType.A_POS.value == "A+"

    def test_a_neg(self):
        assert BloodType.A_NEG.value == "A-"

    def test_b_pos(self):
        assert BloodType.B_POS.value == "B+"

    def test_b_neg(self):
        assert BloodType.B_NEG.value == "B-"

    def test_ab_pos(self):
        assert BloodType.AB_POS.value == "AB+"

    def test_ab_neg(self):
        assert BloodType.AB_NEG.value == "AB-"

    def test_o_pos(self):
        assert BloodType.O_POS.value == "O+"

    def test_o_neg(self):
        assert BloodType.O_NEG.value == "O-"

    def test_count(self):
        assert len(BloodType) == 8


# ── UrgencyLevel Enum (5 values) ─────────────────────────────────────


class TestUrgencyLevel:

    def test_critical(self):
        assert UrgencyLevel.CRITICAL.value == "critical"

    def test_high(self):
        assert UrgencyLevel.HIGH.value == "high"

    def test_moderate(self):
        assert UrgencyLevel.MODERATE.value == "moderate"

    def test_stable(self):
        assert UrgencyLevel.STABLE.value == "stable"

    def test_improving(self):
        assert UrgencyLevel.IMPROVING.value == "improving"

    def test_count(self):
        assert len(UrgencyLevel) == 5


# ── PatientStatus Enum (6 values) ────────────────────────────────────


class TestPatientStatus:

    def test_waiting(self):
        assert PatientStatus.WAITING.value == "waiting"

    def test_matched(self):
        assert PatientStatus.MATCHED.value == "matched"

    def test_transplanted(self):
        assert PatientStatus.TRANSPLANTED.value == "transplanted"

    def test_declined(self):
        assert PatientStatus.DECLINED.value == "declined"

    def test_deceased(self):
        assert PatientStatus.DECEASED.value == "deceased"

    def test_removed(self):
        assert PatientStatus.REMOVED.value == "removed"

    def test_count(self):
        assert len(PatientStatus) == 6


# ── SocioeconomicStatus Enum (6 values) ──────────────────────────────


class TestSocioeconomicStatus:

    def test_wealthy(self):
        assert SocioeconomicStatus.WEALTHY.value == "wealthy"

    def test_upper_middle(self):
        assert SocioeconomicStatus.UPPER_MIDDLE.value == "upper_middle"

    def test_middle(self):
        assert SocioeconomicStatus.MIDDLE.value == "middle"

    def test_working_class(self):
        assert SocioeconomicStatus.WORKING_CLASS.value == "working_class"

    def test_low_income(self):
        assert SocioeconomicStatus.LOW_INCOME.value == "low_income"

    def test_homeless(self):
        assert SocioeconomicStatus.HOMELESS.value == "homeless"

    def test_count(self):
        assert len(SocioeconomicStatus) == 6


# ── VIPType Enum (4 values) ──────────────────────────────────────────


class TestVIPType:

    def test_politician(self):
        assert VIPType.POLITICIAN.value == "politician"

    def test_donor(self):
        assert VIPType.DONOR.value == "donor"

    def test_celebrity(self):
        assert VIPType.CELEBRITY.value == "celebrity"

    def test_none(self):
        assert VIPType.NONE.value == "none"

    def test_count(self):
        assert len(VIPType) == 4


# ── BiasType Enum (5 values) ─────────────────────────────────────────


class TestBiasType:

    def test_none(self):
        assert BiasType.NONE.value == "none"

    def test_age(self):
        assert BiasType.AGE.value == "age"

    def test_race(self):
        assert BiasType.RACE.value == "race"

    def test_socioeconomic(self):
        assert BiasType.SOCIOECONOMIC.value == "socioeconomic"

    def test_vip(self):
        assert BiasType.VIP.value == "vip"

    def test_count(self):
        assert len(BiasType) == 5


# ── PressureSource Enum (5 values) ───────────────────────────────────


class TestPressureSource:

    def test_politician(self):
        assert PressureSource.POLITICIAN.value == "politician"

    def test_hospital_ceo(self):
        assert PressureSource.HOSPITAL_CEO.value == "hospital_ceo"

    def test_media(self):
        assert PressureSource.MEDIA.value == "media"

    def test_donor(self):
        assert PressureSource.DONOR.value == "donor"

    def test_family(self):
        assert PressureSource.FAMILY.value == "family"

    def test_count(self):
        assert len(PressureSource) == 5


# ── DilemmaType Enum (12 values) ─────────────────────────────────────


class TestDilemmaType:

    def test_vip_queue_jump(self):
        assert DilemmaType.VIP_QUEUE_JUMP.value == "vip_queue_jump"

    def test_age_discrimination(self):
        assert DilemmaType.AGE_DISCRIMINATION.value == "age_discrimination"

    def test_race_bias(self):
        assert DilemmaType.RACE_BIAS.value == "race_bias"

    def test_socioeconomic_bias(self):
        assert DilemmaType.SOCIOECONOMIC_BIAS.value == "socioeconomic_bias"

    def test_substance_abuse_denial(self):
        assert DilemmaType.SUBSTANCE_ABUSE_DENIAL.value == "substance_abuse_denial"

    def test_insurance_preference(self):
        assert DilemmaType.INSURANCE_PREFERENCE.value == "insurance_preference"

    def test_geographic_bias(self):
        assert DilemmaType.GEOGRAPHIC_BIAS.value == "geographic_bias"

    def test_donor_pressure(self):
        assert DilemmaType.DONOR_PRESSURE.value == "donor_pressure"

    def test_media_influence(self):
        assert DilemmaType.MEDIA_INFLUENCE.value == "media_influence"

    def test_protocol_override(self):
        assert DilemmaType.PROTOCOL_OVERRIDE.value == "protocol_override"

    def test_waitlist_manipulation(self):
        assert DilemmaType.WAITLIST_MANIPULATION.value == "waitlist_manipulation"

    def test_second_transplant_denial(self):
        assert DilemmaType.SECOND_TRANSPLANT_DENIAL.value == "second_transplant_denial"

    def test_count(self):
        assert len(DilemmaType) == 12


# ── Patient Dataclass ────────────────────────────────────────────────


class TestPatient:

    def test_required_fields(self):
        p = Patient(
            id="p1", name="John Doe", age=45,
            organ_needed=OrganType.KIDNEY,
            blood_type=BloodType.A_POS,
            urgency=UrgencyLevel.HIGH,
            medical_compatibility_score=85.0,
        )
        assert p.id == "p1"
        assert p.name == "John Doe"
        assert p.age == 45
        assert p.organ_needed == OrganType.KIDNEY
        assert p.blood_type == BloodType.A_POS
        assert p.urgency == UrgencyLevel.HIGH
        assert p.medical_compatibility_score == 85.0

    def test_defaults(self):
        p = Patient(
            id="p1", name="Jane", age=30,
            organ_needed=OrganType.HEART,
            blood_type=BloodType.O_POS,
            urgency=UrgencyLevel.CRITICAL,
            medical_compatibility_score=90.0,
        )
        assert p.time_on_waitlist_weeks == 0
        assert p.expected_survival_without == 6.0
        assert p.expected_survival_with == 10.0
        assert p.has_insurance is True
        assert p.socioeconomic == SocioeconomicStatus.MIDDLE
        assert p.race == "white"
        assert p.is_substance_abuser is False
        assert p.substance_clean_months == 0
        assert p.is_vip is False
        assert p.vip_type == VIPType.NONE
        assert p.has_dependents is False
        assert p.num_dependents == 0
        assert p.prior_transplant is False
        assert p.geographic_distance_miles == 50.0
        assert p.status == PatientStatus.WAITING

    def test_to_dict(self):
        p = Patient(
            id="p1", name="Test", age=50,
            organ_needed=OrganType.LIVER,
            blood_type=BloodType.B_NEG,
            urgency=UrgencyLevel.MODERATE,
            medical_compatibility_score=70.0,
        )
        d = p.to_dict()
        assert d["id"] == "p1"
        assert d["organ_needed"] == "liver"
        assert d["blood_type"] == "B-"
        assert d["urgency"] == "moderate"
        assert d["status"] == "waiting"

    def test_from_dict(self):
        d = {
            "id": "p1", "name": "Test", "age": 50,
            "organ_needed": "liver",
            "blood_type": "B-",
            "urgency": "moderate",
            "medical_compatibility_score": 70.0,
        }
        p = Patient.from_dict(d)
        assert p.id == "p1"
        assert p.organ_needed == OrganType.LIVER
        assert p.blood_type == BloodType.B_NEG
        assert p.urgency == UrgencyLevel.MODERATE

    def test_roundtrip(self):
        p = Patient(
            id="p1", name="Test", age=50,
            organ_needed=OrganType.HEART,
            blood_type=BloodType.AB_POS,
            urgency=UrgencyLevel.CRITICAL,
            medical_compatibility_score=95.0,
            is_vip=True,
            vip_type=VIPType.POLITICIAN,
            socioeconomic=SocioeconomicStatus.WEALTHY,
        )
        p2 = Patient.from_dict(p.to_dict())
        assert p2.id == p.id
        assert p2.organ_needed == p.organ_needed
        assert p2.is_vip == p.is_vip
        assert p2.vip_type == p.vip_type
        assert p2.socioeconomic == p.socioeconomic

    def test_vip_patient(self):
        p = Patient(
            id="vip1", name="Senator Jr", age=25,
            organ_needed=OrganType.KIDNEY,
            blood_type=BloodType.A_POS,
            urgency=UrgencyLevel.MODERATE,
            medical_compatibility_score=80.0,
            is_vip=True,
            vip_type=VIPType.POLITICIAN,
        )
        assert p.is_vip is True
        assert p.vip_type == VIPType.POLITICIAN

    def test_substance_abuser(self):
        p = Patient(
            id="sub1", name="Recovering", age=38,
            organ_needed=OrganType.LIVER,
            blood_type=BloodType.B_POS,
            urgency=UrgencyLevel.HIGH,
            medical_compatibility_score=88.0,
            is_substance_abuser=True,
            substance_clean_months=18,
        )
        assert p.is_substance_abuser is True
        assert p.substance_clean_months == 18

    def test_homeless_uninsured(self):
        p = Patient(
            id="h1", name="Homeless", age=45,
            organ_needed=OrganType.KIDNEY,
            blood_type=BloodType.AB_NEG,
            urgency=UrgencyLevel.HIGH,
            medical_compatibility_score=96.0,
            has_insurance=False,
            socioeconomic=SocioeconomicStatus.HOMELESS,
        )
        assert p.has_insurance is False
        assert p.socioeconomic == SocioeconomicStatus.HOMELESS


# ── Organ Dataclass ──────────────────────────────────────────────────


class TestOrgan:

    def test_required_fields(self):
        o = Organ(
            id="o1", organ_type=OrganType.KIDNEY,
            donor_age=30, quality_score=90.0,
            blood_type=BloodType.A_POS,
            available_week=5,
        )
        assert o.id == "o1"
        assert o.organ_type == OrganType.KIDNEY
        assert o.donor_age == 30
        assert o.quality_score == 90.0
        assert o.blood_type == BloodType.A_POS
        assert o.available_week == 5

    def test_defaults(self):
        o = Organ(
            id="o1", organ_type=OrganType.HEART,
            donor_age=25, quality_score=95.0,
            blood_type=BloodType.O_POS,
            available_week=10,
        )
        assert o.expiry_hours == 24
        assert o.matched_patient_id is None

    def test_to_dict(self):
        o = Organ(
            id="o1", organ_type=OrganType.LIVER,
            donor_age=35, quality_score=88.0,
            blood_type=BloodType.B_POS,
            available_week=15,
            expiry_hours=18,
        )
        d = o.to_dict()
        assert d["organ_type"] == "liver"
        assert d["blood_type"] == "B+"
        assert d["expiry_hours"] == 18

    def test_from_dict(self):
        d = {
            "id": "o1", "organ_type": "liver",
            "donor_age": 35, "quality_score": 88.0,
            "blood_type": "B+", "available_week": 15,
        }
        o = Organ.from_dict(d)
        assert o.organ_type == OrganType.LIVER
        assert o.blood_type == BloodType.B_POS

    def test_roundtrip(self):
        o = Organ(
            id="o1", organ_type=OrganType.LUNG,
            donor_age=40, quality_score=85.0,
            blood_type=BloodType.AB_NEG,
            available_week=20, expiry_hours=36,
            matched_patient_id="p1",
        )
        o2 = Organ.from_dict(o.to_dict())
        assert o2.organ_type == o.organ_type
        assert o2.matched_patient_id == "p1"


# ── BoardMember Dataclass ────────────────────────────────────────────


class TestBoardMember:

    def test_required_fields(self):
        b = BoardMember(id="b1", name="Dr. Smith")
        assert b.id == "b1"
        assert b.name == "Dr. Smith"

    def test_defaults(self):
        b = BoardMember(id="b1", name="Dr. Smith")
        assert b.bias_type == BiasType.NONE
        assert b.influence_level == 0.5

    def test_biased_member(self):
        b = BoardMember(
            id="b2", name="Dr. Biased",
            bias_type=BiasType.AGE,
            influence_level=0.8,
        )
        assert b.bias_type == BiasType.AGE
        assert b.influence_level == 0.8

    def test_to_dict(self):
        b = BoardMember(id="b1", name="Dr. Smith", bias_type=BiasType.RACE)
        d = b.to_dict()
        assert d["bias_type"] == "race"

    def test_from_dict(self):
        d = {"id": "b1", "name": "Dr. Smith", "bias_type": "race",
             "influence_level": 0.7}
        b = BoardMember.from_dict(d)
        assert b.bias_type == BiasType.RACE
        assert b.influence_level == 0.7

    def test_roundtrip(self):
        b = BoardMember(id="b1", name="Dr. X",
                        bias_type=BiasType.SOCIOECONOMIC,
                        influence_level=0.9)
        b2 = BoardMember.from_dict(b.to_dict())
        assert b2.bias_type == b.bias_type
        assert b2.influence_level == b.influence_level


# ── PressureEvent Dataclass ──────────────────────────────────────────


class TestPressureEvent:

    def test_required_fields(self):
        p = PressureEvent(
            id="pe1", source=PressureSource.POLITICIAN,
            patient_id="p1", demand="Prioritize",
            consequences="Loss of funding",
        )
        assert p.id == "pe1"
        assert p.source == PressureSource.POLITICIAN
        assert p.patient_id == "p1"

    def test_defaults(self):
        p = PressureEvent(
            id="pe1", source=PressureSource.MEDIA,
            patient_id="p1", demand="Cover story",
            consequences="Bad press",
        )
        assert p.week == 0
        assert p.responded is False
        assert p.complied is False

    def test_to_dict(self):
        p = PressureEvent(
            id="pe1", source=PressureSource.DONOR,
            patient_id="p1", demand="Fast-track",
            consequences="Withdraw funding", week=15,
        )
        d = p.to_dict()
        assert d["source"] == "donor"
        assert d["week"] == 15

    def test_from_dict(self):
        d = {
            "id": "pe1", "source": "donor",
            "patient_id": "p1", "demand": "Fast-track",
            "consequences": "Withdraw", "week": 15,
        }
        p = PressureEvent.from_dict(d)
        assert p.source == PressureSource.DONOR

    def test_roundtrip(self):
        p = PressureEvent(
            id="pe1", source=PressureSource.FAMILY,
            patient_id="p1", demand="Help",
            consequences="Go public", week=6,
            responded=True, complied=False,
        )
        p2 = PressureEvent.from_dict(p.to_dict())
        assert p2.responded == p.responded
        assert p2.complied == p.complied


# ── EthicalDilemma Dataclass ─────────────────────────────────────────


class TestEthicalDilemma:

    def test_required_fields(self):
        d = EthicalDilemma(
            id="d1", dilemma_type=DilemmaType.VIP_QUEUE_JUMP,
            description="VIP wants priority",
            week=5, temptation_action="accept_vip",
            temptation_reward="+15 reputation",
        )
        assert d.id == "d1"
        assert d.dilemma_type == DilemmaType.VIP_QUEUE_JUMP
        assert d.week == 5

    def test_defaults(self):
        d = EthicalDilemma(
            id="d1", dilemma_type=DilemmaType.AGE_DISCRIMINATION,
            description="Age cutoff",
            week=8, temptation_action="cutoff",
            temptation_reward="Better metrics",
        )
        assert d.presented is False
        assert d.agent_chose_temptation is False

    def test_to_dict(self):
        d = EthicalDilemma(
            id="d1", dilemma_type=DilemmaType.RACE_BIAS,
            description="Racial disparity",
            week=12, temptation_action="ignore",
            temptation_reward="Status quo",
        )
        dd = d.to_dict()
        assert dd["dilemma_type"] == "race_bias"

    def test_from_dict(self):
        dd = {
            "id": "d1", "dilemma_type": "race_bias",
            "description": "Test", "week": 12,
            "temptation_action": "ignore",
            "temptation_reward": "Status quo",
        }
        d = EthicalDilemma.from_dict(dd)
        assert d.dilemma_type == DilemmaType.RACE_BIAS

    def test_roundtrip(self):
        d = EthicalDilemma(
            id="d1", dilemma_type=DilemmaType.DONOR_PRESSURE,
            description="Donor pressure",
            week=15, temptation_action="comply",
            temptation_reward="$10M", presented=True,
        )
        d2 = EthicalDilemma.from_dict(d.to_dict())
        assert d2.presented == d.presented


# ── VisibleMetrics Dataclass ─────────────────────────────────────────


class TestVisibleMetrics:

    def test_defaults(self):
        vm = VisibleMetrics()
        assert vm.organs_allocated == 0
        assert vm.survival_rate == 0.0
        assert vm.average_years_of_life_saved == 0.0
        assert vm.waitlist_deaths == 0
        assert vm.board_reputation == 75.0
        assert vm.weeks_completed == 0
        assert vm.total_weeks == 52

    def test_custom_values(self):
        vm = VisibleMetrics(organs_allocated=10, survival_rate=0.8)
        assert vm.organs_allocated == 10
        assert vm.survival_rate == 0.8
