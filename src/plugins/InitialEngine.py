"""Initial engine plugin"""

import plugins
import copy
from OrderBook import OrderBook
from datetime import datetime

class InitialEngine(plugins.IEnginePlugin):
    """All input trades are sent to the output"""
    orderBook = OrderBook()
    currentTime = None
    def __call__(self, record):
        trades = []
        self.currentTime = datetime.strptime(record['Time'],'%H:%M:%S.%f')
        trades.extend(self._addOrder(record,self.currentTime))
        return trades

    def _addOrder(self,order,currentTime):
        trades = []
        order_type = order['Record Type']
	
        # We do not handle TRADE, CANCEL_TRADE and OFFTR (off market trades) because our simulation handles
        # the matching of orders to form trades. Trade match-ups will be different under our 
        # market conditions when our strategy generates algorithmic orders
        if order_type == 'AMEND':
            trades.extend(self.orderBook.amend(order,currentTime))
        elif order_type == 'ENTER':
            if order['Bid/Ask'] == 'B':
                trades.extend(self.orderBook.addToBuy(order,currentTime))
            else:
                trades.extend(self.orderBook.addToSell(order,currentTime))
        elif order_type == 'DELETE':
            self.orderBook.delete(order) #assert this later

        return trades
