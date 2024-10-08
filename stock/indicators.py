from datetime import datetime, timedelta
from urllib.request import urlopen
import certifi
import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
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
        self.__shortSMA    = []
        self.__longSMA     = []
        self.__longSMALength = 0
        self.__shortEMA   = []
        self.__shortMALength = 0
        
        self.__RSI = []
        self.__upperBBRangeValue = []
        self.__lowerBBRangeValue = []
        #self.__BBstddevKoeff = 2

        self.__MACD = []
        self.__MACDSinalLine = []


    def load(self):
        url = self.__url + self.__simbol+"?from=" + self.__from +"&to=" + self.__to + "&apikey=" + self.__apikey# + "&serietype=" + self.__serietype
        #test url with constant range for tests
        #url = 'https://financialmodelingprep.com/api/v3/historical-price-full/FSELX?from=2024-01-01&to=2024-09-07&apikey=VmvqJNpPV26D4SP554R2BkjnrCuJsJ2m'
        sourceData = []
        try:
            response = urlopen(url, cafile=certifi.where())
            data = response.read().decode("utf-8")
            sourceData = json.loads(data)
        except  Exception as msg:
            print(msg)
        
        #data_file = open("uploads\\testData.csv", "w")
       

        for datastr in reversed(sourceData["historical"]):
            self.__date.append(datetime.strptime(datastr["date"], '%Y-%m-%d').date())
            self.__openPrice.append(float(datastr["open"]))
            self.__highPrice.append(float(datastr["high"]))
            self.__lowPrice.append(float(datastr["low"]))
            self.__closePrice.append(float(datastr["close"]))
            self.__adjClose.append(float(datastr["adjClose"]))
            self.__volume.append(float(datastr["volume"]))
            self.__unadjustedVolume.append(float(datastr["unadjustedVolume"]))
            self.__change.append(float(datastr["change"]))
            self.__changePercent.append(float(datastr["changePercent"]))
            self.__vwap.append(float(datastr["vwap"]))
            self.__label.append(datastr["label"])
            self.__changeOverTime.append(float(datastr["changeOverTime"]))
            
            #strl = str(datastr["date"])
            #strl += ("," + str(datastr["close"]))
            #strl += "\n"
            #data_file.writelines(strl)
            
            #self.__longSMA.append(0.0)
         
        #data_file.flush()
        #data_file.close()

    '''
        Calculate Simple Moving Average for defined range of numbers in the list
        data - list of numbers for average calculation
        periodLength - length of period for calculating average
    '''     
    def calcSMA(self, data:list, periodLength:int):
        sma = []
        for i in range(0, periodLength - 1):
            sma.append(0.0)
        for i in range(0, len(self.__date) - periodLength + 1):
            sma.append(statistics.fmean(data[i:i+periodLength]))
        return sma
   
    
    def calcShortSMA(self, periodLength):
        self.__shortSMA = self.calcSMA(self.__closePrice, periodLength)        

    def calcLongSMA(self, periodLength):
        self.__longSMALength = periodLength
        self.__longSMA = self.calcSMA(self.__closePrice, periodLength)
    
    def calcShortEMA(self, periodLength):
        multiplier = 2 / (periodLength + 1)
        self.__shortEMA.append(0.0)
        for i in range(1, len(self.__date)):
            self.__shortEMA.append(self.__closePrice[i] * multiplier + self.__shortEMA[i - 1] * (1 - multiplier))
           
    '''
        Calculate Bollinger's band for defined period
            Band's width calculated based on probability that price lay
            inside calculated band.
            Standard calculation method calculate band width as +- 2*stddev
            from average (in this case probability = 0.95)
            data - list of numbers (dayly prices) for borders calculation
            periodlength - define period for calculation
            probability  - probability that price are inside drawed band                            price out of band
        Return 
            no return
    '''
    def calcBollingerBand(self, periodlength, probability):
        for i in range(0, periodlength):
            self.__upperBBRangeValue.append(0.0)
            self.__lowerBBRangeValue.append(0.0)
 
        for i in range(periodlength, len(self.__closePrice)):
            sample_data = self.__closePrice[i - periodlength : i]
            #sample_data = [15,15,15,15,14,17,18,21,22,24,26,29,29,30,25]
            # Calculate standard deviation
            stddev = statistics.pstdev(sample_data) 
            avr = statistics.fmean(sample_data)
            #-----------------------------------------------------------
            #  Confidence interval calculation
            # Calculate standard error as  stddev / np.sqrt(len(sample_data) - 1)
            #stderr = stats.sem(sample_data)
            #ster = stddev/math.sqrt(len(sample_data)-1)
            # Calculate Z-value for defined confidence level
            #z_value = stats.norm.ppf((1 - confidence_level) / 2)
            # Calculate предел погрешности
            #err_limit = z_value * stderr
            # Calculate the confidence interval
            #confidence_interval = stats.t.interval(confidence_level,df = len(sample_data)-1, loc = avr, scale=stderr)
            # 68-95-99.7
            # (1 - 0.68)/2 = 0.16
            # 0.68 + 0.16 = 0.84 = 1 - 0.16
            normDist = statistics.NormalDist(mu = avr, sigma = stddev)
            lt = (1 - probability) / 2
            rt = (1 - lt)
            # Calculate border level for left tail of normal distribution plot
            lowerLimit = normDist.inv_cdf(lt)
            # Calculate border level for right tail of normal distribution plot
            upperLimit = normDist.inv_cdf(rt)
            #up = avr - err_limit
            #lw = avr + err_limit
            #ci = avr +  stddev * 2
            self.__upperBBRangeValue.append(upperLimit)
            self.__lowerBBRangeValue.append(lowerLimit)
            #self.upperBBRangeValue[i] = avr + stddev * probability
            #self.lowerBBRangeValue[i] = avr - stddev * probability
        return

    def calcRSI(self, periodLength):
        # Calculate Gain and Loss
        gain = [0.0]
        loss = [0.0]
        for i in range(1, len(self.__date)):
            change = self.__openPrice[i] - self.__openPrice[i-1]
            if change > 0 :
                gain.append(change)
                loss.append(0.0)
            else:
                gain.append(0)
                loss.append(0 - change)
        
        gainEMA = self.calcSMA(gain, periodLength)
        lossEMA = self.calcSMA(loss, periodLength)
        # Calculate RSI
        self.__RSI = []
        for i in range(0, periodLength):
            self.__RSI.append(0.0)
        for i in range(periodLength, len(self.__date)):
            # Приводим значение к диапазону 0 - 100
            #self.__RSI.append(100 - 100/(1 + gainEMA[i] / lossEMA[i]))
             # Приводим значение к диапазону -50 +50
            self.__RSI.append(50 - 100/(1 + gainEMA[i] / lossEMA[i]))
    
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
        ema.append(statistics.fmean(data[:periodLength]))
        for i in range(periodLength, len(data)):
            ema.append(data[i] * multiplier + ema[i - 1] * (1 - multiplier))
        return ema

    ''' 
        Calculate Moving Average Convergence Divergence (MACD) for defined range of numbers in the list
        data - list of numbers for calculation
        periodLength - length of period for calculating MACD
    '''
    def calcMACD(self, shortPeriodLength = 12, longPeriodLength = 26, signalPeriodLength = 9):
        shortema = self.calcEMA(self.__closePrice, shortPeriodLength)
        longema = self.calcEMA(self.__closePrice, longPeriodLength)
        self.__MACD = []
        self.__MACDSinalLine = []
        for i in range(0, len(shortema)):
            self.__MACD.append(shortema[i] - longema[i])
        # Fill items in MACD list with 0.0 for items laying before meaningfull macd values
        for i in range(0, longPeriodLength - 1):
            self.__MACD[i]= 0.0
            self.__MACDSinalLine.append(0.0)
        signalLineData = self.calcEMA(self.__MACD[longPeriodLength - 1:], signalPeriodLength)
        self.__MACDSinalLine += signalLineData

    def show(self, startvalue):
               
         # Define plot layout
        gs_kw = dict( height_ratios=[4, 1, 1, 1])
        fig, (ax0, ax1, ax2, ax3) = plt.subplots(4, 1,layout='constrained', gridspec_kw = gs_kw )
        fig.tight_layout(h_pad = 0.5, w_pad = 0) # Set figure margins size
        #plt.legend(loc='upper left')
        fig.set_size_inches(18,12) 
        #fig.suptitle('Historic prices for simbol ' + self.simbol, fontsize=16)
        # Create alias for X-axe values
        x = self.__date[startvalue:]
       
        ax0.set_title(f'Historic prices for simbol {self.__simbol} (Last price:{self.__closePrice[-1]}).')
        ax0.grid(True)
        ax0.left = 0
        # Display daily close prices and moving averages
        ax0.plot(x, self.__closePrice[startvalue:], label = "Daily prices", color='gray', linewidth = 1)
        #ax0.plot(x, self.__shortSMA[startvalue:],   label = "Short SMA")
        ax0.plot(x, self.__longSMA[startvalue:],    label = "Long SMA", color = 'orange')
        ax0.plot(x, self.__shortEMA[startvalue:],   label = "Short EMA", color = 'green')
        
        # Display Bellingham borders
        y1 = self.__upperBBRangeValue[startvalue:]
        y2 = self.__lowerBBRangeValue[startvalue:]
        ax0.fill_between(x, y1, y2, alpha=0.2, color='green')
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
        # Display volumes
        #----------------------------------------------------------------------------------
        ax1.set_title('Volumes for simbol ' + self.__simbol)
        ax1.grid(True)
        ax1.plot(self.__date[startvalue:], self.__volume[startvalue:],
                 label = "Volume", color='steelblue', linewidth = 1)
        ax1.set_xlim(datemin, datemax)
        

        #----------------------------------------------------------------------------------
        # Display RSI
        #----------------------------------------------------------------------------------
        
        ax2.set_title('RSI for simbol ' + self.__simbol)
        ax2.grid(True)
        
        ax2.plot(self.__date[startvalue:], self.__RSI[startvalue:],
                 label = "RSI", color='steelblue', linewidth = 1)
        ax2.set_xlim(datemin, datemax)
        ax2.set_ylim(-40, 40)
        # Define coords of rectangle's corners
        xcoords = [datemin, datemax, datemax, datemin]
        ycoords = [20, 20, -20, -20]
        # Draw a rectangle
        ax2.fill(xcoords, ycoords, alpha = 0.4, color='lightsteelblue')
        # Draw lines to display Overbought and Oversold Levels
        #ax1.axhline( y = 70, color = 'r', linewidth=1)
        #ax1.axhline( y = 30, color = 'r', linewidth=1 )

        ax2.text(self.__date[startvalue + 10],23,"Overbought level", fontsize=10, color='gray')
        ax2.text(self.__date[startvalue + 10],-30,"Oversold level", fontsize=10, color='gray')
        ax2.legend(loc='lower left')    
        
        #----------------------------------------------------------------------------------
        # Display MACD
        #----------------------------------------------------------------------------------       
               
        ax3.set_title('MACD for simbol ' + self.__simbol)
        ax3.grid(True)
        
        ax3.plot(x, self.__MACD[startvalue:], label = "MACD", color='green', linewidth = 1)
        ax3.plot(x, self.__MACDSinalLine[startvalue:], label = "Signal line", color='blue', linewidth = 1)
        ax3.set_xlim(datemin, datemax)
        ax3.legend(loc='upper left')
        
        # Open full screen window
        mng = plt.get_current_fig_manager()
        mng.set_window_title("Indicators for simbol " + self.__simbol)
        #mng.full_screen_toggle()

        plt.show()
       
    