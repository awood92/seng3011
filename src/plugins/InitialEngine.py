"""Initial engine plugin"""

import plugins
import copy

class InitialEngine(plugins.IEnginePlugin):
    """All input trades are sent to the output"""
    previous_trade = None
    orderBook = OrderBook()

    def __call__(self, trading_record):

        trades = []
        record_type = trading_record['Record Type']
        if record_type == 'TRADE':
            trades.append(trading_record)
        elif record_type == 'AMEND':
            pass
        elif record_type == 'ENTER':
            pass
        elif record_type == 'DELETE':
            pass 
        

            
                
        return trades
    def setPrevTrade(self,previous_trade):

        self.previous_trade = previous_trade
        
# elif trading_record['Record Type'] == 'ENTER':
#     currentType = trading_record['Bid/Ask']
#     if 'Bid/Ask' in self.previous_trade: #If not the first trade
#         prevType = self.previous_trade['Bid/Ask']
#         newRecord = copy.deepcopy(trading_record)
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
