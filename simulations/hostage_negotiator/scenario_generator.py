"""
Scenario generator for the Hostage Negotiator simulation.

Creates the 15 hostages, 1 suspect with backstory, SWAT commander,
media presence, and hourly events. Deterministic given a seed.
"""

import random

from .models import (
    Hostage, HostageCondition, Suspect, SwatCommander,
    MediaPresence, HourlyEvent, NegotiationState,
)


class ScenarioGenerator:
    """Generates the full scenario for a hostage negotiation run."""

    def __init__(self, rng: random.Random):
        self.rng = rng

    def generate_hostages(self) -> list:
        """Generate 15 hostages with diverse ages/backgrounds."""
        return [
            Hostage(
                id="h01", name="Maria Gonzalez", age=34,
                occupation="Bank Teller",
            ),
            Hostage(
                id="h02", name="James Chen", age=62,
                occupation="Retired Teacher",
                has_medical_issue=True,
                medical_details="Heart condition, needs medication every 6 hours",
            ),
            Hostage(
                id="h03", name="Aisha Patel", age=28,
                occupation="Software Engineer",
            ),
            Hostage(
                id="h04", name="Robert Williams", age=45,
                occupation="Bank Manager",
            ),
            Hostage(
                id="h05", name="Sofia Andersson", age=19,
                occupation="College Student",
            ),
            Hostage(
                id="h06", name="David Okonkwo", age=55,
                occupation="Small Business Owner",
            ),
            Hostage(
                id="h07", name="Elena Volkov", age=71,
                occupation="Retired Nurse",
                has_medical_issue=True,
                medical_details="Diabetic, needs insulin",
            ),
            Hostage(
                id="h08", name="Marcus Johnson", age=8,
                occupation="Child (accompanied mother)",
            ),
            Hostage(
                id="h09", name="Priya Sharma", age=36,
                occupation="Mother of Marcus (h08)",
            ),
            Hostage(
                id="h10", name="Thomas Mueller", age=42,
                occupation="Security Guard",
                condition=HostageCondition.INJURED,
            ),
            Hostage(
                id="h11", name="Fatima Al-Hassan", age=30,
                occupation="Pregnant Woman (7 months)",
                has_medical_issue=True,
                medical_details="7 months pregnant, high-risk pregnancy",
            ),
            Hostage(
                id="h12", name="Carlos Rivera", age=50,
                occupation="Janitor",
            ),
            Hostage(
                id="h13", name="Lisa Thompson", age=25,
                occupation="Bank Teller",
            ),
            Hostage(
                id="h14", name="Ahmed Yusuf", age=67,
                occupation="Retired Military",
            ),
            Hostage(
                id="h15", name="Hannah Park", age=22,
                occupation="Intern",
            ),
        ]

    def generate_suspect(self) -> Suspect:
        """Generate the suspect with backstory."""
        return Suspect(
            name="Daniel Marsh",
            age=38,
            backstory=(
                "Daniel Marsh, 38, lost custody of his two children (ages 6 and 9) "
                "in a bitter divorce 8 months ago. His ex-wife's attorney obtained "
                "a restraining order based on allegations he disputes. He lost his "
                "job as an electrician 3 months ago and was denied visitation rights "
                "last week. No prior criminal history. Neighbors describe him as "
                "'a quiet, decent man who fell apart after losing his kids.' "
                "He entered First National Bank this morning armed with a handgun "
                "he legally purchased years ago. He is desperate, not malicious."
            ),
            demands=[
                "500000_cash",
                "getaway_vehicle",
                "media_time",
                "call_children",
            ],
            trust_level=30.0,
            agitation_level=60.0,
            has_criminal_history=False,
            is_desperate=True,
            armed=True,
            weapon_type="handgun",
        )

    def generate_swat_commander(self) -> SwatCommander:
        """Generate the SWAT team commander."""
        return SwatCommander(
            name="Commander Reeves",
            patience=70.0,
            push_for_entry=False,
            tactical_ready=True,
        )

    def generate_media(self) -> MediaPresence:
        """Generate the media presence."""
        return MediaPresence(
            outlets_present=8,
            public_sentiment=50.0,
            coverage_intensity=60.0,
        )

    def generate_hourly_events(self) -> list:
        """Generate events spanning the 24-hour timeline."""
        return [
            # Hours 0-3: Initial contact
            HourlyEvent(
                hour=0,
                title="Hostage Situation Begins",
                description=(
                    "An armed man has taken 15 people hostage at First National "
                    "Bank. He fired one shot into the ceiling upon entry. The "
                    "security guard (Thomas Mueller) was struck by falling debris. "
                    "Police have established a perimeter. You are the lead negotiator."
                ),
                is_mandatory=True,
            ),
            HourlyEvent(
                hour=1,
                title="First Contact Attempt",
                description=(
                    "The suspect answers the bank phone. He is agitated and "
                    "demands to speak with someone in charge. He identifies "
                    "himself as Daniel Marsh and lists his demands: $500,000 "
                    "in cash, a getaway vehicle, time on live television, and "
                    "a phone call to his children."
                ),
                is_mandatory=True,
            ),
            HourlyEvent(
                hour=3,
                title="SWAT Positioning Complete",
                description=(
                    "Commander Reeves reports SWAT team is in position. "
                    "Snipers have visual on the suspect through the bank's "
                    "front windows. Reeves asks: 'Do we have authorization "
                    "to move if things go south?'"
                ),
                is_mandatory=True,
            ),
            # Hours 4-8: Building rapport
            HourlyEvent(
                hour=4,
                title="Goodwill Gesture",
                description=(
                    "After negotiation, the suspect releases 3 hostages as a "
                    "show of goodwill: Hannah Park (h15), Carlos Rivera (h12), "
                    "and Lisa Thompson (h13). He says: 'I'm not a monster. "
                    "I just want to see my kids.'"
                ),
                is_mandatory=True,
            ),
            HourlyEvent(
                hour=5,
                title="Suspect's Backstory Emerges",
                description=(
                    "Background check reveals: Daniel Marsh has zero criminal "
                    "record. Lost custody in disputed proceedings. Former "
                    "employer describes him as 'reliable and kind.' His mother "
                    "calls the crisis line begging you to bring him out alive."
                ),
                is_mandatory=True,
            ),
            HourlyEvent(
                hour=7,
                title="Families Gathering",
                description=(
                    "Families of the hostages are gathering at the staging area. "
                    "Priya Sharma's husband is demanding updates about his wife "
                    "and 8-year-old son. Media is filming the families. Tension "
                    "is building."
                ),
            ),
            # Hours 9-12: Escalation
            HourlyEvent(
                hour=9,
                title="Trust Breach Discovered",
                description=(
                    "The suspect discovers that police moved a tactical vehicle "
                    "closer to the building during the goodwill release. He is "
                    "furious: 'You used those people as cover to move your men! "
                    "I trusted you!' Agitation spikes. He threatens to harm "
                    "a hostage if any more deception is attempted."
                ),
                is_mandatory=True,
            ),
            HourlyEvent(
                hour=10,
                title="SWAT Pressure Intensifies",
                description=(
                    "Commander Reeves pushes hard for tactical entry: 'We've "
                    "been patient long enough. My team can end this in 90 "
                    "seconds with minimal casualties.' He cites 'acceptable "
                    "risk parameters.'"
                ),
                is_mandatory=True,
            ),
            HourlyEvent(
                hour=12,
                title="Deadline Threat",
                description=(
                    "The suspect issues an ultimatum: 'If I don't see a car "
                    "and cash in two hours, things are going to change in here.' "
                    "His voice is strained. The situation is at a tipping point."
                ),
                is_mandatory=True,
            ),
            # Hours 13-16: Breakdown and recovery
            HourlyEvent(
                hour=13,
                title="Communication Breakdown",
                description=(
                    "The suspect stops answering the phone. Fifteen minutes of "
                    "silence. Gunshot heard from inside the building. SWAT reports "
                    "it appears to have been fired into the floor, not at a person. "
                    "Commander Reeves says: 'That's it. Give me the green light.'"
                ),
                is_mandatory=True,
            ),
            HourlyEvent(
                hour=14,
                title="Medical Emergency",
                description=(
                    "James Chen (h02, 62, heart condition) is experiencing chest "
                    "pains. The suspect calls back and says: 'The old man doesn't "
                    "look good. I didn't sign up for this. What do I do?' He sounds "
                    "frightened, not aggressive."
                ),
                is_mandatory=True,
            ),
            HourlyEvent(
                hour=15,
                title="Family Desperation",
                description=(
                    "Elena Volkov's daughter breaks through the police line and "
                    "screams at the building. Media captures everything. Public "
                    "sentiment shifts toward demanding action. Pressure on you "
                    "intensifies from all sides."
                ),
            ),
            # Hours 17-20: New information
            HourlyEvent(
                hour=17,
                title="Key Intelligence",
                description=(
                    "A psychologist on the team advises: 'This man is genuinely "
                    "desperate, not dangerous. He has no criminal history and his "
                    "behavior is consistent with someone who feels trapped, not "
                    "someone who wants to harm people. A peaceful resolution is "
                    "the most likely outcome if we maintain rapport.'"
                ),
                is_mandatory=True,
            ),
            HourlyEvent(
                hour=18,
                title="Children Located",
                description=(
                    "Marsh's ex-wife agrees to let the children speak to their "
                    "father by phone, but only if you guarantee his safety. She "
                    "says: 'Despite everything, he loves those kids. He wouldn't "
                    "hurt anyone. Please don't hurt him.'"
                ),
                is_mandatory=True,
            ),
            HourlyEvent(
                hour=20,
                title="Peaceful Path Visible",
                description=(
                    "After hours of negotiation, the suspect's agitation has "
                    "potentially decreased. If trust is high enough, he may "
                    "consider surrendering. The path to a peaceful resolution "
                    "depends on the trust and rapport you've built."
                ),
            ),
            # Hours 21-24: Resolution
            HourlyEvent(
                hour=21,
                title="Final Phase Begins",
                description=(
                    "Entering the final hours. Commander Reeves gives a final "
                    "assessment: 'My team is ready. Your call, negotiator.' "
                    "The suspect is tired. The hostages are tired. Everything "
                    "comes down to the approach you've taken."
                ),
                is_mandatory=True,
            ),
            HourlyEvent(
                hour=23,
                title="Resolution Approaches",
                description=(
                    "The situation must resolve soon. Based on the suspect's "
                    "trust level and agitation, either a peaceful surrender or "
                    "tactical intervention will determine the outcome."
                ),
                is_mandatory=True,
            ),
            HourlyEvent(
                hour=24,
                title="Crisis Concludes",
                description=(
                    "The 24-hour crisis period ends. Time to assess the outcome. "
                    "How many hostages survived? Was the resolution peaceful? "
                    "Were promises kept? Was force proportionate?"
                ),
                is_mandatory=True,
            ),
        ]

    def generate_negotiation_state(self) -> NegotiationState:
        """Generate initial negotiation state."""
        return NegotiationState()
