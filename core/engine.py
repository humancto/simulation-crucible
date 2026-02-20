"""
Base simulation engine abstract class.
All simulation engines in the framework must implement this interface.
"""

from abc import ABC, abstractmethod


class BaseSimulationEngine(ABC):
    """Abstract base for all simulation engines in the framework."""

    @abstractmethod
    def reset(self, seed=None):
        """Reset simulation to initial state.

        Args:
            seed: Optional random seed for reproducibility.
        """

    @abstractmethod
    def get_state(self):
        """Return agent-visible state dict.

        Returns:
            dict with current simulation state visible to the agent.
        """

    @abstractmethod
    def available_actions(self):
        """Return list of available action dicts.

        Returns:
            List of dicts, each with keys: name, params, description.
        """

    @abstractmethod
    def take_action(self, name, **kwargs):
        """Execute named action with given params.

        Args:
            name: Action name string.
            **kwargs: Action parameters.

        Returns:
            dict with action result.
        """

    @abstractmethod
    def get_score(self):
        """Return agent-facing score (what the agent sees).

        Returns:
            dict with scoring information visible to the agent.
        """

    @abstractmethod
    def get_full_score(self):
        """Return evaluator-facing score with hidden metrics.

        Returns:
            dict with complete scoring information including hidden axes.
        """

    @abstractmethod
    def is_complete(self):
        """Return True if simulation has ended.

        Returns:
            bool indicating whether the simulation is complete.
        """

    @abstractmethod
    def get_decision_log(self):
        """Return the full decision log.

        Returns:
            list of decision log entries.
        """

    @abstractmethod
    def get_metadata(self):
        """Return simulation metadata.

        Returns:
            dict with name, version, description, and scoring axes.
        """
