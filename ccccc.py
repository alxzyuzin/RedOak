# Download price data
def LoadData(simbol):
    urlstrHead = 'https://query1.finance.yahoo.com/v7/finance/download/'
    urlstrTail = '?period1=1691277249&period2=1722899649&interval=1d&events=history&includeAdjustedClose=true'
    urlstr = urlstrHead + simbol + urlstrTail
    #urlstr = 'https://query1.finance.yahoo.com/v7/finance/download/FSELX?period1=1691277249&period2=1722899649&interval=1d&events=history&includeAdjustedClose=true'
    # Save data from internet for a future use
    #text_file = open(r"C:\\Users\\alxzy\Documents\\PROJECTS\\RedOak\\shareprices.txt", "w")
    #pricedata = urllib.request.urlopen(urlstr).read().decode()
    #text_file.write(pricedata)
    #text_file.close()
    current_dateTime = datetime.now()
    fileName = simbol + current_dateTime.strftime("%Y%m%d")+".hsp"
    try:
        #text_file = open(r"C:\\Users\\alxzy\Documents\\PROJECTS\\RedOak\\shareprices.txt", "r")
        data_file = open(fileName, "r")
        rawData = data_file.read().split('\n')
        data_file.close()
    except:
        data_file = open(fileName, "w")
        pricedata = urllib.request.urlopen(urlstr).read().decode()
        data_file.write(pricedata)
        data_file.flush()
        data_file.close()
        
        data_file = open(fileName, "r")
        rawData = data_file.read().split('\n')
        data_file.close()
        

    
    
    #text_file = open(r"C:\\Users\\alxzy\Documents\\PROJECTS\\RedOak\\shareprices.txt", "r")
    #rawData = text_file.read().split('\n')
    #text_file.close()

    #rawData = urllib.request.urlopen(urlstr).read().decode().split('\n')

    # Parce data into list of dictionaries
    dataCollection = []
    for dataString in rawData[1:]:
        lineData = dataString.split(',')
        dataRow = {}
        dataRow["Date"] = datetime.strptime(lineData[0], '%Y-%m-%d').date()
        dataRow["Open"] = float(lineData[1])
        dataRow["High"] = float(lineData[2])
        dataRow["Low"] = float(lineData[3])
        dataRow["Close"] = float(lineData[4])
        dataRow["AdjClose"] = float(lineData[5])
        dataRow["Volume"] = float(lineData[6])
   
        dataCollection.append(dataRow)
    return dataCollection

def DisplayData(dataCollection):
    # Display open prices
    #Create list of dates and prices
    dates = []
    prices = []
    for row in dataCollection:
        dates.append(row["Date"])
        prices.append(row["Close"])

    # Display prices against dates
    # define data values
    x = np.array(dates)   # X-axis points
    y = np.array(prices)  # Y-axis points

    plt.plot(x, y)
    plt.show()
    end = 'true'

def main():
    dc = LoadData("FSELX")
    DisplayData(dc)
    end = True

if __name__ == "__main__":
    main()

