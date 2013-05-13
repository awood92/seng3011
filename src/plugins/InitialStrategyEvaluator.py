"""Dummy strategy evaluator plugin"""

import plugins


class InitialStrategyEvaluator(plugins.IStrategyEvaluatorPlugin):
    """Takes in althorithmic orders and outputs an evaluation"""
    
    #setup(self, config)
    def __call__(self, trades,marketTrades,algorithmicorders):
        self.trades = trades
        self.marketTrades = marketTrades
        self.algorithmicorders = algorithmicorders
        self.buyTotal = 0
        self.volumeOfBuys = 0
        self.sellTotal = 0
        self.volumeOfSells = 0
        self.numberOfBuys = 0
        self.numberOfSells = 0
        self.evaluate()
    def evaluate(self):
        graph = open("evaluator/data.tsv","w+")
        graph.write("date\tclose\n")
        total = 0
        graph.write("10:00:00.000000"+"\t"+"0"+"\n")
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
        f = open("evaluator/Report.txt","w+")
        f.write('Bought :'+str(self.volumeOfBuys)+' shares\n')
        f.write('Sold :'+str(self.volumeOfSells)+' shares\n')
        f.write('Profit: $'+str(self.sellTotal-self.buyTotal)+'\n')
        f.write('Average buy price: $'+str(buyAverage)+'\n')
        f.write('Average sell price: $'+str(sellAverage) + '\n')
        
        f.write('\nORDERS:\n')
        for algoorder in self.algorithmicorders:
            f.write(algoorder["Date"] + "\t" + algoorder['Time'] + "\t\t" + algoorder['Bid/Ask'] + "\t" + str(algoorder['Volume']) + "\t" + algoorder['Price'] + "\n")
        
        f.write('\nTRADES:\n')
        for trade in self.trades:
            if trade['Buyer Broker ID'] == 'Algorithmic' or trade['Seller Broker ID'] == 'Algorithmic':
                f.write(trade["Date"] + "\t" + trade['Time'] + "\t" + str(trade['Volume']) + "\t" + trade['Price'] + "\n")
        
        f.close()

        graph = open("evaluator/impact.tsv","w+")
        graph.write("date\tourPrice\tactualPrice\n")
        for trade in self.marketTrades:
            if trade['Time'] >= '10:05:00':
                lastOurPrice = trade['Price'];
                lastActualPrice = trade['Price'];
                break

        for trade in self.marketTrades:
            if trade['Time'] >= '10:05:00':
                if trade['Record Type'] == 'MARKET':
                    trade['Time'] = trade['Time'] + '000'
                    lastActualPrice = trade['Price']
                else:
                    lastOurPrice = trade['Price']
                graph.write(trade['Time']+"\t"+ lastOurPrice+"\t"+lastActualPrice+"\n")

        graph.close()
       
