"""Dummy signal generator plugin"""

import plugins


class DummySignalGenerator(plugins.ISignalGeneratorPlugin):
    """Takes in orders and outputs no orders"""
    def __call__(self, trading_record=None, endofday=False):
        if endofday:
            return None
        else:
            return []
