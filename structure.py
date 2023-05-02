
import pickle
import requests
from bs4 import BeautifulSoup

currentRaceId = 0
racesMaster = []
currentRace = None
horsesMaster = []






def saveAll():
    with open('races.pickle', 'wb') as f:
        pickle.dump(racesMaster, f)

def loadAll():
    with open('races.pickle', "rb") as f:
        racesMaster = pickle.load(f)





class race:
    def __init__(self, raceInfo, raceURL):
        self.horses = []

        self.raceURL = raceURL

        global currentRaceId
        currentRaceId += 1
        self.raceId = currentRaceId

        global racesMaster
        racesMaster.append(self)

        self.day = None
        self.month = None
        self.year = None
        self.date = raceInfo[0]
        self.time = raceInfo[1]
        self.name = raceInfo[2]
        self.title = raceInfo[3]
        self.classif = raceInfo[4]
        self.rating = raceInfo[5]
        self.distance = raceInfo[6]
        self.distanceDetail = raceInfo[7]
        self.condition = raceInfo[8]
        self.prize1 = None
        self.prize2 = None
        self.prize3 = None
        self.prize4 = None
        self.prize5 = None
        self.prize6 = None
        try:
            self.prize1 = raceInfo[9][0]
        except:
            pass
        try:
            self.prize2 = raceInfo[9][1]
        except:
            pass
        try:
            self.prize3 = raceInfo[9][2]
        except:
            pass
        try:
            self.prize4 = raceInfo[9][3]
        except:
            pass
        try:
            self.prize5 = raceInfo[9][4]
        except:
            pass
        try:
            self.prize6 = raceInfo[9][5]
        except:
            pass

        global currentRace
        currentRace = self

    def fixData(self):
        #try:
        #    self.fixPositions()
        #except:
        #    pass
        try:
            self.fixStartingPositions()
        except:
            pass
        try:
            self.fixDates()
        except:
            pass
        try:
            self.fixTime()
        except:
            pass
        try:
            self.setRaceId()
        except:
            pass

    def getAll(self):
        #self.fixData()
        raceData = []
        for H in self.horses:
            horseData = []
            try:
                horseData.append(self.horses)
            except:
                horseData.append(None)
            try:
                horseData.append(self.raceURL)
            except:
                horseData.append(None)
            try:
                horseData.append(self.raceId)
            except:
                horseData.append(None)
            try:
                horseData.append(self.day)
            except:
                horseData.append(None)
            try:
                horseData.append(self.month)
            except:
                horseData.append(None)
            try:
                horseData.append(self.year)
            except:
                horseData.append(None)
            try:
                horseData.append(self.date)
            except:
                horseData.append(None)
            try:
                horseData.append(self.time)
            except:
                horseData.append(None)
            try:
                horseData.append(self.name)
            except:
                horseData.append(None)
            try:
                horseData.append(self.title)
            except:
                horseData.append(None)
            try:
                horseData.append(self.classif)
            except:
                horseData.append(None)
            try:
                horseData.append(self.rating)
            except:
                horseData.append(None)
            try:
                horseData.append(self.distance)
            except:
                horseData.append(None)
            try:
                horseData.append(self.distanceDetail)
            except:
                horseData.append(None)
            try:
                horseData.append(self.condition)
            except:
                horseData.append(None)
            try:
                horseData.append(self.prize1)
            except:
                horseData.append(None)
            try:
                horseData.append(self.prize2)
            except:
                horseData.append(None)
            try:
                horseData.append(self.prize3)
            except:
                horseData.append(None)
            try:
                horseData.append(self.prize4)
            except:
                horseData.append(None)
            try:
                horseData.append(self.prize5)
            except:
                horseData.append(None)
            try:
                horseData.append(self.prize6)
            except:
                horseData.append(None)
            try:
                horseData.append(H.name)
            except:
                horseData.append(None)
            try:
                horseData.append(H.jockey)
            except:
                horseData.append(None)
            try:
                horseData.append(H.trainer)
            except:
                horseData.append(None)
            try:
                horseData.append(H.age)
            except:
                horseData.append(None)
            try:
                horseData.append(H.topspeed)
            except:
                horseData.append(None)
            try:
                horseData.append(H.weight)
            except:
                horseData.append(None)
            try:
                horseData.append(H.rating)
            except:
                horseData.append(None)
            try:
                horseData.append(H.price)
            except:
                horseData.append(None)
            try:
                horseData.append(H.country)
            except:
                horseData.append(None)
            try:
                horseData.append(H.firstWeight)
            except:
                horseData.append(None)
            try:
                horseData.append(H.posLength)
            except:
                horseData.append(None)
            try:
                horseData.append(H.pedigree)
            except:
                horseData.append(None)
            try:
                horseData.append(H.favourite)
            except:
                horseData.append(None)
            try:
                horseData.append(H.position)
            except:
                horseData.append(None)
            try:
                horseData.append(H.startingPosition)
            except:
                horseData.append(None)
            try:
                horseData.append(H.secondWeight)
            except:
                horseData.append(None)
            try:
                horseData.append(H.RPR)
            except:
                horseData.append(None)
            try:
                horseData.append(H.MR)
            except:
                horseData.append(None)
            try:
                horseData.append(H.form)
            except:
                horseData.append(None)
            try:
                raceData.append(horseData)
            except:
                pass
        return raceData
        

    def setRaceId(self):
        self.raceId = int(self.raceURL.split("/")[-1])
    
    def fixDates(self):
        # 27 Mar 2022
        self.day = self.date.split(" ")[0]
        self.month = self.date.split(" ")[1]
        self.year = self.date.split(" ")[2]

    
    def fixFavourites(self):
        for H in self.horses:
            if H.favourite == True:
                H.favourite = int(1)
            else:
                H.favourite = int(0)


    def fixStartingPositions(self):
        for H in self.horses:
            H.startingPosition = H.startingPosition.replace("(", "")
            H.startingPosition = H.startingPosition.replace(")", "")

    
    def fixPositions(self):
        try:
            original = self.raceURL
            #print(original)
            url = "https://www.sportinglife.com/racing/results/DATE/PLACE/RACEID/NAME"

            place = original.split("/")[6]
            raceId = original.split("/")[8]
            name = original.split("/")[-1]

            newURL = url.replace("DATE", races[0].date)
            newURL = newURL.replace("PLACE", place)
            newURL = newURL.replace("RACEID", raceId)
            newURL = newURL.replace("NAME", name)
            print(newURL)
            if newURL == "https://www.sportinglife.com/racing/results/2021-10-02/Naas/647177/Irish-Stallion-Farms-EBF-C-&-G-Maiden":
                print("found")

            response = requests.get(newURL)
            soupthis = response.text
            soup = BeautifulSoup(soupthis, 'html.parser')

            runners = soup.find_all("div", class_="ResultRunner__StyledResultRunnerWrapper-sc-58kifh-13")


            for runner in runners:
                horseName = str(runner.find("div", class_="ResultRunner__StyledHorseName-sc-58kifh-5").text)
                try:
                    position = int(runner.find("div", {"data-test-id":"position-no"}).text[:-2])
                except:
                    position = None
                for h in r.horses:
                    try:
                        if horseName in str(h.name):
                            h.position = position
                            break
                            #print("match " + h.name)
                    except:
                        pass
            r.saveSL()
        except:
            print("FAIL " + r.raceURL)
    
    def fixTime(self):
        t = self.time.split(":")
        t1 = int(t[0])*60
        t2 = int(t[1])
        self.time = int(t1+t2)

    def prep(self, var, data):
        try: 
            data.append(var)
        except:
            data.append(None)
        return data



    def getData(self):
        self.fixData()
        raceData = []
        
        for H in self.horses:
            try:
                H.convertPrice()
            except:
                pass
            try:
                H.convertWeights()
            except:
                pass
            horseData = []
            try:
                horseData.append(self.raceURL)
            except:
                horseData.append(None)
            try:
                horseData.append(self.time)
            except:
                horseData.append(None)
            try:
                horseData.append(self.rating)
            except:
                horseData.append(None)
            try:
                horseData.append(self.distance)
            except:
                horseData.append(None)
            data = H.getData()
            for field in data:
                horseData.append(field)
            
            raceData.append(horseData)
        return raceData


    def switchPosition(self):
        for H in self.horses:
            H.switchPosition()
        
    def saveSL(self):
        #https://www.sportinglife.com/racing/racecards/2022-09-24/Newmarket/racecard/698585/Juddmonte-Royal-Lodge-Stakes-Group-2
        #self.raceId = str(self.raceURL.split("/")[-2])
        filename = "pickles/SL{}.pickle".format(str(self.raceId))
        with open(filename, 'wb') as f:
            pickle.dump(self, f)


    def save(self):
        self.setRaceId()
        filename = "pickles/{}.pickle".format(str(self.raceId))
        with open(filename, 'wb') as f:
            pickle.dump(self, f)



    
    def addHorse(self, horseObject):
        self.horses.append(horseObject)
    
    def exportHorses(self):
        for h in self.horses:
            horsesMaster.append(h)

    def print(self):
        print(self.raceURL)
        print(self.date, self.time, self.name, self.title, self.classif, self.rating, self.distance)

        print("{:25s}{:25s}{:25s}{:10s}{:10s}{:10s}{:10s}".format("Horse", 
                                                                    "Jockey", 
                                                                    "Trainer", 
                                                                    "Age", 
                                                                    "Weight", 
                                                                    "Rating", 
                                                                    "Price"))
                                                                                    
        for horse in self.horses:
            horse.print()





class horse:
    def __init__(self, name, jockey, trainer, age, topspeed, weight, 
                rating, price, country, firstWeight, posLength, pedigree, 
                position, startingPosition, RPR, MR, form):
        self.name = name
        self.jockey = jockey
        self.trainer = trainer
        self.age = age
        self.topspeed = topspeed
        self.weight = str(weight)
        self.rating = rating
        self.price = price
        self.country = country
        self.firstWeight = firstWeight
        self.posLength = posLength
        self.pedigree = pedigree
        self.favourite = False
        self.position = position
        self.startingPosition = startingPosition
        self.secondWeight = 0
        self.RPR = RPR
        self.MR = MR
        self.form = form
        self.prediction = None

        self.processing()

    def sortForm(self):
        form = []
        for ch in self.form:
            if ch.isnumeric():
                form.append(int(ch))
            else:
                form.append(None)
        form.reverse()
        while len(form) < 5:
            form.append(None)
        self.form = form[:5]
    
    def cleanUp(self):
        try:
            self.sortForm()
        except:
            pass
        self.convertWeights()

        s = str("string")
        f = float(0.5)
        i = int(1)
        b = bool(True)
        
        if type(self.name) is not type(s):
            try:
                self.name = str(self.name)    
            except:
                self.name = None
        if type(self.jockey) is not type(s):
            try:
                self.jockey = str(self.jockey)    
            except:
                self.jockey = None
        if type(self.trainer) is not type(s):
            try:
                self.trainer = str(self.trainer)    
            except:
                self.trainer = None
        if type(self.age) is not type(i):
            try:
                self.age = int(self.age)    
            except:
                self.age = None
        if type(self.topspeed) is not type(i):
            try:
                self.topspeed = int(self.topspeed)    
            except:
                self.topspeed = None
        if type(self.weight) is not type(s):
            try:
                self.weight = str(self.weight)    
            except:
                self.weight = None
        if type(self.rating) is not type(i):
            try:
                self.rating = int(self.rating)    
            except:
                self.rating = None
        if type(self.price) is not type(f):
            try:
                self.price = float(self.price)    
            except:
                self.price = None
        if type(self.country) is not type(s):
            try:
                self.country = str(self.country)    
            except:
                self.country = None
        if type(self.firstWeight) is not type(i):
            try:
                self.firstWeight = int(self.firstWeight)    
            except:
                self.firstWeight = None
        if type(self.favourite) is not type(b):
            try:
                self.favourite = bool(self.favourite)    
            except:
                self.favourite = None
        if type(self.position) is not type(i):
            try:
                self.position = int(self.position)    
            except:
                self.position = None
        if type(self.startingPosition) is not type(i):
            try:
                self.startingPosition = int(self.startingPosition)    
            except:
                self.startingPosition = None
        if type(self.secondWeight) is not type(i):
            try:
                self.secondWeight = int(self.secondWeight)    
            except:
                self.secondWeight = None
        if type(self.RPR) is not type(i):
            try:
                self.RPR = int(self.RPR)    
            except:
                self.RPR = None
        if type(self.MR) is not type(i):
            try:
                self.MR = int(self.MR)    
            except:
                self.MR = None



    def switchPosition(self):
        self.startingPosition = self.position

    def prep(self, var, data):
        try: 
            data.append(var)
        except:
            data.append(None)
        return data




    def getData(self):
        self.cleanUp()
        data = []
        try:
            data.append(self.name)
        except:
            data.append(None)
        try:
            data.append(self.jockey)
        except:
            data.append(None)
        try:
            data.append(self.trainer)
        except:
            data.append(None)
        try:
            data.append(self.age)
        except:
            data.append(None)
        try:
            data.append(self.weight)
        except:
            data.append(None)
        try:
            data.append(self.firstWeight)
        except:
            data.append(None)
        try:
            data.append(self.secondWeight)
        except:
            data.append(None)
        try:
            data.append(self.rating)
        except:
            data.append(None)
        try:
            data.append(self.price)
        except:
            data.append(None)
        try:
            data.append(self.form[0])
        except:
            data.append(None)
        try:
            data.append(self.form[1])
        except:
            data.append(None)
        try:
            data.append(self.form[2])
        except:
            data.append(None)
        try:
            data.append(self.form[3])
        except:
            data.append(None)
        try:
            data.append(self.form[4])
        except:
            data.append(None)
        try:
            data.append(self.position)
        except:
            data.append(None)
        return data

    def processing(self):
        #self.convertPrice()
        #self.convertWeights()
        try:
            self.fixCountry()
        except:
            pass

        global currentRace
        currentRace.addHorse(self)

        global horsesMaster
        horsesMaster.append(self)

    def fixCountry(self):
        self.country = self.country.replace("(", "")
        self.country = self.country.replace(")", "")
        if self.country == "":
            self.country = "ENG"

    def convertWeights(self):
        try:
            self.firstWeight = int(self.weight.split("-")[0])
            self.secondWeight = int(self.weight.split("-")[1])
        except:
            pass

    def sortWeight(self):
        self.firstWeight = self.weight.split("-")[0]
        self.secondWeight = self.weight.split("-")[1]

        

    def convertPrice(self):
        try:
            if "F" in self.price:
                self.favourite = True
        except:
            pass
        price = self.price.split("/")
        a = int(price[0].replace("F", ""), 10)
        b = int(price[1].replace("F", ""), 10)
        self.price = float(a/b)

    def print(self):
        print("{:25s}{:25s}{:25s}{:10s}{:10s}{:10s}{:10s}".format(self.name, 
                                                                    self.jockey, 
                                                                    self.trainer, 
                                                                    str(self.age), 
                                                                    str(self.weight), 
                                                                    str(self.rating), 
                                                                    str(self.price)))





