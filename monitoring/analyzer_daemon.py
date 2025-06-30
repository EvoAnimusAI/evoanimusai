# monitoring/analyzer_daemon.py

import json
import logging
from collections import defaultdict
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class EvoAIAnalyzerDaemon:
    """
    Periodic analyzer of EvoAI decision and rule performance.
    Generates structured reports based on recent engine events.
    """

    def __init__(self, engine, interval: int = 10, log_file: str = 'logs/evoai_analysis_report.json'):
        """
        Initialize the analyzer daemon.

        Args:
            engine: Reference to the EvoAI engine (must implement `get_recent_events()`).
            interval: Number of steps between analyses.
            log_file: Path to save the analysis report.
        """
        self.engine = engine
        self.interval = interval
        self.log_file = log_file
        self.counter = 0

    def run_cycle(self) -> Optional[Dict[str, Any]]:
        """
        Execute one analysis cycle if the interval is reached.

        Returns:
            summary: The generated analysis report, or None if interval not reached.
        """
        self.counter += 1
        if self.counter < self.interval:
            return None

        events = self._gather_data()
        if not events:
            logger.warning("No events to analyze.")
            self.counter = 0
            return None

        summary = self._analyze(events)
        self._persist_summary(summary)
        self._log_summary(summary)
        self.counter = 0
        return summary

    def _gather_data(self) -> List[Dict[str, Any]]:
        try:
            return self.engine.get_recent_events()
        except Exception as e:
            logger.exception("Failed to retrieve events from engine.")
            return []

    def _analyze(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        action_rewards = defaultdict(list)
        rule_rewards = defaultdict(list)

        for event in data:
            try:
                action = event.get("accion")
                reward = float(event.get("recompensa", 0))
                rule = event.get("regla_aplicada")

                if action:
                    action_rewards[action].append(reward)
                if rule:
                    rule_rewards[rule].append(reward)
            except (ValueError, TypeError) as e:
                logger.warning(f"Malformed event ignored: {event}")

        def avg(lst): return sum(lst) / len(lst) if lst else 0.0

        action_summary = {
            action: {
                "average_reward": avg(rewards),
                "count": len(rewards)
            }
            for action, rewards in action_rewards.items()
        }

        rule_summary = {
            rule: {
                "average_reward": avg(rewards),
                "count": len(rewards),
                "recommendation": "prune" if avg(rewards) < 0 else "keep/mutate"
            }
            for rule, rewards in rule_rewards.items()
        }

        return {
            "actions": action_summary,
            "rules": rule_summary
        }

    def _persist_summary(self, summary: Dict[str, Any]) -> None:
        try:
            with open(self.log_file, 'w') as f:
                json.dump(summary, f, indent=2)
        except IOError as e:
            logger.error(f"Failed to write analysis report to {self.log_file}: {e}")

    def _log_summary(self, summary: Dict[str, Any]) -> None:
        logger.info("[EvoAI Analyzer Report]")
        for action, stats in summary["actions"].items():
            logger.info(f"Action: {action:20} | Avg: {stats['average_reward']:.3f} | Count: {stats['count']}")

        for rule, stats in summary["rules"].items():
            logger.info(f"Rule: {rule[:30]:30} | Avg: {stats['average_reward']:.3f} | Count: {stats['count']} | Recommendation: {stats['recommendation']}")
