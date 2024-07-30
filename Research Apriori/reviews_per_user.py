import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import csv

ratings = pd.read_csv("/Users/fedya/Documents/Research paper/archive/rating.csv")

review_per_user = np.array(ratings["userId"].value_counts())

users = np.array(ratings["userId"].unique())

fig, ax1 = plt.subplots(figsize=(10,5))

records = []

for i in range(users.size):
    pair = {'userId': users[i], 'reviews': review_per_user[i]}
    records.append(pair)

filename = "/Users/fedya/Documents/Research paper/reviews_per_user.csv"

with open(filename, 'w', newline='') as csvfile:
    fieldnames = ['userId', 'reviews']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for pair in records:
        writer.writerow(pair)

#ax1.plot(users, review_per_user)
#ax1.grid(None)
#ax1.set_ylim(0,)

#ax1.set_xlabel('User')
#ax1.set_ylabel('Number of reviews left')
#plt.title('Reviews per user')
#plt.show()