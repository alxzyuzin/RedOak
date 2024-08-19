import urllib.request;
import matplotlib.pyplot as plot
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import numpy as np

SHORT_TERM_MA_LENGTH = 20
LONG_TERM_MA_LENGTH = 50
SIMBOL = "FSELX"
UPLOADS_DIRECTORY = "uploads\\"

class StockData:
    shortTermLength = 20
    longTermLength = 50

    def __init__(self):
        self.simbol = ""

        # period1 - the beginning of interval for retriving data
        # period2 - the end of interval for retriving data
        # value of parameters nubmer of seconds from 01/01/1970

        self.urlstrHead = 'https://query1.finance.yahoo.com/v7/finance/download/'
                         # https://query1.finance.yahoo.com/v7/finance/download/
        self.urlstrTail = '?period1=1691277249&period2=1722899649&interval=1d&events=history&includeAdjustedClose=true'
                         # ?period1=1692325667&period2=1723948067&interval=1d&events=history&includeAdjustedClose=true
        
               
        self.rawData = ""

       
        #FSELX
        self.date       = []
        self.openPrice  = []
        self.highPrice  = []
        self.lowPrice   = []
        self.closePrice = []
        self.adjClose   = []
        self.volume     = [] 
        self.shortMA    = []
        self.longMA     = []

    def loadData(self,smb):  
        self.simbol = smb
        current_dateTime = datetime.now()
        fileName = UPLOADS_DIRECTORY + self.simbol + current_dateTime.strftime("%Y%m%d")+".txt"
        
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
            self.shortMA.append(0.0)
            self.longMA.append(0.0)
        i=0
         
    def calculateShortMA(self):
      
        i = 0
        while i < (len(self.date) - SHORT_TERM_MA_LENGTH + 1):
            priceTotal = 0
            # Sum closing prices for short term period
            for j in range(i,SHORT_TERM_MA_LENGTH + i): 
                priceTotal += self.closePrice[j] 
            # Calculate average price for this period
            self.shortMA[SHORT_TERM_MA_LENGTH + i -1] = priceTotal / SHORT_TERM_MA_LENGTH
            i+=1
        

    def calculateLongMA(self):
      
        i = 0
        while i < (len(self.date) - LONG_TERM_MA_LENGTH + 1):
            priceTotal = 0
            # Sum closing prices for short term period
            for j in range(i,LONG_TERM_MA_LENGTH + i): 
                priceTotal += self.closePrice[j] 
            # Calculate average price for this period
            self.longMA[LONG_TERM_MA_LENGTH + i -1] = priceTotal / LONG_TERM_MA_LENGTH
            i+=1
        k=0

    def displayData(self):
        
        #plt.plot(np.array(self.date[LONG_TERM_MA_LENGTH:]), 
        #         np.array(self.closePrice[LONG_TERM_MA_LENGTH:]),
        #         label = "Daily prices")
        #plt.plot(np.array(self.date[LONG_TERM_MA_LENGTH:]),
        #         np.array(self.shortMA[LONG_TERM_MA_LENGTH:]),
        #         label = "Short moving average")
        #plt.plot(np.array(self.date[LONG_TERM_MA_LENGTH:]),
        #         np.array(self.longMA[LONG_TERM_MA_LENGTH:]),
        #         label = "Long moveng average")
        #plt.legend()
        #plt.title(self.simbol)
        #plt.xticks(fontsize=10, color='blue', rotation=45)
        #plt.minorticks_on()
        #------------------- Test code -----------------------
        
        startvalue = LONG_TERM_MA_LENGTH
        fig, plt = plot.subplots()
        fig.text(10,10,self.simbol)
        plt.plot(self.date[startvalue:], self.closePrice[startvalue:],
                 label = "Daily prices")
        plt.plot(self.date[startvalue:], self.shortMA[startvalue:],
                 label = "Short moving average")
        plt.plot(self.date[startvalue:], self.longMA[startvalue:],
                 label = "Long moveng average")
        
        plt.legend()
        #plt.title() #.title(self.simbol)
        #plt.xticks(fontsize=10, color='blue', rotation=45)

        years = mdates.YearLocator()   # every year
        months = mdates.MonthLocator()  # every month
        days   = mdates.DayLocator()
        monthsFmt = mdates.DateFormatter('%Y-%m')
        # format the ticks
        plt.xaxis.set_major_locator(months)
        plt.xaxis.set_major_formatter(monthsFmt)
        plt.xaxis.set_minor_locator(days)

        #datemin = min(self.date)
        datemin = self.date[startvalue]
        datemax = max(self.date)
        plt.set_xlim(datemin, datemax)


        # format the coords message box
        def price(x):
            return '$%2.3f' % x
        plt.format_xdata = mdates.DateFormatter('%Y-%m-%d')
        plt.format_ydata = price
        plt.grid(True)

        # rotates and right aligns the x labels, and moves the bottom of the
        # axes up to make room for them
        fig.autofmt_xdate()

# -------------------- Test code ------------------------
        
        plot.show()
        k=1

    @property
    def Date(self):
        return  np.array(self.data)
        
    @property
    def priceAtOpen(self):
        return  np.array(self.openPrice)
        


    def getStockData(self):
        pass       


def ticksToDateTime(t):
    converted_ticks = datetime.now() - timedelta(seconds= t)
    return converted_ticks.strftime("%Y-%m-%d %H:%M:%S")

def ticksFromZeroTime():
    #d = datetime.datetime.strptime( "20170108233000", "%Y%m%d%H%M%S")
    
    d = datetime.strptime ( "20240818023000", "%Y%m%d%H%M%S")
    t0 = datetime(1970, 1, 1, 0, 0, 0)
    ticks = (d - t0).total_seconds()
    return ticks

def main():
            # 1723 937 400
 #1691277249 17 228 99 649
 #1692325667 17 239 48 067
    ts = ticksFromZeroTime()
    s1 = ticksToDateTime(1691277249) # '2024-08-17 22:51:51'
    e1 = ticksToDateTime(1722899649)
    
    s2 = ticksToDateTime(1692325667)
    e2 = ticksToDateTime(1723948067)

    sd = StockData()
    sd.loadData("FSELX")
    sd.calculateShortMA()
    sd.calculateLongMA()
    sd.displayData()
       
if __name__ == '__main__':
    main()
