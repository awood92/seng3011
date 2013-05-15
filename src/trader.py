#!/usr/bin/env python

"""trader module, containing the main logic"""

import itertools
import heapq


def run_trial(market_data, signal_generator,
              engine, strategy_evaluator,progressdialog=None):
    """Run the experiment with the given market data"""
    trades = []
    marketTrades = []
    orders = []
    algorithmicorders = []
    count = itertools.count()

    # Get the signal generators initial orders i.e. before market opens
    for order in signal_generator():
        algorithmicorders.append(order)
        heapq.heappush(orders, (order['Date'], order['Time'], count, order))
        next(count)
        
    tradingrecordsprocessed = 0
    for trading_record in market_data:
        if trading_record['Qualifiers'] != None and (not "OB0" in trading_record['Qualifiers']):
            tradingrecordsprocessed += 1
            if progressdialog != None and tradingrecordsprocessed%1000 == 0:
                progressdialog.Update(tradingrecordsprocessed,"Processing records: "+str(tradingrecordsprocessed)+" complete.")
            recordType = trading_record['Record Type']
            # We need to filter existing trades out, because signal generator now accepts trades
            if ((recordType != 'TRADE') and (recordType != 'CANCEL_TRADE') and (recordType != 'OFFTR')):
                engine_time = (trading_record['Date'], trading_record['Time'])
                newtrades = []
                while len(orders) > 0 and orders[0][:2] <= engine_time:
                    newtrades.extend(engine(heapq.heappop(orders)[3]))
                newtrades.extend(engine(trading_record))
                trades.extend(newtrades)
                marketTrades.extend(newtrades)
                # Inform the signal generator about the new trades made
                for newtrade in newtrades:
                    for order in signal_generator(newtrade):
                        algorithmicorders.append(order.copy())
                        heapq.heappush(orders,
                                       (order['Date'], order['Time'], count, order))
                        next(count)        
                # Inform the signal generator about the new orders placed
                for order in signal_generator(trading_record):
                    algorithmicorders.append(order.copy())
                    heapq.heappush(orders,
                                   (order['Date'], order['Time'], count, order))
                    next(count)
            elif trading_record['Record Type'] == 'TRADE':
                trading_record['Record Type'] = 'MARKET'
                marketTrades.append(trading_record)
    for i in range(len(orders)):
        newtrades = []
        currentorder = heapq.heappop(orders)[3]
        newtrades.extend(engine(currentorder))
        for order in signal_generator(currentorder):
            algorithmicorders.append(order.copy())
            newtrades.extend(engine(order))              
        trades.extend(newtrades)
        marketTrades.extend(newtrades)
    
    # Tell the signal generator its the end of the day
    lastorder = signal_generator(None,True)
    if lastorder != None:
        algorithmicorders.append(lastorder)
    endofdaydump = engine(lastorder)
    trades.extend(endofdaydump)
    marketTrades.extend(endofdaydump)
    
    trades = sorted(trades, key=lambda trade: trade['Time'])
    marketTrades = sorted(marketTrades, key=lambda trade: trade['Time'])
    strategy_evaluator(trades,marketTrades,algorithmicorders)
    return trades

if __name__ == '__main__':
    import doctest
    doctest.testmod()
