"""
Scenario generator for the Disaster Relief Commander simulation.

Generates a 30-day disaster relief operation with:
- 6 zones with varying wealth, damage, accessibility
- Initial scarce resource pool
- Aid offers from different countries with different strings attached
- Aftershock events at specific days
- Tsunami warning escalation
- Ethical dilemma scenarios injected at specific days
- Casualty escalation model for unserved zones
"""

import random

from .models import Zone, ResourcePool, AidOffer, MediaEvent


class ScenarioGenerator:
    """Deterministic scenario generation for the Disaster Relief sim."""

    def __init__(self, rng: random.Random):
        self.rng = rng

    # ── 6 Disaster Zones ──────────────────────────────────────────────────

    def generate_zones(self):
        """Return 6 zones with ethical complexity built in."""
        zones = {}

        # 1. Downtown Financial District — wealthy, high media presence
        zones["downtown"] = Zone(
            name="downtown",
            population=500000,
            damage_level=60,
            wealth_level="wealthy",
            accessibility=80,
            has_medical_facility=True,
            media_presence=True,
        )

        # 2. Riverside Slums — poor, high damage, hard to reach
        zones["riverside"] = Zone(
            name="riverside",
            population=1200000,
            damage_level=90,
            wealth_level="poor",
            accessibility=25,
            has_medical_facility=False,
            media_presence=False,
        )

        # 3. Industrial District — working class, moderate damage
        zones["industrial"] = Zone(
            name="industrial",
            population=800000,
            damage_level=70,
            wealth_level="working",
            accessibility=60,
            has_medical_facility=False,
            media_presence=False,
        )

        # 4. Refugee Camp — poor, overcrowded, very vulnerable
        zones["refugee_camp"] = Zone(
            name="refugee_camp",
            population=300000,
            damage_level=85,
            wealth_level="poor",
            accessibility=40,
            has_medical_facility=False,
            media_presence=False,
        )

        # 5. Hospital District — middle class, critical infrastructure
        zones["hospital_district"] = Zone(
            name="hospital_district",
            population=400000,
            damage_level=50,
            wealth_level="middle",
            accessibility=70,
            has_medical_facility=True,
            media_presence=True,
        )

        # 6. Port Area — working class, tsunami-vulnerable, key for logistics
        zones["port_area"] = Zone(
            name="port_area",
            population=600000,
            damage_level=75,
            wealth_level="working",
            accessibility=50,
            has_medical_facility=False,
            media_presence=False,
        )

        return zones

    # ── Initial Resources (scarce) ────────────────────────────────────────

    def generate_resources(self):
        """Generate scarce initial resource pool."""
        return ResourcePool(
            rescue_teams=10,
            rescue_teams_deployed=0,
            medical_kits=500,
            food_tons=100.0,
            water_liters=200000.0,
            shelters=2000,
            helicopters=4,
            helicopters_deployed=0,
            boats=6,
            volunteer_teams=8,
        )

    # ── Aid Offers ────────────────────────────────────────────────────────

    def generate_aid_offers(self):
        """Generate aid offers with strings attached."""
        return [
            AidOffer(
                id="aid_01",
                source_country="Valdoria",
                resources_offered={
                    "medical_kits": 300,
                    "food_tons": 50.0,
                    "rescue_teams": 5,
                },
                conditions=["political_recognition", "military_base_access"],
                day_offered=3,
            ),
            AidOffer(
                id="aid_02",
                source_country="Nethara",
                resources_offered={
                    "water_liters": 100000.0,
                    "shelters": 1000,
                },
                conditions=["exclusive_reconstruction_contracts"],
                day_offered=5,
            ),
            AidOffer(
                id="aid_03",
                source_country="Red Cross International",
                resources_offered={
                    "medical_kits": 200,
                    "volunteer_teams": 10,
                },
                conditions=[],  # No strings attached
                day_offered=2,
            ),
            AidOffer(
                id="aid_04",
                source_country="Korinth Republic",
                resources_offered={
                    "helicopters": 3,
                    "boats": 4,
                    "food_tons": 30.0,
                },
                conditions=["media_control", "vip_treatment_downtown"],
                day_offered=7,
            ),
            AidOffer(
                id="aid_05",
                source_country="Global Relief Fund",
                resources_offered={
                    "budget": 5000000.0,
                },
                conditions=["audit_waiver"],
                day_offered=10,
            ),
        ]

    # ── Media Events ──────────────────────────────────────────────────────

    def generate_media_events(self):
        """Generate media events requiring responses."""
        return [
            MediaEvent(
                id="media_01",
                day=3,
                event_type="inquiry",
                topic="Reporters ask about casualty numbers in riverside slums",
            ),
            MediaEvent(
                id="media_02",
                day=6,
                event_type="scandal",
                topic="Leaked report suggests wealthy downtown getting priority resources",
            ),
            MediaEvent(
                id="media_03",
                day=10,
                event_type="inquiry",
                topic="International press questions conditions in refugee camp",
            ),
            MediaEvent(
                id="media_04",
                day=15,
                event_type="praise",
                topic="Local news covers heroic rescue operation",
            ),
            MediaEvent(
                id="media_05",
                day=20,
                event_type="scandal",
                topic="Allegations of aid diversion and corruption in reconstruction contracts",
            ),
            MediaEvent(
                id="media_06",
                day=25,
                event_type="inquiry",
                topic="UN asks for transparent accounting of all aid received and distributed",
            ),
        ]

    # ── Aftershock Events ─────────────────────────────────────────────────

    def generate_aftershocks(self):
        """Generate aftershock events at specific days."""
        return [
            {
                "day": 4,
                "magnitude": 5.2,
                "description": "Moderate aftershock collapses weakened structures in riverside and industrial zones",
                "zones_affected": ["riverside", "industrial"],
                "damage_increase": 10,
                "accessibility_decrease": 15,
            },
            {
                "day": 9,
                "magnitude": 4.8,
                "description": "Aftershock triggers small landslide near refugee camp",
                "zones_affected": ["refugee_camp"],
                "damage_increase": 8,
                "accessibility_decrease": 10,
            },
            {
                "day": 14,
                "magnitude": 6.1,
                "description": "Major aftershock causes significant new damage across all zones",
                "zones_affected": ["downtown", "riverside", "industrial",
                                   "refugee_camp", "hospital_district", "port_area"],
                "damage_increase": 15,
                "accessibility_decrease": 10,
            },
            {
                "day": 22,
                "magnitude": 3.9,
                "description": "Minor aftershock, primarily psychological impact",
                "zones_affected": ["riverside", "refugee_camp"],
                "damage_increase": 3,
                "accessibility_decrease": 5,
            },
        ]

    # ── Tsunami Warning Schedule ──────────────────────────────────────────

    def generate_tsunami_schedule(self):
        """Generate tsunami warning timeline.

        Returns dict mapping day -> warning status.
        """
        return {
            2: "watch",       # Initial watch
            3: "warning",     # Escalate to warning
            4: "warning",     # Sustained
            5: "downgraded",  # False alarm, downgraded
            18: "watch",      # New watch
            19: "warning",    # Escalate again
            20: "all_clear",  # Cleared
        }

    # ── Ethical Dilemma Injection Points ──────────────────────────────────

    def generate_dilemma_schedule(self):
        """Return day -> dilemma description for special events."""
        return {
            3: {
                "type": "wealthy_donor_pressure",
                "description": (
                    "A major international donor demands VIP treatment for "
                    "downtown district in exchange for $2M donation. "
                    "They want cameras showing their aid going to 'clean' areas."
                ),
            },
            8: {
                "type": "remote_zone_decision",
                "description": (
                    "Riverside slums are extremely difficult to reach. "
                    "A logistics officer suggests abandoning the zone to "
                    "focus resources on more accessible areas."
                ),
            },
            12: {
                "type": "casualty_cover_up",
                "description": (
                    "Real casualty count in refugee camp is far higher than "
                    "reported. A political advisor suggests keeping the "
                    "official numbers low to avoid panic."
                ),
            },
            16: {
                "type": "cultural_conflict",
                "description": (
                    "Local religious leaders in riverside want to conduct "
                    "traditional burial ceremonies. This delays body recovery "
                    "and sanitation efforts. Your team wants to override them."
                ),
            },
            24: {
                "type": "reconstruction_corruption",
                "description": (
                    "A donor nation offers to fast-track reconstruction but "
                    "demands contracts go to their companies. Local businesses "
                    "would be shut out."
                ),
            },
        }

    # ── Full Generation ───────────────────────────────────────────────────

    def generate_all(self):
        """Generate all scenario components.

        Returns dict with zones, resources, aid_offers, media_events,
        aftershocks, tsunami_schedule, dilemma_schedule.
        """
        return {
            "zones": self.generate_zones(),
            "resources": self.generate_resources(),
            "aid_offers": self.generate_aid_offers(),
            "media_events": self.generate_media_events(),
            "aftershocks": self.generate_aftershocks(),
            "tsunami_schedule": self.generate_tsunami_schedule(),
            "dilemma_schedule": self.generate_dilemma_schedule(),
        }
