"""Mean reversion signal generator plugin"""

import plugins

class MomentumSignalGenerator(plugins.ISignalGeneratorPlugin):
    """Makes buy and sell signals based off the mean reversion strategy"""

    def setup(self, config):
        """Reads mean reversion strategy parameters from the config file"""
        self.buyPacketSize = config.getint('Parameters','buyPacketSize')
        self.sellPacketSize = config.getint('Parameters','sellPacketSize')
        
        self.maxBuyPacketSurplus = config.getint('Parameters','maxBuyPacketSurplus')
        self.buyDistanceFromMeanThreshold = config.getfloat('Parameters','buyDistanceFromMeanThreshold')
        self.sellDistanceFromMeanThreshold = config.getfloat('Parameters','sellDistanceFromMeanThreshold')
        self.minimumAverageSamplesBeforeAction = config.getfloat('Parameters','minimumAverageSamplesBeforeAction')
        self.minimumTimeBeforeAction = config.get('Parameters','minimumTimeBeforeAction')
        
        
        self.BHPsharesInStock = 0
        self.outstandingSellVolume = 0;
        
        self.myorders = []
        self.tradesViewed = []
        self.averagePrice = 0
        
        self.belowAverage = True
        self.consistentMovementPeriod = 0
        
        self.currentTime = '00:00:00.000'

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
            
            self.tradesViewed.insert(0,trading_record)
            self.updateRunningAveragePrice(trading_record)
            
            #if self.belowAverage:
            #    self.consistentMovementPeriod += 1
            #else:
            #    self.rising = True
            #    self.consistentMovementPeriod = 1
            
            if len(self.tradesViewed) >= self.minimumAverageSamplesBeforeAction and self.currentTime >= self.minimumTimeBeforeAction:
                distance = self.distanceFromMean(float(trading_record['Price']))
                if distance <= self.sellDistanceFromMeanThreshold:
                    if self.BHPsharesInStock > 0:
                        sell = trading_record.copy()
                        sell['Record Type'] = 'ENTER'
                        sell['Bid/Ask'] = 'A'
                        sell['Price'] = 'MP' #trading_record['Price'] # we can decrease this if we want
                        
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
                elif distance >= self.buyDistanceFromMeanThreshold:
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
                        self.myorders.append(buy)  
        return orders
    
    def distanceFromMean(self,trade_price):
        return (trade_price-self.averagePrice)/self.averagePrice
    
    def updateRunningAveragePrice(self,trading_record):
        self.averagePrice = (self.averagePrice*(len(self.tradesViewed)-1) + float(trading_record['Price']))/float(len(self.tradesViewed))
    
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
        if self.BHPsharesInStock + self.outstandingSellVolume >= self.maxBuyPacketSurplus*self.buyPacketSize:
            return False
        return True
