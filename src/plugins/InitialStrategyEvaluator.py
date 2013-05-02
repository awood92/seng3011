"""Dummy strategy evaluator plugin"""

import plugins


class InitialStrategyEvaluator(plugins.IStrategyEvaluatorPlugin):
    """Takes in althorithmic orders and outputs an evaluation"""
    
    #setup(self, config)
    def __call__(self, trades):
        self.trades = trades
        self.buyTotal = 0
        self.volumeOfBuys = 0
        self.sellTotal = 0
        self.volumeOfSells = 0
        self.numberOfBuys = 0
        self.numberOfSells = 0
        self.evaluate()
    def evaluate(self):
        graph = open("data.tsv","w+")
        graph.write("date\tclose\n")
        total = 0
        for trade in self.trades:
            amount = float(trade['Price']) * int(trade['Volume'])
            if trade['Buyer Broker ID'] == 'Algorithmic':
                total -= amount
                self.buyTotal += amount
                self.volumeOfBuys += int(trade['Volume'])
                
            if trade['Seller Broker ID'] == 'Algorithmic':
                total += amount                
                self.sellTotal += amount
                self.volumeOfSells += int(trade['Volume'])
            if trade['Seller Broker ID'] == 'Algorithmic' or trade['Buyer Broker ID'] == 'Algorithmic':
                graph.write(trade['Time']+"\t"+str(total)+"\n")
        buyAverage = 0
        sellAverage = 0
        if self.volumeOfBuys > 0:
            buyAverage = self.buyTotal/self.volumeOfBuys
        if self.volumeOfSells > 0:
            sellAverage = self.sellTotal/self.volumeOfSells
        
        graph.close()
        f = open("Report.txt","w+")
        f.write('Bought :'+str(self.volumeOfBuys)+' shares\n')
        f.write('Sold :'+str(self.volumeOfSells)+' shares\n')
        f.write('Profit: $'+str(self.sellTotal-self.buyTotal)+'\n')
        f.write('Average buy price: $'+str(buyAverage)+'\n')
        f.write('Average sell price: $'+str(sellAverage))
        f.close()
