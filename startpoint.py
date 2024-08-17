import urllib.request;
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

#import pandas as pd

SHORT_TERM_MA_LENGTH = 20
LONF_TERM_MA_LENGTH = 50
SIMBOL = "FSELX"


class StockData:
    shortTermLength = 20
    longTermLength = 50

    def __init__(self,smb):
        self.simbol = smb
        self.urlstrHead = 'https://query1.finance.yahoo.com/v7/finance/download/'
        self.urlstrTail = '?period1=1691277249&period2=1722899649&interval=1d&events=history&includeAdjustedClose=true'
        self.rawData = ""

        self.date = []
        self.openPrice = []
        self.highPrice = []
        self.lowPrice = []
        self.closePrice = []
        self.adjClose = []
        self.volume = [] 

    def loadData(self):  

        current_dateTime = datetime.now()
        fileName = self.simbol + current_dateTime.strftime("%Y%m%d")+".txt"
        
        try:
            data_file = open(fileName, "r")
            self.rawData = data_file.read()
            data_file.close()
        except:
            urlstr = self.urlstrHead + self.simbol + self.urlstrTail
            data_file = open(fileName, "w")
            self.rawData = urllib.request.urlopen(urlstr).read().decode()
            data_file.write(self.rawData)
            data_file.flush()
            data_file.close()
        
        datalines = self.rawData.split("\n")

        for dataline in datalines[1:]:
            lineData = dataline.split(',')

            self.date.append(datetime.strptime(lineData[0], '%Y-%m-%d').date())
            self.openPrice.append(float(lineData[1]))
            self.highPrice.append(float(lineData[2]))
            self.lowPrice.append(float(lineData[3]))
            self.closePrice.append(float(lineData[4]))
            self.adjClose.append(float(lineData[5]))
            self.volume.append(float(lineData[6]))

        @property
        def Date(self):
            return  np.array(self.data)
        
        @property
        def priceAtOpen(self):
            return  np.array(self.openPrice)
        


    def getStockData(self):
        pass       
# Download price data

def loadData(simbol):
    urlstr = 'https://query1.finance.yahoo.com/v7/finance/download/FSELX?period1=1691277249&period2=1722899649&interval=1d&events=history&includeAdjustedClose=true'
    # Save data from internet for a future use
    #text_file = open(r"C:\\Users\\alxzy\Documents\\PROJECTS\\RedOak\\shareprices.txt", "w")
    #pricedata = urllib.request.urlopen(urlstr).read().decode()
    #text_file.write(pricedata)
    #text_file.close()

    text_file = open(r"C:\\Users\\alxzy\Documents\\PROJECTS\\RedOak\\shareprices.txt", "r")
    rawData = text_file.read().split('\n')
    text_file.close()

    #rawData = urllib.request.urlopen(urlstr).read().decode().split('\n')

    # Parce data into list of dictionaries
    dataCollection = []
    for dataString in rawData[1:]:
        lineData = dataString.split(',')
        dataRow = {}
        dataRow["Date"] = lineData[0]
        dataRow["Open"] = lineData[1]
        dataRow["High"] = lineData[2]
        dataRow["Low"] = lineData[3]
        dataRow["Close"] = lineData[4]
        dataRow["AdjClose"] = lineData[5]
        dataRow["Volume"] = lineData[6] 
   
        dataCollection.append(dataRow)

    return dataCollection

def displayPlots(dataCollection):
    # Display open prices
    #Create list of dates and prices
    dates = []
    prices = []
    for row in dataCollection:
        date_object = datetime.strptime(row["Date"], '%Y-%m-%d').date()
        dates.append(date_object)
        prices.append(float(row["Close"]))

    # Display prices against dates
    # define data values
    x = np.array(dates)   # X-axis points
    y = np.array(prices)  # Y-axis points

    plt.plot(x, y)
    plt.show()



def main():
    sd = StockData("FSELX")
    sd.loadData()
    plt.plot(np.array(sd.date), np.array(sd.openPrice))
    plt.show()

    
    #dc = loadData("FSELX")
    #displayPlots(dc)
    
if __name__ == '__main__':
    main()


end = 'true'