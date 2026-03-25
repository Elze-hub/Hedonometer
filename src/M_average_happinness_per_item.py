# Meeli
# Instead of just looking at average happiness scores per word, look at average happiness per review or tip (item)

import re
import pandas as pd
from collections import Counter

# Load processed reviews and tips
reviews = pd.read_csv("data/processed/yelp_reviews_processed.csv")
tips = pd.read_csv("data/processed/yelp_tips_processed.csv")
reviews["kind"] = "review"
tips["kind"] = "tip"

data = pd.concat([reviews[["kind", "text"]], tips[["kind", "text"]]], ignore_index=True)

# Load hedonometer scores
labmt = pd.read_csv("data/processed/hedonometer_data.csv")
word_scores = dict(zip(labmt["word"], labmt["happiness_average"]))

# Tokenizer
token_pattern = re.compile(r"[a-zA-Z]+")
def tokenize(text):
    if not isinstance(text, str):
        return []
    return token_pattern.findall(text.lower())

# Average happiness per item (Review or tip)
def happiness_for_text(text, word_scores):
    tokens = tokenize(text)
    scores = [word_scores[w] for w in tokens if w in word_scores]
    if len(scores) == 0:
        return None
    return sum(scores) / len(scores)

# Apply to all rows
data["happiness"] = data["text"].apply(lambda x: happiness_for_text(x, word_scores))

# Print data
print(data.groupby("kind")["happiness"].describe())
# Save data
data.to_csv("data/processed/happiness_per_item.csv", index=False)




## Check for unique words in Yelp reviews and tips that do not exist in Hedonometer

import pandas as pd

## Load processed reviews and tips
reviews = pd.read_csv("data/processed/yelp_reviews_processed.csv")
tips = pd.read_csv("data/processed/yelp_tips_processed.csv")
## Load hedonometer scores
labmt = pd.read_csv("data/processed/hedonometer_data.csv")

## Get unique words in reviews and tips
def get_unique_words(text_series):
    words = set()
    for text in text_series.dropna():
        words.update(text.lower().split())
    return words

review_words = get_unique_words(reviews["text"])
tip_words = get_unique_words(tips["text"])
hedonometer_words = set(labmt["word"])

unique_review_words = review_words - hedonometer_words
unique_tip_words = tip_words - hedonometer_words

print(f"Unique words in reviews not in hedonometer: {len(unique_review_words)}")
print(f"Unique words in tips not in hedonometer: {len(unique_tip_words)}")

### Semantic prosody

### Choose the top 15 happiest words that appear in Yelp
### Get word frequencies
word_freq = Counter()
for text in data["text"].dropna():
    word_freq.update(tokenize(text))

### Get top 15 happiest words that appear in Yelp, apply minimum frequency
min_freq = 20
top_happy_words = sorted([(w, s) for w, s in word_scores.items() if w in word_freq and word_freq[w] >= min_freq], key=lambda x: x[1], reverse=True)[:15]
print("Top 15 happiest words in Yelp reviews and tips:")
for word, score in top_happy_words:
    print(f"{word}: {score:.2f}")

### Collect neighbor scores
### For each of the top happy words, collect the happiness scores of their immediate neighbors in the text (if they exist).
neighbor_scores = {word: [] for word, _ in top_happy_words}
for text in data["text"].dropna():
    tokens = tokenize(text)
    for i, token in enumerate(tokens):
        if token in neighbor_scores:
            # Get neighbors
            left_neighbor = tokens[i - 1] if i > 0 else None
            right_neighbor = tokens[i + 1] if i < len(tokens) - 1 else None
            
            # Get scores
            if left_neighbor and left_neighbor in word_scores:
                neighbor_scores[token].append(word_scores[left_neighbor])
            if right_neighbor and right_neighbor in word_scores:
                neighbor_scores[token].append(word_scores[right_neighbor])

### Compute average neighbour happiness per top word
average_neighbor_happiness = {word: (sum(scores) / len(scores) if scores else None) for word, scores in neighbor_scores.items()}
print("\nAverage happiness of neighbors for top happy words:")
for word, avg_score in average_neighbor_happiness.items():
    print(f"{word}: {avg_score:.2f}" if avg_score is not None else f"{word}: No neighbors with scores")

### Create a table of top happy words, their happiness scores, and the average happiness of their neighbors.
print("\nTop happy words with their scores and average neighbor happiness:")
print(f"{'Word':<15} {'Score':<10} {'Avg Neighbor Happiness':<25}")
for word, score in top_happy_words:
    avg_neighbor_score = average_neighbor_happiness[word]
    print(f"{word:<15} {score:<10.2f} {avg_neighbor_score if avg_neighbor_score is not None else 'No neighbors with scores':<25}")

### Make a scatterplot of the happiness score of the top happy words vs the average happiness of their neighbors and save it
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))
x = [score for word, score in top_happy_words]
y = [average_neighbor_happiness[word] for word, score in top_happy_words]
plt.scatter(x, y, color="blue")
plt.xlabel("Happiness score of top happy words")
plt.ylabel("Average happiness of neighbors")
plt.title("Happiness of top happy words vs average happiness of neighbors in Yelp reviews and tips")
plt.grid()
plt.tight_layout()
plt.savefig("figures/average_neighbor_happiness_scatter.png", dpi=300)



### Create a bar chart: sort by the happiness of the target word and plot neighbour happiness as bars and save it
plt.figure(figsize=(10, 6))
x = [word for word, score in top_happy_words]
y = [average_neighbor_happiness[word] for word, score in top_happy_words]
plt.bar(x, y, color="orange")
plt.xlabel("Top happy words")
plt.ylabel("Average happiness of neighbors")
plt.title("Average happiness of neighbors for top happy words in Yelp reviews and tips")
plt.xticks(rotation=45)
plt.grid(axis="y")
plt.tight_layout()
plt.savefig("figures/average_neighbor_happiness_bar.png", dpi=300)

### Create a difference plot: for each top happy word, plot the difference between its happiness score and the average happiness of its neighbors. Save it.
plt.figure(figsize=(10, 6))
x = [word for word, score in top_happy_words]
y = [score - average_neighbor_happiness[word] if average_neighbor_happiness[word] is not None else None for word, score in top_happy_words]
plt.bar(x, y, color="green")
plt.xlabel("Top happy words")
plt.ylabel("Difference between word happiness and average neighbor happiness")
plt.title("Difference between happiness of top happy words and their neighbors in Yelp reviews and tips")
plt.xticks(rotation=45)
plt.grid(axis="y")
plt.tight_layout()
plt.savefig("figures/difference_happiness_bar.png", dpi=300)

### Heatmap of neighbour distributions
### Collect all left neighbours and right neighbours seperately for the top happy words
left_neighbors = {word: [] for word, _ in top_happy_words}
right_neighbors = {word: [] for word, _ in top_happy_words}
for text in data["text"].dropna():
    tokens = tokenize(text)
    for i, token in enumerate(tokens):
        if token in left_neighbors:
            left_neighbor = tokens[i - 1] if i > 0 else None
            right_neighbor = tokens[i + 1] if i < len(tokens) - 1 else None
            
            if left_neighbor:
                left_neighbors[token].append(left_neighbor)
            if right_neighbor:
                right_neighbors[token].append(right_neighbor)

### Create a heatmap showing the distribution of neighbor scores for each target word
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 8))

max_len = 50 # Number of neighbors to show per word

heatmap_data = []

for word, _ in top_happy_words:
    neighbors = left_neighbors[word] + right_neighbors[word]
    scores = [word_scores[n] for n in neighbors if n in word_scores]

    if len(scores) >= max_len:
        scores = scores[:max_len]
    else:
        scores = scores + [np.nan] * (max_len - len(scores))  # Pad with NaN if less than max_len

    heatmap_data.append(scores)
heatmap_df = pd.DataFrame(
    heatmap_data,
    index=[word for word, _ in top_happy_words]
    )

### Debug prints

print(heatmap_df)
print(heatmap_df.isna().sum())  # Check for NaN values

### Plot
sns.heatmap(
    heatmap_df,
    cmap="YlGnBu",
    cbar=True,
    xticklabels=False,
    yticklabels=True,
)
plt.xlabel("Neighbor Index")
plt.ylabel("Top Happy Words")
plt.title("Distribution of Neighbor Happiness Scores for Top Happy Words")
plt.tight_layout()
plt.savefig("figures/neighbor_happiness_heatmap.png", dpi=300)
plt.show()

#### Choose the top 15 unhhappiest words that appear in Yelp
### Get word frequencies
min_freq = 20
top_unhappy_words = sorted([(w, s) for w, s in word_scores.items() if w in word_freq and word_freq[w] >= min_freq], key=lambda x: x[1])[:15]
print("\nTop 15 unhappiest words in Yelp reviews and tips:")
for word, score in top_unhappy_words:
    print(f"{word}: {score:.2f}")

### Collect neighbor scores
### For each of the top 15 unhappy words, collect the happiness scores of their immediate neighbors in the text (if they exist).
neighbor_scores_unhappy = {word: [] for word, _ in top_unhappy_words}
for text in data["text"].dropna():
    tokens = tokenize(text)
    for i, token in enumerate(tokens):
        if token in neighbor_scores_unhappy:
            # Get neighbors
            left_neighbor = tokens[i - 1] if i > 0 else None
            right_neighbor = tokens[i + 1] if i < len(tokens) - 1 else None
            
            # Get scores
            if left_neighbor and left_neighbor in word_scores:
                neighbor_scores_unhappy[token].append(word_scores[left_neighbor])
            if right_neighbor and right_neighbor in word_scores:
                neighbor_scores_unhappy[token].append(word_scores[right_neighbor])
### Compute average neighbour happiness per top unhappy word
average_neighbor_happiness_unhappy = {word: (sum(scores) / len(scores) if scores else None) for word, scores in neighbor_scores_unhappy.items()}
print("\nAverage happiness of neighbors for top unhappy words:")
for word, avg_score in average_neighbor_happiness_unhappy.items():
    print(f"{word}: {avg_score:.2f}" if avg_score is not None else f"{word}: No neighbors with scores")

### Create a table of top unhappy words, their happiness scores, and the average happiness of their neighbors.
print("\nTop unhappy words with their scores and average neighbor happiness:")
print(f"{'Word':<15} {'Score':<10} {'Avg Neighbor Happiness':<25}")
for word, score in top_unhappy_words:
    avg_neighbor_score = average_neighbor_happiness_unhappy[word]
    print(f"{word:<15} {score:<10.2f} {avg_neighbor_score if avg_neighbor_score is not None else 'No neighbors with scores':<25}")

### Make a scatterplot of the happiness score of the top unhappy words vs the average happiness of their neighbors and save it
plt.figure(figsize=(10, 6))
x = [score for word, score in top_unhappy_words]
y = [average_neighbor_happiness_unhappy[word] for word, score in top_unhappy_words]
plt.scatter(x, y, color="red")
plt.xlabel("Happiness score of top unhappy words")
plt.ylabel("Average happiness of neighbors")
plt.title("Happiness of top unhappy words vs average happiness of neighbors in Yelp reviews and tips")
plt.grid()
plt.tight_layout()
plt.savefig("figures/average_neighbor_happiness_scatter_unhappy.png", dpi=300)
plt.show()

### Create a bar chart: sort by the happiness of the target word and plot neighbour happiness as bars and save it
plt.figure(figsize=(10, 6))
x = [word for word, score in top_unhappy_words]
y = [average_neighbor_happiness_unhappy[word] for word, score in top_unhappy_words]
plt.bar(x, y, color="purple")
plt.xlabel("Top unhappy words")
plt.ylabel("Average happiness of neighbors")
plt.title("Average happiness of neighbors for top unhappy words in Yelp reviews and tips")
plt.xticks(rotation=45)
plt.grid(axis="y")
plt.tight_layout()
plt.savefig("figures/average_neighbor_happiness_bar_unhappy.png", dpi=300)
plt.show()

### Create a difference plot: for each top unhappy word, plot the difference between its happiness score and the average happiness of its neighbors. Save it.
plt.figure(figsize=(10, 6))
x = [word for word, score in top_unhappy_words]
y = [score - average_neighbor_happiness_unhappy[word] if average_neighbor_happiness_unhappy[word] is not None else None for word, score in top_unhappy_words]
plt.bar(x, y, color="brown")
plt.xlabel("Top unhappy words")
plt.ylabel("Difference between word happiness and average neighbor happiness")
plt.title("Difference between happiness of top unhappy words and their neighbors in Yelp reviews and tips")
plt.xticks(rotation=45)
plt.grid(axis="y")
plt.tight_layout()
plt.savefig("figures/difference_happiness_bar_unhappy.png", dpi=300)
plt.show()

### Heatmap of neighbour distributions
### Collect all left neighbours and right neighbours seperately for the top unhappy words
left_neighbors_unhappy = {word: [] for word, _ in top_unhappy_words}
right_neighbors_unhappy = {word: [] for word, _ in top_unhappy_words}
for text in data["text"].dropna():
    tokens = tokenize(text)
    for i, token in enumerate(tokens):
        if token in left_neighbors_unhappy:
            left_neighbor = tokens[i - 1] if i > 0 else None
            right_neighbor = tokens[i + 1] if i < len(tokens) - 1 else None
            
            if left_neighbor:
                left_neighbors_unhappy[token].append(left_neighbor)
            if right_neighbor:
                right_neighbors_unhappy[token].append(right_neighbor)
### Create a heatmap showing the distribution of neighbor scores for each target word
plt.figure(figsize=(12, 8))
heatmap_data_unhappy = []
for word, _ in top_unhappy_words:
    neighbors = left_neighbors_unhappy[word] + right_neighbors_unhappy[word]
    scores = [word_scores[n] for n in neighbors if n in word_scores]

    if len(scores) >= max_len:
        scores = scores[:max_len]
    else:
        scores = scores + [np.nan] * (max_len - len(scores))  # Pad with NaN if less than max_len

    heatmap_data_unhappy.append(scores)
heatmap_df_unhappy = pd.DataFrame(
    heatmap_data_unhappy,
    index=[word for word, _ in top_unhappy_words]
    )
sns.heatmap(
    heatmap_df_unhappy,
    cmap="YlGnBu",
    cbar=True,
    xticklabels=False,
    yticklabels=True,
)
plt.xlabel("Neighbor Index")
plt.ylabel("Top Unhappy Words")
plt.title("Distribution of Neighbor Happiness Scores for Top Unhappy Words")
plt.tight_layout()
plt.savefig("figures/neighbor_happiness_heatmap_unhappy.png", dpi=300)
plt.show()


### Debug prints
print(heatmap_df_unhappy)
print(heatmap_df_unhappy.isna().sum())  # Check for NaN values


### Plot
sns.heatmap(
    heatmap_df_unhappy,
    cmap="YlGnBu",
    cbar=True,
    xticklabels=False,
    yticklabels=True,
)
plt.xlabel("Neighbor Index")
plt.ylabel("Top Unhappy Words")
plt.title("Distribution of Neighbor Happiness Scores for Top Unhappy Words")
plt.tight_layout()
plt.savefig("figures/neighbor_happiness_heatmap_unhappy.png", dpi=300)
plt.show()

#### Compute the correlation between word happiness and average neighbor happiness for the top happy words and top unhappy words separately, and print the results.
from scipy.stats import pearsonr
happy_scores = [score for word, score in top_happy_words if average_neighbor_happiness[word] is not None]
happy_neighbor_scores = [average_neighbor_happiness[word] for word, score in top_happy_words if average_neighbor_happiness[word] is not None]
unhappy_scores = [score for word, score in top_unhappy_words if average_neighbor_happiness_unhappy[word] is not None]
unhappy_neighbor_scores = [average_neighbor_happiness_unhappy[word] for word, score in top_unhappy_words if average_neighbor_happiness_unhappy[word] is not None]
happy_corr, happy_p = pearsonr(happy_scores, happy_neighbor_scores)
unhappy_corr, unhappy_p = pearsonr(unhappy_scores, unhappy_neighbor_scores)
print(f"Correlation between word happiness and average neighbor happiness for top happy words: {happy_corr:.2f} (p={happy_p:.3f})")
print(f"Correlation between word happiness and average neighbor happiness for top unhappy words: {unhappy_corr:.2f} (p={unhappy_p:.3f})")
