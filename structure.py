currentRaceId = 31672
racesMaster = []
horsesMaster = []
currentRace = None

import pickle

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
        self.fixPositions()
        self.fixStartingPositions()
        self.fixDates()

    
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
        position = 1
        for H in self.horses:
            H.position = position
            position += 1



    def getData(self):
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
                horseData.append(self.day)
            except:
                horseData.append("-")
            try:
                horseData.append(self.month)
            except:
                horseData.append("-")
            try:
                horseData.append(self.year)
            except:
                horseData.append("-")
            try:
                horseData.append(self.time)
            except:
                horseData.append("-")
            try:
                horseData.append(self.name)
            except:
                horseData.append("-")
            #try:
            #    horseData.append(self.title)
            #except:
            #    horseData.append("-")
            try:
                horseData.append(self.classif)
            except:
                horseData.append("-")
            try:
                horseData.append(self.rating)
            except:
                horseData.append("-")
            try:
                horseData.append(self.distance)
            except:
                horseData.append("-")
            #try:
            #    horseData.append(self.distanceDetail)
            #except:
            #    horseData.append("-")
            try:
                horseData.append(self.condition)
            except:
                horseData.append("-")
            #try:
            #    horseData.append(self.prize1)
            #except:
            #    horseData.append("-")
            #try:
            #    horseData.append(self.prize2)
            #except:
            #    horseData.append("-")
            #try:
            #    horseData.append(self.prize3)
            #except:
            #    horseData.append("-")
            #try:
            #    horseData.append(self.prize4)
            #except:
            #    horseData.append("-")
            #try:
            #    horseData.append(self.prize5)
            #except:
            #    horseData.append("-")
            #try:
            #    horseData.append(self.prize6)
            #except:
            #    horseData.append("-")
            data = H.getData()
            for field in data:
                horseData.append(field)
            
            raceData.append(horseData)
        return raceData



        

    def save(self):
        filename = "pickles/race{}.pickle".format(self.raceId)
        with open(filename, 'wb') as f:
            pickle.dump(self, f)



    
    def addHorse(self, horseObject):
        self.horses.append(horseObject)
    
    def exportHorses(self):
        for h in self.horses:
            horsesMaster.append(h)

    def print(self):
        print(self.raceURL)
        print(self.date, self.time, self.name, self.title, self.classif, self.rating, self.distance, self.condition)

        print("{:25s}{:25s}{:25s}{:10s}{:10s}{:10s}{:10s}{:10s}{:10s}{:10s}".format("Horse", 
                                                                                    "Jockey", 
                                                                                    "Trainer", 
                                                                                    "Age", 
                                                                                    "TS", 
                                                                                    "Weight", 
                                                                                    "Rating", 
                                                                                    "Price", 
                                                                                    "Country", 
                                                                                    "PosL"))
        for horse in self.horses:
            horse.print()



class horse:
    def __init__(self, name, jockey, trainer, age, topspeed, weight, 
                rating, price, country, firstWeight, posLength, pedigree, 
                position, startingPosition, RPR, MR):
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

        self.processing()
        

    def getData(self):
        data = []

        try: 
            data.append(self.name)
        except:
            data.append("")
        try: 
            data.append(self.jockey)
        except:
            data.append("")
        try: 
            data.append(self.trainer)
        except:
            data.append("")
        try: 
            data.append(self.age)
        except:
            data.append("")
        try: 
            data.append(self.topspeed)
        except:
            data.append("")
        try: 
            data.append(self.weight)
        except:
            data.append("")
        try: 
            data.append(self.rating)
        except:
            data.append("")
        try: 
            data.append(self.price)
        except:
            data.append("")
        try: 
            data.append(self.country)
        except:
            data.append("")
        try: 
            data.append(self.firstWeight)
        except:
            data.append("")
        try: 
            data.append(self.posLength)
        except:
            data.append("")
        try: 
            data.append(self.pedigree[0])
        except:
            data.append("")
        try: 
            data.append(self.pedigree[1])
        except:
            data.append("")
        try: 
            data.append(self.pedigree[2])
        except:
            data.append("")
        try: 
            data.append(self.favourite)
        except:
            data.append("")
        try: 
            data.append(self.position)
        except:
            data.append("")
        try: 
            data.append(self.startingPosition)
        except:
            data.append("")
        try: 
            data.append(self.secondWeight)
        except:
            data.append("")
        try: 
            data.append(self.RPR)
        except:
            data.append("")
        #try: 
        #    data.append(self.MR)
        #except:
        #    data.append("")
        
        return data

    def processing(self):
        #self.convertPrice()
        #self.convertWeights()
        self.fixCountry()

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
        weight = str(self.firstWeight) + "-"
        weight += str(self.weight[len(self.firstWeight):])

        self.weight = weight
        self.firstWeight = int(weight.split("-")[0])
        self.secondWeight = int(weight.split("-")[1])

        

    def convertPrice(self):
        if "F" in self.price:
            self.favourite = True
        price = self.price.split("/")
        a = int(price[0].replace("F", ""), 10)
        b = int(price[1].replace("F", ""), 10)
        self.price = float(a/b)

    def print(self):
        print("{:25s}{:25s}{:25s}{:10s}{:10s}{:10s}{:10s}{:10s}{:10s}{:10s}".format(self.name, 
                                                                                    self.jockey, 
                                                                                    self.trainer, 
                                                                                    str(self.age), 
                                                                                    str(self.topspeed), 
                                                                                    str(self.weight), 
                                                                                    str(self.rating), 
                                                                                    str(self.price), 
                                                                                    self.country, 
                                                                                    self.posLength))





