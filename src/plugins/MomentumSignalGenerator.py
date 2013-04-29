"""Momentum signal generator plugin"""

import plugins

class MomentumSignalGenerator(plugins.ISignalGeneratorPlugin):
    """Makes buy and sell signals based off the momentum strategy"""

    def setup(self, config):
        """Reads momentum strategy parameters from the config file"""
        self.started = False
        
        self.historicalOutlook = config.getint('Parameters','historicalOutlook')
        
        # All the orders which have informed this signal generator
        self.ordersviewed = []
        # All the trades which have informed this signal generator
        self.tradesviewed = []
        
        self.sharesInStock = []

        # Orders made by this signal generator
        self.myorders = []
        # Trades made involving this signal generators orders
        self.mytrades = []

    def __call__(self, trading_record=None):
        orders = []
        
        if trading_record == None:
            # return all initial orders i.e. random before market open
        elif trading_record['Record Type'] == 'TRADE':
            self.tradesviewed.insert(0,trading_record)
            
            if trading_record['Buyer Broker ID'] == 'Algorithmic':
                self.sharesInStock[trading_record['Instrument']] += trading_record['Volume']
            
            if trading_record['Seller Broker ID'] == 'Algorithmic':
                self.sharesInStock[trading_record['Instrument']] -= trading_record['Volume']
            
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
                    buy = trading_record.copy()
                    buy['Record Type'] = 'ENTER'
                    buy['Bid/Ask'] = 'B'
                    buy['Price'] = trading_record['Price'] # we can increase this if we want
                    buy['Volume'] = trading_record['Volume'] # Determine this based off market volume maybe?
                    buy['Bid ID'] = 'Algorithmic' + len(self.myorders)
                    buy['Buyer Broker ID'] = 'Algorithmic'
                    buy['Seller Broker ID'] = ''
                    orders.append(buy)
                    self.myorders.append(buy)
                # Sell trading signal
                elif averageReturn/len(returns) < 0:
                    sell = trading_record.copy()
                    sell['Record Type'] = 'ENTER'
                    sell['Bid/Ask'] = 'A'
                    sell['Price'] = trading_record['Price'] # we can decrease this if we want
                    
                    # Determine volume based off how much we currently hold, can be parameterised
                    volumeToSell = self.sharesInStock[sell['Instrument']] / 4
                    sell['Volume'] = volumeToSell
                    self.sharesInStock[sell['Instrument']] -= volumeToSell
                    
                    sell['Bid ID'] = 'Algorithmic' + len(self.myorders) # Keeps this unique
                    sell['Buyer Broker ID'] = ''
                    sell['Seller Broker ID'] = 'Algorithmic'
                    orders.append(sell)
                    self.myorders.append(sell)
        return orders
