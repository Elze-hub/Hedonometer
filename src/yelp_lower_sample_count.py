import json
import random
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "yelp-dataset"  # <- here
PROCESSED = ROOT / "data" / "processed"
PROCESSED.mkdir(parents=True, exist_ok=True)

def sample_json_lines(path, n_sample, random_state=42):
    random.seed(random_state)
    with path.open("r", encoding="utf-8") as f:
        lines = f.readlines()
    print(f"Total lines in {path.name}: {len(lines)}")

    if n_sample > len(lines):
        n_sample = len(lines)
    sample_lines = random.sample(lines, n_sample)
    records = [json.loads(line) for line in sample_lines]
    return records

def main():
    review_file = RAW / "yelp_academic_dataset_review.json"
    tip_file = RAW / "yelp_academic_dataset_tip.json"

    N_REVIEWS = 5000   # adjust down if too slow
    N_TIPS = 5000

    print("Sampling reviews...")
    review_records = sample_json_lines(review_file, N_REVIEWS)
    print("Sampling tips...")
    tip_records = sample_json_lines(tip_file, N_TIPS)

    df_reviews = pd.DataFrame(review_records)
    df_reviews["kind"] = "review"

    df_tips = pd.DataFrame(tip_records)
    df_tips["kind"] = "tip"

    cols = ["text", "kind"]
    df = pd.concat([df_reviews[cols], df_tips[cols]], ignore_index=True)

    out_path = PROCESSED / "yelp_tips_reviews_sample.csv"
    df.to_csv(out_path, index=False)
    print(f"\nSaved sample to {out_path}")
    print(df["kind"].value_counts())

if __name__ == "__main__":
    main()