#Asena

import json
import os
import random

import pandas as pd


def sample_json_lines(path, n_sample, random_state=42):
    """
    Randomly sample n_sample JSON objects from a JSON-lines file.
    """
    random.seed(random_state)
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    print(f"Total lines in {os.path.basename(path)}: {len(lines)}")

    if n_sample > len(lines):
        n_sample = len(lines)
    sample_lines = random.sample(lines, n_sample)
    records = [json.loads(line) for line in sample_lines]
    return records


def main():
    reviews_path = "data/raw/yelp-dataset/yelp_academic_dataset_review.json"

    if not os.path.exists(reviews_path):
        raise FileNotFoundError(f"{reviews_path} not found. Did you unzip the dataset?")

    # 1. Randomly sample 5000 reviews
    print("Sampling reviews...")
    reviews = sample_json_lines(reviews_path, n_sample=5000, random_state=42)
    df_reviews = pd.DataFrame(reviews)
    print("Reviews shape (raw sample):", df_reviews.shape)

    # 2. Keep only columns you care about
    # Adjust this list if you need more/less later
    df_reviews_small = df_reviews[["review_id", "user_id", "business_id", "stars", "text", "date"]]

    # 3. Basic cleaning: drop empty texts
    df_reviews_small = df_reviews_small.dropna(subset=["text"])
    df_reviews_small = df_reviews_small[df_reviews_small["text"].str.strip() != ""]

    print("Shape after cleaning:", df_reviews_small.shape)

    # 4. Save to processed CSV
    os.makedirs("data/processed", exist_ok=True)
    out_path = "data/processed/yelp_reviews_processed.csv"
    df_reviews_small.to_csv(out_path, index=False)

    print(f"Saved processed reviews to {out_path}")


if __name__ == "__main__":
    main()