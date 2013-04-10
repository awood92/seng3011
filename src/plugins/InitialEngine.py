"""Initial engine plugin"""

import plugins


class InitialEngine(plugins.IEnginePlugin):
    """All input trades are sent to the output"""

    def __call__(self, trading_record):
        trades = []
        if trading_record['Record Type'] == 'TRADE':
            trades.append(trading_record)
        return trades
