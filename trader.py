"""trader module, containing the main logic"""

import sys

def signal_generator(market_data):
    """Reads market data and generates trading signals"""
    raise NotImplementedError

class Engine:
    """Implements the market rules"""

    def __init__(self):
        raise NotImplementedError

    def __call__(self, order):
        raise NotImplementedError

def strategy_evaluator(trades):
    """Gives some sort of payoff from using the trading strategy"""
    raise NotImplementedError

def run_trial(market_data):
    """Run the experiment with the given market data"""
    engine = Engine()
    trades = []
    for order in signal_generator(market_data):
        trades.extend(engine(order))
    strategy_evaluator(trades)

def main():
    """Command line interface, for testing etc"""
    run_trial(sys.stdin)

if __name__ == "__main__":
    main()
