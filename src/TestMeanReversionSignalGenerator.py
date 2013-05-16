import sys
import optparse
import csv
import signal
import os

import yapsy.PluginManager
import plugins

from plugins import MeanReversionSignalGenerator

def testMeanReversionSignalGenerator():  
    
    _testMeanReversionOrderGenerateNoOrders()
    _testMeanReversionGeneratesNoOrdersWhenBelowThreshold()
    _testMeanReversionGeneratesOrdersBasicOne()
    _testMeanReversionGeneratesOrdersBasicTwo()
    _testMeanReversionGeneratesOrdersBasicThree()
    _testMeanReversionGeneratesOrdersBasicFour()
    _testMeanReversionGeneratesOrdersBasicSell()
    _testMeanReversionGeneratesOrdersBuysThenSells()

def _testMeanReversionGeneratesNoOrdersWhenBelowThreshold():
    meanReversionSignalGenerator = MeanReversionSignalGenerator.MeanReversionSignalGenerator()
    parameterList = {"minimumTimeBeforeAction" : "10:05:00.000",
                    "buyDistanceFromMeanThreshold" : 0.001,
                    "sellDistanceFromMeanThreshold" : 0.001,       
                    "buyPacketSize" : 50,
                    "sellPacketSize" : 50,
                    "maxBuyPacketSurplus" : 1,
                    "historicalOutlook" : 2}
    meanReversionSignalGenerator.manualSetup(parameterList)
    trade1 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:00:00.000",'Record Type':"TRADE",'Price':"34.03",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"100",'Ask ID':"101",'Bid/Ask':"",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"1",'Seller Broker ID':"2"}
    trade2 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:02:00.000",'Record Type':"TRADE",'Price':"34.02",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"100",'Ask ID':"101",'Bid/Ask':"",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"1",'Seller Broker ID':"2"}
    trade3 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:03:00.000",'Record Type':"TRADE",'Price':"34.01",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"100",'Ask ID':"101",'Bid/Ask':"",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"1",'Seller Broker ID':"2"}
    trade4 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:04:00.000",'Record Type':"TRADE",'Price':"34.00",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"100",'Ask ID':"101",'Bid/Ask':"",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"1",'Seller Broker ID':"2"}
    
    trades = []
    trades.extend(meanReversionSignalGenerator(trade1))
    trades.extend(meanReversionSignalGenerator(trade2))
    trades.extend(meanReversionSignalGenerator(trade3))
    trades.extend(meanReversionSignalGenerator(trade4))
    
    assert len(trades) == 0

def _testMeanReversionGeneratesOrdersBasicOne():
    print "Testing two increasing trades generate a new order from the signal generator"
    meanReversionSignalGenerator = MeanReversionSignalGenerator.MeanReversionSignalGenerator()
    parameterList = {"minimumTimeBeforeAction" : "10:05:00.000",
                    "buyDistanceFromMeanThreshold" : 0.001,
                    "sellDistanceFromMeanThreshold" : 0.001,       
                    "buyPacketSize" : 50,
                    "sellPacketSize" : 50,
                    "maxBuyPacketSurplus" : 1,
                    "historicalOutlook" : 2}
    meanReversionSignalGenerator.manualSetup(parameterList)
    trade1 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:00:00.000",'Record Type':"TRADE",'Price':"34.1",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"100",'Ask ID':"101",'Bid/Ask':"",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"1",'Seller Broker ID':"2"}
    trade2 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:02:00.000",'Record Type':"TRADE",'Price':"34.0",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"100",'Ask ID':"101",'Bid/Ask':"",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"1",'Seller Broker ID':"2"}
        
    trades = []
    trades.extend(meanReversionSignalGenerator(trade1))
    trades.extend(meanReversionSignalGenerator(trade2))
    
    assert len(trades) == 1,"length of trades is " + str(len(trades)) + " not 1"

def _testMeanReversionGeneratesOrdersBasicTwo():
    print "Testing two decreasing trades generate a new order from the signal generator close to threshold"
    meanReversionSignalGenerator = MeanReversionSignalGenerator.MeanReversionSignalGenerator()
    parameterList = {"minimumTimeBeforeAction" : "10:05:00.000",
                    "buyDistanceFromMeanThreshold" : 0.002,
                    "sellDistanceFromMeanThreshold" : 0.002,       
                    "buyPacketSize" : 50,
                    "sellPacketSize" : 50,
                    "maxBuyPacketSurplus" : 1,
                    "historicalOutlook" : 2}
    meanReversionSignalGenerator.manualSetup(parameterList)
    trade1 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:00:00.000",'Record Type':"TRADE",'Price':"34.1",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"100",'Ask ID':"101",'Bid/Ask':"",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"1",'Seller Broker ID':"2"}
    trade2 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:02:00.000",'Record Type':"TRADE",'Price':"34.0",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"100",'Ask ID':"101",'Bid/Ask':"",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"1",'Seller Broker ID':"2"}
        
    trades = []
    trades.extend(meanReversionSignalGenerator(trade1))
    trades.extend(meanReversionSignalGenerator(trade2))
    
    assert len(trades) == 1,"length of trades is " + str(len(trades)) + " not 1"
    
def _testMeanReversionGeneratesOrdersBasicThree():
    print "Testing two increasing trades generate a no orders when below threshold"
    meanReversionSignalGenerator = MeanReversionSignalGenerator.MeanReversionSignalGenerator()
    parameterList = {"minimumTimeBeforeAction" : "10:05:00.000",
                    "buyDistanceFromMeanThreshold" : 0.003,
                    "sellDistanceFromMeanThreshold" : 0.003,       
                    "buyPacketSize" : 50,
                    "sellPacketSize" : 50,
                    "maxBuyPacketSurplus" : 1,
                    "historicalOutlook" : 2}
    meanReversionSignalGenerator.manualSetup(parameterList)
    trade1 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:00:00.000",'Record Type':"TRADE",'Price':"34.1",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"100",'Ask ID':"101",'Bid/Ask':"",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"1",'Seller Broker ID':"2"}
    trade2 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:02:00.000",'Record Type':"TRADE",'Price':"34.0",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"100",'Ask ID':"101",'Bid/Ask':"",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"1",'Seller Broker ID':"2"}
        
    orders = []
    orders.extend(meanReversionSignalGenerator(trade1))
    orders.extend(meanReversionSignalGenerator(trade2))
    
    assert len(orders) == 0,"length of trades is " + str(len(orders)) + " not 0"

def _testMeanReversionGeneratesOrdersBasicFour():
    print "Testing can buy more when buy packet surplus high enough"
    meanReversionSignalGenerator = MeanReversionSignalGenerator.MeanReversionSignalGenerator()
    parameterList = {"minimumTimeBeforeAction" : "10:05:00.000",
                    "buyDistanceFromMeanThreshold" : 0.001,
                    "sellDistanceFromMeanThreshold" : 0.001,       
                    "buyPacketSize" : 50,
                    "sellPacketSize" : 50,
                    "maxBuyPacketSurplus" : 4,
                    "historicalOutlook" : 2}
    meanReversionSignalGenerator.manualSetup(parameterList)
    trade1 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:00:00.000",'Record Type':"TRADE",'Price':"39",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"100",'Ask ID':"101",'Bid/Ask':"",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"1",'Seller Broker ID':"2"}
    trade2 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:02:00.000",'Record Type':"TRADE",'Price':"38",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"100",'Ask ID':"101",'Bid/Ask':"",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"1",'Seller Broker ID':"2"}
    trade3 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:02:00.000",'Record Type':"TRADE",'Price':"37",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"100",'Ask ID':"101",'Bid/Ask':"",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"1",'Seller Broker ID':"2"}
    trade4 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:02:00.000",'Record Type':"TRADE",'Price':"36",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"100",'Ask ID':"101",'Bid/Ask':"",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"1",'Seller Broker ID':"2"}
    trade5 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:02:00.000",'Record Type':"TRADE",'Price':"35",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"100",'Ask ID':"101",'Bid/Ask':"",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"1",'Seller Broker ID':"2"}
    trade6 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:02:00.000",'Record Type':"TRADE",'Price':"34",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"100",'Ask ID':"101",'Bid/Ask':"",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"1",'Seller Broker ID':"2"}

    orders = []
    orders.extend(meanReversionSignalGenerator(trade1))
    orders.extend(meanReversionSignalGenerator(trade2))
    orders.extend(meanReversionSignalGenerator(trade3))
    orders.extend(meanReversionSignalGenerator(trade4))
    orders.extend(meanReversionSignalGenerator(trade5))
    orders.extend(meanReversionSignalGenerator(trade6))
    
    assert len(orders) == 4,"length of trades is " + str(len(orders)) + " not 4"

def _testMeanReversionGeneratesOrdersBasicSell():
    print "Testing four decreasing trades generate 2 sell orders when shares in stock are sufficient, and not more"
    meanReversionSignalGenerator = MeanReversionSignalGenerator.MeanReversionSignalGenerator()
    parameterList = {"minimumTimeBeforeAction" : "10:05:00.000",
                    "buyDistanceFromMeanThreshold" : 0.001,
                    "sellDistanceFromMeanThreshold" : 0.001,       
                    "buyPacketSize" : 50,
                    "sellPacketSize" : 50,
                    "maxBuyPacketSurplus" : 1,
                    "historicalOutlook" : 2}
    meanReversionSignalGenerator.manualSetup(parameterList)
    meanReversionSignalGenerator.BHPsharesInStock = 100
    
    trade1 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:00:00.000",'Record Type':"TRADE",'Price':"31",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"100",'Ask ID':"101",'Bid/Ask':"",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"1",'Seller Broker ID':"2"}
    trade2 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:02:00.000",'Record Type':"TRADE",'Price':"32",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"100",'Ask ID':"101",'Bid/Ask':"",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"1",'Seller Broker ID':"2"}
    trade3 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:02:00.000",'Record Type':"TRADE",'Price':"33",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"100",'Ask ID':"101",'Bid/Ask':"",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"1",'Seller Broker ID':"2"}
    trade4 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:02:00.000",'Record Type':"TRADE",'Price':"34",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"100",'Ask ID':"101",'Bid/Ask':"",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"1",'Seller Broker ID':"2"}

    orders = []
    orders.extend(meanReversionSignalGenerator(trade1))
    orders.extend(meanReversionSignalGenerator(trade2))
    orders.extend(meanReversionSignalGenerator(trade3))
    
    assert len(orders) == 2,"length of trades is " + str(len(orders)) + " not 2"
    
def _testMeanReversionGeneratesOrdersBuysThenSells():
    print "Testing meanReversion will buy and register a purchase, then sell"
    meanReversionSignalGenerator = MeanReversionSignalGenerator.MeanReversionSignalGenerator()
    parameterList = {"minimumTimeBeforeAction" : "10:05:00.000",
                    "buyDistanceFromMeanThreshold" : 0.001,
                    "sellDistanceFromMeanThreshold" : 0.001,       
                    "buyPacketSize" : 50,
                    "sellPacketSize" : 50,
                    "maxBuyPacketSurplus" : 1,
                    "historicalOutlook" : 2}
    meanReversionSignalGenerator.manualSetup(parameterList)
    
    trade1 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:00:00.000",'Record Type':"TRADE",'Price':"36",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"100",'Ask ID':"101",'Bid/Ask':"",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"1",'Seller Broker ID':"2"}
    trade2 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:02:00.000",'Record Type':"TRADE",'Price':"35",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"100",'Ask ID':"101",'Bid/Ask':"",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"1",'Seller Broker ID':"2"}
    trade3 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:02:00.001",'Record Type':"TRADE",'Price':"36",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"100",'Ask ID':"101",'Bid/Ask':"",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"1",'Seller Broker ID':"2"}
    trade4 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:02:00.002",'Record Type':"TRADE",'Price':"34",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"100",'Ask ID':"101",'Bid/Ask':"",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"1",'Seller Broker ID':"2"}
    trade5 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:02:00.003",'Record Type':"TRADE",'Price':"35",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"100",'Ask ID':"101",'Bid/Ask':"",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"1",'Seller Broker ID':"2"}
    trade6 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:02:00.010",'Record Type':"TRADE",'Price':"34",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"100",'Ask ID':"101",'Bid/Ask':"",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"1",'Seller Broker ID':"2"}
    
    orders = []
    orders.extend(meanReversionSignalGenerator(trade1))
    neworders = meanReversionSignalGenerator(trade2)
    orders.extend(neworders)
    assert len(orders) == 1
    faketrade = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:02:00.005",'Record Type':"TRADE",'Price':35,'Volume':neworders[0]['Volume'],'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':neworders[0]['Bid ID'],'Ask ID':"100",'Bid/Ask':"",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':neworders[0]['Buyer Broker ID'],'Seller Broker ID':"1"}
    orders.extend(meanReversionSignalGenerator(faketrade))
    # Test signal generator realises its order was matched and it increase its stock
    assert meanReversionSignalGenerator.BHPsharesInStock == neworders[0]['Volume']
    neworders = meanReversionSignalGenerator(trade3)
    assert len(neworders) == 1
    assert neworders[0]['Record Type'] == "ENTER"
    assert neworders[0]['Bid/Ask'] == "A"
    orders.extend(neworders)
    assert len(orders) == 2
    assert int(meanReversionSignalGenerator.outstandingSellVolume) == int(neworders[0]['Volume'])
    orders.extend(meanReversionSignalGenerator(trade4))
    orders.extend(meanReversionSignalGenerator(trade5))
    #fake match up the meanReversions last sell with a buy
    neworder = neworders[0]
    faketrade = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:02:00.005",'Record Type':"TRADE",'Price':35,'Volume':neworder['Volume'],'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"100",'Ask ID':neworder['Ask ID'],'Bid/Ask':"",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"1",'Seller Broker ID':neworder['Seller Broker ID']}
    orders.extend(meanReversionSignalGenerator(faketrade))
    assert len(orders) == 2
    assert meanReversionSignalGenerator.outstandingSellVolume == 0
    orders.extend(meanReversionSignalGenerator(trade6))
    assert meanReversionSignalGenerator.outstandingBuyVolume == 50
    
    assert len(orders) == 3,"length of trades is " + str(len(orders)) + " not 3"

def _testMeanReversionOrderGenerateNoOrders():
    meanReversionSignalGenerator = MeanReversionSignalGenerator.MeanReversionSignalGenerator()
    parameterList = {"minimumTimeBeforeAction" : "10:05:00.000",
                    "buyDistanceFromMeanThreshold" : 0.001,
                    "sellDistanceFromMeanThreshold" : 0.001,       
                    "buyPacketSize" : 50,
                    "sellPacketSize" : 50,
                    "maxBuyPacketSurplus" : 1,
                    "historicalOutlook" : 2}

    meanReversionSignalGenerator.manualSetup(parameterList)
    buy1 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:00:00.000",'Record Type':"ENTER",'Price':"34.080",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"6245081189407525023",'Ask ID':"",'Bid/Ask':"B",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"140",'Seller Broker ID':""}
    buy2 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"12:00:00.000",'Record Type':"ENTER",'Price':"35.100",'Volume':"2000",'Undisclosed Volume':"0",'Value':"70200",'Qualifiers':"",'Trans ID':"0",'Bid ID':"",'Ask ID':"6245081189408853421",'Bid/Ask':"A",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"",'Seller Broker ID':"141"}
    buy3 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"13:00:00.000",'Record Type':"ENTER",'Price':"36",'Volume':"2000",'Undisclosed Volume':"0",'Value':"70200",'Qualifiers':"",'Trans ID':"0",'Bid ID':"6245081189408853422",'Ask ID':"",'Bid/Ask':"B",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"140",'Seller Broker ID':""}
    buy4 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"14:00:00.000",'Record Type':"ENTER",'Price':"33",'Volume':"2000",'Undisclosed Volume':"0",'Value':"70200",'Qualifiers':"",'Trans ID':"0",'Bid ID':"6245081189408853420",'Ask ID':"",'Bid/Ask':"B",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"140",'Seller Broker ID':""}

    print ">Testing telling mean reversion about orders does not generate trades"
    trades = []
    trades.extend(meanReversionSignalGenerator(buy1))
    trades.extend(meanReversionSignalGenerator(buy2))
    trades.extend(meanReversionSignalGenerator(buy3))
    trades.extend(meanReversionSignalGenerator(buy4))
    assert len(trades) == 0

print "Testing mean reversion signal generator"
testMeanReversionSignalGenerator()
print "Passed mean reversion tests"
