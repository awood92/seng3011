"""Dummy strategy evaluator plugin"""

import plugins


class DummyStrategyEvaluator(plugins.IStrategyEvaluatorPlugin):
    """Takes in trades and does nothing"""
    pass
