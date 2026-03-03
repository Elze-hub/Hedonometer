# Task 2.3: Corpus comparison: what counts as "common language" depends on where you look
# The dataset includes a rank column for each corpus. This lets you study overlap and differences between the corpora. For example, you could compare the top 100 words in the Twitter corpus to the top 100 words in the Google Books corpus. How much overlap is there? Which words are unique to each corpus? What does this tell you about how people use language differently in different contexts?

## Load the cleaned data
import pandas as pd
data = pd.read_csv('../data/processed/hedonometer_data.csv')
print(data.head())

twitter_count = data['twitter_rank'].isna().sum()

print(twitter_count)