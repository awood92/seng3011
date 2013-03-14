"""Trader module, containing the main logic"""

class SignalGenerator:
    def __call__(self, marketData):
        raise NotImplementedError

class Engine:
    def addOrder(self, order):
        raise NotImplementedError

    def addOrders(self, orders):
        trades = []
        for order in orders:
            trades.extend(addOrder(order))
        return trades

class StrategyEvaluator:
    def __call__(self, trades):
        raise NotImplementedError

def runTrial(marketData):
    signalGenerator = SignalGenerator()
    engine = Engine()
    strategyEvaluator = StrategyEvaluator()
    trades = []
    for order in signalGenerator(marketData):
        trades.extend(engine.addOrder(order))
    strategyEvaluator(trades)
