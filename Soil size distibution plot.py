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


# Sizes and cumulative passing values
sizes = [2.0, 1.18, 0.63, 0.425, 0.30, 0.15]

# To make the curve look complete, let's include a point for 100% passing at a larger size, e.g., 4.0 mm
# since the largest category is >2.0 mm, all particles are assumed to be smaller than some upper limit like 4.0 mm.
sizes_extended = [4.0] + sizes
cum_passing_extended = {
    'Day 1 — 30 cm (%)': [100.0, 76.9, 71.5, 67.6, 60.4, 50.4, 21.4],
    'Day 1 — 60 cm (%)': [100.0, 82.2, 76.6, 68.8, 55.7, 38.8, 15.9],
    'Day 2 — 30 cm (%)': [100.0, 88.5, 82.7, 74.9, 63.0, 48.1, 15.1],
    'Day 2 — 60 cm (%)': [100.0, 93.0, 87.5, 79.0, 68.7, 54.0, 16.2]
}

# Clear any existing plots
plt.clf()

# Plotting each sample
styles = {'Day 1 — 30 cm (%)': '-o', 'Day 1 — 60 cm (%)': '--s', 'Day 2 — 30 cm (%)': '-.^', 'Day 2 — 60 cm (%)': ':d'}

for label, values in cum_passing_extended.items():
    plt.plot(sizes_extended, values, styles[label], label=label.replace(' (%)', ''))

# Formatting the chart
plt.xscale('log')
plt.xlim(4.5, 0.1) # Invert X-axis as is conventional in particle size charts (large to small)
plt.xticks([4.0, 2.0, 1.18, 0.63, 0.425, 0.30, 0.15], ['4.0', '2.0', '1.18', '0.63', '0.425', '0.30', '0.15'])
plt.xlabel('Particle Size (mm)')
plt.ylabel('Cumulative Percent Passing (%)')
plt.title('Particle Size Distribution Curve')
plt.ylim(0, 105)
plt.grid(True, which="both", ls="--", color='0.7')
plt.legend(loc='lower left')
plt.tight_layout()

# Save the plot
plt.savefig('particle_size_distribution_curve.png', dpi=300)
print("Saved cumulative curve successfully.")
