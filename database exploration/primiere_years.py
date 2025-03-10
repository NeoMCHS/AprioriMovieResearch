import matplotlib.pyplot as plt
import pandas as pd
import csv

movies = pd.read_csv("../archive/movie.csv")

titles = movies.title
movieIds = movies.movieId

for title in titles:
    pub_year = title[-5:-1]

records = []

for i in range(titles.size):
    pair = {'movieId': movieIds[i], 'premiere': titles[i][-5:-1]}
    records.append(pair)

filename = "../archive/premiere_years.csv"

with open(filename, 'w', newline='') as csvfile:
    fieldnames = ['movieId', 'premiere']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for pair in records:
        writer.writerow(pair)
