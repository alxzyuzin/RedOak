import urllib.request;

SHORT_TERM_MA_LENGTH = 20
LONF_TERM_MA_LENGTH = 50
SIMBOL = "FSELX"

# Download price data
urlstr = 'https://query1.finance.yahoo.com/v7/finance/download/FSELX?period1=1691277249&period2=1722899649&interval=1d&events=history&includeAdjustedClose=true'
rawData = urllib.request.urlopen(urlstr).read().decode().split('\n')

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

end = 'true'