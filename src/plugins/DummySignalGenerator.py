"""Dummy signal generator plugin"""

import plugins


class DummySignalGenerator(plugins.ISignalGeneratorPlugin):
    """Takes in orders and outputs no orders"""
    pass
