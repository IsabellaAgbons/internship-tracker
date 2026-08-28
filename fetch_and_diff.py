"""Fetch internship listings and save only the ones not already in the database."""
from datetime import datetime
import requests

from database import create_table, get_existing_keys, insert_posting
LISTINGS_URL = (
    "https://raw.githubusercontent.com/SimplifyJobs/Summer2027-Internships/"
    "dev/.github/scripts/listings.json"
)

def fetch_listings():
    """Download the listings JSON and return only postings marked active."""
    response = requests.get(LISTINGS_URL, timeout=30)
    response.raise_for_status()
    listings = response.json()
    return [posting for posting in listings if posting.get("active") is True]

def normalize_posting(raw_posting):
    """Convert one raw feed dict into the shape stored in the database."""
    return {
        "company": raw_posting["company_name"],
        "role": raw_posting["title"],
        "location": ", ".join(raw_posting["locations"]),
        "date_posted": datetime.fromtimestamp(raw_posting["date_posted"]).strftime(
            "%Y-%m-%d"
        ),
        "url": raw_posting["url"],
        "unique_key": str(raw_posting["id"]),
    }

def find_new_postings(all_raw_postings):
    """Normalize raw postings and return those whose unique_key is not stored yet."""
    existing_keys = get_existing_keys()
    new_postings = []
    for raw_posting in all_raw_postings:
        posting = normalize_posting(raw_posting)
        if posting["unique_key"] not in existing_keys:
            new_postings.append(posting)
    return new_postings

def save_new_postings(new_postings):
    """Insert each new posting into the database."""
    for posting in new_postings:
        insert_posting(posting)

def run():
    """Create the table, fetch listings, save unseen postings, and return them."""
    create_table()
    all_raw_postings = fetch_listings()
    new_postings = find_new_postings(all_raw_postings)
    save_new_postings(new_postings)
    return new_postings

if __name__ == "__main__": print(run())