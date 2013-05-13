"""Momentum signal generator plugin"""

import plugins

class MomentumSignalGenerator(plugins.ISignalGeneratorPlugin):
    """Makes buy and sell signals based off the momentum strategy"""

    def setup(self, config):
        """Reads momentum strategy parameters from the config file"""
        self.started = False
        
        self.minimumAverageSamplesBeforeAction = config.getfloat('Parameters','minimumAverageSamplesBeforeAction')
        self.minimumTimeBeforeAction = config.get('Parameters','minimumTimeBeforeAction')
        
        self.buyDistanceFromMeanThreshold = config.getfloat('Parameters','buyDistanceFromMeanThreshold')
        self.sellDistanceFromMeanThreshold = config.getfloat('Parameters','sellDistanceFromMeanThreshold')
        
        self.buyPacketSize = config.getint('Parameters','buyPacketSize')
        self.sellPacketSize = config.getint('Parameters','sellPacketSize')
        self.maxBuyPacketSurplus = config.getint('Parameters','maxBuyPacketSurplus')

        # All the orders which have informed this signal generator
        self.ordersviewed = []
        # All the trades which have informed this signal generator
        self.tradesviewed = []
        self.runningaverage = 0
        
        self.BHPsharesInStock = 0 # convert this into a dictionary for multiple instruments
        self.myorders = []
        self.outstandingSellVolume = 0
        self.outstandingBuyVolume = 0
        self.currentTime = '00:00:00.000'
        
        self.historicalOutlook = config.getint('Parameters','historicalOutlook')
        if self.historicalOutlook < 2:
            self.historicalOutlook = 2


    def __call__(self, trading_record=None, endofday=False):
        orders = []
            
        if trading_record == None and endofday == False:
            # return all initial orders i.e. random before market open
            return orders
        elif trading_record == None and endofday == True:
            if self.BHPsharesInStock > 0:
                # Dump the shares because day is finished
                return self.createDumpShareSell()
            return None
        elif trading_record['Record Type'] == 'TRADE':
            self.currentTime = trading_record['Time']
            if trading_record['Buyer Broker ID'] == 'Algorithmic':
                self.BHPsharesInStock += int(trading_record['Volume'])
            if trading_record['Seller Broker ID'] == 'Algorithmic':
                self.outstandingSellVolume -= int(trading_record['Volume'])
            
            self.tradesviewed.insert(0,trading_record)
            if len(self.tradesviewed) > self.historicalOutlook:
                self.tradesviewed.pop()
            if len(self.tradesviewed) > 1:
                self.runningaverage = self.calculateAverageReturn()
            
            if len(self.tradesviewed) >= self.minimumAverageSamplesBeforeAction and self.currentTime >= self.minimumTimeBeforeAction:
                # Buy trading signal
                if self.runningaverage >= self.buyDistanceFromMeanThreshold:
                    if self.shouldBuyMoreStocks(trading_record['Instrument']) == True:
                        buy = trading_record.copy()
                        buy['Record Type'] = 'ENTER'
                        buy['Bid/Ask'] = 'B'
                        buy['Price'] = 'MP' #trading_record['Price'] # we can increase this if we want
                        buy['Volume'] = self.buyPacketSize # Determine this based off market volume maybe?
                        buy['Bid ID'] = 'Algorithmic' + str(len(self.myorders))
                        buy['Ask ID'] = ''
                        buy['Buyer Broker ID'] = 'Algorithmic'
                        buy['Seller Broker ID'] = ''
                        orders.append(buy)
                        self.outstandingBuyVolume += int(buy['Volume'])
                        self.myorders.append(buy)                        
                # Sell trading signal
                elif self.runningaverage <= -self.sellDistanceFromMeanThreshold:
                    if self.BHPsharesInStock > 0:
                        sell = trading_record.copy()
                        sell['Record Type'] = 'ENTER'
                        sell['Bid/Ask'] = 'A'
                        sell['Price'] = 'MP'
                        
                        if self.BHPsharesInStock >= self.sellPacketSize:
                            sell['Volume'] = str(self.sellPacketSize)
                            self.BHPsharesInStock -= self.sellPacketSize
                        else:
                            sell['Volume'] = str(self.BHPsharesInStock)
                            self.BHPsharesInStock = 0
                        
                        self.outstandingSellVolume += int(sell['Volume'])
                        sell['Ask ID'] = 'Algorithmic' + str(len(self.myorders)) # Keeps this unique
                        sell['Bid ID'] = ''
                        sell['Buyer Broker ID'] = ''
                        sell['Seller Broker ID'] = 'Algorithmic'
                        orders.append(sell)
                        self.myorders.append(sell)
        return orders       
    
    def calculateAverageReturn(self):
        returns = []
        prevTradePrice = -1
        for currTrade in self.tradesviewed:
            if prevTradePrice != -1:
                returns.append(float((prevTradePrice-float(currTrade['Price']))/float(currTrade['Price'])))
            prevTradePrice = float(currTrade['Price'])
        averageReturn = 0
        for ret in returns:
            averageReturn += ret
        return float(averageReturn)/float((len(self.tradesviewed)-1))
    
    def createDumpShareSell(self):
        sell = {
            'Instrument': 'BHP',
            'Date': '20130101',
            'Time': self.currentTime,
            'Record Type': 'ENTER',
            'Price': 'MP',
            'Volume': self.BHPsharesInStock,
            'Undisclosed Volume': '',
            'Value': '',
            'Qualifiers': '',
            'Trans ID': 0,
            'Bid ID': '',
            'Ask ID': 'Algorithmic' + str(len(self.myorders)),
            'Bid/Ask': 'A',
            'Entry Time': '',
            'Old Price': '',
            'Old Volume': '',
            'Buyer Broker ID': '',
            'Seller Broker ID': 'Algorithmic'
        }
        
        return sell
    def shouldBuyMoreStocks(self, instrument):
        if self.BHPsharesInStock + self.outstandingSellVolume + self.outstandingBuyVolume >= self.maxBuyPacketSurplus*self.buyPacketSize:
            return False
        return True
