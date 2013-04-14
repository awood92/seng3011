"""Initial engine plugin"""

import plugins
import copy
from OrderBook import OrderBook

class InitialEngine(plugins.IEnginePlugin):
    """All input trades are sent to the output"""
    previous_trade = None
    orderBook = OrderBook()

    def __call__(self, record):

        trades = []
        record_type = record['Record Type']
        if record_type == 'TRADE':
            trades.append(record)
        elif record_type == 'AMEND':
            self.orderBook.amend(record)
        elif record_type == 'ENTER':
            if record['Bid/Ask'] == 'B':
                self.orderBook.addToBuy(record)
            else:
                self.orderBook.addToSell(record)
        elif record_type == 'DELETE':
            #assert this later
            self.orderBook.delete(record)
                
        return trades
    def setPrevTrade(self,previous_trade):

        self.previous_trade = previous_trade
        
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
