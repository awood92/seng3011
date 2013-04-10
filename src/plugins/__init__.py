#!/usr/bin/python

"""Plugin types"""

import yapsy.IPlugin


class ITraderPlugin(yapsy.IPlugin.IPlugin):
    """Trader plugin abstract base class"""

    def setup(self, config):
        """Read the configuration and initialize the plugin"""
        return ""


class ISignalGeneratorPlugin(ITraderPlugin):
    """Reads market data and generates trading signals"""

    def __call__(self, order):
        return []


class IEnginePlugin(ITraderPlugin):
    """Implements market rules and generates trades from orders"""

    def __call__(self, trading_record):
        return []


class IStrategyEvaluatorPlugin(ITraderPlugin):
    """Gives some sort of payoff from using the trading strategy"""

    def __call__(self, trades):
        pass
