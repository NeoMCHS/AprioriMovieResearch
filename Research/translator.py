import csv
from concurrent.futures import ProcessPoolExecutor

def get_data() -> dict:
    movies = {}

    with open("archive/movie.csv", "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        fields = next(reader)

        for row in reader:
            movies[row[0]] = row[1]
    
    return movies

def main():
    import re

    with open("rules/rules19.txt", "r") as i:
        rules_id = i.read()
    
    movies = get_data()

    keys = (re.escape(k) for k in movies.keys())
    pattern = re.compile(r'\b(' + '|'.join(keys) + r')\b')
    rules_name = pattern.sub(lambda x: movies[x.group()], rules_id)

    with open("translations/translation19.txt", "w") as o:
        o.write(rules_name)

if __name__ == "__main__":
    main()