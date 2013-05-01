#!/usr/bin/env python

"""trader module, containing the main logic"""

import itertools
import heapq


def run_trial(market_data, signal_generator,
              engine, strategy_evaluator):
    """Run the experiment with the given market data"""
    trades = []
    orders = []
    count = itertools.count()

    # Get the signal generators initial orders i.e. before market opens
    for order in signal_generator():
        heapq.heappush(orders, (order['Date'], order['Time'], count, order))
        next(count)

    for trading_record in market_data:
        recordType = trading_record['Record Type']
        # We need to filter existing trades out, because signal generator now accepts trades
        if ((recordType != 'TRADE') and (recordType != 'CANCEL_TRADE') and (recordType != 'OFFTR')):
            engine_time = (trading_record['Date'], trading_record['Time'])
            newtrades = []
            while len(orders) > 0 and orders[0][:2] <= engine_time:
                newtrades.extend(engine(heapq.heappop(orders)[3]))
            newtrades.extend(engine(trading_record))
            trades.extend(newtrades)
            # Inform the signal generator about the new trades made
            for newtrade in newtrades:
                for order in signal_generator(newtrade):
                    heapq.heappush(orders,
                                   (order['Date'], order['Time'], count, order))
                    next(count)        
            # Inform the signal generator about the new orders placed
            for order in signal_generator(trading_record):
                heapq.heappush(orders,
                               (order['Date'], order['Time'], count, order))
                next(count)
    for i in range(len(orders)):
        trades.extend(engine(heapq.heappop(orders)[3]))
    #for order in signal_generator():
    #    trades.extend(engine(order))
    strategy_evaluator(trades)
    return trades

if __name__ == '__main__':
    import doctest
    doctest.testmod()
