import pandas as pd
import numpy as np
import csv

ratings = pd.read_csv("/Users/fedya/Documents/Research paper/archive/rating.csv")

movies = pd.read_csv("/Users/fedya/Documents/Research paper/archive/movie.csv")

total_users = len(ratings['userId'].unique())

viewing_histories = ratings[ratings.duplicated('movieId', keep=False)].groupby('movieId')['userId'].apply(list).reset_index()

records = []

user_bases = viewing_histories["userId"]

movieIds = viewing_histories['movieId']

for i in range(movieIds.size):
    percentage = len(user_bases[i])/total_users
    movie_title = movies[movies.movieId == movieIds[i]].title.item()
    if percentage > 0.10:
        pair = (movie_title,movieIds[i],percentage)
        records.append(pair)

#print(records)
print(len(records))

top3 = [(0,0,0.0001), (0,0,0.0002), (0,0,0.0003)]

for pair in records:
    for i in range(len(top3)):
        if pair[2] > top3[i][2]:
            top3[i] = pair
            break
            

print(top3)

"""
for i in range(movieIds.size):
    percentage = len(user_bases[i])/total_users 
    pair = {'movieId': movieIds[i], 'percentage': percentage}
    records.append(pair)

filename = "/Users/fedya/Documents/Research paper/archive/frequency.csv"

with open(filename, 'w', newline='') as csvfile:
    fieldnames = ['movieId', 'percentage']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for pair in records:
        writer.writerow(pair)
"""