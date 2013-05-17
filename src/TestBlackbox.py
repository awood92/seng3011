import sys
import optparse
import csv
import signal
import os

import yapsy.PluginManager
import plugins

from plugins import DummySignalGenerator
from plugins import InitialEngine
from plugins import DummyStrategyEvaluator
import trader

def testCorrectTrades():
    dummySignalGenerator = DummySignalGenerator.DummySignalGenerator()
    initialEngine = InitialEngine.InitialEngine()
    initialEngine.setup(None)
    dummyStrategyEvalutator = DummyStrategyEvaluator.DummyStrategyEvaluator()
    #put some buys in
    buy1 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:00:00.000",'Record Type':"ENTER",'Price':"35.080",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"6245081189407525022",'Ask ID':"",'Bid/Ask':"B",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"140",'Seller Broker ID':""}
    buy2 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:01:00.000",'Record Type':"ENTER",'Price':"35.100",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"6245081189407525023",'Ask ID':"",'Bid/Ask':"B",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"150",'Seller Broker ID':""}
    buy3 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:02:00.000",'Record Type':"ENTER",'Price':"35.090",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"6245081189407525024",'Ask ID':"",'Bid/Ask':"B",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"160",'Seller Broker ID':""}
    buy4 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"12:04:30.000",'Record Type':"ENTER",'Price':"30.080",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"6245081189407525025",'Ask ID':"",'Bid/Ask':"B",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"160",'Seller Broker ID':""}
    #put some sells in
    sell1 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"12:01:00.000",'Record Type':"ENTER",'Price':"36.100",'Volume':"1000",'Undisclosed Volume':"0",'Value':"70200",'Qualifiers':"",'Trans ID':"0",'Bid ID':"",'Ask ID':"6245081189408853521",'Bid/Ask':"A",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"",'Seller Broker ID':"170"}
    sell2 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"12:02:00.000",'Record Type':"ENTER",'Price':"35.100",'Volume':"1000",'Undisclosed Volume':"0",'Value':"70200",'Qualifiers':"",'Trans ID':"0",'Bid ID':"",'Ask ID':"6245081189408853522",'Bid/Ask':"A",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"",'Seller Broker ID':"180"}
    sell3 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"12:03:00.000",'Record Type':"ENTER",'Price':"35.080",'Volume':"1000",'Undisclosed Volume':"0",'Value':"70200",'Qualifiers':"",'Trans ID':"0",'Bid ID':"",'Ask ID':"6245081189408853523",'Bid/Ask':"A",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"",'Seller Broker ID':"180"}
    sell4 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"12:04:00.000",'Record Type':"ENTER",'Price':"35.080",'Volume':"1000",'Undisclosed Volume':"0",'Value':"70200",'Qualifiers':"",'Trans ID':"0",'Bid ID':"",'Ask ID':"6245081189408853524",'Bid/Ask':"A",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"",'Seller Broker ID':"180"}
    sell5 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"12:05:00.000",'Record Type':"ENTER",'Price':"30.080",'Volume':"1000",'Undisclosed Volume':"0",'Value':"70200",'Qualifiers':"",'Trans ID':"0",'Bid ID':"",'Ask ID':"6245081189408853525",'Bid/Ask':"A",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"",'Seller Broker ID':"180"}
    #put some amends in
    amend1 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:03:00.000",'Record Type':"AMEND",'Price':"40.080",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"6245081189407525022",'Ask ID':"",'Bid/Ask':"B",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"140",'Seller Broker ID':""}
    #put some deletes in
    delete1 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"12:04:45.000",'Record Type':"DELETE",'Price':"40.080",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"6245081189407525025",'Ask ID':"",'Bid/Ask':"B",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"140",'Seller Broker ID':""}

    dr = [buy1,buy2,buy3,amend1,sell1,sell2,sell3,sell4,buy4,delete1,sell5]
    trades = trader.run_trial(dr, dummySignalGenerator,initialEngine, dummyStrategyEvalutator)
    
    assert trades[0]['Bid ID'] == "6245081189407525022"
    assert trades[0]['Ask ID'] == "6245081189408853521"
    assert trades[1]['Bid ID'] == "6245081189407525023"
    assert trades[1]['Ask ID'] == "6245081189408853522"
    assert trades[2]['Ask ID'] == "6245081189408853523"
    assert trades[2]['Bid ID'] == "6245081189407525024"
    assert len (trades) == 3
def testVolume():
    dummySignalGenerator = DummySignalGenerator.DummySignalGenerator()
    initialEngine = InitialEngine.InitialEngine()
    initialEngine.setup(None)
    dummyStrategyEvalutator = DummyStrategyEvaluator.DummyStrategyEvaluator()
    #put some buys in
    buy1 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:00:00.000",'Record Type':"ENTER",'Price':"35.080",'Volume':"500",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"6245081189407525022",'Ask ID':"",'Bid/Ask':"B",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"140",'Seller Broker ID':""}
    buy2 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:01:00.000",'Record Type':"ENTER",'Price':"35.100",'Volume':"100",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"6245081189407525023",'Ask ID':"",'Bid/Ask':"B",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"150",'Seller Broker ID':""}
    buy3 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:02:00.000",'Record Type':"ENTER",'Price':"35.090",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"6245081189407525024",'Ask ID':"",'Bid/Ask':"B",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"160",'Seller Broker ID':""}
    buy4 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"12:04:30.000",'Record Type':"ENTER",'Price':"30.080",'Volume':"50",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"6245081189407525025",'Ask ID':"",'Bid/Ask':"B",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"160",'Seller Broker ID':""}
    buy5 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"12:10:30.000",'Record Type':"ENTER",'Price':"36.100",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"6245081189407525026",'Ask ID':"",'Bid/Ask':"B",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"160",'Seller Broker ID':""}
    #put some sells in
    sell1 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"12:01:00.000",'Record Type':"ENTER",'Price':"36.100",'Volume':"2000",'Undisclosed Volume':"0",'Value':"70200",'Qualifiers':"",'Trans ID':"0",'Bid ID':"",'Ask ID':"6245081189408853521",'Bid/Ask':"A",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"",'Seller Broker ID':"170"}
    sell2 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"12:02:00.000",'Record Type':"ENTER",'Price':"35.100",'Volume':"100",'Undisclosed Volume':"0",'Value':"70200",'Qualifiers':"",'Trans ID':"0",'Bid ID':"",'Ask ID':"6245081189408853522",'Bid/Ask':"A",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"",'Seller Broker ID':"180"}
    sell3 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"12:03:00.000",'Record Type':"ENTER",'Price':"35.080",'Volume':"1000",'Undisclosed Volume':"0",'Value':"70200",'Qualifiers':"",'Trans ID':"0",'Bid ID':"",'Ask ID':"6245081189408853523",'Bid/Ask':"A",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"",'Seller Broker ID':"180"}
    sell4 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"12:04:00.000",'Record Type':"ENTER",'Price':"35.080",'Volume':"1000",'Undisclosed Volume':"0",'Value':"70200",'Qualifiers':"",'Trans ID':"0",'Bid ID':"",'Ask ID':"6245081189408853524",'Bid/Ask':"A",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"",'Seller Broker ID':"180"}
    sell5 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"12:05:00.000",'Record Type':"ENTER",'Price':"30.080",'Volume':"1000",'Undisclosed Volume':"0",'Value':"70200",'Qualifiers':"",'Trans ID':"0",'Bid ID':"",'Ask ID':"6245081189408853525",'Bid/Ask':"A",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"",'Seller Broker ID':"180"}
    #put some amends in
    amend1 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"11:03:00.000",'Record Type':"AMEND",'Price':"40.080",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"6245081189407525022",'Ask ID':"",'Bid/Ask':"B",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"140",'Seller Broker ID':""}
    #put some deletes in
    delete1 = {'Instrument':"BHP",'Date':"2013-03-15",'Time':"12:04:45.000",'Record Type':"DELETE",'Price':"40.080",'Volume':"1000",'Undisclosed Volume':"0",'Value':"35080",'Qualifiers':"",'Trans ID':"0",'Bid ID':"6245081189407525025",'Ask ID':"",'Bid/Ask':"B",'Entry Time':"",'Old Price':"",'Old Volume':"",'Buyer Broker ID':"140",'Seller Broker ID':""}

    dr = [buy1,buy2,buy3,amend1,sell1,sell2,sell3,sell4,buy4,delete1,buy5,sell5]
    trades = trader.run_trial(dr, dummySignalGenerator,initialEngine, dummyStrategyEvalutator)
    
    assert len (trades) == 4
    assert trades[0]['Volume'] == "1000"
    assert trades[1]['Volume'] == "100"
    assert trades[2]['Volume'] == "1000"
    assert trades[3]['Volume'] == "1000"
    
    
testCorrectTrades()
testVolume()