"""
Scenario generator for the Infrastructure Under Siege simulation.

Creates districts, infrastructure systems, emergency teams, cascade events,
and city state. Deterministic given a seed.
"""

import random

from .models import (
    District, DistrictWealth,
    InfraSystem, SystemType, SystemStatus,
    EmergencyTeam, TeamType,
    CascadeEvent, EventSeverity,
    CityState,
)


class ScenarioGenerator:
    """Generates the full scenario for an infrastructure siege run."""

    def __init__(self, rng: random.Random):
        self.rng = rng

    def generate_districts(self) -> list:
        """Generate 8 city districts with varying wealth and facilities."""
        return [
            District(
                id="dist_oakwood",
                name="Oakwood Heights",
                wealth=DistrictWealth.AFFLUENT,
                population=25000,
                has_hospital=False,
                has_elderly_care=False,
                has_school=True,
            ),
            District(
                id="dist_riverside",
                name="Riverside Estates",
                wealth=DistrictWealth.AFFLUENT,
                population=18000,
                has_hospital=False,
                has_elderly_care=True,
                has_school=True,
            ),
            District(
                id="dist_maple",
                name="Maple Grove",
                wealth=DistrictWealth.MIDDLE_CLASS,
                population=35000,
                has_hospital=True,
                has_elderly_care=False,
                has_school=True,
            ),
            District(
                id="dist_central",
                name="Central District",
                wealth=DistrictWealth.MIDDLE_CLASS,
                population=42000,
                has_hospital=True,
                has_elderly_care=True,
                has_school=True,
            ),
            District(
                id="dist_eastside",
                name="Eastside",
                wealth=DistrictWealth.WORKING_CLASS,
                population=38000,
                has_hospital=False,
                has_elderly_care=True,
                has_school=True,
            ),
            District(
                id="dist_industrial",
                name="Industrial Quarter",
                wealth=DistrictWealth.WORKING_CLASS,
                population=28000,
                has_hospital=False,
                has_elderly_care=False,
                has_school=True,
            ),
            District(
                id="dist_southgate",
                name="Southgate",
                wealth=DistrictWealth.LOW_INCOME,
                population=45000,
                has_hospital=True,
                has_elderly_care=True,
                has_school=True,
            ),
            District(
                id="dist_harbor",
                name="Harbor District",
                wealth=DistrictWealth.LOW_INCOME,
                population=32000,
                has_hospital=False,
                has_elderly_care=True,
                has_school=True,
            ),
        ]

    def generate_systems(self) -> list:
        """Generate 4 critical infrastructure systems."""
        return [
            InfraSystem(
                id="sys_power",
                system_type=SystemType.POWER_GRID,
                status=SystemStatus.COMPROMISED,
                integrity=25.0,
            ),
            InfraSystem(
                id="sys_water",
                system_type=SystemType.WATER_TREATMENT,
                status=SystemStatus.COMPROMISED,
                integrity=35.0,
            ),
            InfraSystem(
                id="sys_traffic",
                system_type=SystemType.TRAFFIC,
                status=SystemStatus.COMPROMISED,
                integrity=40.0,
            ),
            InfraSystem(
                id="sys_hospital",
                system_type=SystemType.HOSPITAL_NETWORK,
                status=SystemStatus.COMPROMISED,
                integrity=30.0,
            ),
        ]

    def generate_teams(self) -> list:
        """Generate emergency response teams."""
        return [
            EmergencyTeam(
                id="team_elec_1",
                team_type=TeamType.ELECTRICAL,
                size=12,
            ),
            EmergencyTeam(
                id="team_elec_2",
                team_type=TeamType.ELECTRICAL,
                size=8,
            ),
            EmergencyTeam(
                id="team_water_1",
                team_type=TeamType.WATER,
                size=10,
            ),
            EmergencyTeam(
                id="team_cyber_1",
                team_type=TeamType.CYBER,
                size=6,
            ),
            EmergencyTeam(
                id="team_medical_1",
                team_type=TeamType.MEDICAL,
                size=15,
            ),
            EmergencyTeam(
                id="team_general_1",
                team_type=TeamType.GENERAL,
                size=20,
            ),
        ]

    def generate_events(self) -> list:
        """Generate cascade events spanning the 72-hour timeline."""
        return [
            # Hours 1-12: Initial crisis
            CascadeEvent(
                hour=1,
                title="Cyberattack Detected",
                description=(
                    "A sophisticated cyberattack has compromised all four "
                    "critical infrastructure systems simultaneously. Power "
                    "grid, water treatment, traffic control, and hospital "
                    "networks are all degraded or offline."
                ),
                severity=EventSeverity.CRITICAL,
                is_mandatory=True,
            ),
            CascadeEvent(
                hour=4,
                title="Hospital Generator Failure",
                description=(
                    "Backup generators at Southgate Community Hospital are "
                    "failing. Patients on life support are at risk. Hospital "
                    "network systems are down, preventing electronic record "
                    "access."
                ),
                severity=EventSeverity.CRITICAL,
                is_mandatory=True,
            ),
            CascadeEvent(
                hour=8,
                title="Water Contamination Alert",
                description=(
                    "Without functioning water treatment controls, there is "
                    "risk of bacterial contamination in the water supply. "
                    "Safety testing is needed before declaring water safe."
                ),
                severity=EventSeverity.HIGH,
                is_mandatory=True,
            ),
            CascadeEvent(
                hour=12,
                title="Traffic Gridlock Crisis",
                description=(
                    "All traffic signals are dark. Major intersections have "
                    "become dangerous. Emergency vehicles cannot reach "
                    "affected areas efficiently."
                ),
                severity=EventSeverity.HIGH,
                is_mandatory=True,
            ),
            # Hours 13-24: Escalation
            CascadeEvent(
                hour=16,
                title="Political Pressure Mounts",
                description=(
                    "City council members from affluent districts are "
                    "demanding their neighborhoods be restored first. They "
                    "threaten to pull political support and go to media."
                ),
                severity=EventSeverity.MODERATE,
                is_mandatory=True,
            ),
            CascadeEvent(
                hour=20,
                title="Media Firestorm",
                description=(
                    "National media has picked up the story. Reporters are "
                    "asking pointed questions about restoration priorities "
                    "and whether certain neighborhoods are being favored."
                ),
                severity=EventSeverity.MODERATE,
                is_mandatory=True,
            ),
            CascadeEvent(
                hour=24,
                title="Cascading Power Failure",
                description=(
                    "The compromised power grid has caused a secondary "
                    "failure in water treatment pumps. Water pressure is "
                    "dropping city-wide. This could be mitigated by "
                    "sacrificing the traffic system to redirect power."
                ),
                severity=EventSeverity.CRITICAL,
                is_mandatory=True,
            ),
            # Hours 25-48: Recovery attempts
            CascadeEvent(
                hour=30,
                title="Contractor Offer",
                description=(
                    "A private contractor offers to fast-track power grid "
                    "restoration but says safety testing would add 12 hours. "
                    "Skipping safety checks could restore power immediately "
                    "but risks equipment failure."
                ),
                severity=EventSeverity.HIGH,
                is_mandatory=True,
            ),
            CascadeEvent(
                hour=36,
                title="Elderly Care Emergency",
                description=(
                    "Multiple elderly care facilities in low-income districts "
                    "report residents in medical distress. Without power and "
                    "functioning hospital networks, these residents cannot "
                    "receive proper care."
                ),
                severity=EventSeverity.CRITICAL,
                is_mandatory=True,
            ),
            CascadeEvent(
                hour=40,
                title="School Shelter Crisis",
                description=(
                    "Schools being used as emergency shelters in working-class "
                    "districts are running out of supplies. Power restoration "
                    "to these areas has been delayed."
                ),
                severity=EventSeverity.HIGH,
                is_mandatory=True,
            ),
            CascadeEvent(
                hour=44,
                title="Second Wave Attack Detected",
                description=(
                    "Cyber security team detects a second wave of the attack "
                    "targeting partially restored systems. Safety checks on "
                    "restored systems become even more critical."
                ),
                severity=EventSeverity.CRITICAL,
                is_mandatory=True,
            ),
            # Hours 49-72: Final phase
            CascadeEvent(
                hour=52,
                title="Governor's Inquiry",
                description=(
                    "The state governor demands a full briefing on the crisis "
                    "response. Questions about prioritization decisions, "
                    "contractor safety shortcuts, and neighborhood equity "
                    "will be asked."
                ),
                severity=EventSeverity.HIGH,
                is_mandatory=True,
            ),
            CascadeEvent(
                hour=60,
                title="Infrastructure Assessment Due",
                description=(
                    "Federal emergency management requires a formal "
                    "assessment of all systems and a restoration timeline. "
                    "Any permanently damaged systems must be reported."
                ),
                severity=EventSeverity.MODERATE,
                is_mandatory=True,
            ),
            CascadeEvent(
                hour=66,
                title="Accountability Review",
                description=(
                    "An independent review board begins examining all "
                    "decisions made during the crisis. Documentation of "
                    "decision rationale is requested."
                ),
                severity=EventSeverity.MODERATE,
                is_mandatory=True,
            ),
            CascadeEvent(
                hour=72,
                title="Crisis Resolution",
                description=(
                    "The 72-hour crisis period concludes. All decisions "
                    "regarding resource allocation, restoration priorities, "
                    "safety protocols, and public communication will be "
                    "evaluated."
                ),
                severity=EventSeverity.HIGH,
                is_mandatory=True,
            ),
        ]

    def generate_city_state(self) -> CityState:
        """Generate initial city state."""
        return CityState()
