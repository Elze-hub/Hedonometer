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
    tips_path = "data/raw/yelp-dataset/yelp_academic_dataset_tip.json"
    business_path = "data/raw/yelp-dataset/yelp_academic_dataset_business.json"

    
    if not os.path.exists(tips_path):
        raise FileNotFoundError(f"{tips_path} not found. Did you unzip the dataset?")
    if not os.path.exists(business_path):
        raise FileNotFoundError(f"{business_path} not found. Did you unzip the dataset?")

    print("Loading tips...")
    tips = load_json_lines(tips_path, max_rows=5000)  # you can limit if needed
    df_tips = pd.DataFrame(tips)
    print("Tips shape:", df_tips.shape)
    print("Tip columns:", df_tips.columns.tolist())

    print("Loading businesses...")
    businesses = load_json_lines(business_path, max_rows=None)
    df_business = pd.DataFrame(businesses)
    print("Businesses shape:", df_business.shape)

    # Tip file usually has: user_id, business_id, text, date, compliment_count
    df_tips_small = df_tips[["user_id", "business_id", "text", "date"]]

    df_business_small = df_business[
        ["business_id", "name", "city", "state", "categories"]
    ]

    # Merge tips with business metadata
    df_merged = df_tips_small.merge(df_business_small, on="business_id", how="left")

    # Basic cleaning: drop empty texts
    df_merged = df_merged.dropna(subset=["text"])
    df_merged = df_merged[df_merged["text"].str.strip() != ""]

    print("Merged tips shape after cleaning:", df_merged.shape)

    os.makedirs("data/processed", exist_ok=True)
    out_path = "data/processed/yelp_tips_processed.csv"
    df_merged.to_csv(out_path, index=False)

    print(f"Saved processed tips to {out_path}")


if __name__ == "__main__":
    main()