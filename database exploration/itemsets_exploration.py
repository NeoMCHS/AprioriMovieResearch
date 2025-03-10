import pandas as pd

baskets = pd.read_csv('../archive/basket_items_per_user.csv')

average = baskets.loc[:, 'reviews'].mean()

permutations = 1

for i in range(0, 3):
    positions = int(average)
    for j in range(i+1):
        permutations = permutations*(positions-j)
        print(permutations)
    print(f"permutations with max_length {i} = {permutations}")
    permutations = 1

print(average)