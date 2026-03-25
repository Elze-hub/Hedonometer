# Meeli — Happiness & Semantic Prosody Analysis (Clean Version)

import re
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter

# -----------------------------
# Load data
# -----------------------------
reviews = pd.read_csv("data/processed/yelp_reviews_processed.csv")
tips = pd.read_csv("data/processed/yelp_tips_processed.csv")

reviews["kind"] = "review"
tips["kind"] = "tip"

data = pd.concat(
    [reviews[["kind", "text"]], tips[["kind", "text"]]],
    ignore_index=True
)

labmt = pd.read_csv("data/processed/hedonometer_data.csv")
word_scores = dict(zip(labmt["word"], labmt["happiness_average"]))

# -----------------------------
# Tokenizer
# -----------------------------
token_pattern = re.compile(r"[a-zA-Z]+")

def tokenize(text):
    if not isinstance(text, str):
        return []
    return token_pattern.findall(text.lower())

# -----------------------------
# Happiness per item
# -----------------------------
def happiness_for_text(text):
    tokens = tokenize(text)
    scores = [word_scores[w] for w in tokens if w in word_scores]
    return np.mean(scores) if scores else None

data["happiness"] = data["text"].apply(happiness_for_text)

print("\n=== Happiness per item ===")
print(data.groupby("kind")["happiness"].describe())

data.to_csv("data/processed/happiness_per_item.csv", index=False)

# Boxplot
plt.figure(figsize=(8, 6))
data.boxplot(column="happiness", by="kind")
plt.title("Happiness scores for Yelp reviews and tips")
plt.suptitle("")
plt.xlabel("Kind")
plt.ylabel("Happiness score")
plt.grid()
plt.tight_layout()
plt.savefig("figures/happiness_per_item_boxplot.png", dpi=300)
plt.close()

# -----------------------------
# Length analysis
# -----------------------------
data["length"] = data["text"].apply(lambda x: len(tokenize(x)))

print("\n=== Length stats ===")
print(data.groupby("kind")["length"].describe())

# -----------------------------
# Unique words not in hedonometer
# -----------------------------
def get_unique_words(text_series):
    words = set()
    for text in text_series.dropna():
        words.update(tokenize(text))
    return words

review_words = get_unique_words(reviews["text"])
tip_words = get_unique_words(tips["text"])
hedo_words = set(labmt["word"])

print("\n=== Missing words ===")
print("Reviews:", len(review_words - hedo_words))
print("Tips:", len(tip_words - hedo_words))

# -----------------------------
# Word frequency dataframe
# -----------------------------
def build_word_df(text_series):
    counter = Counter()
    for text in text_series.dropna():
        counter.update(tokenize(text))

    df = pd.DataFrame(counter.items(), columns=["word", "count"])
    df["happiness"] = df["word"].map(word_scores)
    return df.dropna(subset=["happiness"])

df_reviews = build_word_df(reviews["text"])
df_tips = build_word_df(tips["text"])

# -----------------------------
# Top words
# -----------------------------
def get_top_words(df, min_count=20, n=15):
    df = df[df["count"] >= min_count]
    pos = df.sort_values("happiness", ascending=False).head(n)
    neg = df.sort_values("happiness", ascending=True).head(n)

    pos_list = list(zip(pos["word"], pos["happiness"]))
    neg_list = list(zip(neg["word"], neg["happiness"]))
    return pos_list, neg_list

rev_pos, rev_neg = get_top_words(df_reviews)
tip_pos, tip_neg = get_top_words(df_tips)

# -----------------------------
# Neighbor happiness
# -----------------------------
def compute_neighbor_happiness(top_words_list, text_series):
    neighbor_scores = {word: [] for word, _ in top_words_list}

    for text in text_series.dropna():
        tokens = tokenize(text)
        for i, token in enumerate(tokens):
            if token in neighbor_scores:
                left = tokens[i - 1] if i > 0 else None
                right = tokens[i + 1] if i < len(tokens) - 1 else None

                if left in word_scores:
                    neighbor_scores[token].append(word_scores[left])
                if right in word_scores:
                    neighbor_scores[token].append(word_scores[right])

    avg_scores = {
        w: (np.mean(s) if s else None)
        for w, s in neighbor_scores.items()
    }

    return neighbor_scores, avg_scores

# -----------------------------
# Analysis function
# -----------------------------
def analyze_words(top_words_list, text_series, dataset_name, prefix, color):
    neighbor_scores, avg_scores = compute_neighbor_happiness(
        top_words_list, text_series
    )

    print(f"\n=== {dataset_name} ===")
    print(f"{'Word':<15}{'Score':<10}{'Neighbor Avg':<15}")

    for word, score in top_words_list:
        avg = avg_scores[word]
        avg_str = f"{avg:.2f}" if avg is not None else "NA"
        print(f"{word:<15}{score:<10.2f}{avg_str:<15}")

    # Scatter
    plt.figure(figsize=(8, 5))
    x = [score for _, score in top_words_list]
    y = [avg_scores[w] for w, _ in top_words_list]
    plt.scatter(x, y, color=color)
    plt.xlabel("Word happiness")
    plt.ylabel("Neighbor happiness")
    plt.title(dataset_name)
    plt.grid()
    plt.tight_layout()
    plt.savefig(f"figures/{prefix}_scatter.png", dpi=300)
    plt.close()

    # Bar
    words = [w for w, _ in top_words_list]
    vals = [avg_scores[w] for w in words]

    plt.figure(figsize=(10, 5))
    plt.bar(words, vals, color=color)
    plt.xticks(rotation=45)
    plt.ylabel("Neighbor happiness")
    plt.title(dataset_name)
    plt.tight_layout()
    plt.savefig(f"figures/{prefix}_bar.png", dpi=300)
    plt.close()

    # Heatmap
    max_len = 100
    heatmap_data = []

    for word, _ in top_words_list:
        scores = neighbor_scores[word][:max_len]
        scores += [np.nan] * (max_len - len(scores))
        heatmap_data.append(scores)

    heatmap_df = pd.DataFrame(
        heatmap_data,
        index=[w for w, _ in top_words_list]
    )

    plt.figure(figsize=(12, 6))
    sns.heatmap(heatmap_df, cmap="YlGnBu", xticklabels=False)
    plt.title(dataset_name)
    plt.tight_layout()
    plt.savefig(f"figures/{prefix}_heatmap.png", dpi=300)
    plt.close()

    return heatmap_df

# -----------------------------
# Run analyses
# -----------------------------
analyze_words(rev_pos, reviews["text"], "Happy words (Reviews)", "rev_pos", "green")
analyze_words(tip_pos, tips["text"], "Happy words (Tips)", "tip_pos", "green")

analyze_words(rev_neg, reviews["text"], "Unhappy words (Reviews)", "rev_neg", "red")
analyze_words(tip_neg, tips["text"], "Unhappy words (Tips)", "tip_neg", "red")

print("\nDone.")