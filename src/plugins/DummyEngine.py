"""Dummy engine plugin"""

import plugins


class DummyEngine(plugins.IEnginePlugin):
    """Takes in orders and outputs no trades"""
    pass
