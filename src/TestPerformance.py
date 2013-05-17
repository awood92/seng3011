
from plugins import MomentumSignalGenerator
from plugins import MeanReversionSignalGenerator
from plugins import InitialEngine
from plugins import DummyStrategyEvaluator


import time
import trader
import csv
import sys

def benchmarkMomen(filePath):

    signalGenerator = MomentumSignalGenerator.MomentumSignalGenerator()
    parameterList = {"minimumTimeBeforeAction" : "10:05:00.000",
                    "buyDistanceFromMeanThreshold" : 0.001,
                    "sellDistanceFromMeanThreshold" : 0.001,       
                    "buyPacketSize" : 50,
                    "sellPacketSize" : 50,
                    "maxBuyPacketSurplus" : 1,
                    "historicalOutlook" : 2}
    signalGenerator.manualSetup(parameterList)

    engine = InitialEngine.InitialEngine()
    engine.setup(None)
   
    strategyEvaluator = DummyStrategyEvaluator.DummyStrategyEvaluator()

    lines = 0
    for line in open(filePath) :
        lines += 1

    sys.stdout.write("lines: %d | Time(sec): " % lines)
    stream = open(filePath, "r")
    dr = csv.DictReader(stream)

    initialTime = time.time()
    trader.run_trial(dr,signalGenerator,engine,strategyEvaluator)
    print "%.4f" % (time.time() - initialTime)

def benchmarkMeanRev(filePath):
    signalGenerator = MeanReversionSignalGenerator.MeanReversionSignalGenerator()
    parameterList = {"minimumTimeBeforeAction" : "10:05:00.000",
                    "buyDistanceFromMeanThreshold" : 0.001,
                    "sellDistanceFromMeanThreshold" : 0.001,       
                    "buyPacketSize" : 50,
                    "sellPacketSize" : 50,
                    "maxBuyPacketSurplus" : 1,
                    "historicalOutlook" : 2}
    signalGenerator.manualSetup(parameterList)

    engine = InitialEngine.InitialEngine()
    engine.setup(None)
   
    strategyEvaluator = DummyStrategyEvaluator.DummyStrategyEvaluator()

    lines = 0
    for line in open(filePath) :
        lines += 1

    sys.stdout.write("lines: %d | Time(sec): " % lines)
    stream = open(filePath, "r")
    dr = csv.DictReader(stream)

    initialTime = time.time()
    trader.run_trial(dr,signalGenerator,engine,strategyEvaluator)
    print "%.4f" % (time.time() - initialTime)

print "BENCHMARCH (Momentum)"
benchmarkMomen('../sample/10line.csv')
benchmarkMomen('../sample/100line.csv')
benchmarkMomen('../sample/1000line.csv')
benchmarkMomen('../sample/10000line.csv')
benchmarkMomen('../sample/50000line.csv')
print "BENCHMARCH (MeanReversion)"
benchmarkMeanRev('../sample/10line.csv')
benchmarkMeanRev('../sample/100line.csv')
benchmarkMeanRev('../sample/1000line.csv')
benchmarkMeanRev('../sample/10000line.csv')
benchmarkMeanRev('../sample/50000line.csv')
