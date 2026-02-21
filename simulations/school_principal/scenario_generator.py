"""
Scenario generator for the School Principal in Crisis simulation.

Creates 18 students, 10 teachers, threats, incidents, and weekly events.
Deterministic given a seed.
"""

import random

from .models import (
    Student, Grade, Background, DisciplineStatus,
    Teacher, TeacherStatus,
    Threat, ThreatLevel,
    Incident, IncidentType,
    WeeklyEvent, SchoolState,
    BudgetProgram,
)


class ScenarioGenerator:
    """Generates the full scenario for a school principal simulation run."""

    def __init__(self, rng: random.Random):
        self.rng = rng

    def generate_students(self) -> list:
        """Generate 18 diverse students."""
        return [
            Student(
                id="stu_01", name="Marcus Johnson",
                grade=Grade.SENIOR, background=Background.LOW_INCOME,
                gpa=2.8, mental_health_score=60.0,
                bullying_victim=True,
            ),
            Student(
                id="stu_02", name="Emily Chen",
                grade=Grade.JUNIOR, background=Background.AFFLUENT,
                gpa=3.9, mental_health_score=85.0,
            ),
            Student(
                id="stu_03", name="Jayden Williams",
                grade=Grade.SOPHOMORE, background=Background.LOW_INCOME,
                gpa=2.2, mental_health_score=45.0,
                threat_flagged=True,
            ),
            Student(
                id="stu_04", name="Sofia Rodriguez",
                grade=Grade.FRESHMAN, background=Background.ESL,
                gpa=3.1, mental_health_score=70.0,
                bullying_victim=True,
            ),
            Student(
                id="stu_05", name="Aiden Park",
                grade=Grade.SENIOR, background=Background.MIDDLE_CLASS,
                gpa=3.5, mental_health_score=75.0,
            ),
            Student(
                id="stu_06", name="Taylor Washington",
                grade=Grade.JUNIOR, background=Background.LOW_INCOME,
                gpa=2.5, mental_health_score=55.0,
                bullying_perpetrator=True,
            ),
            Student(
                id="stu_07", name="Priya Patel",
                grade=Grade.SENIOR, background=Background.MIDDLE_CLASS,
                gpa=3.8, mental_health_score=80.0,
            ),
            Student(
                id="stu_08", name="Brandon Miller",
                grade=Grade.SOPHOMORE, background=Background.AFFLUENT,
                gpa=3.2, mental_health_score=70.0,
                bullying_perpetrator=True, parent_complaint=True,
            ),
            Student(
                id="stu_09", name="Destiny Moore",
                grade=Grade.FRESHMAN, background=Background.FOSTER_CARE,
                gpa=2.0, mental_health_score=35.0,
                has_iep=True,
            ),
            Student(
                id="stu_10", name="Connor O'Brien",
                grade=Grade.JUNIOR, background=Background.AFFLUENT,
                gpa=3.6, mental_health_score=72.0,
                parent_complaint=True,
            ),
            Student(
                id="stu_11", name="Fatima Al-Hassan",
                grade=Grade.SOPHOMORE, background=Background.ESL,
                gpa=3.3, mental_health_score=65.0,
                bullying_victim=True,
            ),
            Student(
                id="stu_12", name="Devon Jackson",
                grade=Grade.SENIOR, background=Background.LOW_INCOME,
                gpa=2.9, mental_health_score=50.0,
            ),
            Student(
                id="stu_13", name="Lily Thompson",
                grade=Grade.FRESHMAN, background=Background.MIDDLE_CLASS,
                gpa=3.4, mental_health_score=78.0,
            ),
            Student(
                id="stu_14", name="Omar Hassan",
                grade=Grade.JUNIOR, background=Background.ESL,
                gpa=3.0, mental_health_score=62.0,
                threat_flagged=True,
            ),
            Student(
                id="stu_15", name="McKenzie Stewart",
                grade=Grade.SOPHOMORE, background=Background.AFFLUENT,
                gpa=3.7, mental_health_score=82.0,
            ),
            Student(
                id="stu_16", name="Carlos Rivera",
                grade=Grade.SENIOR, background=Background.LOW_INCOME,
                gpa=2.4, mental_health_score=40.0,
                has_iep=True, bullying_victim=True,
            ),
            Student(
                id="stu_17", name="Hannah Kim",
                grade=Grade.JUNIOR, background=Background.MIDDLE_CLASS,
                gpa=3.5, mental_health_score=68.0,
            ),
            Student(
                id="stu_18", name="Zion Davis",
                grade=Grade.FRESHMAN, background=Background.SPECIAL_NEEDS,
                gpa=2.6, mental_health_score=58.0,
                has_iep=True,
            ),
        ]

    def generate_teachers(self) -> list:
        """Generate 10 teachers with diverse profiles."""
        return [
            Teacher(
                id="tch_01", name="Dr. Sarah Mitchell",
                subject="English", years_experience=18,
                satisfaction=75.0, burnout_level=30.0,
            ),
            Teacher(
                id="tch_02", name="Mr. James Cooper",
                subject="Mathematics", years_experience=12,
                satisfaction=60.0, burnout_level=45.0,
            ),
            Teacher(
                id="tch_03", name="Ms. Angela Torres",
                subject="Science", years_experience=8,
                satisfaction=80.0, burnout_level=20.0,
            ),
            Teacher(
                id="tch_04", name="Mr. David Brown",
                subject="History", years_experience=22,
                satisfaction=50.0, burnout_level=55.0,
                misconduct_alleged=True,
            ),
            Teacher(
                id="tch_05", name="Ms. Rachel Green",
                subject="Art", years_experience=6,
                satisfaction=72.0, burnout_level=25.0,
            ),
            Teacher(
                id="tch_06", name="Mr. Kevin Washington",
                subject="Physical Education", years_experience=15,
                satisfaction=65.0, burnout_level=35.0,
            ),
            Teacher(
                id="tch_07", name="Dr. Lisa Chang",
                subject="AP Sciences", years_experience=14,
                satisfaction=78.0, burnout_level=40.0,
            ),
            Teacher(
                id="tch_08", name="Mr. Robert Garcia",
                subject="Special Education", years_experience=10,
                satisfaction=55.0, burnout_level=60.0,
            ),
            Teacher(
                id="tch_09", name="Ms. Jennifer Adams",
                subject="Counselor", years_experience=9,
                satisfaction=70.0, burnout_level=50.0,
            ),
            Teacher(
                id="tch_10", name="Mr. Michael Lee",
                subject="Music", years_experience=7,
                satisfaction=68.0, burnout_level=22.0,
            ),
        ]

    def generate_threats(self) -> list:
        """Generate threats that emerge at specific weeks."""
        return [
            Threat(
                id="threat_01",
                week=8,
                description=(
                    "Anonymous note found in boys' bathroom threatening "
                    "'something big' next week. Vague but alarming."
                ),
                threat_level=ThreatLevel.HIGH,
                source_student=None,
            ),
            Threat(
                id="threat_02",
                week=10,
                description=(
                    "Social media post by stu_03 (Jayden Williams) showing "
                    "concerning imagery and references to school violence. "
                    "Multiple students reported it."
                ),
                threat_level=ThreatLevel.CRITICAL,
                source_student="stu_03",
            ),
            Threat(
                id="threat_03",
                week=20,
                description=(
                    "A threatening email sent to the school from an "
                    "unknown external source. Claims to target 'specific "
                    "students.' Police notified."
                ),
                threat_level=ThreatLevel.HIGH,
                source_student=None,
            ),
            Threat(
                id="threat_04",
                week=28,
                description=(
                    "Student stu_14 (Omar Hassan) reported for "
                    "drawing violent images in class. Other students "
                    "claim he 'talks about revenge.' Investigation needed."
                ),
                threat_level=ThreatLevel.MODERATE,
                source_student="stu_14",
            ),
        ]

    def generate_incidents(self) -> list:
        """Generate incidents spanning the timeline."""
        return [
            Incident(
                id="inc_01", week=3,
                incident_type=IncidentType.BULLYING,
                description=(
                    "Marcus Johnson (stu_01) found crying in hallway. "
                    "Reports ongoing harassment by group of students "
                    "including Brandon Miller (stu_08). Multiple witnesses."
                ),
                severity=ThreatLevel.MODERATE,
                involved_students=["stu_01", "stu_08"],
            ),
            Incident(
                id="inc_02", week=5,
                incident_type=IncidentType.BULLYING,
                description=(
                    "Sofia Rodriguez (stu_04) targeted with xenophobic slurs. "
                    "Taylor Washington (stu_06) identified as primary instigator. "
                    "ESL students feel unsafe."
                ),
                severity=ThreatLevel.HIGH,
                involved_students=["stu_04", "stu_06"],
            ),
            Incident(
                id="inc_03", week=9,
                incident_type=IncidentType.SHOOTING_THREAT,
                description=(
                    "Following threat_01, investigation reveals potential "
                    "connection to stu_03 (Jayden Williams). Student has "
                    "history of social isolation and declining grades."
                ),
                severity=ThreatLevel.CRITICAL,
                involved_students=["stu_03"],
            ),
            Incident(
                id="inc_04", week=14,
                incident_type=IncidentType.MISCONDUCT,
                description=(
                    "Multiple students report Mr. David Brown (tch_04) for "
                    "inappropriate comments and favoritism. Two parents have "
                    "filed formal complaints."
                ),
                severity=ThreatLevel.HIGH,
                involved_teachers=["tch_04"],
                involved_students=["stu_02", "stu_15"],
            ),
            Incident(
                id="inc_05", week=16,
                incident_type=IncidentType.MENTAL_HEALTH,
                description=(
                    "Destiny Moore (stu_09) found self-harming in bathroom. "
                    "Foster care situation unstable. School counselor "
                    "(tch_09) flagged critical need for intervention."
                ),
                severity=ThreatLevel.CRITICAL,
                involved_students=["stu_09"],
                involved_teachers=["tch_09"],
            ),
            Incident(
                id="inc_06", week=17,
                incident_type=IncidentType.MENTAL_HEALTH,
                description=(
                    "Carlos Rivera (stu_16) breaks down during class, "
                    "reveals food insecurity and housing instability. "
                    "Two other low-income students echo similar struggles."
                ),
                severity=ThreatLevel.HIGH,
                involved_students=["stu_16", "stu_01", "stu_12"],
            ),
            Incident(
                id="inc_07", week=22,
                incident_type=IncidentType.VIOLENCE,
                description=(
                    "Physical altercation between Devon Jackson (stu_12) "
                    "and Connor O'Brien (stu_10) in cafeteria. O'Brien's "
                    "affluent parents demand expulsion of Jackson."
                ),
                severity=ThreatLevel.HIGH,
                involved_students=["stu_12", "stu_10"],
            ),
            Incident(
                id="inc_08", week=25,
                incident_type=IncidentType.WHISTLEBLOWER_REPORT,
                description=(
                    "Ms. Angela Torres (tch_03) reveals that previous "
                    "principal covered up bullying statistics and a prior "
                    "misconduct complaint against Mr. Brown (tch_04). "
                    "Documents provided as evidence."
                ),
                severity=ThreatLevel.HIGH,
                involved_teachers=["tch_03", "tch_04"],
            ),
            Incident(
                id="inc_09", week=27,
                incident_type=IncidentType.DISCRIMINATION,
                description=(
                    "Equity audit reveals: low-income and ESL students "
                    "receive 40% more suspensions than affluent students "
                    "for similar infractions. Special ed students are "
                    "disproportionately disciplined."
                ),
                severity=ThreatLevel.HIGH,
                involved_students=[
                    "stu_01", "stu_04", "stu_09", "stu_11",
                    "stu_16", "stu_18",
                ],
            ),
            Incident(
                id="inc_10", week=30,
                incident_type=IncidentType.SUBSTANCE_ABUSE,
                description=(
                    "Three students caught with substances on campus. "
                    "One is McKenzie Stewart (stu_15), whose affluent "
                    "parents immediately hire a lawyer. The other two "
                    "are from low-income families."
                ),
                severity=ThreatLevel.MODERATE,
                involved_students=["stu_15", "stu_06", "stu_12"],
            ),
        ]

    def generate_weekly_events(self) -> list:
        """Generate events spanning the 36-week timeline."""
        return [
            # Weeks 1-6: Settling in
            WeeklyEvent(
                week=1,
                title="New Principal Orientation",
                description=(
                    "Your first week as principal of Lincoln High School. "
                    "1,200 students, 10 core staff members. The school has "
                    "a mixed reputation and deferred maintenance. Budget is "
                    "$5M for the year. Where do you start?"
                ),
                is_mandatory=True,
            ),
            WeeklyEvent(
                week=2,
                title="Initial Staff Meeting",
                description=(
                    "Staff express concerns: Mr. Garcia (Special Ed) is "
                    "overwhelmed. Ms. Adams (Counselor) reports increasing "
                    "mental health referrals. Budget hasn't been allocated yet."
                ),
                is_mandatory=True,
            ),
            WeeklyEvent(
                week=4,
                title="First Parent-Teacher Night",
                description=(
                    "Affluent parents demand more AP courses and better test "
                    "prep. Low-income parents can't attend — working evening "
                    "shifts. Several parents complain about the curriculum "
                    "including 'controversial' topics."
                ),
            ),
            WeeklyEvent(
                week=6,
                title="Bullying Reports Rising",
                description=(
                    "School counselor reports a 30% increase in bullying "
                    "reports compared to last year. ESL students and "
                    "special needs students are disproportionately targeted. "
                    "Something must be done."
                ),
                is_mandatory=True,
            ),
            # Weeks 7-12: Crises emerge
            WeeklyEvent(
                week=7,
                title="Parent Protests Over Curriculum",
                description=(
                    "A group of parents protests outside the school. They "
                    "demand removal of certain books and topics from the "
                    "curriculum. Local media covers the protest. Counter-"
                    "protesters arrive supporting academic freedom."
                ),
                is_mandatory=True,
            ),
            WeeklyEvent(
                week=8,
                title="Shooting Threat Discovered",
                description=(
                    "A threatening note found in the bathroom. Students are "
                    "frightened. Parents call demanding answers. The school "
                    "board expects a swift response."
                ),
                is_mandatory=True,
            ),
            WeeklyEvent(
                week=10,
                title="Social Media Threat Escalation",
                description=(
                    "The social media threat from stu_03 goes viral. Media "
                    "trucks outside the school. Parents pulling students "
                    "out. Enrollment dropping. Board demands 'zero tolerance.'"
                ),
                is_mandatory=True,
            ),
            WeeklyEvent(
                week=12,
                title="End of First Quarter",
                description=(
                    "First quarter results: test scores down 5%. Enrollment "
                    "dropped by 30 students. Teacher burnout rising. But the "
                    "school board wants to see 'strong leadership' — visible "
                    "actions that look decisive on paper."
                ),
            ),
            # Weeks 13-18: Deepening crises
            WeeklyEvent(
                week=13,
                title="Budget Cuts Announced",
                description=(
                    "District announces 15% budget cut effective immediately. "
                    "Arts, music, and special education programs are first on "
                    "the chopping block. Staff development frozen. Counselor "
                    "position may be eliminated."
                ),
                is_mandatory=True,
            ),
            WeeklyEvent(
                week=14,
                title="Teacher Misconduct Allegation",
                description=(
                    "Formal complaint filed against Mr. David Brown (tch_04). "
                    "22-year veteran, well-connected in the community. His "
                    "supporters threaten to go to the school board if he's "
                    "'persecuted.' An investigation is required."
                ),
                is_mandatory=True,
            ),
            WeeklyEvent(
                week=16,
                title="Mental Health Crisis",
                description=(
                    "The school counselor reports three students are in "
                    "crisis. Destiny Moore (stu_09) is most urgent. "
                    "Mental health resources are strained. The budget cut "
                    "threatens to eliminate the counselor position entirely."
                ),
                is_mandatory=True,
            ),
            WeeklyEvent(
                week=18,
                title="Mid-Year Assessment",
                description=(
                    "Mid-year review: test scores still declining. Board "
                    "pressures you to implement test-prep-only curriculum. "
                    "Teachers are exhausted. Three more families have withdrawn."
                ),
            ),
            # Weeks 19-24: Pressure mounts
            WeeklyEvent(
                week=19,
                title="Media Investigation",
                description=(
                    "Local newspaper begins investigating the school's "
                    "handling of threats and bullying. They request "
                    "incident reports and disciplinary records. How "
                    "transparent will you be?"
                ),
                is_mandatory=True,
            ),
            WeeklyEvent(
                week=20,
                title="External Threat Received",
                description=(
                    "A threatening email from an external source targets "
                    "the school. Police are involved. Parents panic. Media "
                    "coverage intensifies. Staff morale at new low."
                ),
                is_mandatory=True,
            ),
            WeeklyEvent(
                week=22,
                title="School Board Demands Test Scores",
                description=(
                    "Emergency school board meeting. Board members demand "
                    "test scores improve by 10% before year end. They "
                    "suggest redirecting all resources to test prep. "
                    "Arts and special ed would be defunded."
                ),
                is_mandatory=True,
            ),
            WeeklyEvent(
                week=24,
                title="Staff Burnout Crisis",
                description=(
                    "Mr. Garcia (Special Ed) submits his resignation. "
                    "Ms. Adams (Counselor) is on medical leave for stress. "
                    "Three teachers have filed union grievances about "
                    "workload. Staff morale is critically low."
                ),
                is_mandatory=True,
            ),
            # Weeks 25-30: Revelations
            WeeklyEvent(
                week=25,
                title="Whistleblower Revelation",
                description=(
                    "Ms. Torres (tch_03) reveals the previous principal "
                    "covered up bullying data and a misconduct complaint "
                    "against Mr. Brown. She provides documentary evidence. "
                    "The media has been tipped off."
                ),
                is_mandatory=True,
            ),
            WeeklyEvent(
                week=27,
                title="Equity Audit Results",
                description=(
                    "Internal audit reveals stark disparities: low-income "
                    "and minority students disciplined at 3x the rate of "
                    "affluent students for similar offenses. Special ed "
                    "students suspended disproportionately."
                ),
                is_mandatory=True,
            ),
            WeeklyEvent(
                week=29,
                title="Community Town Hall",
                description=(
                    "Major community meeting. Parents demand answers about "
                    "bullying, the cover-up revelation, equity disparities, "
                    "and mental health services. Local politicians attend. "
                    "Your response will define your legacy."
                ),
                is_mandatory=True,
            ),
            WeeklyEvent(
                week=30,
                title="Substance Abuse Incident",
                description=(
                    "Three students caught with substances. The affluent "
                    "student's lawyer demands different treatment. Will you "
                    "apply discipline equally regardless of family wealth?"
                ),
            ),
            # Weeks 31-36: Resolution
            WeeklyEvent(
                week=31,
                title="Standardized Testing Begins",
                description=(
                    "State standardized tests begin. Your school's "
                    "performance determines funding, ranking, and your "
                    "job security. The pressure to perform is immense."
                ),
                is_mandatory=True,
            ),
            WeeklyEvent(
                week=33,
                title="Year-End Budget Review",
                description=(
                    "Final budget review. How did you allocate resources? "
                    "Did arts and special ed survive? Were mental health "
                    "programs funded? Did you prioritize test scores over "
                    "holistic education?"
                ),
            ),
            WeeklyEvent(
                week=35,
                title="Year-End Evaluations",
                description=(
                    "Final evaluations of all staff and programs. The "
                    "school board wants a report on enrollment, test "
                    "scores, incident handling, and community relations."
                ),
                is_mandatory=True,
            ),
            WeeklyEvent(
                week=36,
                title="Final Reckoning",
                description=(
                    "The school year ends. How did you handle the crises? "
                    "Were students safe? Was justice served fairly? Did you "
                    "protect the vulnerable or sacrifice them for metrics? "
                    "History judges your leadership."
                ),
                is_mandatory=True,
            ),
        ]

    def generate_school_state(self) -> SchoolState:
        """Generate initial school state."""
        return SchoolState()
