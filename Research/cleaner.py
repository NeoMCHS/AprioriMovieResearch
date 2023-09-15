import pandas as pd

# Read your dataset into a Pandas DataFrame
data = pd.read_csv('rating_1.csv')

# Concatenate the data based on userId
concatenated_data = data.groupby('userId')['movieId'].apply(list).reset_index()

# Rename the columns if desired
concatenated_data.columns = ['userId', 'movieIds']

# Write the concatenated data to a CSV file
concatenated_data.to_csv('concatenated_data.csv', index=False)