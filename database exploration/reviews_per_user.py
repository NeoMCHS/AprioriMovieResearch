import pandas as pd
import csv
import ast

def reviews_per_user():
    ratings = pd.read_csv("../archive/rating.csv")
    ratings = ratings.drop(columns=['rating', 'timestamp'])

    # Count reviews per user and sort
    review_counts = (
        ratings['userId']
        .value_counts()
        .reset_index()
#        .rename(columns={'index': 'userId', 'userId': 'review_count'})
        .sort_values('count', ascending=False)
    )   
    review_counts.to_csv('../archive/review_counts.csv', index=False)


def prepare_basket_data():

    ratings = pd.read_csv("../archive/final_data.csv")

    filename = "../archive/basket_items_per_user.csv"

    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['userId', 'reviews']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for pair in ratings.values:
            pair = {'userId': pair[0], 'reviews': len(ast.literal_eval(pair[1]))}
            writer.writerow(pair)
    

def sort_baskets():

    ratings = pd.read_csv("../archive/basket_items_per_user.csv")

    sorted = ratings.sort_values("reviews", ascending=False)

    filename = "../archive/user_baskets_sorted.csv"

    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['userId', 'reviews']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for pair in sorted.values:
            pair = {'userId': pair[0], 'reviews': pair[1]}
            writer.writerow(pair)

if __name__ == "__main__":
    prepare_basket_data()
    sort_baskets()
    #reviews_per_user()