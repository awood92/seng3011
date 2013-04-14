"""Initial signal generator plugin"""

import plugins


class InitialSignalGenerator(plugins.ISignalGeneratorPlugin):
    """Takes in orders and outputs algorithmic orders"""
    #setup(self, config)
    def __call__(self, trades):
    	trades = []
        if trading_record['Record Type'] == 'TRADE':
            trades.append(trading_record)
        trades.append(trading_record)
        return trades

