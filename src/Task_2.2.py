# Task 2.2 Disagreement: which words are "contested"?

import pandas as pd
## Read the cleaned data from the processed directory
data = pd.read_csv('../data/processed/hedonometer_data.csv')

## Plot happiness_average (x-axis) vs. happiness_standard_deviation (y-axis) as a scatterplot
import matplotlib.pyplot as plt
plt.scatter(data['happiness_average'], data['happiness_standard_deviation'], alpha=0.5)
plt.title('Happiness Average vs. Standard Deviation')
plt.xlabel('Happiness Average')
plt.ylabel('Happiness Standard Deviation')
plt.grid()
plt.show()

## Identify 15 words with the highest disagreement (high standard deviation)
top_disagreement = data.sort_values(by='happiness_standard_deviation', ascending=False).head(15)
print("Top 15 Words with Highest Disagreement:")
print(top_disagreement[['word', 'happiness_average', 'happiness_standard_deviation']])



