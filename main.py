"""Fetch new internship postings and email a digest."""
from email_digest import run as email_run
from fetch_and_diff import run as fetch_run
def main():
    """Fetch new postings, then send them in an email digest."""
    new_postings = fetch_run()
    email_run(new_postings)
if __name__ == "__main__":
    main()