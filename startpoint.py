import urllib.request;
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import ConciseDateFormatter
from datetime import datetime, timedelta
import numpy as np
import math
import statistics

UPLOADS_DIRECTORY = "uploads\\"

class StockDataQuery:
    def __init__(self, simbol, date = datetime(1970, 1, 1, 0, 0, 0) ):
          
        self.__url = 'https://query1.finance.yahoo.com/v7/finance/download/'
        self.__periodLastDate = datetime.now()
        self.__simbol = simbol
        self.periodEnd = 0
        if date == datetime(1970, 1, 1, 0, 0, 0):
            self.periodEnd = int((datetime.now() - datetime(1970, 1, 1, 0, 0, 0)).total_seconds()) # Number of seconds from start of epoch Jan 1, 1970 00H:00M:00S
        else:
            self.periodEnd = int((date - datetime(1970, 1, 1, 0, 0, 0)).total_seconds())
            
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
    

    def __init__(self):
        self.simbol = ""
        self.plotStartPointOffset = 0
        self.rawData = ""
        
        self.date       = []
        self.openPrice  = []
        self.highPrice  = []
        self.lowPrice   = []
        self.closePrice = []
        self.adjClose   = []
        self.volume     = [] 
        self.shortSMA    = []
        self.longSMA     = []
        self.shortEMA   = []
        self.gain  = []
        self.loss  = []
        self.gainEMA  = []
        self.lossEMA  = []
        self.RS = []
        self.RSI = []
        self.upperBBRangeValue = []
        self.lowerBBRangeValue = []

        self.MACD = []
        self.MACDSinalLine = []

    def loadData(self,dataquery:StockDataQuery):  
        self.simbol = dataquery.simbol
        fileName = UPLOADS_DIRECTORY + self.simbol + dataquery.periodLastDate.strftime("%Y%m%d")+".txt"
        
        try:
            data_file = open(fileName, "r")
            self.rawData = data_file.read()
            data_file.close()
        except:
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
            self.shortEMA.append(0.0)
            # RSI
            self.gain.append(0.0)
            self.loss.append(0.0)
            self.gainEMA.append(0.0)
            self.lossEMA.append(0.0)
            self.RS.append(0.0)
            self.RSI.append(0.0)
            # Bollinger's band
            self.upperBBRangeValue.append(0.0)
            self.lowerBBRangeValue.append(0.0)
 

    '''
        Calculate Simple Moving Average for defined range of numbers in the list
        data - list of numbers for average calculation
        periodLength - length of period for calculating average
    '''     
    def calcSMA(self, data:list, periodLength:int):
        sma = []
        for i in range(0, periodLength - 1):
            sma.append(0.0)
        for i in range(0, len(self.date) - periodLength + 1):
            sma.append(self.calcSA(self.closePrice, i, i + periodLength))
        return sma
   
    
    def calculateShortSMA(self, periodLength):
        self.shortSMA = self.calcSMA(self.closePrice, periodLength)
    
    def calculateShortEMA(self, periodLength):
      
        multiplier = 2 / (periodLength + 1)
        i = 1
        while i < len(self.date):
            self.shortEMA[i] = self.closePrice[i] * multiplier + self.shortEMA[i - 1] * (1 - multiplier)
            i+=1
        i=0
    
    '''
        Calculate Exponential Moving Average for defined range of numbers in the list
        data - list of numbers for average calculation (list of close prices)
        periodLength - length of period for calculating average
    '''     
    def calcEMA(self, data:list, periodLength:int):
        multiplier = 2 / (periodLength + 1)
        ema = []
        for i in range(0, periodLength - 1):
            ema.append(0.0)
        # Calculate simple average for defined period.
        # It'll be first value for exponential average
        ema.append(statistics.mean(data[:periodLength]))
        for i in range(periodLength, len(self.date)):
            ema.append(data[i] * multiplier + ema[i - 1] * (1 - multiplier))
        return ema
    
    ''' 
        Calculate Moving Average Convergence Divergence (MACD) for defined range of numbers in the list
        data - list of numbers for calculation
        periodLength - length of period for calculating MACD
    '''
    def calculateMACD(self, shortPeriodLength, longPeriodLength):
        shortema = self.calcEMA(self.closePrice, shortPeriodLength)
        longema = self.calcEMA(self.closePrice, longPeriodLength)
        self.MACD = []
        for i in range(0, len(shortema)):
            self.MACD.append(shortema[i] - longema[i])
        self.MACDSinalLine = self.calcEMA(self.MACD, 9)

    def calculateLongSMA(self, periodLength):
        self.plotStartPointOffset = periodLength
        self.longSMA = self.calcSMA(self.closePrice, periodLength)
 
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
        # Calculate RSI
        for i in range(periodLength, len(self.date)):
            self.RSI[i] = 100 - 100/(1 + self.gainEMA[i] / self.lossEMA[i])
        k=0

    '''
        Calculate simple average for defined range of numbers in the list
        data - list of numbers for average calculation
        start, and - define range in data calculation of average should be completed for
        start - first element
        end - last element
    '''
    def calcSA(self, data:list, start, end):
        s = 0
        if start < 0 or start > len(data):
            raise Exception("calculateSimpleAverage() - 'start' value outside data range")
        if end < 0 or end > len(data):
            raise Exception("calculateSimpleAverage() - 'end' value outside data range")
        
        for i in range(start,end):
            s+=data[i]
        return s / (end - start)    

    '''
        Calculate standart deviation for defined range of numbers in the list
            data - list of numbers for average calculation
            start, and - define range in data calculation of average should be completed for
            start - first element
            end - last element
        Return tuple
            first value - standart deviation for defined perion
            second value average for defined periob
    '''
    def calcSD(self, data:list, start, end):
        avr = self.calcSA(data, start, end)
        s = 0
        for i in range(start,end):
            s += (avr - data[i])**2
        return math.sqrt(s / (end - start)), avr
    
    '''
        Calculate Bollinger's band for defined period
            data - list of numbers (dayly prices) for borders calculation
            periodlength - define period for calculation
            probability  - define width of band based on probability moving
                            price out of band
                            1 - probability = 0.15
                            2 - pobability  = 0.02
        Return 
            no return
    '''
    def calcBB(self, periodlength, probability):
        
        for i in range(periodlength, len(self.closePrice)):
            end   = i
            start = i - periodlength
            stddev,avr = self.calcSD(self.closePrice, start, end)
            self.upperBBRangeValue[i] = avr + stddev * probability
            self.lowerBBRangeValue[i] = avr - stddev * probability

        return

    def displayData(self, startvalue):
               
        gs_kw = dict( height_ratios=[4, 1, 1])
        # Define plot layout
        fig, (ax0, ax1, ax2) = plt.subplots(3, 1,layout='constrained', gridspec_kw = gs_kw )
        fig.tight_layout(h_pad = 0.5, w_pad = 0) # Set figure margins size
        plt.legend(loc='upper left')
        fig.set_size_inches(18,10) 
        #fig.suptitle('Historic prices for simbol ' + self.simbol, fontsize=16)
        # Create alias for X-axe values
        x = self.date[startvalue:]

        # Display daily close prices and moving averages
        ax0.plot(x, self.closePrice[startvalue:], label = "Daily prices", color='gray', linewidth = 1)
        ax0.plot(x, self.shortSMA[startvalue:],   label = "Short SMA")
        ax0.plot(x, self.longSMA[startvalue:],    label = "Long SMA")
        ax0.plot(x, self.shortEMA[startvalue:],   label = "Short EMA")
        
        # Display Bellingham borders
        y1 = self.upperBBRangeValue[startvalue:]
        y2 = self.lowerBBRangeValue[startvalue:]
        ax0.fill_between(x, y1, y2, alpha=0.2, color='green')
        #ax0.plot(x, y1, label = "Upper Billingham border", color='red', linewidth = 1)
        #ax0.plot(x, y2, label = "Lower Billingham border", color='red', linewidth = 1)
        
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
        
        # Set range for displayig data
        #datemin = min(self.date) + timedelta(days=self.plotStartPointOffset +20)
        datemin = self.date[startvalue]
        datemax = self.date[-1] +  timedelta(days=2) 
        ax0.set_xlim(datemin, datemax)
        
        # rotates and right aligns the x labels, and moves the bottom of the
        # axes up to make room for them
        #fig.autofmt_xdate()

        #----------------------------------------------------------------------------------
        # Display RSI
        #----------------------------------------------------------------------------------
        #ax1.legend(loc='upper left')
        ax1.set_title('RSI for simbol ' + self.simbol)
        ax1.grid(True)
        
        ax1.plot(self.date[startvalue:], self.RSI[startvalue:],
                 label = "RSI", color='green', linewidth = 1)
        ax1.set_xlim(datemin, datemax)
        # Define coords of rectangle's corners
        xcoords = [datemin, datemax, datemax, datemin]
        ycoords = [70, 70, 30, 30]
        # Draw a rectangle
        ax1.fill(xcoords, ycoords, alpha = 0.2, color='green')
        # Draw lines to display Overbought and Oversold Levels
        #ax1.axhline( y = 70, color = 'r', linewidth=1)
        #ax1.axhline( y = 30, color = 'r', linewidth=1 )

        ax1.text(self.date[startvalue + 10],73,"Overbought level", fontsize=10, color='gray')
        ax1.text(self.date[startvalue + 10],23,"Oversold level", fontsize=10, color='gray')
               
        #----------------------------------------------------------------------------------
        # Display MACD
        #----------------------------------------------------------------------------------       
        
        #ax2.legend(loc='upper left')
        ax2.set_title('MACD for simbol ' + self.simbol)
        ax2.grid(True)
        
        ax2.plot(x, self.MACD[startvalue:], label = "MACD", color='green', linewidth = 1)
        ax2.plot(x, self.MACDSinalLine[startvalue:], label = "Signal line", color='blue', linewidth = 1)
        ax2.set_xlim(datemin, datemax)
        
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
# FSELX
# FSPTX
   
    stockDataQuery = StockDataQuery("FSPTX")
    url = stockDataQuery.url
    
    sd = StockData()
    
    sd.loadData(stockDataQuery)
    stddev=sd.calcBB(20, 1.5)
    sd.calculateShortSMA(20)
    sd.calculateLongSMA(50)
    # Usually EMA calculates fo 12 day and 26 day period
    sd.calculateShortEMA(10)
    aaa = sd.calcEMA(sd.closePrice,10)
    sd.calculateRSI(20)
    sd.calculateMACD(12,26)
 
    sd.displayData(50)
    i=1
if __name__ == '__main__':
    main()
