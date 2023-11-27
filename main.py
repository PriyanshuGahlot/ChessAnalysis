import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import math
import streamlit as st

data = pd.read_csv("games.csv")

openingsArchetypePopularity = {}
openingsArchetypeWinDrawLoss = {}

st.set_page_config(page_title="Chess Analysis",page_icon="♟")

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

st.title("Analysis of Chess Openings")
st.write("Using data of more that 20,000 chess games and what opening was played in each one of them to analyse how diffrent opeings are played in diffrent ratings, how an opening can effect the probability of wining a game and more")
st.markdown("***")

st.header("Analysing Top Openings")

n = st.text_input("Number of top openings to analyse")

if(n.isdigit()):
    st.markdown("##")
    n = int(n)
    st.subheader("Top "+str(n)+" Opening Popularity")
    top_n_keys_opening = [item[0] for item in list(sortedOpeningsArchetypePopularity.items())[:n]]
    top_n_values_opeinig = [item[1] for item in list(sortedOpeningsArchetypePopularity.items())[:n]]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(top_n_keys_opening, top_n_values_opeinig)
    plt.xticks(rotation=90)
    plt.subplots_adjust(bottom=0.35)
    plt.xlabel("Opening")
    plt.ylabel("Frequency")
    st.pyplot(fig)
    st.markdown("##")
    # plt.show()

    st.subheader("Probability that a random game played will have a particular opening")
    prob = []
    for i in top_n_values_opeinig:
        prob.append(i/len(data["opening_name"]))
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(top_n_keys_opening, prob)
    plt.xticks(rotation=90)
    plt.subplots_adjust(bottom=0.35)
    plt.xlabel("Opening")
    plt.ylabel("Probability of that Opening played")
    st.pyplot(fig)
    st.markdown("##")

    st.subheader("Probability of winning a game if a particular opening is played")
    topnWinRatio = []
    for i in top_n_keys_opening:
        l = openingsArchetypeWinDrawLoss[i]
        topnWinRatio.append(l[0] / (l[0] + l[1] + l[2]))

    stdWinLoss = np.array(topnWinRatio).std()
    # print(stdWinLoss)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(top_n_keys_opening, topnWinRatio)
    plt.xticks(rotation=90)
    plt.subplots_adjust(bottom=0.35)
    plt.axhline(y=0.5, color='green', linestyle='--')
    plt.xlabel("Openings")
    plt.ylabel("Probability of Winning")
    st.pyplot(fig)
    st.write("""
    The analysis reveals a standard deviation of {:.3f} across all probabilities, suggesting that employing different chess openings can provide players with a strategic edge. However, this advantage is observed to be moderate rather than substantial.

The relatively low standard deviation indicates a degree of consistency in game outcomes when employing various openings. While selecting different openings may offer a strategic advantage, the impact on the overall game is not characterized by a significant margin.

This nuanced insight underscores the importance of adaptability in chess strategy. While certain openings may provide a tactical advantage, the limited variability in probabilities implies that the game's outcome is influenced by a combination of factors. Players seeking a competitive edge should consider a diverse repertoire of openings, recognizing that the strategic advantage may not be overwhelmingly pronounced but can contribute to a more well-rounded and adaptable playing style
    """.format(stdWinLoss))

    st.markdown("##")
    # plt.show()

    st.subheader("How Popularity of an Opening effects the probability of winning a game")
    popularities = []
    winRatios = []
    for i in top_n_keys_opening:
        popularities.append(openingsArchetypePopularity[i])
        l = openingsArchetypeWinDrawLoss[i]
        winRatios.append(l[0] / (l[0] + l[1] + l[2]))

    fig, ax = plt.subplots(figsize=(10, 6))
    plt.plot(popularities, winRatios)
    plt.axhline(y=0.5, color='green', linestyle='--')
    plt.ylabel("Probability of Winning")
    plt.xlabel("Frequency of Opening")
    st.pyplot(fig)
    st.write("""
    We observe an interesting trend in chess game outcomes corresponding to the popularity of different openings. In cases where a less popular opening is played, we often see a higher degree of variability in game outcomes. This variability may be attributed to players' limited experience with that particular opening, leading to less predictable outcomes.

On the other hand, as the popularity of an opening increases, we notice a nuanced shift in the probability of winning. Surprisingly, the likelihood of winning tends to decrease with very high popularity levels. One plausible explanation is that highly popular openings become well-studied and widely known, prompting opponents to develop effective defensive strategies. Consequently, players encounter greater challenges in securing victories with these widely recognized openings.

This insight suggests that the relationship between opening popularity and game outcomes is not linear. Instead, it highlights the intricate dynamics of chess strategy, where less-explored openings introduce uncertainty, and extremely popular openings may face stronger defensive responses, making the game outcomes less predictable.
    """)
    # plt.show()

st.markdown("***")
st.header("Analysis of a particular Opening")


openingToAnalize = st.text_input("Name of Opening to Analyse")

if(openingToAnalize in openingsArchetypePopularity.keys()):
    ratings = []
    for opening, rating in zip(data["opening_name"], data["white_rating"]):
        if (opening.split(":")[0] == openingToAnalize):
            ratings.append(rating)

    ratings = sorted(ratings)

    r1 = min(ratings)
    r2 = max(ratings)

    spread = np.linspace(r1, r2, 100)

    ratios = []
    sens = 400

    for i in range(0, len(spread)):
        wins = 0
        count = 0
        for opening, winner, rating in zip(data["opening_name"], data["winner"], data["white_rating"]):
            if (opening == openingToAnalize and math.fabs(spread[i] - rating) < sens):
                count += 1
                if (winner == "white"):
                    wins += 1
        if (count == 0):
            ratios.append(0)
            print("0 at ", ratings[i])
        else:
            ratios.append(wins / count)

    st.write("Probability of winning a game if "+openingToAnalize+" is played with respect to the player's rating")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(spread, ratios)
    plt.axhline(y=0.5, color='green', linestyle='--')
    plt.xlabel("Player's Rating")
    plt.ylabel("Probability of winning")
    plt.title(openingToAnalize)
    st.pyplot(fig)
    st.write("""
    Notably, the analysis reveals a non-linear increase in the probability of winning as the player's rating advances. This trend implies that experienced players tend to have a higher likelihood of success when employing a particular opening. The non-linear nature of this relationship suggests that the advantage gained by experienced players is not proportional but becomes more pronounced with increased expertise.

These findings underscore the importance of considering player experience and skill level when evaluating the effectiveness of chess openings. While the probability of winning is influenced by various factors, the non-linear correlation with player rating emphasizes the strategic significance of experience in leveraging specific openings to achieve success on the chessboard.

The consistent straight line observed at 0 and 1 in the probability distribution can be attributed to the limited availability of data for games played at those ratings.
    """)

    # plt.show()
