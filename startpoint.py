import urllib.request;
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import ConciseDateFormatter
from datetime import datetime, timedelta
import numpy as np

UPLOADS_DIRECTORY = "uploads\\"

class StockDataQuery:
    def __init__(self, simbol):
          
        self.__url = 'https://query1.finance.yahoo.com/v7/finance/download/'
        self.__periodLastDate = datetime.now()
        self.__simbol = simbol
       
        self.periodEnd = int((datetime.now() - datetime(1970, 1, 1, 0, 0, 0)).total_seconds()) # Number of seconds from start of epoch Jan 1, 1970 00H:00M:00S
        self.periodStart = self.periodEnd - 31622400 # 31622400 sec. == 366 days == 1 year
        self.interval = "1d"
        self.events = 'history'
        self.includeAjustedClose = True
    
    @property
    def simbol(self):
        return self.__simbol

   
    @property
    def periodLastDate(self):
        return self.__periodLastDate

    @property
    def url(self):
        # example of query url
        # https://query1.finance.yahoo.com/v7/finance/download/FSELX?period1=1691277249&period2=1722899649&interval=1d&events=history&includeAdjustedClose=true'
        # period1 - the beginning of interval for retriving data
        # period2 - the end of interval for retriving data
        # value of parameters nubmer of seconds from 01/01/1970
        qurl = self.__url + self.simbol
        qurl +="?period1=" + str(self.periodStart)
        qurl +="&period2=" + str(self.periodEnd)
        qurl +="&interval=" + self.interval
        qurl +="&events=" + self.events
        qurl +="&includeAdjustedClose=" + str(self.includeAjustedClose).lower()
        return  qurl
    
    @url.setter
    def url(self, value):
        self.__url = value

class StockData:
    shortTermLength = 20
    longTermLength = 50

    def __init__(self):
        self.simbol = ""
        #self.urlstrHead = 'https://query1.finance.yahoo.com/v7/finance/download/'
                         # https://query1.finance.yahoo.com/v7/finance/download/
        #self.urlstrTail = '?period1=1691277249&period2=1722899649&interval=1d&events=history&includeAdjustedClose=true'
                         # ?period1=1692325667&period2=1723948067&interval=1d&events=history&includeAdjustedClose=true
               
        self.rawData = ""
        
        self.date       = []
        self.openPrice  = []
        self.highPrice  = []
        self.lowPrice   = []
        self.closePrice = []
        self.adjClose   = []
        self.volume     = [] 
        self.shortMA    = []
        self.longMA     = []

    def loadData(self,dataquery:StockDataQuery):  
        self.simbol = dataquery.simbol
        #current_dateTime = datetime.now()
        fileName = UPLOADS_DIRECTORY + self.simbol + dataquery.periodLastDate.strftime("%Y%m%d")+".txt"
        
        try:
            data_file = open(fileName, "r")
            self.rawData = data_file.read()
            data_file.close()
        except:
            #urlstr = self.urlstrHead + self.simbol + self.urlstrTail
            data_file = open(fileName, "w")
            self.rawData = urllib.request.urlopen(dataquery.url).read().decode()
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
            self.shortMA.append(0.0)
            self.longMA.append(0.0)
        i=0
         
    def calculateShortMA(self, periodLength):
      
        i = 0
        while i < (len(self.date) - periodLength + 1):
            priceTotal = 0
            # Sum closing prices for short term period
            for j in range(i,periodLength + i): 
                priceTotal += self.closePrice[j] 
            # Calculate average price for this period
            self.shortMA[periodLength + i -1] = priceTotal / periodLength
            i+=1
        
    #def calculateShortMA(self):
      
    #    i = 0
    #    while i < (len(self.date) - SHORT_TERM_MA_LENGTH + 1):
    #        priceTotal = 0
    #        # Sum closing prices for short term period
    #        for j in range(i,SHORT_TERM_MA_LENGTH + i): 
    #            priceTotal += self.closePrice[j] 
    #        # Calculate average price for this period
    #        self.shortMA[SHORT_TERM_MA_LENGTH + i -1] = priceTotal / SHORT_TERM_MA_LENGTH
    #        i+=1

    def calculateLongMA(self, periodLength):
      
        i = 0
        while i < (len(self.date) - periodLength + 1):
            priceTotal = 0
            # Sum closing prices for short term period
            for j in range(i,periodLength + i): 
                priceTotal += self.closePrice[j] 
            # Calculate average price for this period
            self.longMA[periodLength + i -1] = priceTotal / periodLength
            i+=1
        k=0

    def displayData(self, startvalue):
               
        
        fig, ax = plt.subplots()
        plt.legend(loc='upper left')

        fig.set_size_inches(18,10) 
        #fig.suptitle('Historic prices for simbol ' + self.simbol, fontsize=16)
      
        ax.plot(self.date[startvalue:], self.closePrice[startvalue:],
                 label = "Daily prices", color='gray', linewidth = 1)
        ax.plot(self.date[startvalue:], self.shortMA[startvalue:],
                 label = "Short moving average")
        ax.plot(self.date[startvalue:], self.longMA[startvalue:],
                 label = "Long moving average")
        
        ax.legend(loc='upper left')
        ax.set_title('Historic prices for simbol ' + self.simbol)
        ax.grid(True)
        
        # format the major ticks
        #years = mdates.YearLocator()    # every year
        months = mdates.MonthLocator()  # every month
        monthsFmt = mdates.DateFormatter('%Y-%m')
        ax.xaxis.set_major_locator(months)
        ax.xaxis.set_major_formatter(monthsFmt)
        #
        # format the minor ticks
        days   = mdates.DayLocator(interval = 5)    # every 5 day
        daysFmt = mdates.DateFormatter('%d')
        ax.xaxis.set_minor_locator(days)
        ax.xaxis.set_minor_formatter(daysFmt)  # Display days numbers on x axis 

        #ax.xaxis.set_major_formatter(
        #    ConciseDateFormatter(ax.xaxis.get_major_locator()))

        ax.tick_params(axis='x', pad=15)
        datemin = self.date[startvalue]
        datemax = max(self.date)
        ax.set_xlim(datemin)
        
        # rotates and right aligns the x labels, and moves the bottom of the
        # axes up to make room for them
        fig.autofmt_xdate()
 
        plt.show()
        k=1

    @property
    def Date(self):
        return  np.array(self.data)
        
    @property
    def priceAtOpen(self):
        return  np.array(self.openPrice)
 
    def getStockData(self):
        pass       



def main():
# FSELX
# FSPTX
    stockDataQuery = StockDataQuery("FSELX")
    url = stockDataQuery.url
    
    sd = StockData()
    sd.loadData(stockDataQuery)
    sd.calculateShortMA(10)
    sd.calculateLongMA(30)
    sd.displayData(30)
    i=1
if __name__ == '__main__':
    main()
