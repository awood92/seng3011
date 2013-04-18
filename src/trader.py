#!/usr/bin/python

"""trader module, containing the main logic"""

import itertools
import heapq


def run_trial(market_data, signal_generator,
              engine, strategy_evaluator):
    """Run the experiment with the given market data"""
    trades = []
    orders = []
    count = itertools.count()
    for order in signal_generator():
        heapq.heappush(orders, (order['Date'], order['Time'], count, order))
        next(count)
    for trading_record in market_data:
        engine_time = (trading_record['Date'], trading_record['Time'])
        while len(orders) > 0 and orders[0][0:2] < engine_time:
            trades.extend(engine(heapq.heappop(orders)[3]))
	trades.extend(engine(trading_record))
        for order in signal_generator(trading_record):
            heapq.heappush(orders, (order['Date'], order['Time'], count, order))
            next(count)
    for i in range(len(orders)):
        trades.extend(engine(heapq.heappop(orders)[3]))
    for order in signal_generator():
        trades.extend(engine(order))
    strategy_evaluator(trades)
    return trades

if __name__ == '__main__':
    import doctest
    doctest.testmod()
