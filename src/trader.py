#!/usr/bin/python

"""trader module, containing the main logic"""

class SignalGenerator:
    """Reads market data and generates trading signals"""

    def __init__(self):
        raise NotImplementedError

    def __call__(self, order):
        raise NotImplementedError

class Engine:
    """Implements the market rules and generates trades from orders"""

    def __init__(self):
        raise NotImplementedError

    def __call__(self, order):
        raise NotImplementedError

def strategy_evaluator(trades):
    """Gives some sort of payoff from using the trading strategy"""
    raise NotImplementedError

def market_simulator(market_data):
    """Parses a market csv file into orders"""
    raise NotImplementedError

def run_trial(market_data):
    """Run the experiment with the given market data"""
    signal_generator = SignalGenerator()
    engine = Engine()
    trades = []
    for order in market_simulator(market_data):
        trades.extend(engine(order))
        for algorithmic_order in signal_generator(order):
            trades.extend(engine(algorithmic_order))
    strategy_evaluator(trades)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
