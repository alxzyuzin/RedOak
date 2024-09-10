from stock.indicators import  ChartsData
def main():
    stockData = ChartsData("FSELX",250)
    stockData.load()
    stockData.calcShortSMA(40)
    stockData.calcLongSMA(50)
    # Usually EMA calculates fo 12 day and 26 day period
    stockData.calcShortEMA(10)
    stockData.calcBollingerBand(20, 0.95)
    stockData.calcRSI(20)
    stockData.show(50)

    i=1
if __name__ == '__main__':
    main()

