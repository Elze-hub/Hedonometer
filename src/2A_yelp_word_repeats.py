#Asena

import re
from collections import Counter

import pandas as pd

# 1. Load processed reviews and tips
reviews = pd.read_csv("data/processed/yelp_reviews_processed.csv")
tips = pd.read_csv("data/processed/yelp_tips_processed.csv")

reviews["kind"] = "review"
tips["kind"] = "tip"

data = pd.concat([reviews[["kind", "text"]], tips[["kind", "text"]]], ignore_index=True)

# 2. Load hedonometer scores
labmt = pd.read_csv("data/processed/hedonometer_data.csv")
word_scores = dict(zip(labmt["word"], labmt["happiness_average"]))

# simple tokenizer
token_pattern = re.compile(r"[a-zA-Z]+")

def tokenize(text):
    if not isinstance(text, str):
        return []
    return token_pattern.findall(text.lower())

# 3. Count word frequencies separately for tips and reviews
counts = {"review": Counter(), "tip": Counter()}

for _, row in data.iterrows():
    kind = row["kind"]
    tokens = tokenize(row["text"])
    for w in tokens:
        if w in word_scores:  # only count words that have a hedonometer score
            counts[kind][w] += 1

# 4. Convert to DataFrame and add happiness scores
def counts_to_df(kind):
    c = counts[kind]
    df = pd.DataFrame.from_dict(c, orient="index", columns=["count"]).reset_index()
    df = df.rename(columns={"index": "word"})
    df["happiness"] = df["word"].map(word_scores)
    df["kind"] = kind
    return df

df_reviews_words = counts_to_df("review")
df_tips_words = counts_to_df("tip")

all_words = pd.concat([df_reviews_words, df_tips_words], ignore_index=True)

# 5. Save overall table
all_words.to_csv("data/processed/yelp_word_repeats_with_happiness.csv", index=False)

# 6. Show top repeated positive/negative words for each kind
def top_words(df, min_count=20, n=15):
    df_filt = df[df["count"] >= min_count]
    top_positive = df_filt.sort_values("happiness", ascending=False).head(n)
    top_negative = df_filt.sort_values("happiness", ascending=True).head(n)
    return top_positive, top_negative

print("=== Reviews ===")
rev_pos, rev_neg = top_words(df_reviews_words)
print("Top positive (reviews):")
print(rev_pos[["word", "count", "happiness"]])

print("\nTop negative (reviews):")
print(rev_neg[["word", "count", "happiness"]])

print("\n=== Tips ===")
tip_pos, tip_neg = top_words(df_tips_words)
print("Top positive (tips):")
print(tip_pos[["word", "count", "happiness"]])

print("\nTop negative (tips):")
print(tip_neg[["word", "count", "happiness"]])

# 7. Optionally save these summary tables
rev_pos.to_csv("data/processed/yelp_top_positive_words_reviews.csv", index=False)
rev_neg.to_csv("data/processed/yelp_top_negative_words_reviews.csv", index=False)
tip_pos.to_csv("data/processed/yelp_top_positive_words_tips.csv", index=False)
tip_neg.to_csv("data/processed/yelp_top_negative_words_tips.csv", index=False)