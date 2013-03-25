#!/usr/bin/python

"""Trader command line interface"""

import sys
import optparse
import yapsy.PluginManager
import trader
import plugins


def main():
    """Run the trial, taking market data from stdin"""
    parser = optparse.OptionParser()
    parser.add_option("-g", "--generator", dest="generator",
                      default="Dummy Signal Generator",
                      help="signal generator")
    parser.add_option("-e", "--engine", dest="engine",
                      default="Dummy Engine", help="engine")
    parser.add_option("-s", "--strategyevaluator",
                      dest="strategyevaluator",
                      default="Dummy Strategy Evaluator",
                      help="strategy evaluator")
    (options, args) = parser.parse_args()
    plugin_manager = yapsy.PluginManager.PluginManager()
    plugin_manager.setPluginPlaces(["plugins"])
    plugin_manager.setCategoriesFilter({
        "SignalGenerator": plugins.ISignalGeneratorPlugin,
        "Engine": plugins.IEnginePlugin,
        "StrategyEvaluator": plugins.IStrategyEvaluatorPlugin,
        })
    plugin_manager.collectPlugins()
    plugin_info = plugin_manager.getPluginByName(options.generator,
                                                 "SignalGenerator")
    signal_generator = plugin_info.plugin_object
    signal_generator.setup(plugin_info)
    plugin_info = plugin_manager.getPluginByName(options.engine,
                                                 "Engine")
    engine = plugin_info.plugin_object
    engine.setup(plugin_info)
    plugin_info = plugin_manager.getPluginByName(options.strategyevaluator,
                                                 "StrategyEvaluator")
    strategy_evaluator = plugin_info.plugin_object
    strategy_evaluator.setup(plugin_info)
    trader.run_trial(sys.stdin, signal_generator,
                     engine, strategy_evaluator)

if __name__ == '__main__':
    main()
