from bs4 import BeautifulSoup
import requests
import structure
import pickle

races = []
def loadAllRaces():
    print("Loading All Data")
    global races
    races = []
    with open("allRaces.pickle", "rb") as f:
        races = pickle.load(f)
    print("All Data Loaded")

loadAllRaces()



for r in races:
    try:
        original = r.raceURL
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
    


# ssh root@109.74.205.244