"""Initial engine plugin"""

import plugins
import copy
from OrderBook import OrderBook

class InitialEngine(plugins.IEnginePlugin):
    """All input trades are sent to the output"""
    previous_trade = None
    algorithmicOrderQueue = []
    orderBook = OrderBook()

    def __call__(self, record):
        trades = []
        if self._isAlgorithmicOrder(record):
            algorithmicOrderQueue.append(record) # fix this to insert in time order
        else:
            trades.extend(self._addOrder(record))

        algOrdersToRemove = []
        for algOrder in algorithmicOrderQueue:
            algOrderTime = datetime.strptime(algOrder['Time'],'%H:%M:%S.%f')
            currentRecordTime = datetime.strptime(record['Time'],'%H:%M:%S.%f')
            if currentRecordTime >= algOrderTime:
                trades.extend(self._addOrder(algOrder))
                algOrdersToRemove.append(algOrder)

        for order in algOrdersToRemove:
            algorithmicOrderQueue.remove(order)
        return trades

    def _addOrder(self,order):
        trades = []
        record_type = record['Record Type']

        if record_type == 'AMEND':
            trades.extend(self.orderBook.amend(record))
        elif record_type == 'ENTER':
            if record['Bid/Ask'] == 'B':
                trades.extend(self.orderBook.addToBuy(record))
            else:
                trades.extend(self.orderBook.addToSell(record))
        elif record_type == 'DELETE':
	    #assert this later
            self.orderBook.delete(record)

        return trades
    
    def _isAlgorithmicOrder(record):
        return (record['Buyer Broker ID'] == "algorithmictrader") or (record['Seller Broker ID'] == "algorithmictrader")
        
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
