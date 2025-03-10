import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def get_ratings_over_years():
    ratings = pd.read_csv("../archive/rating.csv")

    ratings.timestamp = pd.to_datetime(ratings.timestamp)
    ratings.timestamp = ratings.timestamp.dt.year

    fig, ax1 = plt.subplots(figsize=(10,5))

    dftmp = ratings[['rating', 'timestamp']].groupby('timestamp')
    ax1.plot(dftmp.timestamp.first(), dftmp.rating.count())
    ax1.grid(None)
    ax1.set_ylim(0,)

    ax1.set_xlabel('Year')
    ax1.set_ylabel('Number of ratings')
    plt.title('Ratings per year')
    plt.show()


def get_popularity_dynamic(movieId: int):
    ratings = pd.read_csv("../archive/rating.csv")

    relevant_reviews = ratings.loc[ratings['movieId'] == movieId]
    relevant_reviews.timestamp = pd.to_datetime(relevant_reviews.timestamp)
    relevant_reviews.timestamp = relevant_reviews.timestamp.dt.year

    fig, ax1 = plt.subplots(figsize=(10,5))

    dftmp = relevant_reviews[['rating', 'timestamp']].groupby('timestamp')

    ax1.plot(dftmp.timestamp.first(), dftmp.rating.mean())
    ax1.grid(None)
    ax1.set_ylim(0,)

    ax1.set_xlabel('Year')
    ax1.set_ylabel('Mean rating')
    plt.title(f'Rating dynamic for movie with movieId {movieId}')
    plt.show()

    #fig = plt.figure(figsize = (10, 5))

    plt.bar(dftmp.timestamp.first(), dftmp.rating.count(), color ='maroon', width = 0.4)

    plt.xlabel("Year")
    plt.ylabel("Amount of reviews")
    plt.title(f"Amount of reviews per year for movieId {movieId}")
    plt.show()

get_popularity_dynamic(int(input("Enter movieId (from 1 to 131262): ")))

#get_ratings_over_years()