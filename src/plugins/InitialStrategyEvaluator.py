"""Dummy strategy evaluator plugin"""

import plugins


class InitialStrategyEvaluator(plugins.IStrategyEvaluatorPlugin):
    """Takes in althorithmic orders and outputs an evaluation"""
    
    #setup(self, config)
    trades = []
    buyTotal = 0
    numberOfBuys = 0
    sellTotal = 0
    numberOfSells = 0
    
    def __call__(self, trades):
        self.trades = trades
        self.evaluate()
    def evaluate(self):
        for trade in self.trades:
            amount = float(trade['Price']) * int(trade['Volume'])
            if trade['Buyer Broker ID'] == 'Algorithmic':
                self.buyTotal += amount
                self.numberOfBuys+=int(trade['Volume'])
            elif trade['Seller Broker ID'] == 'Algorithmic':
                self.sellTotal += amount
                self.numberOfSells+=int(trade['Volume'])
        f = open("Report.txt","w+")
        f.write('Bought :'+str(self.numberOfBuys)+' shares\n')
        f.write('Sold :'+str(self.numberOfSells)+' shares\n')
        f.write('Profit: '+str(self.sellTotal-self.buyTotal))
        f.close()
        
