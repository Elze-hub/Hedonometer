# Task 2.1 Distribution of happiness scores

import pandas as pd

# Read the cleaned data from the processed directory
data = pd.read_csv('../data/processed/hedonometer_data.csv')

# Calculate the distribution of happiness scores
## Plot a histogram of happiness_average
import matplotlib.pyplot as plt
plt.hist(data['happiness_average'].dropna(), bins=20, edgecolor='black')
plt.title('Distribution of Happiness Scores')
plt.xlabel('Happiness Average')
plt.ylabel('Frequency')
plt.grid(axis='y', alpha=0.75)
plt.show()

## Compute summary statistics for happiness_average
### Mean
mean_happiness = data['happiness_average'].mean()
### Median
median_happiness = data['happiness_average'].median()
### Standard Deviation
std_happiness = data['happiness_average'].std()
### 5th and 95th percentiles
percentiles = data['happiness_average'].quantile([0.05, 0.95])

## Print summary statistics
print(f"Mean Happiness Average: {mean_happiness:.2f}")
print(f"Median Happiness Average: {median_happiness:.2f}")
print(f"Standard Deviation of Happiness Average: {std_happiness:.2f}")
print(f"5th Percentile of Happiness Average: {percentiles[0.05]:.2f}")
print(f"95th Percentile of Happiness Average: {percentiles[0.95]:.2f}")


