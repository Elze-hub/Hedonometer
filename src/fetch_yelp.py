import os
import json
import time

import requests
from dotenv import load_dotenv


# Load environment variables from .env in project root
load_dotenv()
API_KEY = os.getenv("YELP_API_KEY")

if API_KEY is None:
    raise RuntimeError("YELP_API_KEY not found. Did you add it to .env?")

HEADERS = {"Authorization": f"Bearer {API_KEY}"}
BASE_URL = "https://api.yelp.com/v3"


def search_businesses(location, category, limit=50, offset=0):
    """
    Search for businesses in a given location and category.
    Returns a list of business objects.
    """
    url = f"{BASE_URL}/businesses/search"
    params = {
        "location": location,
        "categories": category,
        "limit": limit,
        "offset": offset,
        "sort_by": "rating",  # you can change this if you want
    }

    resp = requests.get(url, headers=HEADERS, params=params)
    resp.raise_for_status()
    data = resp.json()
    return data.get("businesses", [])


def fetch_reviews_for_business(business):
    """
    Given a business object, fetch its reviews and attach business metadata.
    """
    business_id = business["id"]
    url = f"{BASE_URL}/businesses/{business_id}/reviews"

    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    data = resp.json()
    reviews = data.get("reviews", [])

    # Attach useful metadata from the business to each review
    for r in reviews:
        r["business_id"] = business_id
        r["business_name"] = business.get("name")
        r["business_rating"] = business.get("rating")
        r["business_city"] = business.get("location", {}).get("city")
        r["business_categories"] = [c["title"] for c in business.get("categories", [])]

    return reviews


def main():
    # >>> EDIT THESE to match your research question <<<
    location = "Amsterdam"
    category = "restaurants"

    # How many businesses to retrieve (each business has up to ~3 reviews via this endpoint)
    max_businesses = 40
    per_page = 20  # Yelp max is usually 50 per request

    print(f"Searching for businesses in {location} (category={category})...")
    all_businesses = []
    offset = 0

    while len(all_businesses) < max_businesses:
        batch = search_businesses(location, category, limit=per_page, offset=offset)
        if not batch:
            print("No more businesses returned by API.")
            break

        all_businesses.extend(batch)
        print(f"Fetched {len(all_businesses)} businesses so far...")
        offset += per_page

        time.sleep(0.2)  # be polite to the API

    # Trim to exactly max_businesses if we overshot
    all_businesses = all_businesses[:max_businesses]

    print(f"Total businesses to fetch reviews for: {len(all_businesses)}")

    all_reviews = []
    for i, b in enumerate(all_businesses, start=1):
        try:
            reviews = fetch_reviews_for_business(b)
            all_reviews.extend(reviews)
            print(f"[{i}/{len(all_businesses)}] {b.get('name')} -> {len(reviews)} reviews")
        except Exception as e:
            print(f"Error fetching reviews for {b.get('id')}: {e}")
        time.sleep(0.2)

    # Ensure raw data folder exists
    os.makedirs("data/raw", exist_ok=True)
    out_path = "data/raw/yelp_reviews_raw.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_reviews, f, ensure_ascii=False, indent=2)

    print(f"\nSaved {len(all_reviews)} reviews to {out_path}")


if __name__ == "__main__":
    main()