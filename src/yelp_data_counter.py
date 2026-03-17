from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "yelp-dataset"  # note the extra folder

def count_lines(path):
    n = 0
    with path.open("r", encoding="utf-8") as f:
        for _ in f:
            n += 1
    return n

def main():
    review_file = RAW / "yelp_academic_dataset_review.json"
    tip_file = RAW / "yelp_academic_dataset_tip.json"

    print("Counting lines... this may take a bit.")
    print("Reviews file:", review_file)
    print("Tips file:", tip_file)

    n_reviews = count_lines(review_file)
    n_tips = count_lines(tip_file)

    print(f"\nTotal reviews: {n_reviews}")
    print(f"Total tips:    {n_tips}")

if __name__ == "__main__":
    main()