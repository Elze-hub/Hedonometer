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
    tips_path = "data/raw/yelp-dataset/yelp_academic_dataset_tip.json"

    if not os.path.exists(tips_path):
        raise FileNotFoundError(f"{tips_path} not found. Did you unzip the dataset?")

    # 1. Randomly sample 5000 tips
    print("Sampling tips...")
    tips = sample_json_lines(tips_path, n_sample=5000, random_state=42)
    df_tips = pd.DataFrame(tips)
    print("Tips shape (raw sample):", df_tips.shape)
    print("Tip columns:", df_tips.columns.tolist())

    # 2. Keep only columns you care about
    # Tip file usually has: user_id, business_id, text, date, compliment_count
    df_tips_small = df_tips[["user_id", "business_id", "text", "date"]]

    # 3. Basic cleaning: drop empty texts
    df_tips_small = df_tips_small.dropna(subset=["text"])
    df_tips_small = df_tips_small[df_tips_small["text"].str.strip() != ""]

    print("Shape after cleaning:", df_tips_small.shape)

    # 4. Save to processed CSV
    os.makedirs("data/processed", exist_ok=True)
    out_path = "data/processed/yelp_tips_processed.csv"
    df_tips_small.to_csv(out_path, index=False)

    print(f"Saved processed tips to {out_path}")


if __name__ == "__main__":
    main()