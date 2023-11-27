import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import math
import streamlit as st

data = pd.read_csv("games.csv")

openingsArchetypePopularity = {}
openingsArchetypeWinDrawLoss = {}

for opening,winner in zip(data["opening_name"],data["winner"]):
    opening = opening.split(":")[0];
    if(openingsArchetypePopularity.__contains__(opening)):
        openingsArchetypePopularity[opening] += 1
    else:
        openingsArchetypePopularity[opening] = 1
    if(openingsArchetypeWinDrawLoss.__contains__(opening)):
        winDrawLoss = openingsArchetypeWinDrawLoss[opening]
        if(winner=="white"):
            winDrawLoss[0] += 1
        elif(winner=="black"):
            winDrawLoss[2]+=1
        elif(winner=="draw"):
            winDrawLoss[1]+=1
        openingsArchetypeWinDrawLoss[opening] = winDrawLoss
    else:
        openingsArchetypeWinDrawLoss[opening] = [0,0,0]

sortedOpeningsArchetypePopularity = dict(sorted(openingsArchetypePopularity.items(),key=lambda item: item[1],reverse=True))
print(sortedOpeningsArchetypePopularity)
print(openingsArchetypeWinDrawLoss)

n = 50

top_n_keys_opening = [item[0] for item in list(sortedOpeningsArchetypePopularity.items())[:n]]
top_n_values_opeinig = [item[1] for item in list(sortedOpeningsArchetypePopularity.items())[:n]]
# plt.bar(top_10_keys_opening,top_10_values_opeinig)
# plt.xticks(rotation=90)
# plt.subplots_adjust(bottom=0.35)
# plt.show()

topnWinRatio = []
for i in top_n_keys_opening:
    l = openingsArchetypeWinDrawLoss[i]
    topnWinRatio.append(l[0]/(l[0]+l[1]+l[2]))

stdWinLoss = np.array(topnWinRatio).std()
#print(stdWinLoss)

# plt.bar(top_n_keys_opening, topnWinRatio)
# plt.xticks(rotation=90)
# plt.subplots_adjust(bottom=0.35)
# plt.axhline(y=0.5, color='green', linestyle='--')
# plt.show()

openingToAnalize = "Sicilian Defense"

ratings = []
for opening,rating in zip(data["opening_name"],data["white_rating"]):
    if(opening.split(":")[0]==openingToAnalize):
        ratings.append(rating)

ratings = sorted(ratings)


r1 = min(ratings)
r2 = max(ratings)

spread = np.linspace(r1,r2,100)

ratios = []
sens = 400

for i in range(0,len(spread)):
    wins = 0
    count = 0
    for opening, winner, rating in zip(data["opening_name"], data["winner"], data["white_rating"]):
        if (opening == openingToAnalize and math.fabs(spread[i]-rating)<sens):
            count+=1
            if(winner=="white"):
                wins+=1
    if(count==0):
        ratios.append(0)
        print("0 at ",ratings[i])
    else:
        ratios.append(wins / count)

# plt.plot(spread,ratios)
# plt.axhline(y=0.5, color='green', linestyle='--')
# plt.xlabel("Players Rating")
# plt.ylabel("Win %")
# plt.title(openingToAnalize)
# plt.show()


popularities = []
winRatios = []
for i in top_n_keys_opening:
    popularities.append(openingsArchetypePopularity[i])
    l = openingsArchetypeWinDrawLoss[i]
    winRatios.append(l[0]/(l[0]+l[1]+l[2]))

# plt.plot(popularities,winRatios)
# plt.axhline(y=0.5, color='green', linestyle='--')
# plt.show()
