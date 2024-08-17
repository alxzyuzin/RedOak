import urllib.request;
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

SHORT_TERM_MA_LENGTH = 20
LONF_TERM_MA_LENGTH = 50
SIMBOL = "FSELX"


class StockData:
    shortTermLength = 20
    longTermLength = 50

    def __init__(self):
        self.simbol = ""
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

    def loadData(self,smb):  
        self.simbol = smb
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


    def displayData(self):
        plt.plot(np.array(self.date), np.array(self.openPrice))
        plt.show()

    @property
    def Date(self):
        return  np.array(self.data)
        
    @property
    def priceAtOpen(self):
        return  np.array(self.openPrice)
        


    def getStockData(self):
        pass       




def main():
    sd = StockData()
    sd.loadData("FSELX")
    sd.displayData()
       
if __name__ == '__main__':
    main()
