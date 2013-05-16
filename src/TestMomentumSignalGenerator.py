import sys
import optparse
import csv
import signal
import os

import yapsy.PluginManager
import plugins

from plugins import MomentumSignalGenerator

def testMomentumSignalGenerator():  
    
    _testMomentumOrderGenerateNoOrders()
    _testMomentumGeneratesNoOrdersWhenBelowThreshold()
    _testMomentumGeneratesOrdersBasicOne()
    _testMomentumGeneratesOrdersBasicTwo()
    _testMomentumGeneratesOrdersBasicThree()
    _testMomentumGeneratesOrdersBasicFour()
    _testMomentumGeneratesOrdersBasicSell()
    _testMomentumGeneratesOrdersBuysThenSells()

def _testMomentumGeneratesNoOrdersWhenBelowThreshold():
    momentumSignalGenerator = MomentumSignalGenerator.MomentumSignalGenerator()
    parameterList = {"minimumTimeBeforeAction" : "10:05:00.000",
                    "buyDistanceFromMeanThreshold" : 0.001,
                    "sellDistanceFromMeanThreshold" : 0.001,       
                    "buyPacketSize" : 50,
                    "sellPacketSize" : 50,
                    "maxBuyPacketSurplus" : 1,
                    "historicalOutlook" : 2}
    momentumSignalGenerator.manualSetup(parameterList)
    trade1 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:00:00.000",'Record Type':"TRADE",'Price':"34",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"100",'Ask ID':"101",'Bid/Ask':"",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"1",'Seller Broker ID':"2"}
    trade2 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:02:00.000",'Record Type':"TRADE",'Price':"34.01",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"100",'Ask ID':"101",'Bid/Ask':"",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"1",'Seller Broker ID':"2"}
    trade3 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:03:00.000",'Record Type':"TRADE",'Price':"34.02",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"100",'Ask ID':"101",'Bid/Ask':"",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"1",'Seller Broker ID':"2"}
    trade4 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:04:00.000",'Record Type':"TRADE",'Price':"34.03",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"100",'Ask ID':"101",'Bid/Ask':"",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"1",'Seller Broker ID':"2"}
    
    trades = []
    trades.extend(momentumSignalGenerator(trade1))
    trades.extend(momentumSignalGenerator(trade2))
    trades.extend(momentumSignalGenerator(trade3))
    trades.extend(momentumSignalGenerator(trade4))
    
    assert len(trades) == 0

def _testMomentumGeneratesOrdersBasicOne():
    print "Testing two increasing trades generate a new order from the signal generator"
    momentumSignalGenerator = MomentumSignalGenerator.MomentumSignalGenerator()
    parameterList = {"minimumTimeBeforeAction" : "10:05:00.000",
                    "buyDistanceFromMeanThreshold" : 0.001,
                    "sellDistanceFromMeanThreshold" : 0.001,       
                    "buyPacketSize" : 50,
                    "sellPacketSize" : 50,
                    "maxBuyPacketSurplus" : 1,
                    "historicalOutlook" : 2}
    momentumSignalGenerator.manualSetup(parameterList)
    trade1 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:00:00.000",'Record Type':"TRADE",'Price':"34",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"100",'Ask ID':"101",'Bid/Ask':"",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"1",'Seller Broker ID':"2"}
    trade2 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:02:00.000",'Record Type':"TRADE",'Price':"34.1",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"100",'Ask ID':"101",'Bid/Ask':"",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"1",'Seller Broker ID':"2"}
        
    trades = []
    trades.extend(momentumSignalGenerator(trade1))
    trades.extend(momentumSignalGenerator(trade2))
    
    assert len(trades) == 1,"length of trades is " + str(len(trades)) + " not 1"

def _testMomentumGeneratesOrdersBasicTwo():
    print "Testing two increasing trades generate a new order from the signal generator close to threshold"
    momentumSignalGenerator = MomentumSignalGenerator.MomentumSignalGenerator()
    parameterList = {"minimumTimeBeforeAction" : "10:05:00.000",
                    "buyDistanceFromMeanThreshold" : 0.002,
                    "sellDistanceFromMeanThreshold" : 0.002,       
                    "buyPacketSize" : 50,
                    "sellPacketSize" : 50,
                    "maxBuyPacketSurplus" : 1,
                    "historicalOutlook" : 2}
    momentumSignalGenerator.manualSetup(parameterList)
    trade1 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:00:00.000",'Record Type':"TRADE",'Price':"34",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"100",'Ask ID':"101",'Bid/Ask':"",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"1",'Seller Broker ID':"2"}
    trade2 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:02:00.000",'Record Type':"TRADE",'Price':"34.1",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"100",'Ask ID':"101",'Bid/Ask':"",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"1",'Seller Broker ID':"2"}
        
    trades = []
    trades.extend(momentumSignalGenerator(trade1))
    trades.extend(momentumSignalGenerator(trade2))
    
    assert len(trades) == 1,"length of trades is " + str(len(trades)) + " not 1"
    
def _testMomentumGeneratesOrdersBasicThree():
    print "Testing two increasing trades generate a no orders when below threshold"
    momentumSignalGenerator = MomentumSignalGenerator.MomentumSignalGenerator()
    parameterList = {"minimumTimeBeforeAction" : "10:05:00.000",
                    "buyDistanceFromMeanThreshold" : 0.003,
                    "sellDistanceFromMeanThreshold" : 0.003,       
                    "buyPacketSize" : 50,
                    "sellPacketSize" : 50,
                    "maxBuyPacketSurplus" : 1,
                    "historicalOutlook" : 2}
    momentumSignalGenerator.manualSetup(parameterList)
    trade1 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:00:00.000",'Record Type':"TRADE",'Price':"34",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"100",'Ask ID':"101",'Bid/Ask':"",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"1",'Seller Broker ID':"2"}
    trade2 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:02:00.000",'Record Type':"TRADE",'Price':"34.1",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"100",'Ask ID':"101",'Bid/Ask':"",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"1",'Seller Broker ID':"2"}
        
    orders = []
    orders.extend(momentumSignalGenerator(trade1))
    orders.extend(momentumSignalGenerator(trade2))
    
    assert len(orders) == 0,"length of trades is " + str(len(orders)) + " not 0"

def _testMomentumGeneratesOrdersBasicFour():
    print "Testing can buy more when buy packet surplus high enough"
    momentumSignalGenerator = MomentumSignalGenerator.MomentumSignalGenerator()
    parameterList = {"minimumTimeBeforeAction" : "10:05:00.000",
                    "buyDistanceFromMeanThreshold" : 0.001,
                    "sellDistanceFromMeanThreshold" : 0.001,       
                    "buyPacketSize" : 50,
                    "sellPacketSize" : 50,
                    "maxBuyPacketSurplus" : 4,
                    "historicalOutlook" : 2}
    momentumSignalGenerator.manualSetup(parameterList)
    trade1 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:00:00.000",'Record Type':"TRADE",'Price':"34",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"100",'Ask ID':"101",'Bid/Ask':"",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"1",'Seller Broker ID':"2"}
    trade2 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:02:00.000",'Record Type':"TRADE",'Price':"35",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"100",'Ask ID':"101",'Bid/Ask':"",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"1",'Seller Broker ID':"2"}
    trade3 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:02:00.000",'Record Type':"TRADE",'Price':"36",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"100",'Ask ID':"101",'Bid/Ask':"",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"1",'Seller Broker ID':"2"}
    trade4 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:02:00.000",'Record Type':"TRADE",'Price':"37",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"100",'Ask ID':"101",'Bid/Ask':"",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"1",'Seller Broker ID':"2"}
    trade5 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:02:00.000",'Record Type':"TRADE",'Price':"38",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"100",'Ask ID':"101",'Bid/Ask':"",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"1",'Seller Broker ID':"2"}
    trade6 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:02:00.000",'Record Type':"TRADE",'Price':"39",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"100",'Ask ID':"101",'Bid/Ask':"",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"1",'Seller Broker ID':"2"}

    orders = []
    orders.extend(momentumSignalGenerator(trade1))
    orders.extend(momentumSignalGenerator(trade2))
    orders.extend(momentumSignalGenerator(trade3))
    orders.extend(momentumSignalGenerator(trade4))
    orders.extend(momentumSignalGenerator(trade5))
    orders.extend(momentumSignalGenerator(trade6))
    
    assert len(orders) == 4,"length of trades is " + str(len(orders)) + " not 4"

def _testMomentumGeneratesOrdersBasicSell():
    print "Testing four decreasing trades generate 2 sell orders when shares in stock are sufficient, and not more"
    momentumSignalGenerator = MomentumSignalGenerator.MomentumSignalGenerator()
    parameterList = {"minimumTimeBeforeAction" : "10:05:00.000",
                    "buyDistanceFromMeanThreshold" : 0.001,
                    "sellDistanceFromMeanThreshold" : 0.001,       
                    "buyPacketSize" : 50,
                    "sellPacketSize" : 50,
                    "maxBuyPacketSurplus" : 1,
                    "historicalOutlook" : 2}
    momentumSignalGenerator.manualSetup(parameterList)
    momentumSignalGenerator.BHPsharesInStock = 100
    
    trade1 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:00:00.000",'Record Type':"TRADE",'Price':"34",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"100",'Ask ID':"101",'Bid/Ask':"",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"1",'Seller Broker ID':"2"}
    trade2 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:02:00.000",'Record Type':"TRADE",'Price':"33",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"100",'Ask ID':"101",'Bid/Ask':"",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"1",'Seller Broker ID':"2"}
    trade3 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:02:00.000",'Record Type':"TRADE",'Price':"32",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"100",'Ask ID':"101",'Bid/Ask':"",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"1",'Seller Broker ID':"2"}
    trade4 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:02:00.000",'Record Type':"TRADE",'Price':"31",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"100",'Ask ID':"101",'Bid/Ask':"",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"1",'Seller Broker ID':"2"}

    orders = []
    orders.extend(momentumSignalGenerator(trade1))
    orders.extend(momentumSignalGenerator(trade2))
    orders.extend(momentumSignalGenerator(trade3))
    
    assert len(orders) == 2,"length of trades is " + str(len(orders)) + " not 2"
    
def _testMomentumGeneratesOrdersBuysThenSells():
    print "Testing momentum will buy and register a purchase, then sell"
    momentumSignalGenerator = MomentumSignalGenerator.MomentumSignalGenerator()
    parameterList = {"minimumTimeBeforeAction" : "10:05:00.000",
                    "buyDistanceFromMeanThreshold" : 0.001,
                    "sellDistanceFromMeanThreshold" : 0.001,       
                    "buyPacketSize" : 50,
                    "sellPacketSize" : 50,
                    "maxBuyPacketSurplus" : 1,
                    "historicalOutlook" : 2}
    momentumSignalGenerator.manualSetup(parameterList)
    
    trade1 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:00:00.000",'Record Type':"TRADE",'Price':"34",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"100",'Ask ID':"101",'Bid/Ask':"",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"1",'Seller Broker ID':"2"}
    trade2 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:02:00.000",'Record Type':"TRADE",'Price':"35",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"100",'Ask ID':"101",'Bid/Ask':"",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"1",'Seller Broker ID':"2"}
    trade3 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:02:00.001",'Record Type':"TRADE",'Price':"34",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"100",'Ask ID':"101",'Bid/Ask':"",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"1",'Seller Broker ID':"2"}
    trade4 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:02:00.002",'Record Type':"TRADE",'Price':"31",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"100",'Ask ID':"101",'Bid/Ask':"",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"1",'Seller Broker ID':"2"}
    trade5 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:02:00.003",'Record Type':"TRADE",'Price':"35",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"100",'Ask ID':"101",'Bid/Ask':"",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"1",'Seller Broker ID':"2"}
    trade6 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:02:00.010",'Record Type':"TRADE",'Price':"36",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"100",'Ask ID':"101",'Bid/Ask':"",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"1",'Seller Broker ID':"2"}
    
    orders = []
    orders.extend(momentumSignalGenerator(trade1))
    neworders = momentumSignalGenerator(trade2)
    orders.extend(neworders)
    assert len(orders) == 1
    faketrade = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:02:00.005",'Record Type':"TRADE",'Price':35,'Volume':neworders[0]['Volume'],'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':neworders[0]['Bid ID'],'Ask ID':"100",'Bid/Ask':"",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':neworders[0]['Buyer Broker ID'],'Seller Broker ID':"1"}
    orders.extend(momentumSignalGenerator(faketrade))
    # Test signal generator realises its order was matched and it increase its stock
    assert momentumSignalGenerator.BHPsharesInStock == neworders[0]['Volume']
    neworders = momentumSignalGenerator(trade3)
    assert len(neworders) == 1
    assert neworders[0]['Record Type'] == "ENTER"
    assert neworders[0]['Bid/Ask'] == "A"
    orders.extend(neworders)
    assert len(orders) == 2
    assert int(momentumSignalGenerator.outstandingSellVolume) == int(neworders[0]['Volume'])
    orders.extend(momentumSignalGenerator(trade4))
    orders.extend(momentumSignalGenerator(trade5))
    #fake match up the momentums last sell with a buy
    neworder = neworders[0]
    faketrade = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:02:00.005",'Record Type':"TRADE",'Price':35,'Volume':neworder['Volume'],'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"100",'Ask ID':neworder['Ask ID'],'Bid/Ask':"",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"1",'Seller Broker ID':neworder['Seller Broker ID']}
    orders.extend(momentumSignalGenerator(faketrade))
    assert len(orders) == 2
    assert momentumSignalGenerator.outstandingSellVolume == 0
    orders.extend(momentumSignalGenerator(trade6))
    
    assert len(orders) == 3,"length of trades is " + str(len(orders)) + " not 3"
    
def _testMomentumOrderGenerateNoOrders():
    momentumSignalGenerator = MomentumSignalGenerator.MomentumSignalGenerator()
    parameterList = {"minimumTimeBeforeAction" : "10:05:00.000",
                    "buyDistanceFromMeanThreshold" : 0.001,
                    "sellDistanceFromMeanThreshold" : 0.001,       
                    "buyPacketSize" : 50,
                    "sellPacketSize" : 50,
                    "maxBuyPacketSurplus" : 1,
                    "historicalOutlook" : 2}

    momentumSignalGenerator.manualSetup(parameterList)
    buy1 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:00:00.000",'Record Type':"ENTER",'Price':"34.080",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"6245081189407525023",'Ask ID':"",'Bid/Ask':"B",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"140",'Seller Broker ID':""}
    buy2 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"12:00:00.000",'Record Type':"ENTER",'Price':"35.100",'Volume':"2000",'Undisclosed Volume':"0",'Value':"70200",'Qualifiers':"",'Trans ID':"0",'Bid ID':"",'Ask ID':"6245081189408853421",'Bid/Ask':"A",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"",'Seller Broker ID':"141"}
    buy3 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"13:00:00.000",'Record Type':"ENTER",'Price':"36",'Volume':"2000",'Undisclosed Volume':"0",'Value':"70200",'Qualifiers':"",'Trans ID':"0",'Bid ID':"6245081189408853422",'Ask ID':"",'Bid/Ask':"B",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"140",'Seller Broker ID':""}
    buy4 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"14:00:00.000",'Record Type':"ENTER",'Price':"33",'Volume':"2000",'Undisclosed Volume':"0",'Value':"70200",'Qualifiers':"",'Trans ID':"0",'Bid ID':"6245081189408853420",'Ask ID':"",'Bid/Ask':"B",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"140",'Seller Broker ID':""}

    print ">Testing telling momentum about orders does not generate trades"
    trades = []
    trades.extend(momentumSignalGenerator(buy1))
    trades.extend(momentumSignalGenerator(buy2))
    trades.extend(momentumSignalGenerator(buy3))
    trades.extend(momentumSignalGenerator(buy4))
    assert len(trades) == 0

print "Testing momentum signal generator"
testMomentumSignalGenerator()
print "Passed momentum tests"
