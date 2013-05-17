"""Initial engine plugin"""

import plugins

from datetime import datetime


class OrderBook:
    """This is a data structure used for matching buys and sells"""

    def __init__(self):
        self.buys = []
        self.sells = []

    def addToBuy(self, newRecord, currentTime):
        self._insortBuy(newRecord)
        if not self._startOfDay(currentTime):
            return self._matchOrders(currentTime)
        return []

    def addToSell(self, newRecord, currentTime):
        self._insortSell(newRecord)
        if not self._startOfDay(currentTime):
            return self._matchOrders(currentTime)
        return []

    def amend(self, recordToAmend, currentTime):
        #assert this later
        matchedOrders = []
        if self.delete(recordToAmend):
            recordToAmend['Record Type'] = 'ENTER'
            recordType = recordToAmend['Bid/Ask']
            if recordType == 'B':
                self._insortBuy(recordToAmend)
            elif recordType == 'A':
                self._insortSell(recordToAmend)

            if not self._startOfDay(currentTime):
                matchedOrders = self._matchOrders(currentTime)
        return matchedOrders

    def delete(self, recordToRemove):
        #returns True if deleted False otherwise
        valueToFind = None
        recordType = recordToRemove['Bid/Ask']
        removed = False
        # TODO - can improve this by making it a binary search since they are in price order
        if recordType == 'B':
            valueToFind = recordToRemove['Bid ID'] 
            for record in self.buys:
                if record['Bid ID'] == valueToFind:
                    recordToRemove = record
                    removed = True
                    break
            if removed:
                self.buys.remove(recordToRemove)
        else:
            valueToFind = recordToRemove['Ask ID']
            for record in self.sells:
                if record['Ask ID'] == valueToFind:
                    recordToRemove = record
                    removed = True
                    break
            if removed:
                self.sells.remove(recordToRemove)
        return removed

    def _matchOrders(self, currentTime):
        #This will go through buys and sells and return matched orders
        trades = []
        finished = False
        buysToDelete = []
        for buyOrd in self.buys:
            sellsToDelete = []
            for sellOrd in self.sells:
                if (buyOrd['Price'] == 'MP' or sellOrd['Price'] == 'MP' or float(buyOrd['Price']) >= float(sellOrd['Price'])):
                    # Match the trades
                    finishedBuyOrder = self._matchTrade(trades,buyOrd,sellOrd,buysToDelete,sellsToDelete,currentTime)
                    
                    if finishedBuyOrder:
                        break
                else:
                    finished = True
                    break
            
            for sell in sellsToDelete:
                self.sells.remove(sell)
                
            if finished:  # The spread (difference between buy price and sell price) is less then 0
                break
                
        for buy in buysToDelete:
            self.buys.remove(buy)
        
        # Delete the first item in the list if it is market order
        if len(self.buys) > 0:
            if self.buys[0]['Price'] == 'MP':
                self.buys.pop(0)
        if len(self.sells) > 0:
            if self.sells[0]['Price'] == 'MP':
                self.sells.pop(0)

        return trades
    
    def _matchTrade(self,trades,buyOrd,sellOrd,buysToDelete,sellsToDelete,currentTime):
        if int(buyOrd['Volume']) > int(sellOrd['Volume']):
            trades.append(self._createTrade(buyOrd, sellOrd, sellOrd['Volume'], currentTime))
            buyOrd['Volume'] = str(int(buyOrd['Volume']) - int(sellOrd['Volume']))
            sellsToDelete.append(sellOrd)
        elif int(buyOrd['Volume']) == int(sellOrd['Volume']):
            trades.append(self._createTrade(buyOrd, sellOrd, buyOrd['Volume'], currentTime))
            sellsToDelete.append(sellOrd)
            buysToDelete.append(buyOrd)
            return True
        else:
            trades.append(self._createTrade(buyOrd, sellOrd, buyOrd['Volume'], currentTime))
            sellOrd['Volume'] = str(int(sellOrd['Volume']) - int(buyOrd['Volume']))
            buysToDelete.append(buyOrd)
            return True
        
        return False # Hasnt finished the current buy order yet
    
    def _createTrade(self, buyOrder, sellOrder, volume, currentTime):
        trade = buyOrder.copy()
        trade['Record Type'] = "TRADE"
        
        # Should never be the case
        #if sellOrder['Price'] == 'MP' and buyOrder['Price'] == 'MP':
        #    trade['Price'] = self.lastTrade['Price']
       
        if sellOrder['Price'] == 'MP' and buyOrder['Price'] != 'MP':
            trade['Price'] = buyOrder['Price']
        elif sellOrder['Price'] != 'MP' and buyOrder['Price'] == 'MP':
            trade['Price'] = sellOrder['Price']
        else:
            trade['Price'] = sellOrder['Price']
        
        trade['Volume'] = volume    
        trade['Value'] = int(volume) * float(trade['Price'])
        trade['Ask ID'] = sellOrder['Ask ID']
        trade['Bid/Ask'] = ""
        trade['Seller Broker ID'] = sellOrder['Seller Broker ID']
        trade['Time'] = datetime.strftime(currentTime, "%H:%M:%S.%f")
        return trade
        
    def _insortSell(self, record):
        count = 0
        if record['Price'] != 'MP':
            insertPrice = float(record['Price'])
            for order in self.sells:
                if order['Price'] != 'MP' and insertPrice < float(order['Price']):
                    break
                else:
                    count += 1
        self.sells.insert(count, record)

    def _insortBuy(self, record):
        count = 0
        if record['Price'] != 'MP':
            insertPrice = float(record['Price'])
            for order in self.buys:
                if order['Price'] != 'MP' and insertPrice > float(order['Price']):
                    break
                else:
                    count += 1
        self.buys.insert(count, record)

    def printBook(self):
        for item in self.buys:
            print item
        for item in self.sells:
            print item
            
    def _startOfDay(self, currentTime):
        # anything before 10am is in the pre-open market phase. no trading
        return currentTime < datetime.strptime("10:00:00.000", "%H:%M:%S.%f")

class InitialEngine(plugins.IEnginePlugin):
    """All input trades are sent to the output"""

    def setup(self, config):
        self.orderBook = OrderBook()
        self.currentTime = None

    def __call__(self, record=None):
        trades = []
        if record != None:  # this might be None when a trader has nothing to dump at end of day
            self.currentTime = datetime.strptime(record['Time'], '%H:%M:%S.%f')
            trades.extend(self._addOrder(record, self.currentTime))
        return trades

    def _addOrder(self, order, currentTime):
        trades = []
        order_type = order['Record Type']
    
        # We do not handle TRADE, CANCEL_TRADE and OFFTR (off market trades) because our simulation handles
        # the matching of orders to form trades. Trade match-ups will be different under our 
        # market conditions when our strategy generates algorithmic orders
        if order_type == 'AMEND':
            trades.extend(self.orderBook.amend(order, currentTime))
        elif order_type == 'ENTER':
            if order['Bid/Ask'] == 'B':
                trades.extend(self.orderBook.addToBuy(order, currentTime))
            else:
                trades.extend(self.orderBook.addToSell(order, currentTime))
        elif order_type == 'DELETE':
            self.orderBook.delete(order)  # assert this later

        return trades
