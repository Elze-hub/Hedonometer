# Task 2.3: Corpus comparison: what counts as "common language" depends on where you look
# The dataset includes a rank column for each corpus. This lets you study overlap and differences between the corpora. For example, you could compare the top 100 words in the Twitter corpus to the top 100 words in the Google Books corpus. How much overlap is there? Which words are unique to each corpus? What does this tell you about how people use language differently in different contexts?

## Load the cleaned data
import pandas as pd
data = pd.read_csv('../data/processed/hedonometer_data.csv')

## Count how many words from the labMT list appear in the top 5000 of each corpus (no missing rank)
twitter_count = data['twitter_rank'].notna().sum()
nyt_count = data['nyt_rank'].notna().sum()
google_count = data['google_rank'].notna().sum()
lyrics_count = data['lyrics_rank'].notna().sum()
print(f"Number of labMT words in Twitter top 5000: {twitter_count}")
print(f"Number of labMT words in NYT top 5000: {nyt_count}")
print(f"Number of labMT words in Google Books top 5000: {google_count}")
print(f"Number of labMT words in Lyrics top 5000: {lyrics_count}")


## Compute a simple overlap table showing how many words appear in both Twitter and NYT
twitter_words = set(data.loc[data['twitter_rank'].notna(), 'word'])
nyt_words = set(data.loc[data['nyt_rank'].notna(), 'word'])
overlap = twitter_words.intersection(nyt_words)
print(f"Number of words in both Twitter and NYT top 5000: {len(overlap)}")

## Compute a simple overlap table showing how many words appear in both Twitter and Google Books
google_words = set(data.loc[data['google_rank'].notna(), 'word'])
overlap = twitter_words.intersection(google_words)
print(f"Number of words in both Twitter and Google Books top 5000: {len(overlap)}")

## Compute a simple overlap table showing how many words appear in both Twitter and Lyrics
lyrics_words = set(data.loc[data['lyrics_rank'].notna(), 'word'])
overlap = twitter_words.intersection(lyrics_words)
print(f"Number of words in both Twitter and Lyrics top 5000: {len(overlap)}")

## Compute a simple overlap table showing how many words appear in both NYT and Google Books
overlap = nyt_words.intersection(google_words)
print(f"Number of words in both NYT and Google Books top 5000: {len(overlap)}")

## Compute a simple overlap table showing how many words appear in both NYT and Lyrics
overlap = nyt_words.intersection(lyrics_words)
print(f"Number of words in both NYT and Lyrics top 5000: {len(overlap)}")

## Compute a simple overlap table showing how many words appear in both Google Books and Lyrics
overlap = google_words.intersection(lyrics_words)
print(f"Number of words in both Google Books and Lyrics top 5000: {len(overlap)}")


## Compute a simple overlap table showing how many words appear in all four
overlap_all = twitter_words.intersection(nyt_words, google_words, lyrics_words)
print(f"Number of words in all four corpora top 5000: {len(overlap_all)}")


### Optional from me: Identify words that are unique to each corpus (appear in one but not the others)
twitter_unique = twitter_words - (nyt_words | google_words | lyrics_words)
nyt_unique = nyt_words - (twitter_words | google_words | lyrics_words)
google_unique = google_words - (twitter_words | nyt_words | lyrics_words)
lyrics_unique = lyrics_words - (twitter_words | nyt_words | google_words)
print(f"Number of words unique to Twitter: {len(twitter_unique)}")
print(f"Number of words unique to NYT: {len(nyt_unique)}")
print(f"Number of words unique to Google Books: {len(google_unique)}")
print(f"Number of words unique to Lyrics: {len(lyrics_unique)}")

## Make a plot about corpus differences
### Bar chart of how many different words appear in each corpus
import matplotlib.pyplot as plt
corpora = ['Twitter', 'NYT', 'Google Books', 'Lyrics']
counts = [twitter_count, nyt_count, google_count, lyrics_count]
plt.bar(corpora, counts, color=['blue', 'orange', 'green', 'red'])
plt.title('Number of labMT Words in Top 5000 of Each Corpus')
plt.xlabel('Corpus')
plt.ylabel('Number of Words')
plt.show()


### Heatmap-like table showing overlap between corpora (number of shared words in top 5000)
import numpy as np
corpora = ['Twitter', 'NYT', 'Google Books', 'Lyrics']
overlap_matrix = np.zeros((4, 4), dtype=int)
overlap_matrix[0, 1] = len(twitter_words.intersection(nyt_words))
overlap_matrix[0, 2] = len(twitter_words.intersection(google_words))
overlap_matrix[0, 3] = len(twitter_words.intersection(lyrics_words))
overlap_matrix[1, 0] = overlap_matrix[0, 1]
overlap_matrix[1, 2] = len(nyt_words.intersection(google_words))
overlap_matrix[1, 3] = len(nyt_words.intersection(lyrics_words))
overlap_matrix[2, 0] = overlap_matrix[0, 2]
overlap_matrix[2, 1] = overlap_matrix[1, 2]
overlap_matrix[2, 3] = len(google_words.intersection(lyrics_words))
overlap_matrix[3, 0] = overlap_matrix[0, 3]
overlap_matrix[3, 1] = overlap_matrix[1, 3]
overlap_matrix[3, 2] = overlap_matrix[2, 3]
plt.imshow(overlap_matrix, cmap='Blues')
plt.xticks(range(4), corpora)
plt.yticks(range(4), corpora)
plt.colorbar(label='Number of Shared Words in Top 5000')
plt.title('Overlap of Words in Top 5000 Across Corpora')
plt.show()


### Scatterplot of Twitter rank vs NYT rank for words present in both
common_words = twitter_words.intersection(nyt_words)
common_data = data[data['word'].isin(common_words)]
plt.scatter(common_data['twitter_rank'], common_data['nyt_rank'], alpha=0.5)
plt.title('Twitter Rank vs NYT Rank for Common Words')
plt.xlabel('Twitter Rank')
plt.ylabel('NYT Rank')
plt.grid()
plt.show()