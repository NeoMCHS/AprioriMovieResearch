import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#The four tiers present are:
#1st tier - from positive infinity to 2000
#2nd tier - from 1999 to 1000
#3rd tier - from 999 to 100
#4th tier - from 99 to 0

tier_values = [0, 0, 0, 0]

ratings = pd.read_csv("/Users/fedya/Documents/Research paper/archive/rating.csv")

review_per_user = np.array(ratings["userId"].value_counts())

#users = np.array(ratings["userId"].unique())

reviews_per_tier = [0, 0, 0, 0]

for review_count in review_per_user:
    if review_count >= 2000:
        reviews_per_tier[0] = reviews_per_tier[0] + review_count
        tier_values[0] += 1
    if review_count < 2000 and review_count >= 1000:
        reviews_per_tier[1] = reviews_per_tier[1] + review_count
        tier_values[1] +=1
    if review_count < 1000 and review_count >= 100:
        reviews_per_tier[2] = reviews_per_tier[2] + review_count
        tier_values[2] += 1
    if review_count < 100:
        reviews_per_tier[3] = reviews_per_tier[3] + review_count
        tier_values[3] += 1

for i in range(len(reviews_per_tier)):
    reviews_per_tier[i] = round(reviews_per_tier[i]/100)

converter = []

for i in range(len(tier_values)):
    if i == 0:
        tier = 1
    if i == 1:
        tier = 2
    if i == 2:
        tier = 3
    if i == 3:
        tier = 4
    for iterations in range(tier_values[i]):
        converter.append(tier)

tier_values = pd.Series(converter)

converer_2 = []

for i in range(len(reviews_per_tier)):
    if i == 0:
        tier = 1
    if i == 1:
        tier = 2
    if i == 2:
        tier = 3
    if i == 3:
        tier = 4
    for iterations in range(reviews_per_tier[i]):
        converer_2.append(tier)

reviews_per_tier = pd.Series(converer_2)

df = pd.concat([tier_values.value_counts(), reviews_per_tier.value_counts()], axis=1, sort=True)
df.columns = ["Users", "Reviews"]

df.plot(kind="bar")
plt.show()