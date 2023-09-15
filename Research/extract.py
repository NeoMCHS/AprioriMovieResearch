import csv

def extract_data(input_file, output_file, attribute, threshold):
    with open(input_file, 'r', newline='') as input_csv:
        reader = csv.DictReader(input_csv)
        data = [row for row in reader if float(row[attribute]) >= threshold]

    with open(output_file, 'w', newline='') as output_csv:
        fieldnames = ['userId', 'movieId', 'rating','timestamp']
        writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

if __name__ == "__main__":
    input_file = "rating.csv"
    output_file = "rating_1.csv"
    attribute_to_check = "rating"
    threshold_value = 3.5
    extract_data(input_file, output_file, attribute_to_check, threshold_value)
