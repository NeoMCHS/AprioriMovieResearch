from efficient_apriori import apriori
import pandas as pd
import numpy as np
from tqdm import tqdm
from timeit import default_timer

# Before running this code ensure that you replace ALL of the csv and txt references
# Pipeline function will write a txt file with the rules generated. It requires a txt file that holds a single number that marks what iteration is the programm on
# Without it the programm will rewrite the same document

ratings = pd.read_csv("/Users/fedya/Documents/Research paper/archive/rating.csv")

def identify_users(movieId: int, threshold_original_movie: int):
    #this function relies on good reviews to ensure more relvant baskets

    relevant_reviews = ratings[ratings["movieId"] == movieId]
    satisfied_users = relevant_reviews[relevant_reviews['rating'] >= threshold_original_movie]
    return list(satisfied_users['userId'])

def identify_users_list(movieIds: list):
    #this function accepts viewing history so we hawe made a decision to forsake the threshold for the sake of both simplicity and wider selection
    #as if we would apply threshold to a relatively large list we would likely not get any results

    viewing_histories = ratings[ratings.duplicated('movieId', keep=False)].groupby('movieId')['userId'].apply(list).reset_index()
    viewing_histories["check"] = viewing_histories.movieId.isin(movieIds)
    relevant_reviewers = viewing_histories[viewing_histories["check"] == True]
    viewers_set = list(relevant_reviewers['userId'])
    return list(set.intersection(*map(set,viewers_set)))

def create_viewing_histories(userIds: list, threshold_recommended_movies: int):
    ratings['check'] = ratings.userId.isin(userIds)
    viewing_histories_df = ratings[ratings['check'] == True]
    viewing_histories_df = viewing_histories_df[viewing_histories_df['rating'] >= threshold_recommended_movies]
    viewing_histories_df = viewing_histories_df[['userId', 'movieId']]
    viewing_history = viewing_histories_df[viewing_histories_df.duplicated('userId', keep=False)].groupby('userId')['movieId'].apply(tuple).reset_index()
    return list(viewing_history['movieId'])

def pipeline(movieId: int|list, min_support: float = 0.3, min_confidence: float = 0.9, max_length: float = 4.0):
    start = default_timer()
    if type(movieId) == int:
        users = identify_users(movieId, 4)
    if type(movieId) == list:
        users = identify_users_list(movieId)

    baskets = create_viewing_histories(users, 4)

    itemsets, rules = apriori(tqdm(baskets), min_support=min_support, min_confidence=min_confidence, max_length=max_length, output_transaction_ids = True)

    with open("/Users/fedya/Documents/Research paper/archive/rules/iteration.txt", "r") as file:
        it = file.read()

    name = "/Users/fedya/Documents/Research paper/archive/rules/rules" + str(it) + ".txt"

    print("Writing results...")

    with open(name, "w") as file:
        file.write(f"movieId = {movieId}\nmin support - {str(min_support)}\nmin confidence - {str(min_confidence)}\nmax length - {str(max_length)}\n")
        for i in rules:
            file.write(str(i) + "\n")
    
    it = int(it) + 1

    with open("/Users/fedya/Documents/Research paper/archive/rules/iteration.txt", "w") as file:
        file.write(str(it))
    
    print("Done!")

    runtime = default_timer() - start
    print ("Elapsed time(sec): ", round(runtime,2))

if __name__ == "__main__":
    mode = int(input("Choose mode. 0 for single movie, 1 for a list of movies: "))

    if mode == 0:
            movieId = int(input("Input movieId for which to generate rules: "))
    if mode == 1:
        #the list mode does not work well :(
        movieId = input("Input movieIds separating them by a comma ('1, 2, 3') for which to generate rules: ").split(", ")
        movieId = list(map(int, movieId))

    #min_support = float(input("enter min_support"))
    #min_confidence = float(input("enter min_confidence"))
    #max_length = float(input("enter max_length"))

    pipeline(movieId=movieId)