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

## Create figures directory if it doesn't exist
import os
figures_dir = '../figures'
if not os.path.exists(figures_dir):
    os.makedirs(figures_dir)

## Make a plot about corpus differences
### Bar chart of how many different words appear in each corpus and save it to /figures
import matplotlib.pyplot as plt
corpora = ['Twitter', 'NYT', 'Google Books', 'Lyrics']
counts = [twitter_count, nyt_count, google_count, lyrics_count]
plt.bar(corpora, counts, color=['blue', 'orange', 'green', 'red'])
plt.title('Number of labMT Words in Top 5000 of Each Corpus')
plt.xlabel('Corpus')
plt.ylabel('Number of Words')
plt.savefig('../figures/corpus_word_counts.png')

## Clear previous plot (otherwise figures get muddled together)
plt.clf()

### Heatmap-like table showing overlap between corpora (number of shared words in top 5000) and save it to /figures
import numpy as np
corpora = ['Twitter', 'NYT', 'Google Books', 'Lyrics']
overlap_matrix = np.array([[twitter_count, len(twitter_words.intersection(nyt_words)), len(twitter_words.intersection(google_words)), len(twitter_words.intersection(lyrics_words))],
                           [len(nyt_words.intersection(twitter_words)), nyt_count, len(nyt_words.intersection(google_words)), len(nyt_words.intersection(lyrics_words))],
                           [len(google_words.intersection(twitter_words)), len(google_words.intersection(nyt_words)), google_count, len(google_words.intersection(lyrics_words))],
                           [len(lyrics_words.intersection(twitter_words)), len(lyrics_words.intersection(nyt_words)), len(lyrics_words.intersection(google_words)), lyrics_count]])
plt.imshow(overlap_matrix, cmap='Blues')
plt.xticks(range(len(corpora)), corpora, rotation=45)
plt.yticks(range(len(corpora)), corpora)
plt.colorbar(label='Number of Shared Words')
plt.title('Overlap of labMT Words in Top 5000 of Each Corpus')
plt.savefig('../figures/corpus_overlap_heatmap.png')

## Clear previous plot (otherwise figures get muddled together)
plt.clf()

### Scatterplot of Twitter rank vs NYT rank for words present in both and save to /figures
common_words = twitter_words.intersection(nyt_words)
twitter_ranks = data.loc[data['word'].isin(common_words), 'twitter_rank']
nyt_ranks = data.loc[data['word'].isin(common_words), 'nyt_rank']
plt.scatter(twitter_ranks, nyt_ranks, alpha=0.5)
plt.title('Twitter Rank vs NYT Rank for Common Words')
plt.xlabel('Twitter Rank')
plt.ylabel('NYT Rank')
plt.savefig('../figures/twitter_nyt_rank_scatter.png')
