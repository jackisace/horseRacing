



def getHorse(name):
    global horsesMaster
    for h in horsesMaster:
        if h.name == name:
            return h


class race:
    def __init__(self):
        self.horses = []

        global currentRaceId
        currentRaceId += 1
        self.raceId = currentRaceId

        global racesMaster
        racesMaster.append(self)

        global raceInfo
        self.date = raceInfo[0]
        self.time = raceInfo[1]
        self.name = raceInfo[2]
        self.title = raceInfo[3]
        self.classif = raceInfo[4]
        self.rating = raceInfo[5]
        self.distance = raceInfo[6]
        self.detail = raceInfo[7]
        self.condition = raceInfo[8]
        self.prize1 = float(raceInfo[9][0])
        self.prize2 = float(raceInfo[9][1])
        self.prize3 = float(raceInfo[9][2])
        self.prize4 = float(raceInfo[9][3])
        self.prize5 = float(raceInfo[9][4])
        self.prize6 = float(raceInfo[9][5])

        self.print()

    
    def addHorse(self, horseObject):
        self.horses.append(horseObject)
    
    def exportHorses(self):
        for h in self.horses:
            horsesMaster.append(h)

    def print(self):
        print(self.date, self.time, self.name, self.title, self.classif, self.rating, self.distance, self.detail, self.condition)

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
        

        

    def processing(self):
        self.convertPrice()
        self.convertWeights()
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
                                                                                    str(self.price)[:4], 
                                                                                    self.country, 
                                                                                    self.posLength))





