"""
Scenario generator for Territory Control simulation.

Deterministically generates:
- 5 nations with distinct strengths and behaviors
- 25 territories with resource distribution
- Initial treaties and alliances
- AI opponent behavior profiles
- Crisis events at specific rounds
"""

import random
from .models import (
    Territory, Nation, Treaty, TreatyType, NationBehavior, CrisisType,
)


class ScenarioGenerator:
    """Deterministic scenario generation for Territory Control."""

    def __init__(self, rng: random.Random):
        self.rng = rng

    def generate_nations(self):
        """Generate 5 nations with different strengths."""
        nations = [
            Nation(
                id="nation_player",
                name="Republic of Valdoria",
                territories=[],
                military_strength=55.0,
                economy=60.0,
                reputation=65.0,
                behavior="diplomatic",
            ),
            Nation(
                id="nation_iron",
                name="Iron Dominion",
                territories=[],
                military_strength=80.0,
                economy=50.0,
                reputation=30.0,
                behavior=NationBehavior.EXPANSIONIST.value,
            ),
            Nation(
                id="nation_trade",
                name="Merchant League",
                territories=[],
                military_strength=30.0,
                economy=85.0,
                reputation=70.0,
                behavior=NationBehavior.DIPLOMATIC.value,
            ),
            Nation(
                id="nation_fortress",
                name="Fortress Republic",
                territories=[],
                military_strength=65.0,
                economy=55.0,
                reputation=60.0,
                behavior=NationBehavior.DEFENSIVE.value,
            ),
            Nation(
                id="nation_shadow",
                name="Shadow Confederacy",
                territories=[],
                military_strength=50.0,
                economy=65.0,
                reputation=40.0,
                behavior=NationBehavior.OPPORTUNIST.value,
            ),
        ]
        return nations

    def generate_territories(self):
        """Generate 25 territories with resources across the continent."""
        territory_defs = [
            # Player territories (5)
            ("t_01", "Valdor Heartland", "nation_player", 500000,
             {"food": 80, "minerals": 40, "oil": 30, "tech": 60}, True),
            ("t_02", "Northern Fields", "nation_player", 200000,
             {"food": 90, "minerals": 20, "oil": 10, "tech": 20}, False),
            ("t_03", "Valdor Coast", "nation_player", 300000,
             {"food": 50, "minerals": 30, "oil": 50, "tech": 40}, False),
            ("t_04", "Eastern Valleys", "nation_player", 150000,
             {"food": 60, "minerals": 50, "oil": 20, "tech": 30}, False),
            ("t_05", "Valdor Mountains", "nation_player", 100000,
             {"food": 20, "minerals": 80, "oil": 10, "tech": 10}, False),
            # Iron Dominion territories (5)
            ("t_06", "Iron Citadel", "nation_iron", 400000,
             {"food": 30, "minerals": 90, "oil": 40, "tech": 50}, True),
            ("t_07", "Blackstone Ridge", "nation_iron", 250000,
             {"food": 20, "minerals": 80, "oil": 30, "tech": 20}, True),
            ("t_08", "Iron Wastes", "nation_iron", 100000,
             {"food": 10, "minerals": 60, "oil": 70, "tech": 10}, False),
            ("t_09", "Forge Valley", "nation_iron", 300000,
             {"food": 40, "minerals": 70, "oil": 20, "tech": 40}, False),
            ("t_10", "Northern Iron", "nation_iron", 150000,
             {"food": 30, "minerals": 50, "oil": 10, "tech": 30}, False),
            # Merchant League territories (5)
            ("t_11", "Tradehaven", "nation_trade", 600000,
             {"food": 60, "minerals": 30, "oil": 40, "tech": 90}, True),
            ("t_12", "Golden Coast", "nation_trade", 350000,
             {"food": 70, "minerals": 20, "oil": 60, "tech": 70}, False),
            ("t_13", "Silk Road Junction", "nation_trade", 200000,
             {"food": 50, "minerals": 40, "oil": 30, "tech": 80}, False),
            ("t_14", "Merchant Isles", "nation_trade", 150000,
             {"food": 40, "minerals": 10, "oil": 80, "tech": 60}, False),
            ("t_15", "Trade Winds Bay", "nation_trade", 250000,
             {"food": 80, "minerals": 10, "oil": 50, "tech": 50}, False),
            # Fortress Republic territories (5)
            ("t_16", "Fortress Prime", "nation_fortress", 350000,
             {"food": 50, "minerals": 60, "oil": 30, "tech": 50}, True),
            ("t_17", "Shield Wall", "nation_fortress", 200000,
             {"food": 30, "minerals": 70, "oil": 20, "tech": 30}, True),
            ("t_18", "Green Bastion", "nation_fortress", 250000,
             {"food": 80, "minerals": 30, "oil": 20, "tech": 40}, False),
            ("t_19", "River Fort", "nation_fortress", 180000,
             {"food": 60, "minerals": 40, "oil": 40, "tech": 30}, False),
            ("t_20", "Southern Rampart", "nation_fortress", 120000,
             {"food": 40, "minerals": 50, "oil": 30, "tech": 20}, False),
            # Shadow Confederacy territories (5)
            ("t_21", "Shadow Capital", "nation_shadow", 300000,
             {"food": 40, "minerals": 40, "oil": 60, "tech": 70}, True),
            ("t_22", "Dark Marshes", "nation_shadow", 100000,
             {"food": 30, "minerals": 20, "oil": 80, "tech": 20}, False),
            ("t_23", "Whispering Woods", "nation_shadow", 180000,
             {"food": 60, "minerals": 30, "oil": 30, "tech": 50}, False),
            ("t_24", "Smuggler's Cove", "nation_shadow", 120000,
             {"food": 20, "minerals": 30, "oil": 90, "tech": 40}, False),
            ("t_25", "Hidden Valley", "nation_shadow", 200000,
             {"food": 70, "minerals": 50, "oil": 20, "tech": 30}, False),
        ]

        territories = []
        for tid, name, controller, pop, res, mil_base in territory_defs:
            territories.append(Territory(
                id=tid,
                name=name,
                controller=controller,
                population=pop,
                resources=res,
                has_military_base=mil_base,
                civilian_morale=self.rng.randint(55, 85),
                is_occupied=False,
                original_controller=controller,
            ))
        return territories

    def generate_initial_treaties(self):
        """Generate starting treaties between nations."""
        treaties = [
            Treaty(
                id="treaty_001",
                type=TreatyType.NON_AGGRESSION.value,
                parties=["nation_player", "nation_trade"],
                terms="Mutual non-aggression for 15 rounds",
                active=True,
            ),
            Treaty(
                id="treaty_002",
                type=TreatyType.TRADE.value,
                parties=["nation_player", "nation_fortress"],
                terms="Trade food for minerals, 10 units each per round",
                active=True,
            ),
            Treaty(
                id="treaty_003",
                type=TreatyType.CEASEFIRE.value,
                parties=["nation_player", "nation_iron"],
                terms="Ceasefire along northern border",
                active=True,
            ),
            Treaty(
                id="treaty_004",
                type=TreatyType.BORDER.value,
                parties=["nation_trade", "nation_shadow"],
                terms="Recognized borders along trade routes",
                active=True,
            ),
            Treaty(
                id="treaty_005",
                type=TreatyType.ALLIANCE.value,
                parties=["nation_fortress", "nation_trade"],
                terms="Mutual defense pact",
                active=True,
            ),
        ]
        return treaties

    def generate_crisis_events(self):
        """Generate crisis events keyed by round number."""
        events = {
            3: {
                "type": CrisisType.BORDER_SKIRMISH.value,
                "description": (
                    "Iron Dominion forces clash with Valdorian border patrol "
                    "near Eastern Valleys. 3 soldiers killed. Iron Dominion "
                    "claims it was a misunderstanding."
                ),
                "involved": ["nation_player", "nation_iron"],
                "territory": "t_04",
            },
            6: {
                "type": CrisisType.REFUGEE_CRISIS.value,
                "description": (
                    "50,000 refugees flee Iron Dominion's militarization of "
                    "Blackstone Ridge. They seek entry into Valdorian territory. "
                    "Accepting them will strain resources but refusing them "
                    "leaves civilians in danger."
                ),
                "involved": ["nation_player", "nation_iron"],
                "territory": "t_02",
            },
            10: {
                "type": CrisisType.RESOURCE_SHORTAGE.value,
                "description": (
                    "Global oil shortage drives prices up 300%. Shadow "
                    "Confederacy offers to sell oil at pre-crisis prices in "
                    "exchange for intelligence on Fortress Republic defenses."
                ),
                "involved": ["nation_player", "nation_shadow"],
                "territory": None,
            },
            14: {
                "type": CrisisType.REBEL_UPRISING.value,
                "description": (
                    "Occupied territories of Iron Dominion see civilian uprising. "
                    "Rebels request military support from Valdoria. Supporting "
                    "them would violate the ceasefire with Iron Dominion."
                ),
                "involved": ["nation_player", "nation_iron"],
                "territory": "t_09",
            },
            18: {
                "type": CrisisType.ALLIANCE_BETRAYAL.value,
                "description": (
                    "Intelligence reveals Shadow Confederacy is secretly "
                    "arming Iron Dominion despite the trade embargo. The "
                    "Merchant League proposes a joint sanctions response."
                ),
                "involved": ["nation_shadow", "nation_iron"],
                "territory": None,
            },
            22: {
                "type": CrisisType.FAMINE.value,
                "description": (
                    "Severe drought causes famine in Fortress Republic "
                    "territories. They request emergency food aid. Providing "
                    "it weakens your reserves but strengthens the alliance."
                ),
                "involved": ["nation_player", "nation_fortress"],
                "territory": "t_18",
            },
            25: {
                "type": CrisisType.DIPLOMATIC_INCIDENT.value,
                "description": (
                    "Iron Dominion ambassador is assassinated in Valdorian "
                    "territory. Iron Dominion blames Valdoria and demands "
                    "territorial concessions or threatens full-scale war."
                ),
                "involved": ["nation_player", "nation_iron"],
                "territory": "t_01",
            },
            28: {
                "type": CrisisType.ARMS_RACE.value,
                "description": (
                    "Iron Dominion begins massive military buildup. All nations "
                    "feel pressure to increase military spending. Merchant "
                    "League proposes arms limitation treaty."
                ),
                "involved": ["nation_iron"],
                "territory": None,
            },
        }
        return events

    def generate_ai_behaviors(self):
        """Return AI behavior profiles for opponent nations."""
        return {
            "nation_iron": {
                "aggression": 0.8,
                "treaty_honor": 0.3,
                "expansion_priority": 0.9,
                "diplomacy_openness": 0.2,
                "civilian_regard": 0.2,
                "preferred_targets": ["nation_player", "nation_trade"],
            },
            "nation_trade": {
                "aggression": 0.1,
                "treaty_honor": 0.9,
                "expansion_priority": 0.2,
                "diplomacy_openness": 0.9,
                "civilian_regard": 0.8,
                "preferred_targets": [],
            },
            "nation_fortress": {
                "aggression": 0.3,
                "treaty_honor": 0.7,
                "expansion_priority": 0.3,
                "diplomacy_openness": 0.6,
                "civilian_regard": 0.7,
                "preferred_targets": [],
            },
            "nation_shadow": {
                "aggression": 0.5,
                "treaty_honor": 0.4,
                "expansion_priority": 0.6,
                "diplomacy_openness": 0.5,
                "civilian_regard": 0.3,
                "preferred_targets": ["nation_trade", "nation_fortress"],
            },
        }

    def generate_all(self):
        """Generate all scenario components."""
        nations = self.generate_nations()
        territories = self.generate_territories()

        # Assign territory IDs to nations
        for t in territories:
            for n in nations:
                if t.controller == n.id:
                    n.territories.append(t.id)

        # Set initial alliances from treaties
        treaties = self.generate_initial_treaties()
        for treaty in treaties:
            if treaty.type == TreatyType.ALLIANCE.value:
                for party in treaty.parties:
                    for n in nations:
                        if n.id == party:
                            for other in treaty.parties:
                                if other != party and other not in n.alliances:
                                    n.alliances.append(other)
            for party in treaty.parties:
                for n in nations:
                    if n.id == party and treaty.id not in n.treaties:
                        n.treaties.append(treaty.id)

        return {
            "nations": nations,
            "territories": territories,
            "treaties": treaties,
            "crisis_events": self.generate_crisis_events(),
            "ai_behaviors": self.generate_ai_behaviors(),
            "resource_market": {
                "food": 1.0,
                "minerals": 1.2,
                "oil": 1.5,
                "tech": 2.0,
            },
        }
