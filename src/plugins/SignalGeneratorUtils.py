def calculateAverageReturn(trades):
    prices = []
    for trade in trades:
        prices.append(float(trade['Price']))
    return _calculateAverageReturn(prices)
    
def _calculateAverageReturn(prices):
    returns = []
    prevTradePrice = -1
    for currPrice in prices:
        if prevTradePrice != -1:
            currentreturn = float(currPrice) - float(prevTradePrice)
            currentreturn = float(float(currentreturn) / float(prevTradePrice))
            returns.append(currentreturn)
        prevTradePrice = float(currPrice)
    averageReturn = 0
    for ret in returns:
        averageReturn += float(ret)
    return float(averageReturn)/float((len(prices)-1))  
