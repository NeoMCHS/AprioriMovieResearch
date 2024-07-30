import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import statistics

ratings = pd.read_csv("/Users/fedya/Documents/Research paper/archive/rating.csv")
primieres = pd.read_csv("/Users/fedya/Documents/Research paper/premiere_years.csv")

ratings.timestamp = pd.to_datetime(ratings.timestamp)

primiere_year = primieres.premiere
movieId = primieres.movieId

primiere_year = pd.to_datetime(primiere_year, format='%Y')

ratings_premiere = []

ratings_postpremiere = []

for i in range(primiere_year.size):
    relevant_premiere = primiere_year[i]
    relevant_movieId = movieId[i]
    print(f"exploring movieId {relevant_movieId}")
    relevant_ratings = ratings[ratings['movieId'] == relevant_movieId]

    close_premiere_ratings = relevant_ratings[relevant_ratings['timestamp'] < relevant_premiere + pd.DateOffset(years=2)]

    ratings_premiere.append(close_premiere_ratings.size)

    ratings_postpremiere.append(relevant_ratings.size - close_premiere_ratings.size)

print(f"average premiere window reviews - {statistics.mean(ratings_premiere)}")
print(f"average post-premiere reviews - {statistics.mean(ratings_postpremiere)}")