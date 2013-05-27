"""Dummy strategy evaluator plugin"""

import plugins


class InitialStrategyEvaluator(plugins.IStrategyEvaluatorPlugin):
    """Takes in althorithmic orders and outputs an evaluation"""
    
    #setup(self, config)
    def __call__(self, trades,marketTrades,algorithmicorders,orders,tradesbeforeorder):
        self.trades = trades
        self.marketTrades = marketTrades
        self.algorithmicorders = algorithmicorders
        self.orders = orders
        self.buyTotal = 0
        self.volumeOfBuys = 0
        self.sellTotal = 0
        self.volumeOfSells = 0
        self.numberOfBuys = 0
        self.numberOfSells = 0
        self.tradesbeforeorder = tradesbeforeorder
        self.evaluate()
        
    def evaluate(self):
        self.generateStrategyPerformanceSummaryJson()
    
        graph = open("evaluator/data.tsv","w+")
        graph.write("date\tclose\n")
        total = 0
        graph.write("10:00:00.000000"+"\t"+"0"+"\n")
        first = 1

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
                if first != 1:
                    graph.write(prevTime+"\t"+str(total)+"\n")
                first = 0
                graph.write(trade['Time']+"\t"+str(total)+"\n")
                prevTime = trade['Time']

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
            f.write(str(algoorder["Date"]) + "\t" + str(algoorder['Time']) + "\t\t" + str(algoorder['Bid/Ask']) + "\t" + str(algoorder['Volume']) + "\t" + str(algoorder['Price']) + "\n")
        
        f.write('\nTRADES:\n')
        for trade in self.trades:
            if trade['Buyer Broker ID'] == 'Algorithmic' or trade['Seller Broker ID'] == 'Algorithmic':
                f.write(str(trade["Date"]) + "\t" + str(trade['Time']) + "\t" + str(trade['Volume']) + "\t" + str(trade['Price']) + "\n")
        
        f.close()

        # impact.tsv
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

        # filter.tsv
        graph = open("evaluator/filter.tsv","w+")

        graph.write("date,delay,distance,origin,destination,bbid,sbid\n")

        for trade in self.trades:
            date = str(trade['Date']) + ":"
            time = str(trade['Time'])
            if (len(time) == 15):
                time = time[:-3]
            if (len(date) == 9):
                date = date[:4] + "-" + date[4:]
                date = date[:7] + "-" + date[7:]
            datetime = date + time;

            graph.write(str(datetime) + "," + str(trade['Price']) + "," + str(trade['Volume']) + "," + str(trade['Value']) + "," + str(trade['Instrument']) + "," + str(trade['Buyer Broker ID']) + "," +str(trade['Seller Broker ID']) + "\n")

        graph.close()

        # filtermarket.tsv
        graph = open("evaluator/filtermarket.tsv","w+")

        graph.write("date,delay,distance,origin,destination,bbid,sbid,type\n")

        for trade in self.marketTrades:
            date = str(trade['Date']) + ":"
            time = str(trade['Time'])
            if (len(time) == 15):
                time = time[:-3]
            if (len(date) == 9):
                date = date[:4] + "-" + date[4:]
                date = date[:7] + "-" + date[7:]
            datetime = date + time;

            graph.write(str(datetime) + "," + str(trade['Price']) + "," + str(trade['Volume']) + "," + str(trade['Value']) + "," + str(trade['Instrument']) + "," + str(trade['Buyer Broker ID']) + "," +str(trade['Seller Broker ID']) + "," + str(trade['Record Type']) + "\n")

        graph.close()

        # filtermarket.tsv
        graph = open("evaluator/filterorder.tsv","w+")

        graph.write("date,delay,distance,origin,destination,bbid,sbid,type\n")

        for trade in self.orders:
            date = str(trade['Date']) + ":"
            time = str(trade['Time'])
            if (len(time) == 15):
                time = time[:-3]
            if (len(date) == 9):
                date = date[:4] + "-" + date[4:]
                date = date[:7] + "-" + date[7:]
            if(time < "10:00:00.000"):
                time = "10:00:00.000"
            datetime = date + time;

            if(str(trade['Record Type']) == "ENTER"):
                if(str(trade['Bid/Ask']) == "A"):
                    tempType = "S"
                else:
                    tempType = str(trade['Bid/Ask'])
            else:
                tempType = str(trade['Record Type'])[0]
            


            graph.write(str(datetime) + "," + str(trade['Price']) + "," + str(trade['Volume']) + "," + str(trade['Value']) + "," + str(trade['Instrument']) + "," + str(trade['Buyer Broker ID']) + "," +str(trade['Seller Broker ID']) + "," + tempType + "\n")

        graph.close()

    def generateStrategyPerformanceSummaryJson(self):
        graph = open("evaluator/performancesummary.json","w+")
        
        #-----------------------------------------------
        first = 1
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
     
        buyAverage = 0
        sellAverage = 0
        if self.volumeOfBuys > 0:
            buyAverage = self.buyTotal/self.volumeOfBuys
        if self.volumeOfSells > 0:
            sellAverage = self.sellTotal/self.volumeOfSells
        #--------------------------------------------------------        
        
        graph.write('{')
        graph.write('"name" : "Strategy Performance Report",')
        graph.write('"children" : [')
        graph.write('{')
        graph.write('"name" : "Performance Summary",')
        graph.write('"children" : [')
        graph.write('{"name": "Bought ' +str(self.volumeOfBuys)+ ' shares"},')
        graph.write('{"name": "Sold: ' +str(self.volumeOfSells)+ ' shares"},')
        graph.write('{"name": "Profit: ' +str(self.sellTotal-self.buyTotal)+ '"},')
        graph.write('{"name": "Average buy price: ' +str(buyAverage)+ '"},')
        graph.write('{"name": "Average sell price: ' +str(sellAverage)+ '"}')
        graph.write(']')
        graph.write('},')
        
        graph.write('{')
        graph.write('"name" : "ORDERS - Each order contains upto 5 trades which occured before it was placed by the strategy",')
        graph.write('"children" : [')
        count = 0
        previousfive = []
        currenttradelocation = 0
        for algoorder in self.algorithmicorders:
            
            if len(self.tradesbeforeorder) > 0:
               previousfive = self.tradesbeforeorder.pop(0)
                                
            count += 1
            orderstring = str(algoorder["Date"]) + "   " + str(algoorder['Time']) + "   " + str(algoorder['Bid/Ask']) + "   " + str(algoorder['Volume']) + "   " + str(algoorder['Price'])
            
            graph.write('{"name": "' +orderstring+ '",')
            
            graph.write('"children" : [')    
            prevcount = 0
            for pasttrade in previousfive:
                prevcount += 1
                prevtradestring = str(pasttrade["Date"]) + "   " + str(pasttrade['Time']) + "   " + str(pasttrade['Volume']) + "   " + str(pasttrade['Price'])
                graph.write('{"name": "' +prevtradestring)
                
                if prevcount < len(previousfive):
                    graph.write('"},')
                else:
                    graph.write('"}')
            
            
            graph.write(']')
            
            
            
            if count < len(self.algorithmicorders):
                graph.write('},')
            else:
                graph.write('}')
        graph.write(']')
        graph.write('},')
        
        graph.write('{')
        graph.write('"name" : "TRADES",')
        graph.write('"children" : [')
        countww = 0
        tracecounter = 0
        first = True
        for tradecounter in xrange(len(self.trades)):
            trade = self.trades[tradecounter]        
            countww = countww + 1
            if trade['Buyer Broker ID'] == 'Algorithmic' or trade['Seller Broker ID'] == 'Algorithmic':
                actiontype = ""
                if trade['Buyer Broker ID'] == 'Algorithmic':
                    actiontype = "Bought"
                if trade['Seller Broker ID'] == 'Algorithmic':
                    actiontype = actiontype + "Sold"
                
                tradestring = str(trade["Date"]) + "   " + str(trade['Time']) + "   " + actiontype + "   " + str(trade['Volume']) + "   " + str(trade['Price'])
                if first:
                    graph.write('{"name": "' +tradestring)
                    first = False
                else:
                    graph.write(',{"name": "' +tradestring)
                    
                if countww < len(self.trades):
                    graph.write('"}')
                else:
                    graph.write('"}')
        graph.write(']')
        graph.write('}')
        graph.write(']')
        graph.write('}')
        graph.close()
