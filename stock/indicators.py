from datetime import datetime, timedelta
from urllib.request import urlopen
import certifi
import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
#import numpy as np
import math
import statistics


class ChartsData:

    def __init__(self, simbol, numberOfDays = 250):
          
        self.__url = 'https://financialmodelingprep.com/api/v3/historical-price-full/'
        self.__simbol = simbol
        self.__from = (datetime.now() - timedelta(days = numberOfDays)).strftime("%Y-%m-%d")
        self.__to = datetime.now().strftime("%Y-%m-%d")
        self.__serietype = "line"
        self.__apikey = "VmvqJNpPV26D4SP554R2BkjnrCuJsJ2m"

        # Source data       
        self.__date       = []
        self.__openPrice  = []
        self.__highPrice  = []
        self.__lowPrice   = []
        self.__closePrice = []
        self.__adjClose   = []
        self.__volume     = [] 
        self.__unadjustedVolume = [] 
        self.__change = []
        self.__changePercent = []
        self.__vwap = []
        self.__label = []
        self.__changeOverTime = []
        
        # Calculated indicators
        self.shortSMA    = []
        self.longSMA     = []
        self.shortEMA   = []
        self.RSI = []
        self.upperBBRangeValue = []
        self.lowerBBRangeValue = []

        self.MACD = []
        self.MACDSinalLine = []


    def load(self):
        url = self.__url + self.__simbol+"?from=" + self.__from +"&to=" + self.__to + "&apikey=" + self.__apikey# + "&serietype=" + self.__serietype
        sourceData = []
        try:
            response = urlopen(url, cafile=certifi.where())
            data = response.read().decode("utf-8")
            sourceData = json.loads(data)
        except  Exception as msg:
            print(msg)
        
        for datastr in reversed(sourceData["historical"]):
            self.__date.append(datetime.strptime(datastr["date"], '%Y-%m-%d').date())
            self.__openPrice.append(datastr["open"])
            self.__highPrice.append(datastr["high"])
            self.__lowPrice.append(datastr["low"])
            self.__closePrice.append(datastr["close"])
            self.__adjClose.append(datastr["adjClose"])
            self.__volume.append(datastr["volume"])
            self.__unadjustedVolume.append(datastr["unadjustedVolume"])
            self.__change.append(datastr["change"])
            self.__changePercent.append(datastr["changePercent"])
            self.__vwap.append(datastr["vwap"])
            self.__label.append(datastr["label"])
            self.__changeOverTime.append(datastr["changeOverTime"])
        i=0
            
       
    def show(self, startvalue):
               
        gs_kw = dict( height_ratios=[4, 1, 1])
        # Define plot layout
        fig, (ax0, ax1, ax2) = plt.subplots(3, 1,layout='constrained', gridspec_kw = gs_kw )
        fig.tight_layout(h_pad = 0.5, w_pad = 0) # Set figure margins size
        plt.legend(loc='upper left')
        fig.set_size_inches(18,12) 
        #fig.suptitle('Historic prices for simbol ' + self.simbol, fontsize=16)
        # Create alias for X-axe values
        x = self.__date[startvalue:]
       
        ax0.set_title('Historic prices for simbol ' + self.__simbol)
        ax0.grid(True)
        ax0.left = 0
        # Display daily close prices and moving averages
        ax0.plot(x, self.__closePrice[startvalue:], label = "Daily prices", color='gray', linewidth = 1)
        #ax0.plot(x, self.shortSMA[startvalue:],   label = "Short SMA")
        #//////ax0.plot(x, self.longSMA[startvalue:],    label = "Long SMA", color = 'orange')
        #//////ax0.plot(x, self.shortEMA[startvalue:],   label = "Short EMA", color = 'green')
        
        # Display Bellingham borders
        #y1 = self.upperBBRangeValue[startvalue:]
        #y2 = self.lowerBBRangeValue[startvalue:]
        #ax0.fill_between(x, y1, y2, alpha=0.2, color='green')
        #ax0.plot(x, y1, label = "Upper Billingham border", color='red', linewidth = 1)
        #ax0.plot(x, y2, label = "Lower Billingham border", color='red', linewidth = 1)
        ax0.legend(loc='upper left')
       
        
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
        datemin = self.__date[startvalue]
        datemax = self.__date[-1] +  timedelta(days=2) 
        ax0.set_xlim(datemin, datemax)
        
        # rotates and right aligns the x labels, and moves the bottom of the
        # axes up to make room for them
        #fig.autofmt_xdate()

        #----------------------------------------------------------------------------------
        # Display RSI
        #----------------------------------------------------------------------------------
        
        #ax1.set_title('RSI for simbol ' + self.simbol)
        #ax1.grid(True)
        
        #ax1.plot(self.__date[startvalue:], self.RSI[startvalue:],
        #         label = "RSI", color='green', linewidth = 1)
        #ax1.set_xlim(datemin, datemax)
        # Define coords of rectangle's corners
        #xcoords = [datemin, datemax, datemax, datemin]
        #ycoords = [70, 70, 30, 30]
        # Draw a rectangle
        #ax1.fill(xcoords, ycoords, alpha = 0.2, color='green')
        # Draw lines to display Overbought and Oversold Levels
        #ax1.axhline( y = 70, color = 'r', linewidth=1)
        #ax1.axhline( y = 30, color = 'r', linewidth=1 )

        #ax1.text(self.__date[startvalue + 10],73,"Overbought level", fontsize=10, color='gray')
        #ax1.text(self.__date[startvalue + 10],23,"Oversold level", fontsize=10, color='gray')
        #ax1.legend(loc='upper left')    
        #----------------------------------------------------------------------------------
        # Display MACD
        #----------------------------------------------------------------------------------       
        
        
        #ax2.set_title('MACD for simbol ' + self.__simbol)
        #ax2.grid(True)
        
        #ax2.plot(x, self.MACD[startvalue:], label = "MACD", color='green', linewidth = 1)
        #ax2.plot(x, self.MACDSinalLine[startvalue:], label = "Signal line", color='blue', linewidth = 1)
        #ax2.set_xlim(datemin, datemax)
        #ax2.legend(loc='upper left')
        
        plt.show()
       
    