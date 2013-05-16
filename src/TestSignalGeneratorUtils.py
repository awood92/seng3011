import plugins
from plugins.SignalGeneratorUtils import _calculateAverageReturn

def testAverageReturnCalculation():
    data = [7,4]
    data_result = -0.42857142857142855
    assert data_result == _calculateAverageReturn(data)

    data = [1,2,3,4,5,6,7,8,9]
    data_result = 0.3397321428571428
    assert data_result == _calculateAverageReturn(data)
    
    data = [7,4,1,6,2,10,2,3,6,6,5,13]
    data_result = 0.8443722943722943
    assert data_result == _calculateAverageReturn(data)
    
    data = [2.5,2.45,2.35,2.2,2.5,2.45,2.35,2.2,2.1,2,1.8]
    data_result = -0.03060021842392663
    assert data_result == _calculateAverageReturn(data)
    
    

