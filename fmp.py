import sys
import argparse
from stock.indicators import  ChartsData

# FSELX
# FSPTX

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--simbol", type=str)
    
    args = parser.parse_args()
    simbol = args.simbol

    #name_of_script = sys.argv[0]
    #simbol = sys.argv[1]

    print(simbol)

    stockData = ChartsData(simbol,250)
    stockData.load()
    stockData.calcShortSMA(40)
    stockData.calcLongSMA(50)
    # Usually EMA calculates fo 12 day and 26 day period
    stockData.calcShortEMA(10)
    stockData.calcBollingerBand(20, 0.95)
    stockData.calcRSI(20)
    stockData.calcMACD(shortPeriodLength = 12, longPeriodLength = 26, signalPeriodLength = 9)
    stockData.show(50)

    i=1
if __name__ == '__main__':
    main()

