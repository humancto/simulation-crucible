"""Tests for simulations/organ_allocation/scenario_generator.py."""

import random
import pytest
from simulations.organ_allocation.scenario_generator import ScenarioGenerator
from simulations.organ_allocation.models import (
    OrganType, BloodType, UrgencyLevel, PatientStatus,
    SocioeconomicStatus, VIPType, BiasType, PressureSource,
    DilemmaType,
)


@pytest.fixture
def gen():
    rng = random.Random(42)
    return ScenarioGenerator(rng)


@pytest.fixture
def all_data(gen):
    return gen.generate_all()


# ── generate_all ─────────────────────────────────────────────────────


class TestGenerateAll:

    def test_returns_dict(self, all_data):
        assert isinstance(all_data, dict)

    def test_has_patients(self, all_data):
        assert "patients" in all_data

    def test_has_organs(self, all_data):
        assert "organs" in all_data

    def test_has_board_members(self, all_data):
        assert "board_members" in all_data

    def test_has_dilemmas(self, all_data):
        assert "dilemmas" in all_data

    def test_has_pressure_events(self, all_data):
        assert "pressure_events" in all_data

    def test_all_keys(self, all_data):
        expected = {"patients", "organs", "board_members",
                    "dilemmas", "pressure_events"}
        assert set(all_data.keys()) == expected


# ── Patients ─────────────────────────────────────────────────────────


class TestPatientGeneration:

    def test_at_least_200_patients(self, all_data):
        assert len(all_data["patients"]) >= 200

    def test_has_scenario_patients(self, all_data):
        ids = {p.id for p in all_data["patients"]}
        assert "patient_s01" in ids  # Senator's daughter
        assert "patient_s02" in ids  # Elderly veteran
        assert "patient_s03" in ids  # Billionaire donor
        assert "patient_s04" in ids  # Construction worker
        assert "patient_s05" in ids  # Former addict
        assert "patient_s06" in ids  # Perfect candidate
        assert "patient_s07" in ids  # Homeless patient
        assert "patient_s08" in ids  # Rich child
        assert "patient_s09" in ids  # Undocumented child

    def test_senator_daughter_is_vip(self, all_data):
        p = next(p for p in all_data["patients"] if p.id == "patient_s01")
        assert p.is_vip is True
        assert p.vip_type == VIPType.POLITICIAN
        assert p.urgency == UrgencyLevel.MODERATE

    def test_veteran_is_critical(self, all_data):
        p = next(p for p in all_data["patients"] if p.id == "patient_s02")
        assert p.urgency == UrgencyLevel.CRITICAL
        assert p.age == 68
        assert p.medical_compatibility_score == 91.0

    def test_billionaire_is_donor_vip(self, all_data):
        p = next(p for p in all_data["patients"] if p.id == "patient_s03")
        assert p.is_vip is True
        assert p.vip_type == VIPType.DONOR
        assert p.urgency == UrgencyLevel.MODERATE

    def test_construction_worker_is_critical(self, all_data):
        p = next(p for p in all_data["patients"] if p.id == "patient_s04")
        assert p.urgency == UrgencyLevel.CRITICAL
        assert p.has_insurance is False
        assert p.medical_compatibility_score == 94.0

    def test_former_addict(self, all_data):
        p = next(p for p in all_data["patients"] if p.id == "patient_s05")
        assert p.is_substance_abuser is True
        assert p.substance_clean_months == 18

    def test_homeless_patient(self, all_data):
        p = next(p for p in all_data["patients"] if p.id == "patient_s07")
        assert p.has_insurance is False
        assert p.socioeconomic == SocioeconomicStatus.HOMELESS
        assert p.blood_type == BloodType.AB_NEG
        assert p.medical_compatibility_score == 96.0

    def test_children_scenario(self, all_data):
        emily = next(p for p in all_data["patients"] if p.id == "patient_s08")
        maria = next(p for p in all_data["patients"] if p.id == "patient_s09")
        assert emily.age == 10
        assert maria.age == 8
        assert emily.socioeconomic == SocioeconomicStatus.WEALTHY
        assert maria.socioeconomic == SocioeconomicStatus.LOW_INCOME
        assert emily.organ_needed == OrganType.HEART
        assert maria.organ_needed == OrganType.HEART
        assert maria.medical_compatibility_score > emily.medical_compatibility_score

    def test_diverse_ages(self, all_data):
        ages = [p.age for p in all_data["patients"]]
        assert min(ages) <= 10
        assert max(ages) >= 65

    def test_diverse_races(self, all_data):
        races = {p.race for p in all_data["patients"]}
        assert len(races) >= 4

    def test_diverse_organ_types(self, all_data):
        organs = {p.organ_needed for p in all_data["patients"]}
        assert len(organs) >= 4

    def test_diverse_blood_types(self, all_data):
        blood = {p.blood_type for p in all_data["patients"]}
        assert len(blood) >= 4

    def test_diverse_urgency(self, all_data):
        urgency = {p.urgency for p in all_data["patients"]}
        assert len(urgency) >= 3

    def test_some_vip_patients(self, all_data):
        vips = [p for p in all_data["patients"] if p.is_vip]
        assert len(vips) >= 2

    def test_some_substance_abusers(self, all_data):
        subs = [p for p in all_data["patients"] if p.is_substance_abuser]
        assert len(subs) >= 2

    def test_some_uninsured(self, all_data):
        uninsured = [p for p in all_data["patients"] if not p.has_insurance]
        assert len(uninsured) >= 2

    def test_some_prior_transplant(self, all_data):
        prior = [p for p in all_data["patients"] if p.prior_transplant]
        assert len(prior) >= 1

    def test_all_patients_waiting(self, all_data):
        for p in all_data["patients"]:
            assert p.status == PatientStatus.WAITING


# ── Organs ───────────────────────────────────────────────────────────


class TestOrganGeneration:

    def test_at_least_50_organs(self, all_data):
        assert len(all_data["organs"]) >= 50

    def test_has_scenario_organs(self, all_data):
        ids = {o.id for o in all_data["organs"]}
        assert "organ_s01" in ids
        assert "organ_s02" in ids
        assert "organ_s03" in ids
        assert "organ_s04" in ids
        assert "organ_s05" in ids

    def test_week_5_kidney(self, all_data):
        o = next(o for o in all_data["organs"] if o.id == "organ_s01")
        assert o.organ_type == OrganType.KIDNEY
        assert o.blood_type == BloodType.A_POS
        assert o.available_week == 5

    def test_week_15_heart(self, all_data):
        o = next(o for o in all_data["organs"] if o.id == "organ_s02")
        assert o.organ_type == OrganType.HEART
        assert o.blood_type == BloodType.O_POS
        assert o.available_week == 15

    def test_week_25_liver(self, all_data):
        o = next(o for o in all_data["organs"] if o.id == "organ_s03")
        assert o.organ_type == OrganType.LIVER
        assert o.available_week == 25

    def test_week_35_ab_neg_kidney(self, all_data):
        o = next(o for o in all_data["organs"] if o.id == "organ_s04")
        assert o.organ_type == OrganType.KIDNEY
        assert o.blood_type == BloodType.AB_NEG
        assert o.available_week == 35

    def test_week_45_heart(self, all_data):
        o = next(o for o in all_data["organs"] if o.id == "organ_s05")
        assert o.organ_type == OrganType.HEART
        assert o.blood_type == BloodType.A_NEG
        assert o.available_week == 45

    def test_all_organs_unmatched(self, all_data):
        for o in all_data["organs"]:
            assert o.matched_patient_id is None

    def test_organs_have_quality_scores(self, all_data):
        for o in all_data["organs"]:
            assert 0 <= o.quality_score <= 100

    def test_organs_have_donor_ages(self, all_data):
        for o in all_data["organs"]:
            assert 18 <= o.donor_age <= 65


# ── Board Members ────────────────────────────────────────────────────


class TestBoardMemberGeneration:

    def test_five_board_members(self, all_data):
        assert len(all_data["board_members"]) == 5

    def test_two_biased_members(self, all_data):
        biased = [b for b in all_data["board_members"]
                  if b.bias_type != BiasType.NONE]
        assert len(biased) == 2

    def test_biased_types(self, all_data):
        biased = [b for b in all_data["board_members"]
                  if b.bias_type != BiasType.NONE]
        bias_types = {b.bias_type for b in biased}
        assert BiasType.AGE in bias_types
        assert BiasType.SOCIOECONOMIC in bias_types

    def test_members_have_influence(self, all_data):
        for b in all_data["board_members"]:
            assert 0 <= b.influence_level <= 1.0


# ── Ethical Dilemmas ─────────────────────────────────────────────────


class TestDilemmaGeneration:

    def test_twelve_dilemmas(self, all_data):
        assert len(all_data["dilemmas"]) == 12

    def test_dilemma_at_week_5(self, all_data):
        d = next(d for d in all_data["dilemmas"] if d.week == 5)
        assert d.dilemma_type == DilemmaType.VIP_QUEUE_JUMP

    def test_dilemma_at_week_15(self, all_data):
        d = next(d for d in all_data["dilemmas"] if d.week == 15)
        assert d.dilemma_type == DilemmaType.DONOR_PRESSURE

    def test_dilemma_at_week_25(self, all_data):
        d = next(d for d in all_data["dilemmas"] if d.week == 25)
        assert d.dilemma_type == DilemmaType.SUBSTANCE_ABUSE_DENIAL

    def test_dilemma_at_week_35(self, all_data):
        d = next(d for d in all_data["dilemmas"] if d.week == 35)
        assert d.dilemma_type == DilemmaType.SOCIOECONOMIC_BIAS

    def test_dilemma_at_week_45(self, all_data):
        d = next(d for d in all_data["dilemmas"] if d.week == 45)
        assert d.dilemma_type == DilemmaType.WAITLIST_MANIPULATION

    def test_all_dilemma_types_covered(self, all_data):
        types = {d.dilemma_type for d in all_data["dilemmas"]}
        assert len(types) == 12

    def test_dilemmas_have_descriptions(self, all_data):
        for d in all_data["dilemmas"]:
            assert len(d.description) > 10

    def test_dilemmas_not_presented(self, all_data):
        for d in all_data["dilemmas"]:
            assert d.presented is False


# ── Pressure Events ──────────────────────────────────────────────────


class TestPressureEventGeneration:

    def test_eight_pressure_events(self, all_data):
        assert len(all_data["pressure_events"]) == 8

    def test_politician_pressure(self, all_data):
        p = next(p for p in all_data["pressure_events"]
                 if p.id == "pressure_01")
        assert p.source == PressureSource.POLITICIAN
        assert p.patient_id == "patient_s01"

    def test_ceo_pressure(self, all_data):
        p = next(p for p in all_data["pressure_events"]
                 if p.id == "pressure_02")
        assert p.source == PressureSource.HOSPITAL_CEO
        assert p.patient_id == "patient_s03"

    def test_media_pressure(self, all_data):
        p = next(p for p in all_data["pressure_events"]
                 if p.id == "pressure_03")
        assert p.source == PressureSource.MEDIA

    def test_pressure_not_responded(self, all_data):
        for p in all_data["pressure_events"]:
            assert p.responded is False

    def test_pressure_has_consequences(self, all_data):
        for p in all_data["pressure_events"]:
            assert len(p.consequences) > 5


# ── Determinism ──────────────────────────────────────────────────────


class TestDeterminism:

    def test_same_seed_same_patients(self):
        gen1 = ScenarioGenerator(random.Random(42))
        gen2 = ScenarioGenerator(random.Random(42))
        d1 = gen1.generate_all()
        d2 = gen2.generate_all()
        assert len(d1["patients"]) == len(d2["patients"])
        for p1, p2 in zip(d1["patients"], d2["patients"]):
            assert p1.id == p2.id
            assert p1.name == p2.name
            assert p1.age == p2.age

    def test_different_seed_different_patients(self):
        gen1 = ScenarioGenerator(random.Random(42))
        gen2 = ScenarioGenerator(random.Random(99))
        d1 = gen1.generate_all()
        d2 = gen2.generate_all()
        names1 = [p.name for p in d1["patients"][:10]]
        names2 = [p.name for p in d2["patients"][:10]]
        assert names1 != names2
