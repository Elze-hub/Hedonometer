# src/fetch_yelp_data.py

import os
import random
import zipfile
from pathlib import Path

# Folder where raw data should live
RAW_DIR = Path("data/raw")

# How many reviews you want in your sample (change if you like)
SAMPLE_SIZE = 50000


def ensure_raw_dir():
    """Make sure data/raw/ exists."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Using RAW_DIR = {RAW_DIR.resolve()}")


def unzip_yelp_if_needed():
    """
    If there is a Yelp zip file in data/raw/, unzip it.
    If there is no zip, just print a message.
    """
    # Look for any zip starting with 'yelp' (e.g. yelp-dataset.zip)
    zip_files = list(RAW_DIR.glob("yelp*.zip"))
    if not zip_files:
        print("No Yelp .zip file found in data/raw/.")
        print(
            "If you haven't yet, download the Yelp Open Dataset from:\n"
            "  https://business.yelp.com/data/resources/open-dataset/\n"
            "or the Kaggle mirror:\n"
            "  https://www.kaggle.com/datasets/yelp-dataset/yelp-dataset\n"
            "then place the ZIP file in data/raw/."
        )
        return

    zip_path = zip_files[0]
    print(f"Found zip file: {zip_path.name}")
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(RAW_DIR)
    print("Unzipped Yelp dataset into data/raw/.")


def create_review_sample():
    """
    Create a smaller sample of the Yelp review JSON file for easier processing.
    Looks for yelp_academic_dataset_review.json in data/raw/.
    """
    review_path = RAW_DIR / "yelp_academic_dataset_review.json"
    if not review_path.exists():
        print(
            f"Could not find {review_path.name} in {RAW_DIR}.\n"
            "Make sure the dataset is unzipped and that file exists."
        )
        return

    sample_path = RAW_DIR / "yelp_reviews_sample.json"

    print(f"Reading reviews from {review_path} ...")
    with review_path.open("r", encoding="utf-8") as f:
        lines = f.readlines()

    total_reviews = len(lines)
    print(f"Total reviews in file: {total_reviews}")

    if total_reviews <= SAMPLE_SIZE:
        print(
            f"Dataset has <= {SAMPLE_SIZE} reviews; copying all reviews to {sample_path}."
        )
        with sample_path.open("w", encoding="utf-8") as out_f:
            out_f.writelines(lines)
        return

    print(f"Sampling {SAMPLE_SIZE} reviews at random ...")
    sample_lines = random.sample(lines, SAMPLE_SIZE)  # random subset of lines

    print(f"Writing sample to {sample_path} ...")
    with sample_path.open("w", encoding="utf-8") as out_f:
        out_f.writelines(sample_lines)

    print("Done. Sample file created.")


def main():
    ensure_raw_dir()
    unzip_yelp_if_needed()
    create_review_sample()


if __name__ == "__main__":
    main()