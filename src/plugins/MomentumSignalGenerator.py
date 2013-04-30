"""Momentum signal generator plugin"""

import plugins

class MomentumSignalGenerator(plugins.ISignalGeneratorPlugin):
    """Makes buy and sell signals based off the momentum strategy"""

    def setup(self, config):
        """Reads momentum strategy parameters from the config file"""
        self.started = False
        
        # This is the interval for consistent movement before registering momentum
        self.momentumInterval = config.getint('Parameters','momentumInterval')
        self.historicalOutlook = config.getint('Parameters','historicalOutlook')
        if self.historicalOutlook < 2:
            self.historicalOutlook = 2
        self.buyPacketSize = config.getint('Parameters','buyPacketSize')
        self.sellPacketSize = config.getint('Parameters','sellPacketSize')
        self.maxBuyPacketSurplus = config.getint('Parameters','maxBuyPacketSurplus')
        
        self.consistentMovementPeriod = 0
        self.rising = False
        
        # All the orders which have informed this signal generator
        self.ordersviewed = []
        # All the trades which have informed this signal generator
        self.tradesviewed = []
        
        self.BHPsharesInStock = 0 # convert this into a dictionary for multiple instruments
        self.myorders = []
        self.outstandingSellVolume = 0

    def __call__(self, trading_record=None):
        orders = []
        
        if trading_record == None:
            # return all initial orders i.e. random before market open
            return orders
        elif trading_record['Record Type'] == 'TRADE':
            self.tradesviewed.insert(0,trading_record)
            
            if trading_record['Buyer Broker ID'] == 'Algorithmic':
                self.BHPsharesInStock += int(trading_record['Volume'])
            if trading_record['Seller Broker ID'] == 'Algorithmic':
                self.outstandingSellVolume -= int(trading_record['Volume'])
            
            if len(self.tradesviewed) > self.historicalOutlook:
                self.tradesviewed.pop()
                
                returns = []
                prevTradePrice = -1
                for currTrade in self.tradesviewed:
                    if prevTradePrice != -1:
                        returns.append((float(currTrade['Price'])-prevTradePrice)/prevTradePrice)
                    prevTradePrice = float(currTrade['Price'])
                
                averageReturn = 0
                for ret in returns:
                    averageReturn += ret
                
                # Buy trading signal
                if averageReturn/len(returns) > 0:
                    if self.rising:
                        self.consistentMovementPeriod += 1
                    else:
                        self.rising = True
                        self.consistentMovementPeriod = 1

                    if self.consistentMovementPeriod == self.momentumInterval:
                        if self.shouldBuyMoreStocks(trading_record['Instrument']):
                            buy = trading_record.copy()
                            buy['Record Type'] = 'ENTER'
                            buy['Bid/Ask'] = 'B'
                            buy['Price'] = trading_record['Price'] # we can increase this if we want
                            buy['Volume'] = self.buyPacketSize # Determine this based off market volume maybe?
                            buy['Bid ID'] = 'Algorithmic' + str(len(self.myorders))
                            buy['Buyer Broker ID'] = 'Algorithmic'
                            buy['Seller Broker ID'] = ''
                            orders.append(buy)
                            self.myorders.append(buy)                        

                # Sell trading signal
                elif averageReturn/len(returns) < 0:
                    if not self.rising:
                        self.consistentMovementPeriod += 1
                    else:
                        self.rising = False
                        self.consistentMovementPeriod = 1
                    
                    if self.consistentMovementPeriod == self.momentumInterval:
                        if self.BHPsharesInStock > 0:
                            sell = trading_record.copy()
                            sell['Record Type'] = 'ENTER'
                            sell['Bid/Ask'] = 'A'
                            sell['Price'] = trading_record['Price'] # we can decrease this if we want
                            
                            # Determine volume based off how much we currently hold, can be parameterised
                            if self.BHPsharesInStock >= self.sellPacketSize:
                                sell['Volume'] = self.sellPacketSize
                                self.BHPsharesInStock -= self.sellPacketSize
                            else:
                                sell['Volume'] = self.BHPsharesInStock
                                self.BHPsharesInStock = 0
                            
                            self.outstandingSellVolume += int(sell['Volume'])
                            sell['Bid ID'] = 'Algorithmic' + str(len(self.myorders)) # Keeps this unique
                            sell['Buyer Broker ID'] = ''
                            sell['Seller Broker ID'] = 'Algorithmic'
                            orders.append(sell)
                            self.myorders.append(sell)
        return orders
        
    def shouldBuyMoreStocks(self, instrument):
        if self.BHPsharesInStock + self.outstandingSellVolume >= self.maxBuyPacketSurplus*self.buyPacketSize:
            return False
        return True
