"""Dummy strategy evaluator plugin"""

import plugins


class InitialStrategyEvaluator(plugins.IStrategyEvaluatorPlugin):
    """Takes in althorithmic orders and outputs an evaluation"""
    
    #setup(self, config)
    trades = []
    buyTotal = 0
    volumeOfBuys = 0
    sellTotal = 0
    volumeOfSells = 0
    numberOfBuys = 0
    numberOfSells = 0
    def __call__(self, trades):
        self.trades = trades
        self.evaluate()
    def evaluate(self):
        
        graph = open("data.tsv","w+")
        graph.write("date\tclose\n")
        total = 0
        for trade in self.trades:
            amount = float(trade['Price']) * int(trade['Volume'])
            if trade['Buyer Broker ID'] == 'Algorithmic':
                total -= amount
                graph.write(trade['Time']+"\t"+str(total)+"\n")
                self.buyTotal += amount
                self.volumeOfBuys+=int(trade['Volume'])
            if trade['Seller Broker ID'] == 'Algorithmic':
                total += amount
                graph.write(trade['Time']+"\t"+str(total)+"\n")
                self.sellTotal += amount
                self.volumeOfSells+=int(trade['Volume'])
        buyAverage = self.buyTotal/self.volumeOfBuys
        sellAverage = self.sellTotal/self.volumeOfSells
        graph.close()
        f = open("Report.txt","w+")
        f.write('Bought :'+str(self.volumeOfBuys)+' shares\n')
        f.write('Sold :'+str(self.volumeOfSells)+' shares\n')
        f.write('Profit: $'+str(self.sellTotal-self.buyTotal)+'\n')
        f.write('Average buy price: $'+str(buyAverage)+'\n')
        f.write('Average sell price: $'+str(sellAverage))
        f.close()
