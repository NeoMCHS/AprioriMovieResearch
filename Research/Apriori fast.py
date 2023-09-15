import csv 
from efficient_apriori import apriori
from tqdm import tqdm

def CandyCrush():
    L = []
    with open('final_data.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=("userId", "movieIds"))
        for row in reader:
            if row["userId"] == "userId":
                continue
            a = row["movieIds"].strip('[]')
            L.append(tuple(a.split(", ")))
    return L

data = CandyCrush()

min_support = float(input("enter min_support"))
min_confidence = float(input("enter min_confidence"))
max_length = float(input("enter max_length"))

itemsets, rules = apriori(tqdm(data), min_support=min_support, min_confidence=min_confidence, max_length=max_length)

with open("iteration.txt", "r") as file:
    it = file.read()

print(it)

name = "rules/rules" + str(it) + ".txt"

with open(name, "w") as file:
    file.write(f"min support - {str(min_support)} \nmin confidence - {str(min_confidence)} \nmax length - {str(max_length)}\n")
    for i in rules:
        file.write(str(i) + "\n")
    
it = int(it) + 1

with open("iteration.txt", "w") as file:
    file.write(str(it))