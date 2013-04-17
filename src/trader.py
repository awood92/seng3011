#!/usr/bin/python

"""trader module, containing the main logic"""

import heapq


def run_trial(market_data, signal_generator,
              engine, strategy_evaluator):
    """Run the experiment with the given market data"""
    trades = []
    orders = []
    for order in signal_generator():
        heapq.heappush(orders, ((order['Date'], order['Time']), order))
    for trading_record in market_data:
        engine_Time = (trading_record['Date'], trading_record['Time'])
        while len(orders) > 0 and orders[0][0] < engine_Time:
            trades.extend(engine(heapq.heappop(orders)[1]))
        trades.extend(engine(trading_record))
        for order in signal_generator(trading_record):
            heapq.heappush(orders, ((order['Date'], order['Time']), order))
    for i in range(len(orders)):
        trades.extend(engine(heapq.heappop(orders)[1]))
    for order in signal_generator():
        trades.extend(engine(order))
    strategy_evaluator(trades)
    return trades

if __name__ == '__main__':
    import doctest
    doctest.testmod()
