"""Initial engine plugin"""

import plugins
import copy
from OrderBook import OrderBook
from datetime import datetime

class InitialEngine(plugins.IEnginePlugin):
    """All input trades are sent to the output"""
    algorithmicOrderQueue = []
    orderBook = OrderBook()
    currentTime = None
    def __call__(self, record):
        trades = []
        if self._isAlgorithmicOrder(record):
            algorithmicOrderQueue.append(record) # fix this to insert in time order
        else:
            self.currentTime = datetime.strptime(record['Time'],'%H:%M:%S.%f')
            trades.extend(self._addOrder(record,self.currentTime))

        algOrdersToRemove = []
        for algOrder in self.algorithmicOrderQueue:
            algOrderTime = datetime.strptime(algOrder['Time'],'%H:%M:%S.%f')
            currentRecordTime = datetime.strptime(record['Time'],'%H:%M:%S.%f')
            if currentRecordTime >= algOrderTime:
                trades.extend(self._addOrder(algOrder,currentTime))
                algOrdersToRemove.append(algOrder)

        for order in algOrdersToRemove:
            algorithmicOrderQueue.remove(order)
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
    
    def _isAlgorithmicOrder(self,record):
        return (record['Buyer Broker ID'] == "Algorithmic") or (record['Seller Broker ID'] == "Algorithmic")
        
# elif record['Record Type'] == 'ENTER':
#     currentType = record['Bid/Ask']
#     if 'Bid/Ask' in self.previous_trade: #If not the first trade
#         prevType = self.previous_trade['Bid/Ask']
#         newRecord = copy.deepcopy(record)
#         if self.previous_trade['Record Type'] == 'ENTER' and currentType != prevType:
            
#             newRecord['Bid/Ask'] = ''
#             newRecord['Record Type'] = 'ALGOTRADE'
#             if currentType == 'B': #buy
#                 newRecord['Ask ID'] = self.previous_trade['Bid ID']
#             else: #sell
#                 newRecord['Bid ID'] = self.previous_trade['Ask ID']
#             trades.append(newRecord)
#     else:
#         self.previous_trade['Bid/Ask'] = ''
