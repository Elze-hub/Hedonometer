#Asena

import pandas as pd
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

file_path = ROOT_DIR / "data" / "raw" / "Data_Set_S1.txt"

# 1. Load the dataset (ADJUST THE PATH AND FILENAME IF NEEDED)
df = pd.read_csv(
    file_path,   # <-- change this to your actual file path
    sep="\t",
    comment="#",                    # skip metadata lines starting with '#'
    skiprows=2,
    na_values="--"                  # treat '--' as NaN
)

# Optional: quick check of columns
print("Columns:", list(df.columns))
print(df.head())

# 2. Build the 20-word exhibit

# 5 very positive
positive_5 = (
    df.dropna(subset=["happiness_average"])
      .sort_values("happiness_average", ascending=False)
      .head(5)
      .assign(category="very positive")
)

# 5 very negative
negative_5 = (
    df.dropna(subset=["happiness_average"])
      .sort_values("happiness_average", ascending=True)
      .head(5)
      .assign(category="very negative")
)

# 5 most contested (highest standard deviation)
contested_5 = (
    df.dropna(subset=["happiness_standard_deviation"])
      .sort_values("happiness_standard_deviation", ascending=False)
      .head(5)
      .assign(category="highly contested")
)

# 5 weird/surprising/historically dated/culturally loaded – choose manually
weird_words = [
    "thou",
    "hehehe",
    "ipod",
    "gr8",
    "groovy",
]

weird_5 = (
    df[df["word"].isin(weird_words)]
      .assign(category="weird/surprising")
)

# Combine all into one exhibit table
exhibit = pd.concat(
    [positive_5, negative_5, contested_5, weird_5],
    ignore_index=True
)

# Choose columns to show
cols = [
    "category",
    "word",
    "happiness_average",
    "happiness_standard_deviation",
    # add rank columns here if you want them, e.g.:
    # "rank_twitter", "rank_google_books", "rank_nyt", "rank_lyrics"
]

cols = [c for c in cols if c in exhibit.columns]
exhibit = exhibit[cols]

# Print the exhibit nicely
print("\n=== 20-word exhibit ===")
print(exhibit.to_string(index=False))

# Optionally save to CSV
# exhibit.to_csv("../results/Task_3.1_exhibit.csv", index=False)