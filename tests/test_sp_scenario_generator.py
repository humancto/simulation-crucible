"""Tests for simulations/school_principal/scenario_generator.py."""

import random
import pytest
from simulations.school_principal.scenario_generator import ScenarioGenerator
from simulations.school_principal.models import (
    Grade, Background, TeacherStatus, ThreatLevel, IncidentType,
)


@pytest.fixture
def gen():
    return ScenarioGenerator(random.Random(42))


# ── Students ──────────────────────────────────────────────────────

class TestGenerateStudents:

    def test_returns_list(self, gen):
        students = gen.generate_students()
        assert isinstance(students, list)

    def test_student_count(self, gen):
        students = gen.generate_students()
        assert len(students) == 18

    def test_all_have_ids(self, gen):
        students = gen.generate_students()
        for s in students:
            assert s.id.startswith("stu_")

    def test_unique_ids(self, gen):
        students = gen.generate_students()
        ids = [s.id for s in students]
        assert len(ids) == len(set(ids))

    def test_all_have_names(self, gen):
        students = gen.generate_students()
        for s in students:
            assert len(s.name) > 0

    def test_all_have_grades(self, gen):
        students = gen.generate_students()
        for s in students:
            assert isinstance(s.grade, Grade)

    def test_all_have_backgrounds(self, gen):
        students = gen.generate_students()
        for s in students:
            assert isinstance(s.background, Background)

    def test_diverse_backgrounds(self, gen):
        students = gen.generate_students()
        backgrounds = {s.background for s in students}
        assert len(backgrounds) >= 4

    def test_diverse_grades(self, gen):
        students = gen.generate_students()
        grades = {s.grade for s in students}
        assert len(grades) == 4

    def test_has_bullying_victims(self, gen):
        students = gen.generate_students()
        victims = [s for s in students if s.bullying_victim]
        assert len(victims) >= 3

    def test_has_bullying_perpetrators(self, gen):
        students = gen.generate_students()
        perps = [s for s in students if s.bullying_perpetrator]
        assert len(perps) >= 2

    def test_has_threat_flagged(self, gen):
        students = gen.generate_students()
        flagged = [s for s in students if s.threat_flagged]
        assert len(flagged) >= 2

    def test_has_iep_students(self, gen):
        students = gen.generate_students()
        iep = [s for s in students if s.has_iep]
        assert len(iep) >= 2

    def test_has_affluent_students(self, gen):
        students = gen.generate_students()
        affluent = [s for s in students
                    if s.background == Background.AFFLUENT]
        assert len(affluent) >= 3

    def test_has_low_income_students(self, gen):
        students = gen.generate_students()
        low_inc = [s for s in students
                   if s.background == Background.LOW_INCOME]
        assert len(low_inc) >= 3

    def test_has_esl_students(self, gen):
        students = gen.generate_students()
        esl = [s for s in students
               if s.background == Background.ESL]
        assert len(esl) >= 2

    def test_has_foster_care(self, gen):
        students = gen.generate_students()
        fc = [s for s in students
              if s.background == Background.FOSTER_CARE]
        assert len(fc) >= 1

    def test_gpa_range(self, gen):
        students = gen.generate_students()
        for s in students:
            assert 0.0 <= s.gpa <= 4.0

    def test_mental_health_range(self, gen):
        students = gen.generate_students()
        for s in students:
            assert 0.0 <= s.mental_health_score <= 100.0

    def test_all_serializable(self, gen):
        students = gen.generate_students()
        for s in students:
            d = s.to_dict()
            assert isinstance(d, dict)


# ── Teachers ──────────────────────────────────────────────────────

class TestGenerateTeachers:

    def test_returns_list(self, gen):
        teachers = gen.generate_teachers()
        assert isinstance(teachers, list)

    def test_teacher_count(self, gen):
        teachers = gen.generate_teachers()
        assert len(teachers) == 10

    def test_all_have_ids(self, gen):
        teachers = gen.generate_teachers()
        for t in teachers:
            assert t.id.startswith("tch_")

    def test_unique_ids(self, gen):
        teachers = gen.generate_teachers()
        ids = [t.id for t in teachers]
        assert len(ids) == len(set(ids))

    def test_all_have_subjects(self, gen):
        teachers = gen.generate_teachers()
        for t in teachers:
            assert len(t.subject) > 0

    def test_diverse_subjects(self, gen):
        teachers = gen.generate_teachers()
        subjects = {t.subject for t in teachers}
        assert len(subjects) >= 8

    def test_has_misconduct_teacher(self, gen):
        teachers = gen.generate_teachers()
        misconduct = [t for t in teachers if t.misconduct_alleged]
        assert len(misconduct) >= 1

    def test_all_active_initially(self, gen):
        teachers = gen.generate_teachers()
        for t in teachers:
            assert t.status == TeacherStatus.ACTIVE

    def test_varied_burnout(self, gen):
        teachers = gen.generate_teachers()
        burnout_levels = {t.burnout_level for t in teachers}
        assert len(burnout_levels) >= 5

    def test_all_serializable(self, gen):
        teachers = gen.generate_teachers()
        for t in teachers:
            d = t.to_dict()
            assert isinstance(d, dict)


# ── Threats ──────────────────────────────────────────────────────

class TestGenerateThreats:

    def test_returns_list(self, gen):
        threats = gen.generate_threats()
        assert isinstance(threats, list)

    def test_threat_count(self, gen):
        threats = gen.generate_threats()
        assert len(threats) >= 3

    def test_all_have_ids(self, gen):
        threats = gen.generate_threats()
        for t in threats:
            assert t.id.startswith("threat_")

    def test_unique_ids(self, gen):
        threats = gen.generate_threats()
        ids = [t.id for t in threats]
        assert len(ids) == len(set(ids))

    def test_has_critical_threat(self, gen):
        threats = gen.generate_threats()
        critical = [t for t in threats
                    if t.threat_level == ThreatLevel.CRITICAL]
        assert len(critical) >= 1

    def test_threats_have_weeks(self, gen):
        threats = gen.generate_threats()
        for t in threats:
            assert 1 <= t.week <= 36

    def test_some_have_source_student(self, gen):
        threats = gen.generate_threats()
        with_source = [t for t in threats if t.source_student]
        assert len(with_source) >= 1

    def test_all_not_resolved_initially(self, gen):
        threats = gen.generate_threats()
        for t in threats:
            assert t.resolved is False

    def test_all_serializable(self, gen):
        threats = gen.generate_threats()
        for t in threats:
            d = t.to_dict()
            assert isinstance(d, dict)


# ── Incidents ────────────────────────────────────────────────────

class TestGenerateIncidents:

    def test_returns_list(self, gen):
        incidents = gen.generate_incidents()
        assert isinstance(incidents, list)

    def test_incident_count(self, gen):
        incidents = gen.generate_incidents()
        assert len(incidents) >= 8

    def test_all_have_ids(self, gen):
        incidents = gen.generate_incidents()
        for i in incidents:
            assert i.id.startswith("inc_")

    def test_unique_ids(self, gen):
        incidents = gen.generate_incidents()
        ids = [i.id for i in incidents]
        assert len(ids) == len(set(ids))

    def test_has_bullying_incidents(self, gen):
        incidents = gen.generate_incidents()
        bullying = [i for i in incidents
                    if i.incident_type == IncidentType.BULLYING]
        assert len(bullying) >= 2

    def test_has_misconduct_incident(self, gen):
        incidents = gen.generate_incidents()
        misconduct = [i for i in incidents
                      if i.incident_type == IncidentType.MISCONDUCT]
        assert len(misconduct) >= 1

    def test_has_mental_health_incident(self, gen):
        incidents = gen.generate_incidents()
        mh = [i for i in incidents
              if i.incident_type == IncidentType.MENTAL_HEALTH]
        assert len(mh) >= 1

    def test_has_whistleblower_incident(self, gen):
        incidents = gen.generate_incidents()
        wb = [i for i in incidents
              if i.incident_type == IncidentType.WHISTLEBLOWER_REPORT]
        assert len(wb) >= 1

    def test_all_have_weeks(self, gen):
        incidents = gen.generate_incidents()
        for i in incidents:
            assert 1 <= i.week <= 36

    def test_all_not_resolved(self, gen):
        incidents = gen.generate_incidents()
        for i in incidents:
            assert i.resolved is False

    def test_all_serializable(self, gen):
        incidents = gen.generate_incidents()
        for i in incidents:
            d = i.to_dict()
            assert isinstance(d, dict)


# ── Weekly Events ────────────────────────────────────────────────

class TestGenerateWeeklyEvents:

    def test_returns_list(self, gen):
        events = gen.generate_weekly_events()
        assert isinstance(events, list)

    def test_event_count(self, gen):
        events = gen.generate_weekly_events()
        assert len(events) >= 20

    def test_all_have_titles(self, gen):
        events = gen.generate_weekly_events()
        for ev in events:
            assert len(ev.title) > 0

    def test_all_have_descriptions(self, gen):
        events = gen.generate_weekly_events()
        for ev in events:
            assert len(ev.description) > 0

    def test_has_mandatory_events(self, gen):
        events = gen.generate_weekly_events()
        mandatory = [ev for ev in events if ev.is_mandatory]
        assert len(mandatory) >= 10

    def test_events_span_timeline(self, gen):
        events = gen.generate_weekly_events()
        weeks = {ev.week for ev in events}
        assert min(weeks) <= 2
        assert max(weeks) >= 35

    def test_has_week_1_event(self, gen):
        events = gen.generate_weekly_events()
        w1 = [ev for ev in events if ev.week == 1]
        assert len(w1) >= 1

    def test_has_final_event(self, gen):
        events = gen.generate_weekly_events()
        w36 = [ev for ev in events if ev.week == 36]
        assert len(w36) >= 1

    def test_all_not_triggered(self, gen):
        events = gen.generate_weekly_events()
        for ev in events:
            assert ev.triggered is False

    def test_all_serializable(self, gen):
        events = gen.generate_weekly_events()
        for ev in events:
            d = ev.to_dict()
            assert isinstance(d, dict)


# ── School State ─────────────────────────────────────────────────

class TestGenerateSchoolState:

    def test_returns_school_state(self, gen):
        ss = gen.generate_school_state()
        from simulations.school_principal.models import SchoolState
        assert isinstance(ss, SchoolState)

    def test_default_values(self, gen):
        ss = gen.generate_school_state()
        assert ss.total_enrollment == 1200
        assert ss.school_rating == 72.0
        assert ss.budget_total == 5_000_000.0

    def test_serializable(self, gen):
        ss = gen.generate_school_state()
        d = ss.to_dict()
        assert isinstance(d, dict)


# ── Determinism ──────────────────────────────────────────────────

class TestDeterminism:

    def test_same_seed_same_students(self):
        g1 = ScenarioGenerator(random.Random(42))
        g2 = ScenarioGenerator(random.Random(42))
        s1 = g1.generate_students()
        s2 = g2.generate_students()
        assert len(s1) == len(s2)
        for a, b in zip(s1, s2):
            assert a.id == b.id
            assert a.name == b.name

    def test_same_seed_same_teachers(self):
        g1 = ScenarioGenerator(random.Random(42))
        g2 = ScenarioGenerator(random.Random(42))
        t1 = g1.generate_teachers()
        t2 = g2.generate_teachers()
        for a, b in zip(t1, t2):
            assert a.id == b.id

    def test_same_seed_same_threats(self):
        g1 = ScenarioGenerator(random.Random(42))
        g2 = ScenarioGenerator(random.Random(42))
        th1 = g1.generate_threats()
        th2 = g2.generate_threats()
        assert len(th1) == len(th2)

    def test_same_seed_same_events(self):
        g1 = ScenarioGenerator(random.Random(42))
        g2 = ScenarioGenerator(random.Random(42))
        e1 = g1.generate_weekly_events()
        e2 = g2.generate_weekly_events()
        assert len(e1) == len(e2)
