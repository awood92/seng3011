#!/usr/bin/python

"""trader module, containing the main logic"""


def run_trial(market_data, signal_generator,
              engine, strategy_evaluator):
    """Run the experiment with the given market data"""
    trades = []
    for trading_record in market_data:
        trades.extend(engine(trading_record))
        if trading_record['Record Type'] != 'TRADE':
            for algorithmic_order in signal_generator(trading_record):
                trades.extend(engine(algorithmic_order))
    strategy_evaluator(trades)
    return trades

if __name__ == '__main__':
    import doctest
    doctest.testmod()
