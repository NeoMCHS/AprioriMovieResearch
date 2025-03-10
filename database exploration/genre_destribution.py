import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

movies = pd.read_csv("../archive/movie.csv")

movies.sort_values(by='movieId', inplace=True)
movies.reset_index(inplace=True, drop=True)

movies['year'] = movies.title.str.extract("\((\d{4})\)", expand=True)
movies.year = pd.to_datetime(movies.year, format='%Y')
movies.year = movies.year.dt.year 
movies.title = movies.title.str[:-7]

genres_unique = pd.DataFrame(movies.genres.str.split('|').tolist()).stack().unique()
genres_unique = pd.DataFrame(genres_unique, columns=['genre'])
movies = movies.join(movies.genres.str.get_dummies().astype(bool))
movies.drop('genres', inplace=True, axis=1)

movies.sort_values(by='movieId', inplace=True)
movies.reset_index(inplace=True, drop=True)

dftmp = movies[['movieId', 'year']].groupby('year')
df = pd.DataFrame({'All_movies' : dftmp.movieId.nunique().cumsum()})

for genre in genres_unique.genre:
    dftmp = movies[movies[genre]][['movieId', 'year']].groupby('year')
    df[genre]=dftmp.movieId.nunique().cumsum()
df.fillna(method='ffill', inplace=True)

plt.figure(figsize=(15,7))
barlist = df.iloc[-1].plot.bar()
barlist.patches[0].set_color('b') 
plt.xticks(rotation='vertical')
plt.title('Movies per genre tag')
plt.xlabel('Genre')
plt.ylabel('Number of movies tagged')
plt.show()