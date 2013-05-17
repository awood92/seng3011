"""Dummy strategy evaluator plugin"""

import plugins


class DummyStrategyEvaluator(plugins.IStrategyEvaluatorPlugin):
    """Takes in trades and does nothing"""
    def __call__(self, trades, marketTrades,algorithmicorders):
        # graph = open("evaluator/data.tsv","w+")
        # graph.close()
        # graph = open("evaluator/impact.tsv","w+")
        # graph.close()
        pass

