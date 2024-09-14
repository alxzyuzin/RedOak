
class Simbol:
    def __init__(self, simbol:str, name:str, category:str, yearreturn:float, status:str):
        self.simbol = simbol
        self.status = status
        self.description = name
        self.category = category
        self.ytdreturn = yearreturn
        self.dic = {}
        self.dic['simbol'] = simbol
        self.dic['status'] = status
        self.dic['name'] = name
        self.dic['category'] = category
        self.dic['yearreturn'] = yearreturn

class SimbolsCollection:
    def __init__(self):
        self.simbols = []

    def load_csv(self, filename:str):
        # CSV file structure        
        #  0 - Simbol                  string
        #  1 - Name                    string
        #  2 - Morningstar Category    string
        #  3 - YTD # (Daily)           float
        #  4 - 1 Yr                    float
        #  5 - 3 Yr                    float
        #  6 - 5 Yr                    float
        #  7 - 10 Yr                   float
        #  8 - Life of Fund            float
        #  9 - Net †                   float
        # 10 - Gross ‡                 float
        # 11 - Overall                 float
        
        try:
            with open(filename, 'r') as file:
                for line in file:
                    linedata = line.split(',')
                    if linedata[4] == '--':
                        yr = 0.0
                    else:
                        yr = float(linedata[4].replace("%", ""))
                    smb = Simbol(simbol = linedata[0],
                                name = linedata[1].replace('ï¿½',' '),
                                category = linedata[2],
                                yearreturn =  yr, 
                                status = 'unselected')
                    self.simbols.append(smb)
                   
                   
            
        except FileNotFoundError:
            print(f"The file {filename} does not exist.")   
        except PermissionError:
            print("You do not have permission to access this file.")  
        except IsADirectoryError:
            print("The specified path is a directory, not a file.")
        except IOError:
            print("An I/O error occurred.")
        
    def save(self):
        pass

    def delete(self, simbol:Simbol):
        for i in range(0,len(self.simbols)):
            if self.simbols[i].simbol == simbol.simbol:
                break
        self.simbols.pop(i)

    def append(self, simbol):
        self.simbols.append(simbol)

    def set_status(self, simbol:Simbol, new_status):
        for i in range(0,self.simbols):
            if self.simbols[i].simbol == simbol:
                self.simbols[i].status = new_status
                self.simbols[i].dic['status'] = new_status
                break
       


def main():
    #s = Simbol('HHHHH','portolio','Fake simbol')
    sl = SimbolsCollection()
    sl.load_csv("docs\\fondslist.csv")
    #sl.delete(s)
    i=1

if __name__ == '__main__':
    main()

    'Fidelityï¿½Select Energy Portfolio (FSENX)'