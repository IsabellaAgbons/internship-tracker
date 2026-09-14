# Internship Tracker

A fully automated pipeline that tracks new internship postings and emails a weekly digest, with a live dashboard showing posting trends over time.

🔗 **[Live Dashboard](https://internship-tracker-2ebm.onrender.com/)**

## What it does
- Pulls current internship listings weekly from a public feed ([SimplifyJobs Summer Internships](https://github.com/SimplifyJobs/Summer2027-Internships))
- Deduplicates against previously seen postings using a unique-key hash set
- Emails a digest of genuinely new postings via Gmail SMTP
- Commits the updated database back to the repo, keeping a running history
- Serves a live dashboard (deployed on Render) with charts of posting trends and top hiring companies

## Architecture
A scheduler (GitHub Actions, weekly cron) triggers a fetch-and-diff script, which pulls from the external feed and stores new postings in a SQLite database. Two independent consumers read from that same database: an email digest (scheduled) and a Flask dashboard (on-demand, auto-redeployed on every update). Each piece has a single responsibility — the fetch script has no knowledge of email or dashboard logic, and vice versa.

## Tech stack
- **Python** — core logic
- **SQLite** — storage, with a schema derived from a single source of truth
- **Flask + matplotlib** — dashboard and charts
- **smtplib (Gmail)** — email delivery
- **GitHub Actions** — weekly automation
- **Render** — dashboard hosting, auto-deployed from GitHub

## Status
✅ Complete and running automatically every week.