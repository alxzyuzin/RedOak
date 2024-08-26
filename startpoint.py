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
        self.shortEMA   = []
        self.gain  = []
        self.loss  = []
        self.gainEMA  = []
        self.lossEMA  = []
        self.RS = []
        self.RSI = []

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
            # Create variables for future calculation
            # Moving average
            self.shortMA.append(0.0)
            self.longMA.append(0.0)
            self.shortEMA.append(0.0)
            # RSI
            self.gain.append(0.0)
            self.loss.append(0.0)
            self.gainEMA.append(0.0)
            self.lossEMA.append(0.0)
            self.RS.append(0.0)
            self.RSI.append(0.0)
        i=0
         
    def calculateShortMA(self, periodLength):
      
        i = 0
        while i < (len(self.date) - periodLength + 1):
            priceTotal = 0
            # Sum closing prices for short term period
            for j in range(i,periodLength + i): 
                priceTotal += self.closePrice[j] 
            # Calculate average price for this period
            self.shortMA[periodLength + i - 1] = priceTotal / periodLength
            i+=1
        
    def calculateShortEMA(self, periodLength):
      
        multiplier = 2 / (periodLength + 1)
        i = 1
        while i < len(self.date):
            self.shortEMA[i] = self.closePrice[i] * multiplier + self.shortEMA[i - 1] * (1 - multiplier)
            i+=1
        i=0

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

    def calculateRSI(self, periodLength):
      
        # Calculate Gain and Loss
        for i in range(1, len(self.date)):
            change = self.openPrice[i] - self.openPrice[i-1]
            if change > 0 :
                self.gain[i] = change
            else:
                self.loss[i] = 0 - change
        
        # Calculate simple moving average for gain and loss
        for i in range(periodLength - 1, len(self.date)-1):
            # Separatly sum gains and losses for defined period
            totalGain = 0
            totalLoss =0
            for j in range(i - periodLength +2 , i + 2): 
                totalGain += self.gain[j] 
                totalLoss += self.loss[j] 
            
            self.gainEMA[i + 1] = totalGain / periodLength
            self.lossEMA[i + 1] = totalLoss / periodLength   
         

        # Recalculate moving average for gain and loss 
        # into exponential moving average and calculate RSI 
        #oldGain = 0
        #oldLoss = 0
        #newGain = 0
        #newLoss = 0

        #for i in range(periodLength, len(self.date)):
        #while i  < len(self.date):
            
        #    oldGain = newGain
        #    oldLoss = newLoss
        #    newGain = (self.gainEMA[i - 1] * (periodLength - 1) + self.gain[i]) / periodLength
        #    newLoss = (self.lossEMA[i - 1] * (periodLength - 1) + self.loss[i]) / periodLength
            
        #    self.gainEMA[i] =  oldGain
        #    self.lossEMA[i] =  oldLoss
            
            #self.gainEMA[i] =  (self.gainEMA[i - 1] * (periodLength - 1) + self.gain[i]) / periodLength
            #self.lossEMA[i] =  (self.lossEMA[i - 1] * (periodLength - 1) + self.loss[i]) / periodLength
            #self.RSI[i] = 100 - 100/(1 + self.gainEMA[i] / self.lossEMA[i])
     
        # Calculate RSI
        for i in range(periodLength, len(self.date)):
            self.RSI[i] = 100 - 100/(1 + self.gainEMA[i] / self.lossEMA[i])
        k=0


    def displayData(self, startvalue):
               
        gs_kw = dict( height_ratios=[4, 1])
        fig, (ax0, ax1) = plt.subplots(2, 1,
                                        layout='constrained', 
                                        gridspec_kw = gs_kw
                                        )
        fig.tight_layout(h_pad = 0.5, w_pad = 0) # Set figure margins size
        plt.legend(loc='upper left')

        fig.set_size_inches(18,10) 
        #fig.suptitle('Historic prices for simbol ' + self.simbol, fontsize=16)
      
        ax0.plot(self.date[startvalue:], self.closePrice[startvalue:],
                 label = "Daily prices", color='gray', linewidth = 1)
        ax0.plot(self.date[startvalue:], self.shortMA[startvalue:],
                 label = "Short SMA")
        ax0.plot(self.date[startvalue:], self.longMA[startvalue:],
                 label = "Long SMA")
        ax0.plot(self.date[startvalue:], self.shortEMA[startvalue:],
                 label = "Short EMA")
        
        ax0.legend(loc='upper left')
        ax0.set_title('Historic prices for simbol ' + self.simbol)
        ax0.grid(True)
        ax0.left = 0
        
        # format the major ticks
        #years = mdates.YearLocator()    # every year
        months = mdates.MonthLocator()  # every month
        monthsFmt = mdates.DateFormatter('%Y-%m')
        ax0.xaxis.set_major_locator(months)
        ax0.xaxis.set_major_formatter(monthsFmt)
        #
        # format the minor ticks
        days   = mdates.DayLocator(interval = 5)    # every 5 day
        daysFmt = mdates.DateFormatter('%d')
        ax0.xaxis.set_minor_locator(days)
        ax0.xaxis.set_minor_formatter(daysFmt)  # Display days numbers on x axis 

        #ax.xaxis.set_major_formatter(
        #    ConciseDateFormatter(ax.xaxis.get_major_locator()))

        ax0.tick_params(axis='x', pad=15)
        datemin = self.date[startvalue]
        datemax = max(self.date)
        ax0.set_xlim(datemin)
        
        # rotates and right aligns the x labels, and moves the bottom of the
        # axes up to make room for them
        #fig.autofmt_xdate()
 
        ax1.legend(loc='upper left')
        ax1.set_title('RSI for simbol ' + self.simbol)
        ax1.grid(True)
        
        ax1.plot(self.date[startvalue:], self.RSI[startvalue:],
                 label = "RSI", color='green', linewidth = 1)
        ax1.set_xlim(datemin)
        ax1.axhline( y = 70, color = 'r', linewidth=1)
        
        ax1.axhline( y = 30, color = 'r', linewidth=1 )
        ax1.text(self.date[startvalue + 10],75,"Overbought level", fontsize=10, color='red')
        ax1.text(self.date[startvalue + 10],20,"Oversold level", fontsize=10, color='red')
               
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
    # Usually EMA calculates fo 12 day and 26 day period
    sd.calculateShortEMA(10)

    sd.calculateRSI(14)
      

    sd.displayData(30)
    i=1
if __name__ == '__main__':
    main()
