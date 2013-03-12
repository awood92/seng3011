"""Trader module, containing the main logic"""

def runTrial(strategy, testDataCsv):
    """Run the strategy against the test data and report the results"""
    class Engine:
        """Trader Engine"""
        def addOrder(self, order):
            """Process a single order and return a list of resultant trades"""
            raise NotImplementedError

        def addOrders(self, orders):
            """Process multiple orders and return a list of resultant trades"""
            trades = []
            for order in orders:
                trades.extend(addOrder(order))
            return trades

    def signalGenerator(testDataCsv):
        """Process the file and return a list of orders"""
        raise NotImplementedError

    def strategyEvaluator(orders, trades):
        """Analyze the orders and trades and output the evaluation of the strategy"""
        raise NotImplementedError

    engine = Engine()
    orders = signalGenerator(testDataCsv)
    trades = []
    for order in orders:
        trades.extend(engine.addOrder(order))
        trades.extend(engine.addOrders(strategy(order)))
    strategyEvaluator(orders, trades)
