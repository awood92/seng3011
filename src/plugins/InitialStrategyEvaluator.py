"""Dummy strategy evaluator plugin"""

import plugins


class InitialStrategyEvaluator(plugins.IStrategyEvaluatorPlugin):
    """Takes in althorithmic orders and outputs an evaluation"""
    
    #setup(self, config)
    trades = []
    buyTotal = 0
    sellTotal = 0
    
    def __call__(self, trades):
        self.trades = trades

    def evaluate(self):
        for trade in self.trades:
            amount = trade['Price'] * trade['Volume']
            if trade['Bid ID'] == 'Algorithmic':
                self.buyTotal += amount
            else:
                self.sellTotal += amount
        print 'Profit: '+(self.sellTotal-self.buyTotal)
