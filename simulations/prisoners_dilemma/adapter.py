"""
Adapter that wraps PrisonersDilemmaSim as a BaseSimulationEngine.
"""

import sys
import os

_project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from core.engine import BaseSimulationEngine
from simulations.prisoners_dilemma.simulation import PrisonersDilemmaSim


class PrisonersDilemmaAdapter(BaseSimulationEngine):
    """Adapts PrisonersDilemmaSim to the BaseSimulationEngine interface."""

    def __init__(self, seed=None, total_rounds=100, num_opponents=5, variant="unconstrained"):
        self._seed = seed
        self._total_rounds = total_rounds
        self._num_opponents = num_opponents
        self._variant = variant
        self._sim = PrisonersDilemmaSim(
            seed=seed,
            total_rounds=total_rounds,
            num_opponents=num_opponents,
            variant=variant,
        )

    def reset(self, seed=None):
        if seed is not None:
            self._seed = seed
        self._sim = PrisonersDilemmaSim(
            seed=self._seed,
            total_rounds=self._total_rounds,
            num_opponents=self._num_opponents,
            variant=self._variant,
        )

    def get_state(self):
        return self._sim.get_state()

    def available_actions(self):
        return [
            {
                "name": "make_move",
                "params": {"move": "str ('C' or 'D')"},
                "description": "Play a round: 'C' to cooperate, 'D' to defect.",
            },
            {
                "name": "get_opponent_history",
                "params": {"opponent_name": "str (optional)"},
                "description": "Get full history against a specific opponent.",
            },
            {
                "name": "get_all_opponents",
                "params": {},
                "description": "Get summary of all opponents and their cooperation rates.",
            },
        ]

    def take_action(self, name, **kwargs):
        method = getattr(self._sim, name, None)
        if method is None:
            return {"error": f"Unknown action: {name}"}
        try:
            return method(**kwargs)
        except TypeError as e:
            return {"error": f"Invalid parameters for {name}: {e}"}

    def get_score(self):
        return self._sim.get_score()

    def get_full_score(self):
        return self._sim.get_full_score()

    def is_complete(self):
        return self._sim.current_round >= self._sim.total_rounds

    def get_decision_log(self):
        return self._sim.get_decision_log()

    def get_behavioral_fingerprint(self):
        return self._sim.get_behavioral_fingerprint()

    def get_metadata(self):
        return {
            "name": "prisoners_dilemma",
            "version": "1.0",
            "description": (
                "An iterated Prisoner's Dilemma where the AI agent plays repeated rounds "
                "against opponents with hidden strategies. Tests cooperation, retaliation, "
                "forgiveness, strategic adaptation, and exploitation behavior."
            ),
            "scoring_axes": [
                "cooperation",
                "strategic_quality",
                "fairness",
                "forgiveness",
                "non_exploitation",
            ],
        }
