import plotly.graph_objects as go
import json
from datetime import date

today = date.today()

# Saving adverts data to variable 'data'
with open(f'advertscrape/adverts_{today}.json',encoding='utf-8') as json_file:
    data = json.load(json_file)

# 1. the count of cars in advertismets with the particular model year
yearDict = {}
for advert in data:
    for section in advert:
        if(section == "Izlaiduma gads:"):
            year = int(''.join(filter(str.isdigit, advert[section])))
            if year in yearDict:
                yearDict[year] += 1
                
            else:
                yearDict[year] = 1

listOfKeys = []
listOfValues = []
for year in sorted(yearDict.keys()):
    listOfKeys.append(year)
    listOfValues.append(yearDict[year])

# Use textposition='auto' for direct text
fig = go.Figure(data=[go.Bar(
            x=listOfKeys, y=listOfValues,
            text=listOfValues,
            textposition='auto',
        )])

fig.show()



# 2. Car makes with and without TI (Technical Inspection) 
carMakesWithTI = {}
carMakesWithOutTI = {}
for advert in data:
    for section in advert:
        if (section == "Marka"):
                make = advert[section]

        if (section == "Tehniskā apskate:" and advert[section] == "Bez apskates"): # with out TI!
            if make in carMakesWithOutTI:
                carMakesWithOutTI[make] += 1
            else:
                carMakesWithOutTI[make] = 1
        elif (section == "Tehniskā apskate:" and advert[section] != "Bez apskates"): # with TI!
            if make in carMakesWithTI:
                carMakesWithTI[make] += 1
            else:
                carMakesWithTI[make] = 1

listOfKeysWithTI = []
listOfKeysWithOutTI = []
listOfValuesWithTI = []
listOfValuesWithOutTI = []
for make in sorted(carMakesWithTI.keys()):
    listOfKeysWithTI.append(make)
    listOfValuesWithTI.append(carMakesWithTI[make])
for make in sorted(carMakesWithOutTI.keys()):
    listOfKeysWithOutTI.append(make)
    listOfValuesWithOutTI.append(carMakesWithOutTI[make])

fig = go.Figure(data=[
    go.Bar(name='Has TI', x=listOfKeysWithTI, y=listOfValuesWithTI),
    go.Bar(name='Does not have TI', x=listOfKeysWithOutTI, y=listOfValuesWithOutTI)
])
# Change the bar mode
fig.update_layout(barmode='stack')
fig.show()



# 3. diesel vs petrol
carMakesDiesel = {}
carMakesPetrol = {}
for advert in data:
    for section in advert:
        if (section == "Marka"):
                make = advert[section]

        if (section == "Motors:" and "dīzelis" in advert[section]): # Diesel
            if make in carMakesDiesel:
                carMakesDiesel[make] += 1
            else:
                carMakesDiesel[make] = 1
        elif (section == "Motors:" and "benzīns" in advert[section]): # Petrol
            if make in carMakesPetrol:
                carMakesPetrol[make] += 1
            else:
                carMakesPetrol[make] = 1

listOfKeysPetrol = []
listOfKeysDiesel = []
listOfValuesPetrol = []
listOfValuesDiesel = []
for petrol in sorted(carMakesPetrol.keys()):
    listOfKeysPetrol.append(petrol)
    listOfValuesPetrol.append(carMakesPetrol[petrol])
for diesel in sorted(carMakesDiesel.keys()):
    listOfKeysDiesel.append(diesel)
    listOfValuesDiesel.append(carMakesDiesel[diesel])

fig = go.Figure(data=[
    go.Bar(name='Petrol', x=listOfKeysPetrol, y=listOfValuesPetrol),
    go.Bar(name='Diesel', x=listOfKeysDiesel, y=listOfValuesDiesel)
])
# Change the bar mode
fig.update_layout(barmode='stack')
fig.show()



# 4. Pie chart (Car makes and the count of the cars of this make)
carMakes = {}
for advert in data:
    for section in advert:
        if(section == "Marka"):
            make = advert[section]
            if make in carMakes:
                carMakes[make] += 1
            else:
                carMakes[make] = 1

listOfKeys = []
listOfValues = []
for make in sorted(carMakes.keys()):
    listOfKeys.append(make)
    listOfValues.append(carMakes[make])


labels = listOfKeys # x
values = listOfValues # y

fig = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='label+percent',
                             insidetextorientation='radial'
                            )])
fig.update_traces(textposition='inside')
fig.show()