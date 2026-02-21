"""Tests for simulations/school_principal/models.py."""

import pytest
from simulations.school_principal.models import (
    Student, Grade, Background, DisciplineStatus,
    Teacher, TeacherStatus,
    Incident, IncidentType, ThreatLevel,
    Threat,
    WeeklyEvent,
    SchoolState,
    BudgetProgram, BullyingApproach, StaffSupportAction,
)


# ── Enums ──────────────────────────────────────────────────────────

class TestEnums:

    def test_grade_values(self):
        assert Grade.FRESHMAN.value == "freshman"
        assert Grade.SENIOR.value == "senior"

    def test_background_values(self):
        assert Background.AFFLUENT.value == "affluent"
        assert Background.LOW_INCOME.value == "low_income"
        assert Background.ESL.value == "esl"
        assert Background.FOSTER_CARE.value == "foster_care"
        assert Background.SPECIAL_NEEDS.value == "special_needs"

    def test_discipline_status_values(self):
        assert DisciplineStatus.CLEAN.value == "clean"
        assert DisciplineStatus.EXPELLED.value == "expelled"
        assert DisciplineStatus.HEARING_PENDING.value == "hearing_pending"

    def test_teacher_status_values(self):
        assert TeacherStatus.ACTIVE.value == "active"
        assert TeacherStatus.FIRED.value == "fired"
        assert TeacherStatus.WHISTLEBLOWER_PROTECTED.value == "whistleblower_protected"

    def test_threat_level_values(self):
        assert ThreatLevel.LOW.value == "low"
        assert ThreatLevel.CRITICAL.value == "critical"

    def test_incident_type_values(self):
        assert IncidentType.BULLYING.value == "bullying"
        assert IncidentType.SHOOTING_THREAT.value == "shooting_threat"
        assert IncidentType.MISCONDUCT.value == "misconduct"
        assert IncidentType.WHISTLEBLOWER_REPORT.value == "whistleblower_report"

    def test_bullying_approach_values(self):
        assert BullyingApproach.RESTORATIVE_JUSTICE.value == "restorative_justice"
        assert BullyingApproach.IGNORE.value == "ignore"

    def test_staff_support_action_values(self):
        assert StaffSupportAction.COUNSELING.value == "counseling"
        assert StaffSupportAction.REDUCED_LOAD.value == "reduced_load"

    def test_budget_program_values(self):
        assert BudgetProgram.SAFETY.value == "safety"
        assert BudgetProgram.MENTAL_HEALTH.value == "mental_health"
        assert BudgetProgram.ARTS.value == "arts"
        assert BudgetProgram.SPECIAL_ED.value == "special_ed"


# ── Student ────────────────────────────────────────────────────────

class TestStudent:

    def test_create_student(self):
        s = Student(id="s1", name="Alice", grade=Grade.FRESHMAN,
                    background=Background.AFFLUENT)
        assert s.id == "s1"
        assert s.name == "Alice"
        assert s.grade == Grade.FRESHMAN
        assert s.background == Background.AFFLUENT

    def test_student_defaults(self):
        s = Student(id="s1", name="Bob", grade=Grade.JUNIOR,
                    background=Background.LOW_INCOME)
        assert s.gpa == 3.0
        assert s.discipline_status == DisciplineStatus.CLEAN
        assert s.mental_health_score == 75.0
        assert s.bullying_victim is False
        assert s.bullying_perpetrator is False
        assert s.threat_flagged is False
        assert s.has_iep is False
        assert s.expelled_without_hearing is False
        assert s.parent_complaint is False

    def test_student_to_dict(self):
        s = Student(id="s1", name="Alice", grade=Grade.SOPHOMORE,
                    background=Background.ESL, gpa=3.5)
        d = s.to_dict()
        assert d["id"] == "s1"
        assert d["name"] == "Alice"
        assert d["grade"] == "sophomore"
        assert d["background"] == "esl"
        assert d["gpa"] == 3.5

    def test_student_to_dict_has_all_fields(self):
        s = Student(id="s1", name="A", grade=Grade.SENIOR,
                    background=Background.FOSTER_CARE)
        d = s.to_dict()
        expected_keys = {
            "id", "name", "grade", "background", "gpa",
            "discipline_status", "mental_health_score",
            "bullying_victim", "bullying_perpetrator", "threat_flagged",
            "has_iep", "expelled_without_hearing", "parent_complaint",
        }
        assert set(d.keys()) == expected_keys

    def test_student_from_dict(self):
        d = {
            "id": "s2", "name": "Cara", "grade": "junior",
            "background": "middle_class", "gpa": 3.7,
            "discipline_status": "warning",
            "mental_health_score": 60.0,
            "bullying_victim": True,
        }
        s = Student.from_dict(d)
        assert s.id == "s2"
        assert s.name == "Cara"
        assert s.grade == Grade.JUNIOR
        assert s.background == Background.MIDDLE_CLASS
        assert s.gpa == 3.7
        assert s.discipline_status == DisciplineStatus.WARNING
        assert s.mental_health_score == 60.0
        assert s.bullying_victim is True

    def test_student_roundtrip(self):
        s = Student(id="s1", name="Test", grade=Grade.SENIOR,
                    background=Background.LOW_INCOME, gpa=2.5,
                    bullying_victim=True, has_iep=True)
        d = s.to_dict()
        s2 = Student.from_dict(d)
        assert s.id == s2.id
        assert s.gpa == s2.gpa
        assert s.bullying_victim == s2.bullying_victim
        assert s.has_iep == s2.has_iep

    def test_student_from_dict_defaults(self):
        d = {"id": "s1", "name": "X", "grade": "freshman",
             "background": "affluent"}
        s = Student.from_dict(d)
        assert s.gpa == 3.0
        assert s.mental_health_score == 75.0
        assert s.bullying_victim is False


# ── Teacher ────────────────────────────────────────────────────────

class TestTeacher:

    def test_create_teacher(self):
        t = Teacher(id="t1", name="Smith", subject="Math",
                    years_experience=10)
        assert t.id == "t1"
        assert t.name == "Smith"
        assert t.subject == "Math"
        assert t.years_experience == 10

    def test_teacher_defaults(self):
        t = Teacher(id="t1", name="A", subject="Art",
                    years_experience=5)
        assert t.status == TeacherStatus.ACTIVE
        assert t.burnout_level == 20.0
        assert t.satisfaction == 70.0
        assert t.misconduct_alleged is False
        assert t.is_whistleblower is False
        assert t.fired_without_investigation is False

    def test_teacher_to_dict(self):
        t = Teacher(id="t1", name="Jones", subject="Science",
                    years_experience=15, burnout_level=45.0)
        d = t.to_dict()
        assert d["id"] == "t1"
        assert d["burnout_level"] == 45.0
        assert d["status"] == "active"

    def test_teacher_to_dict_all_fields(self):
        t = Teacher(id="t1", name="A", subject="B", years_experience=1)
        d = t.to_dict()
        expected = {
            "id", "name", "subject", "years_experience", "status",
            "burnout_level", "satisfaction", "misconduct_alleged",
            "misconduct_investigated", "is_whistleblower",
            "whistleblower_protected", "fired_without_investigation",
        }
        assert set(d.keys()) == expected

    def test_teacher_from_dict(self):
        d = {
            "id": "t2", "name": "Dr. X", "subject": "History",
            "years_experience": 20, "status": "under_investigation",
            "burnout_level": 60.0, "satisfaction": 40.0,
            "misconduct_alleged": True,
        }
        t = Teacher.from_dict(d)
        assert t.status == TeacherStatus.UNDER_INVESTIGATION
        assert t.misconduct_alleged is True
        assert t.burnout_level == 60.0

    def test_teacher_roundtrip(self):
        t = Teacher(id="t1", name="Test", subject="PE",
                    years_experience=8,
                    status=TeacherStatus.ON_LEAVE,
                    burnout_level=70.0, is_whistleblower=True)
        d = t.to_dict()
        t2 = Teacher.from_dict(d)
        assert t.id == t2.id
        assert t.status == t2.status
        assert t.burnout_level == t2.burnout_level
        assert t.is_whistleblower == t2.is_whistleblower


# ── Incident ──────────────────────────────────────────────────────

class TestIncident:

    def test_create_incident(self):
        inc = Incident(id="i1", week=5,
                       incident_type=IncidentType.BULLYING,
                       description="Test incident")
        assert inc.id == "i1"
        assert inc.week == 5
        assert inc.incident_type == IncidentType.BULLYING

    def test_incident_defaults(self):
        inc = Incident(id="i1", week=1,
                       incident_type=IncidentType.VIOLENCE,
                       description="Test")
        assert inc.severity == ThreatLevel.MODERATE
        assert inc.investigated is False
        assert inc.covered_up is False
        assert inc.resolved is False
        assert inc.resolution is None
        assert inc.involved_students == []
        assert inc.involved_teachers == []

    def test_incident_to_dict(self):
        inc = Incident(id="i1", week=3,
                       incident_type=IncidentType.MISCONDUCT,
                       description="Teacher issue",
                       severity=ThreatLevel.HIGH,
                       involved_teachers=["t1"])
        d = inc.to_dict()
        assert d["id"] == "i1"
        assert d["incident_type"] == "misconduct"
        assert d["severity"] == "high"
        assert d["involved_teachers"] == ["t1"]

    def test_incident_from_dict(self):
        d = {
            "id": "i2", "week": 10,
            "incident_type": "shooting_threat",
            "description": "Serious threat",
            "severity": "critical",
            "investigated": True,
            "involved_students": ["s1", "s2"],
        }
        inc = Incident.from_dict(d)
        assert inc.incident_type == IncidentType.SHOOTING_THREAT
        assert inc.severity == ThreatLevel.CRITICAL
        assert inc.investigated is True
        assert len(inc.involved_students) == 2

    def test_incident_roundtrip(self):
        inc = Incident(id="i1", week=7,
                       incident_type=IncidentType.MENTAL_HEALTH,
                       description="Crisis",
                       covered_up=True)
        d = inc.to_dict()
        inc2 = Incident.from_dict(d)
        assert inc.id == inc2.id
        assert inc.covered_up == inc2.covered_up


# ── Threat ────────────────────────────────────────────────────────

class TestThreat:

    def test_create_threat(self):
        t = Threat(id="th1", week=8, description="Note found")
        assert t.id == "th1"
        assert t.week == 8

    def test_threat_defaults(self):
        t = Threat(id="th1", week=1, description="Test")
        assert t.threat_level == ThreatLevel.MODERATE
        assert t.source_student is None
        assert t.investigated is False
        assert t.resolved is False

    def test_threat_to_dict(self):
        t = Threat(id="th1", week=5, description="Threat",
                   threat_level=ThreatLevel.CRITICAL,
                   source_student="s1")
        d = t.to_dict()
        assert d["threat_level"] == "critical"
        assert d["source_student"] == "s1"

    def test_threat_from_dict(self):
        d = {
            "id": "th2", "week": 12, "description": "Email threat",
            "threat_level": "high", "investigated": True,
            "resolved": True,
        }
        t = Threat.from_dict(d)
        assert t.threat_level == ThreatLevel.HIGH
        assert t.investigated is True
        assert t.resolved is True

    def test_threat_roundtrip(self):
        t = Threat(id="th1", week=3, description="Test",
                   threat_level=ThreatLevel.LOW,
                   source_student="s5",
                   resolution="Resolved peacefully")
        d = t.to_dict()
        t2 = Threat.from_dict(d)
        assert t.id == t2.id
        assert t.source_student == t2.source_student


# ── WeeklyEvent ──────────────────────────────────────────────────

class TestWeeklyEvent:

    def test_create_event(self):
        ev = WeeklyEvent(week=1, title="First Day",
                         description="Orientation")
        assert ev.week == 1
        assert ev.title == "First Day"

    def test_event_defaults(self):
        ev = WeeklyEvent(week=1, title="T", description="D")
        assert ev.triggered is False
        assert ev.is_mandatory is False
        assert ev.outcome is None

    def test_event_to_dict(self):
        ev = WeeklyEvent(week=5, title="Crisis",
                         description="Bad things",
                         is_mandatory=True)
        d = ev.to_dict()
        assert d["week"] == 5
        assert d["is_mandatory"] is True

    def test_event_from_dict(self):
        d = {
            "week": 10, "title": "Mid Year",
            "description": "Assessment",
            "triggered": True,
            "is_mandatory": True,
            "outcome": "Survived",
        }
        ev = WeeklyEvent.from_dict(d)
        assert ev.triggered is True
        assert ev.outcome == "Survived"

    def test_event_roundtrip(self):
        ev = WeeklyEvent(week=36, title="End",
                         description="Final",
                         is_mandatory=True)
        d = ev.to_dict()
        ev2 = WeeklyEvent.from_dict(d)
        assert ev.week == ev2.week
        assert ev.title == ev2.title


# ── SchoolState ──────────────────────────────────────────────────

class TestSchoolState:

    def test_create_default(self):
        ss = SchoolState()
        assert ss.total_enrollment == 1200
        assert ss.school_rating == 72.0
        assert ss.test_scores == 68.0
        assert ss.enrollment_retention == 95.0
        assert ss.budget_total == 5_000_000.0

    def test_state_to_dict(self):
        ss = SchoolState()
        d = ss.to_dict()
        assert d["total_enrollment"] == 1200
        assert d["school_rating"] == 72.0
        assert "budget_remaining" in d
        assert "parent_satisfaction" in d

    def test_state_to_dict_all_fields(self):
        ss = SchoolState()
        d = ss.to_dict()
        expected = {
            "total_enrollment", "school_rating", "test_scores",
            "enrollment_retention", "budget_total", "budget_remaining",
            "budget_safety", "budget_mental_health", "budget_academics",
            "budget_arts", "budget_special_ed", "budget_staff_development",
            "parent_satisfaction", "media_attention",
            "bullying_reports", "threats_reported", "incidents_total",
            "hearings_held", "expulsions",
            "honest_communications", "dishonest_communications",
        }
        assert set(d.keys()) == expected

    def test_state_from_dict(self):
        d = {
            "total_enrollment": 1100,
            "school_rating": 60.0,
            "test_scores": 55.0,
            "enrollment_retention": 88.0,
            "budget_remaining": 3_000_000.0,
        }
        ss = SchoolState.from_dict(d)
        assert ss.total_enrollment == 1100
        assert ss.school_rating == 60.0
        assert ss.budget_remaining == 3_000_000.0

    def test_state_roundtrip(self):
        ss = SchoolState()
        ss.school_rating = 80.0
        ss.budget_remaining = 4_000_000.0
        ss.expulsions = 2
        d = ss.to_dict()
        ss2 = SchoolState.from_dict(d)
        assert ss.school_rating == ss2.school_rating
        assert ss.budget_remaining == ss2.budget_remaining
        assert ss.expulsions == ss2.expulsions

    def test_state_from_dict_defaults(self):
        d = {}
        ss = SchoolState.from_dict(d)
        assert ss.total_enrollment == 1200
        assert ss.budget_total == 5_000_000.0
