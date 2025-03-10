import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

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

