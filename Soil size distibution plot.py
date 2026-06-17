import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Data from the user
data = {
    'Sieve': ['>2.0', '1.18–2.0', '0.63–1.18', '0.425–0.63', '0.30–0.425', '0.15–0.30', '<0.15'],
    'Day 1 — 30 cm (%)': [23.1, 5.4, 3.9, 7.2, 10.0, 29.0, 21.4],
    'Day 1 — 60 cm (%)': [17.9, 5.6, 7.8, 13.1, 16.9, 22.9, 15.9],
    'Day 2 — 30 cm (%)': [11.5, 5.8, 7.8, 11.9, 14.9, 33.0, 15.1],
    'Day 2 — 60 cm (%)': [6.9, 5.5, 8.5, 10.3, 14.7, 37.8, 16.2]
}

df = pd.DataFrame(data)
print("Original DataFrame:")
print(df)

# Sieve sizes corresponding to the boundaries (upper limit of what passes through)
# >2.0 means retained on 2.0, so passing 2.0 is the sum of everything else.
# Sizes: 2.0, 1.18, 0.63, 0.425, 0.30, 0.15
sizes = [2.0, 1.18, 0.63, 0.425, 0.30, 0.15]

# Let's compute the cumulative percent passing for each boundary size.
# For each column, cumulative percent passing at size[i] is the sum of rows from i+1 to the end.
# Let's verify: 
# at 2.0 mm: sum of rows 1 to 6 (which is 100 - row 0)
# at 1.18 mm: sum of rows 2 to 6
# ...
# at 0.15 mm: row 6 (<0.15)

cum_passing = {col: [] for col in df.columns[1:]}

for col in df.columns[1:]:
    total = df[col].sum()
    current_passing = total
    for i in range(len(sizes)):
        current_passing -= df.iloc[i][col]
        cum_passing[col].append(current_passing)

print("\nComputed Cumulative Passing (%):")
for col in cum_passing:
    print(f"{col}: {cum_passing[col]}")