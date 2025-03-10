import csv
import pandas as pd

#run this script if you want to run any database exploration scripts

def extract_data(input_file, output_file, attribute, threshold):
    with open(input_file, 'r', newline='') as input_csv:
        reader = csv.DictReader(input_csv)
        data = [row for row in reader if float(row[attribute]) >= threshold]

    with open(output_file, 'w', newline='') as output_csv:
        fieldnames = ['userId', 'movieId', 'rating', 'timestamp']
        writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def finalize(input_file, output_file):
    data = pd.read_csv(input_file)
    concatenated_data = data.groupby('userId')['movieId'].agg(list).reset_index()
    concatenated_data.columns = ['userId', 'movieIds']
    concatenated_data.to_csv(output_file, index=False)

if __name__ == "__main__":
    input_file = "./archive/rating.csv"
    intermediate_file = "./archive/reviews_rating_restricted.csv"
    final_file = "./archive/final_data.csv"
    attribute_to_check = "rating"
    threshold_value = 4
    extract_data(input_file, intermediate_file, attribute_to_check, threshold_value)
    finalize(intermediate_file, final_file)
