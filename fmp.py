from stock.indicators import  ChartsData
def main():
    stockData = ChartsData("FSELX",250)
    stockData.load()
    stockData.show(0)

    i=1
if __name__ == '__main__':
    main()

