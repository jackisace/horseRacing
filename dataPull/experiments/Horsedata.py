from argparse import _MutuallyExclusiveGroup
from bs4 import BeautifulSoup
import requests
import re
#from sqlalchemy import Index


'''urls to test'''

url = "https://www.racingpost.com/results/36/newbury/2022-09-16/819636"
url = "https://www.racingpost.com/results/22/hamilton/2022-09-18/819663"
#url = "https://www.racingpost.com/results/36/newbury/2022-09-16/819634"
#url = 'https://www.racingpost.com/results/36/newbury/2022-09-16/819632'
urlhtml = requests.get(url)

soupthis = urlhtml.text
open("b.html", "w").write(soupthis)

soup = BeautifulSoup(soupthis, 'html.parser')
output = ''
horses = []
jockeys = []
trainers = []
ages = []
ors = []
weights = []
topspeed = []


'''Horse names'''
for item in soup.find_all('a',class_=["rp-horseTable__horse__name ui-link ui-link_table js-popupLink",""]):
    output += ("{}, {}".format(' '.join(item['class']),item.text))


output = "".join(line.strip() for line in output.split("rp-horseTable__horse__name ui-link ui-link_table js-popupLink"))
output = output.replace('\n', '')
horses = output.split(',')
temp = []
for item in horses:
    if len(item) == 0:
        pass
    else:
        temp.append(item[25:])

horses = temp


'''Jockey names'''

output = ''
for item in soup.find_all('a',class_=['rp-horseTable__human__link ui-link ui-link_table ui-link_marked ui-profileLink js-popupLink',""]):
    output += ("{}, {}".format(' '.join(item['class']),item.text))


output = "".join(line.strip() for line in output.split("rp-horseTable__human__link ui-link ui-link_table ui-link_marked ui-profileLink js-popupLink"))
output = output.replace('\n', '')
jockeys = output.split(',')
temp = []
for item in jockeys:
    if len(item) == 0:
        pass
    else:
        temp.append(item[29:])

jockeys = temp


'''Horse Age'''

output = ''
for item in soup.find_all('td',class_=['rp-horseTable__spanNarrow rp-horseTable__spanNarrow_age',""]):
    output += ("{}, {}".format(' '.join(item['class']),item.text))


output = "".join(line.strip() for line in output.split("rp-horseTable__spanNarrow rp-horseTable__spanNarrow_age"))
output = output.replace('\n', '')
ages = output.split(',')
temp = []
for item in ages:
    if len(item) == 0:
        pass
    else:
        temp.append(item[9:])

ages = temp


'''Topsspeed of horse'''


output = ''
for item in soup.find_all('td', {'data-test-selector':"full-result-topspeed"}):
    output += ("{}, {}".format(' '.join(item['class']),item.text))


output = "".join(line.strip() for line in output.split("rp-horseTable__spanNarrow"))
output = output.replace('\n', '')
topspeed = output.split(',')
temp = []
for item in topspeed:
    if len(item) == 0:
        pass
    else:
        temp.append(item[9:])

topspeed = temp

'''Weight -- Still needs to be split by a slash e.g. 810 should be 8/10'''

output = ''
for item in soup.find_all('td',class_=['rp-horseTable__spanNarrow rp-horseTable__wgt']):
    output += ("{}, {}".format(' '.join(item['class']),item.text))


output = "".join(line.strip() for line in output.split("rp-horseTable__spanNarrow rp-horseTable__wgt"))
output = output.replace('\n', '')
weights = output.split(',')
temp = []
for item in weights:
    if len(item) == 0:
        pass
    else:
        temp.append(item[13:])

weights = temp

'''Offical record'''

output = ''
for item in soup.find_all('td', {'data-ending':"OR"}):
    output += ("{}, {}".format(' '.join(item['class']),item.text))


output = "".join(line.strip() for line in output.split("rp-horseTable__spanNarrow"))
output = output.replace('\n', '')
ors = output.split(',')
temp = []
for item in ors:
    if len(item) == 0:
        pass
    else:
        temp.append(item[9:])

ors = temp




'''Trainers names'''
output = ''
for item in soup.find_all('a', {'data-test-selector':"link-trainerName"}):
    output += ("{}, {}".format(' '.join(item['class']),item.text))


output = "".join(line.strip() for line in output.split("rp-horseTable__human__link ui-link ui-link_table ui-profileLink js-popupLink"))
output = output.replace('\n', '')
trainers = output.split(',')
temp = []


'''Index wont Fuckin work so had to comment ths one out
for some reason the trainers come back doubled to tried to append every other name to the list'''


'''for item in trainers:
    if len(item) == 0:
        pass 
    elif (index(item)%2) == 0:
        pass
    else:
        temp.append(item[29:])

#trainers = temp

'''

race = []
for i in range(len(horses)):
    race.append(horses[i])
    race.append(jockeys[i])
    race.append(ages[i])
    race.append(topspeed[i])
    race.append(weights[i])
    race.append(ors[i])
    
    
print(race)
print(trainers)