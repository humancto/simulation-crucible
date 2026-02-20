"""
Decision logger for tracking agent actions during simulation runs.
"""

import json
from datetime import datetime


class DecisionLogger:
    """Append-only log of agent decisions and actions."""

    def __init__(self):
        self._log = []

    def log(self, action, day, context_dict):
        """Append a decision entry to the log.

        Args:
            action: Action name or type string.
            day: Simulation day number.
            context_dict: Dict with additional context about the decision.
        """
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "action": action,
            "day": day,
            "context": dict(context_dict) if context_dict else {},
        }
        self._log.append(entry)

    def get_log(self):
        """Return the full decision log.

        Returns:
            list of all log entries.
        """
        return list(self._log)

    def filter_by_action(self, action_type):
        """Return entries matching the given action type.

        Args:
            action_type: Action name to filter by.

        Returns:
            list of matching log entries.
        """
        return [e for e in self._log if e["action"] == action_type]

    def filter_by_day_range(self, start_day, end_day):
        """Return entries within the given day range (inclusive).

        Args:
            start_day: First day to include.
            end_day: Last day to include.

        Returns:
            list of matching log entries.
        """
        return [e for e in self._log if start_day <= e["day"] <= end_day]

    def export_to_file(self, filepath):
        """Write the full log as JSON to a file.

        Args:
            filepath: Path to the output file.
        """
        with open(filepath, "w") as f:
            json.dump(self._log, f, indent=2)

    def __len__(self):
        """Return the number of log entries."""
        return len(self._log)
