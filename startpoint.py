import urllib.request;
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

#import pandas as pd

SHORT_TERM_MA_LENGTH = 20
LONF_TERM_MA_LENGTH = 50
SIMBOL = "FSELX"

# Download price data


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



end = 'true'