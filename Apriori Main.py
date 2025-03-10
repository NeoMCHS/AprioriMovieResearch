from efficient_apriori import apriori
import pandas as pd
from timeit import default_timer
import matplotlib.pyplot as plt
from pathlib import Path

ratings = pd.read_csv("./archive/rating.csv")

def identify_users(movieId: int, threshold_original_movie: int, verbose: bool = False):
    """
    Identifies users which have ranked a film above a certain threshold\n
    movieId (int) - the internal identificator of a movie we want to identify relevant users for\n
    threshold_original_movie (int) - regulates the rating threshold\n
    verbose (bool) - regulates console output 
    """

    relevant_reviews = ratings[ratings["movieId"] == movieId]
    satisfied_users = relevant_reviews[relevant_reviews['rating'] >= threshold_original_movie]

    baskets = pd.read_csv("./archive/user_baskets_sorted.csv")

    baskets = baskets["userId"]

    baskets = list(baskets.head(100))

    if len(satisfied_users['userId']) <= 100 and verbose == True and len(list(set(satisfied_users['userId']) & set(baskets))) > 0:
        print(f"{movieId} users intersectection - {list(set(satisfied_users['userId']) & set(baskets))}")

    if verbose == True:
        print(f"{movieId} total relevant baskets - {len(satisfied_users['userId'])}")

    return list(satisfied_users['userId'])

def create_viewing_histories(userIds: list, threshold_recommended_movies: int, verbose: bool = False):
    '''
    Accepts a list of users and outputs a list containing "viewing histories" (lists of movieIds of movies which were rated highly\n
    userIds (list) - list of users\n
    threshold_recommended_movies (int) - regulates the rating threshold\n
    verbose (bool) - regulates console output 
    '''
    ratings['check'] = ratings.userId.isin(userIds)
    viewing_histories_df = ratings[ratings['check'] == True]
    viewing_histories_df = viewing_histories_df[viewing_histories_df['rating'] >= threshold_recommended_movies]
    viewing_histories_df = viewing_histories_df[['userId', 'movieId']]
    viewing_history = viewing_histories_df[viewing_histories_df.duplicated('userId', keep=False)].groupby('userId')['movieId'].apply(tuple).reset_index()

    if verbose == True:
        intersection = set.intersection(*map(set,list(viewing_history['movieId'])))
        print(f"length of intersection between relevant baskets - {len(intersection)}\nintersection between relevant baskets - {intersection}\n")

    return list(viewing_history['movieId'])

def pipeline(movieId: int, rating_threshold: int = 4,  min_support: float = 0.3, min_confidence: float = 1.0, max_length: int = 2, output_format: int = 0, update: bool = False, verbose: bool = False) -> list|int:
    """
    The main pipeline of the experiment. Accepts movieId and writes rules in the "rules" folder.\n
    movieId (int) - the movieId we want to get rules for\n
    rating_threshold (int) - regulates threshold values throughout the process\n
    min_support (float) - a value from 0 to 1.0 which represents the minimal support level\n
    min_confidence (float) - a value from 0 to 1.0 which represents the minimal confidence level\n
    max_length (int) - maximum length of rules generated\n
    output_format (int) - set to 0 for the function to return rules generated, set to 1 to return amount of rules generated\n
    update (bool) - when set to false, function will skip generating rules if they already exist. Set to True when changing any variables and rerunning the pipeline for the same movieId!\n
    verbose (bool) -  regulates console output\n
    """
    start = default_timer()
    users = identify_users(movieId, rating_threshold)

    if verbose == True:
        print("------------------------------------")

    name = "./rules/rules_support" + str(min_support) + "_movieid"+ str(movieId) + ".txt"

    my_file = Path(name)
    if my_file.is_file() and update == False:
        if verbose == True:
            print("File already exists, skipping")
    else:
        baskets = create_viewing_histories(users, rating_threshold, verbose=verbose)

        itemsets, rules = apriori(baskets, min_support=min_support, min_confidence=min_confidence, max_length=max_length, output_transaction_ids = True)

        with open(name, "w") as file:
            if verbose == True:
                print("Writing results...")
            file.write(f"movieId = {movieId}\nmin support - {str(min_support)}\nmin confidence - {str(min_confidence)}\nmax length - {str(max_length)}\namount of rules - {str(len(rules))}\n")
            for i in rules:
                file.write(str(i) + "\n")
        if verbose == True:
            print("Done!")

        runtime = default_timer() - start
        if verbose == True:
            print ("Elapsed time(sec): ", round(runtime,2))

        if output_format == 0:
            return rules
        elif output_format == 1:
            return len(rules)

    runtime = default_timer() - start
    if verbose == True:
        print ("Elapsed time(sec): ", round(runtime,2))
    with open(name, "r") as file:
        for i, line in enumerate(file):
            if i == 4:
                rules = [int(s) for s in line.split() if s.isdigit()]
            elif i > 4:
                break
    
    if output_format == 0:
        itemsets, rules = apriori(baskets, min_support=min_support, min_confidence=min_confidence, max_length=max_length, output_transaction_ids = True)
        return rules
    elif output_format == 1:
        return rules[0]

def investigate_support_levels(update):
    """
    This function was used to fine-tune minimal support level. Creates plots and writes them to the "plots" folder.\n
    update (bool) - passes the update argument to the pipeline() function
    """
    movieids = []

    lower_bound = int(input("enter exact lower bound: "))
    upper_bound = int(input("enter exact upper bound: "))+1

    for j in range(lower_bound, upper_bound):

        rules_len = []

        support_vals = []

        for i in range(1, 9):
            rules = pipeline(movieId=j, min_support=(i/10), output_format=1, rating_threshold=4, update=update)
            rules_len.append(rules)
            support_vals.append((i/10))

        movieids.append(j)
        plt.plot(support_vals, rules_len, label=f"movieid {j}")

    plt.title(f"Destribution for movieids {movieids[0]}-{movieids[-1]}")
    plt.xlabel("min support")
    plt.ylabel("rules")
    if (upper_bound - lower_bound) < 15:
        plt.legend(loc='best')
    plt.savefig(f"./plots/{movieids[0]}-{movieids[-1]}", dpi=200)

def translate(movieId, min_support: float = 0.3):
    '''
    This function translates rules generated by the pipeline() function.\n
    movieId (int) - specifies the movieId rules for which we want to translate\n
    min_support (float) - a value from 0 to 1.0 which helps to identify the correct file
    '''
    target = f"./rules/rules_support{min_support}_movieid{movieId}.txt"
    movies = pd.read_csv("./archive/movie.csv")
    path = f"./translations/translation_support{min_support}_movieid{movieId}.txt"

    with open(path, "w") as save_file:
        save_file.write(f"movieId = {movieId}\nmin support - {str(min_support)}\n")
        with open(target, "r") as file:
            for i, line in enumerate(file):
                line = line.replace("}", "").replace("{", "")
                if i > 4:
                    films = [int(s) for s in line.split() if s.isdigit()]
                    for film in films:
                        relevant_record = movies.loc[movies['movieId'] == film]
                        title = relevant_record["title"].values[0]
                        save_file.write(str(title) + " ")
                    save_file.write("\n")

if __name__ == "__main__":
    #investigate_support_levels(update=True)
    #translate(12)
    pipeline(1, 4, update=True)