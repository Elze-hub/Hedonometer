import json
import os

import pandas as pd


def load_json_lines(path, max_rows=None):
    """
    Load a JSON-lines file (one JSON object per line) into a list of dicts.
    Optionally limit to max_rows to keep file sizes manageable.
    """
    records = []
    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if max_rows is not None and i >= max_rows:
                break
            records.append(json.loads(line))
    return records


def main():
    reviews_path = "data/raw/yelp-dataset/yelp_academic_dataset_review.json"
    business_path = "data/raw/yelp-dataset/yelp_academic_dataset_business.json"

    if not os.path.exists(reviews_path):
        raise FileNotFoundError(f"{reviews_path} not found. Did you unzip the dataset?")
    if not os.path.exists(business_path):
        raise FileNotFoundError(f"{business_path} not found. Did you unzip the dataset?")

    # 1. Load a subset of reviews (limit to keep it manageable; you can increase later)
    print("Loading reviews...")
    reviews = load_json_lines(reviews_path, max_rows=50000)  # change 50000 if you want
    df_reviews = pd.DataFrame(reviews)
    print("Reviews shape:", df_reviews.shape)

    # 2. Load business metadata
    print("Loading businesses...")
    businesses = load_json_lines(business_path, max_rows=None)
    df_business = pd.DataFrame(businesses)
    print("Businesses shape:", df_business.shape)

    # 3. Keep only columns you care about
    df_reviews_small = df_reviews[["review_id", "user_id", "business_id", "stars", "text", "date"]]
    df_business_small = df_business[["business_id", "name", "city", "state", "categories"]]

    # 4. Merge reviews with business metadata on business_id
    df_merged = df_reviews_small.merge(df_business_small, on="business_id", how="left")

    # 5. Basic cleaning: drop empty texts
    df_merged = df_merged.dropna(subset=["text"])
    df_merged = df_merged[df_merged["text"].str.strip() != ""]

    print("Merged shape after cleaning:", df_merged.shape)

    # 6. Save to processed CSV
    os.makedirs("data/processed", exist_ok=True)
    out_path = "data/processed/yelp_reviews_processed.csv"
    df_merged.to_csv(out_path, index=False)

    print(f"Saved processed data to {out_path}")


if __name__ == "__main__":
    main()